## Dataset and ingestion benchmarks

The project uses the HDFS_v1 dataset from
[Loghub](https://github.com/logpai/loghub), containing **11,175,629 log events**.

Logs are parsed incrementally and loaded into PostgreSQL using Psycopg’s
`COPY` interface. Each event retains its source filename and line number
so investigation findings can reference the original evidence.

### Local benchmark results

Measured on a MacBook with Apple M2 Pro and 8 GB RAM, with Python and
PostgreSQL 16 running through Docker.

| Metric | Result |
|---|---:|
| Events parsed and imported | 11,175,629 |
| Parsing failures | 0 |
| Parsing time | 95.07 seconds |
| Parsing throughput | 117,553 lines/second |
| Database ingestion time | 157.67 seconds |
| Database ingestion throughput | 70,879 events/second |
| PostgreSQL table size, including indexes | 3,150 MB |

Parsing time includes reading, parsing, and counting the source records.
Ingestion time includes parsing the file again, writing records through
`COPY`, and committing the transaction. These are separate measurements
from single local runs, not averages across repeated trials.

### Data validation

SQL checks confirmed the imported record count and severity distribution:

| Log level | Events |
|---|---:|
| INFO | 10,812,836 |
| WARN | 362,793 |
| **Total** | **11,175,629** |

The initial 2,000-line sample was replaced during the full import to avoid
duplicate events. PostgreSQL statistics were refreshed using `ANALYZE`.

These results measure the data pipeline. They do not measure agent
investigation accuracy, search latency, or LLM throughput.

### Dataset attribution

Download: [HDFS_v1 on Zenodo](https://zenodo.org/records/8196385).

Reference: Jieming Zhu et al., *Loghub: A Large Collection of System Log
Datasets for AI-driven Log Analytics*, ISSRE 2023.

Downloaded data is excluded from Git. Retain the dataset’s original
license and attribution notices when using or distributing it.