# Week 2: Cursor, Notebooks vs Python Files, Testing, Prompt Engineering

**Title**: CSE255: Scalable Data Analysis with Dask  
**Subtitle**: Week 2: Cursor, Notebooks vs Python Files, Testing, Prompt Engineering  
**Author**: Course Instructor

---

## Slide 1: Title Page

---

## Slide 2: Learning Objectives

- Understand productive workflows in Cursor IDE
- Learn when to use notebooks vs Python modules
- Set up proper repository structure for data science
- Implement testing strategies with pytest
- Master prompt engineering for AI-assisted development
- Understand reproducibility and guardrails

---

## Slide 3: Cursor IDE Workflows


### Best Practices
- Provide clear, specific prompts
- Start by creating a plan and editing it, before allowing generation of code.
- Review AI-generated code carefully
- Test everything before committing
- Use AI to learn, not just generate code, as questions in chat.

---

## Slide 4: Repository Structure

### Standard Layout

```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── preprocessing.py
│       ├── analysis.py
│       └── models.py
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_analysis.ipynb
│   └── 03_visualization.ipynb
├── tests/
│   ├── test_preprocessing.py
│   └── test_analysis.py
├── data/
├── environment.yml
├── README.md
└── Makefile
```

---

## Slide 5: Notebooks vs Python Modules

**Use Notebooks For:**
- Exploratory data analysis
- Rapid prototyping
- Visualization and presentation
- Interactive debugging
- Learning and experimentation

**Use Modules For:**
- Production code
- Reusable functions
- Testable components
- Data pipelines
- Complex logic

### Rule of Thumb
If it needs to run in production or be tested, it belongs in a module

---

## Slide 6: Refactoring Pattern

### Workflow
1. Start in notebook for exploration
2. Identify reusable patterns
3. Extract to module with tests
4. Import module back into notebook
5. Document the decision

### Example
```python
# In notebook
def clean_data(df):
    # complex logic
    
# Extract to src/preprocessing.py
# Add tests in tests/test_preprocessing.py
# Import in notebook: from src.preprocessing import clean_data
```

---

## Slide 7: Testing Strategies

### pytest Basics
- Use pytest for all tests
- Test files: `test_*.py`
- Test functions: `def test_*()`
- Use fixtures for reusable setup

### Testing Types
- **Unit tests**: Individual functions
- **Integration tests**: Component interactions
- **Data contract tests**: Schema validation
- **Lightweight fixtures**: Sample data for testing

---

## Slide 8: Data Contract Tests

### Schema Validation
- Verify column names and types
- Check expected ranges
- Validate relationships
- Ensure no nulls in critical columns

### Example
```python
def test_schema_validation(df):
    assert 'timestamp' in df.columns
    assert df['timestamp'].dtype == 'datetime64[ns]'
    assert df['value'].min() >= 0
    assert df['value'].notna().all()
```

---

## Slide 9: Prompt Engineering

### Effective Prompts
- Be specific about context
- Include examples when possible
- Specify desired output format
- Ask for explanations

### Common Templates
- **Code generation**: "Write a function that..."
- **Refactoring**: "Refactor this code to..."
- **Review**: "Review this code for..."
- **Debugging**: "Why does this code fail when..."

---

## Slide 10: Prompt Snippets

### Code Generation
`"Create a plan for a function to load Parquet files from S3 using dask, with error handling and logging"`

### Refactoring
`"Refactor this pandas code to use dask, maintaining the same API and adding type hints"`

### Code Review
`"Review this data preprocessing function for performance, correctness, and best practices"`

### Documentation
`"Add docstrings to this function following numpy style, including parameter types and return values"`

---

## Slide 11: Reproducibility

### Guardrails
- Lock dependency versions in `environment.yml`
- Use seeded randomness for ML
- Document all parameters
- Version control all code
- Provide clear README

### Runnable Pipeline
- Single entrypoint: `make` or `python -m`
- Clear documentation of steps
- Idempotent operations
- Deterministic results

---

## Slide 12: Partition Planning

### Document Partition Strategy
- Partition keys (e.g., date, region)
- Expected partition sizes
- Query patterns
- Trade-offs considered

### Example
```
Partitioning Strategy:
- Key: date (YYYY-MM-DD)
- Expected size: ~100MB per partition
- Query pattern: Filter by date range
- Rationale: Most queries are time-based
```

---

## Slide 13: Week 2 Deliverables

### Repository Skeleton
- Clear module boundaries in `src/`
- `notebooks/` directory with examples
- `tests/` directory with pytest setup
- `pytest` passing locally

### Refactored Example
- One notebook refactored into module
- Minimal documentation on when to use each
- Tests for the module

### Prompt Templates
Short templates the team will use in Cursor for common tasks

---

## Slide 14: Week 2 Deliverables (cont.)

### Runnable Pipeline
- `make` or `python -m` entrypoint
- Clear README with usage instructions

### Partition Plan
Documented with keys, expected sizes, and rationale

### Cost Visibility
- Vacoreum cost trend
- Storage footprint
- Table of cost per 1M rows ingested

---

## Slide 15: Homework 2 (5%)

### CSV/JSON to Parquet Conversion
- Convert messy CSV/JSON to Parquet
- Implement validation checks
- Document schema

### Justify Choices
- Partitioning strategy
- Compression choices
- Data type decisions
- Performance considerations

---

## Slide 16: Best Practices Summary

### Code Organization
- Clear separation: notebooks for exploration, modules for production
- Testable, reusable code in modules
- Document decisions

### AI-Assisted Development
- Use AI responsibly
- Review all generated code
- Learn from AI suggestions
- Build prompt templates

### Testing
- Write tests early
- Use fixtures for data
- Validate schemas
- Test edge cases

---

## Slide 17: Next Steps

1. Set up repository structure
2. Refactor one notebook example
3. Create prompt templates
4. Write tests for modules
5. Document partition plan
6. Complete HW2

### Questions?

