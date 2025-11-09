#!/usr/bin/env python3
"""
Inspect the schemas of Parquet files in ~/flight_data and report mismatches.

The script treats the first Parquet file alphabetically as the reference schema
and compares all remaining files against it, listing any field additions,
removals, or type differences.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Optional

import pyarrow as pa
import pyarrow.parquet as pq


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare the schemas of Parquet files in a directory."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path.home() / "flight_data",
        help="Directory containing the Parquet files (default: %(default)s)",
    )
    parser.add_argument(
        "--pattern",
        default="*.parquet",
        help="Glob pattern to match Parquet files (relative to --input-dir).",
    )
    return parser.parse_args(argv)


def find_parquet_files(input_dir: Path, pattern: str) -> list[Path]:
    return sorted(path for path in input_dir.glob(pattern) if path.is_file())


def fields_to_dict(schema: pa.Schema) -> dict[str, pa.Field]:
    return {field.name: field for field in schema}


def compare_schemas(schemas: dict[str, pa.Schema]) -> dict[str, dict[str, list[str]]]:
    differences: dict[str, dict[str, list[str]]] = {}

    reference_file, reference_schema = next(iter(schemas.items()))
    reference_fields = fields_to_dict(reference_schema)

    for filename, schema in list(schemas.items())[1:]:
        current_fields = fields_to_dict(schema)

        missing = sorted(name for name in reference_fields if name not in current_fields)
        extra = sorted(name for name in current_fields if name not in reference_fields)

        type_mismatches = []
        for field_name in reference_fields:
            if field_name in current_fields:
                ref_field = reference_fields[field_name]
                cur_field = current_fields[field_name]
                if ref_field.type != cur_field.type or ref_field.nullable != cur_field.nullable:
                    type_mismatches.append(
                        f"{field_name} (expected {ref_field.type}, nullable={ref_field.nullable}; "
                        f"found {cur_field.type}, nullable={cur_field.nullable})"
                    )

        if missing or extra or type_mismatches:
            differences[filename] = {
                "missing_fields": missing,
                "extra_fields": extra,
                "type_mismatches": type_mismatches,
            }

    return {"reference_file": reference_file, "differences": differences}


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)

    parquet_files = find_parquet_files(args.input_dir, args.pattern)
    if not parquet_files:
        print(
            f"No Parquet files found in {args.input_dir} matching {args.pattern}",
            file=sys.stderr,
        )
        return 1

    schemas: dict[str, pa.Schema] = {}
    for path in parquet_files:
        try:
            schemas[path.name] = pq.read_metadata(path).schema.to_arrow_schema()
        except Exception as exc:  # pragma: no cover
            print(f"Unable to read schema from {path}: {exc}", file=sys.stderr)
            return 1

    comparison = compare_schemas(schemas)
    reference_file = comparison["reference_file"]
    differences = comparison["differences"]

    print(f"Reference schema: {reference_file}")
    if not differences:
        print("All Parquet files share the same schema.")
        return 0

    print("Schema mismatches detected:")
    for filename, details in differences.items():
        print(f"- {filename}:")
        if details["missing_fields"]:
            print(f"    missing fields: {', '.join(details['missing_fields'])}")
        if details["extra_fields"]:
            print(f"    extra fields: {', '.join(details['extra_fields'])}")
        if details["type_mismatches"]:
            print("    type mismatches:")
            for mismatch in details["type_mismatches"]:
                print(f"        {mismatch}")

    return 1


if __name__ == "__main__":
    sys.exit(main())

