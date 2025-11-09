# Flight Parquet Schema

Field descriptions for the annual Parquet files under `~/flight_data`. Types reflect the current Arrow schema; nullable fields may contain missing values.

| Field | Type | Description |
| --- | --- | --- |
| `FL_DATE` | string | Flight departure date in ISO format (`YYYY-MM-DD`). |
| `OP_CARRIER` | string | Two-letter/three-letter designator of the operating air carrier. |
| `OP_CARRIER_FL_NUM` | int64 | Flight number assigned by the operating carrier. |
| `ORIGIN` | string | Origin airport IATA code. |
| `DEST` | string | Destination airport IATA code. |
| `CRS_DEP_TIME` | int64 | Scheduled (carrier-reported) departure time in local clock minutes (`HHMM`). |
| `DEP_TIME` | double | Actual departure time in local clock minutes (`HHMM`), may be fractional or missing. |
| `DEP_DELAY` | double | Departure delay in minutes relative to the scheduled departure. Positive values indicate lateness. |
| `TAXI_OUT` | double | Taxi-out time in minutes from gate departure to wheels-off. |
| `WHEELS_OFF` | double | Time the aircraft became airborne, expressed as local clock minutes (`HHMM`). |
| `WHEELS_ON` | double | Time the aircraft touched down, expressed as local clock minutes (`HHMM`). |
| `TAXI_IN` | double | Taxi-in time in minutes from wheels-on to gate arrival. |
| `CRS_ARR_TIME` | int64 | Scheduled arrival time in local clock minutes (`HHMM`). |
| `ARR_TIME` | double | Actual arrival time in local clock minutes (`HHMM`). |
| `ARR_DELAY` | double | Arrival delay in minutes relative to the scheduled arrival. |
| `CANCELLED` | double | Cancellation flag (`1.0` for cancelled flights, `0.0` otherwise). |
| `CANCELLATION_CODE` | string | Reason code for cancellations (`A`=Carrier, `B`=Weather, `C`=National Air System, `D`=Security). |
| `DIVERTED` | double | Diversion flag (`1.0` if the flight diverted, `0.0` otherwise). |
| `CRS_ELAPSED_TIME` | double | Scheduled elapsed flight time in minutes. |
| `ACTUAL_ELAPSED_TIME` | double | Actual elapsed flight time in minutes. |
| `AIR_TIME` | double | Airborne time in minutes (actual). |
| `DISTANCE` | double | Great-circle distance between origin and destination in statute miles. |
| `CARRIER_DELAY` | double | Minutes of delay attributed to carrier operations. |
| `WEATHER_DELAY` | double | Minutes of delay attributed to weather. |
| `NAS_DELAY` | double | Minutes of delay attributed to the National Airspace System. |
| `SECURITY_DELAY` | double | Minutes of delay attributed to security-related causes. |
| `LATE_AIRCRAFT_DELAY` | double | Minutes of delay attributed to a late inbound aircraft. |
| `Unnamed: 27` | double | Unused placeholder column (all values missing). |

**Notes**
- Time-of-day fields follow the `HHMM` convention from the BTS On-Time Performance dataset; values such as `745` represent 7:45 a.m.
- Delay columns record minutes and can be negative when a flight arrives or departs early.
- Placeholder column `Unnamed: 27` is retained for compatibility with the raw CSV layout and can be dropped safely in downstream analysis.

