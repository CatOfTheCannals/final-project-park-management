# Final Project Report

## Introduction
This project aims to develop a database system for managing information about natural parks and protected areas in Argentina. The system will provide tools for tracking ecological data, visitor statistics, and park management activities.

## Design Approach
1. **Test-Driven Development:** We follow a test-first approach to ensure all requirements are clearly defined and met.
2. **Modular Implementation:** Implement core functionalities first, progressively adding more features while maintaining test coverage.
3. **Documentation:** Keep detailed records of design decisions and trade-offs.

## Current Status
### Implemented Requirements:
- Initial test framework setup

### Next Steps:
1. Complete database schema definition
2. Implement data validation constraints
3. Add query functionality

## Assumptions
1. We are using **MySQL** as the database engine. (Updated from original assumption)
2. All data will be stored in a single database instance (`park_management`) for simplicity.
3. Park codes (`parks.code`) are unique identifiers for parks (e.g., 'A', 'B').
4. Visitors are directly associated with the park they are visiting (`visitors.park_id`), even though they stay in accommodations. This simplifies querying visitor counts per park.

## Design Decisions & Simplifications
- **Surveillance Vehicle:** The `surveillance_personnel` table links a vehicle directly to the personnel member. The requirement nuance "siempre es el mismo en cada área que vigila" (always the same in each area they watch) is simplified; we assume one primary vehicle per surveillance staff member rather than tracking vehicle assignments per area vigilated. This meets the requirement as stated, assuming a single vehicle per staff member across all their assigned areas.
- **Research Element Link:** Implemented via `research_projects.element_id` foreign key, assuming a project focuses on one primary element.
- **Conservation Area Link:** Implemented via `conservation_personnel.park_id` and `conservation_personnel.area_number` composite foreign key, assuming a conservation staff member is assigned to one specific area.
- **Element Food Constraints:** The constraints preventing minerals from being food (`check_mineral_not_food`) and preventing plants from feeding (`check_vegetal_not_feeding`) are implemented using `BEFORE INSERT` and `BEFORE UPDATE` triggers on the `element_food` table. This approach was chosen because MySQL does not support subqueries within `CHECK` constraints.
- **Visitor-Excursion Link:** A many-to-many relationship table `visitor_excursions` was added to link visitors to the excursions they attend, fulfilling requirement 13.c.

## Analysis and Additional Requirements

### Table Size Estimation (Additional Req 2)

*(Add your estimation here. Consider factors like:*
*   *Number of provinces (~24)*
*   *Number of parks (e.g., estimate 50-100 total, average size)*
*   *Average areas per park (e.g., 5-10)*
*   *Average elements per area (e.g., 20-50 species)*
*   *Number of personnel (e.g., estimate total staff)*
*   *Number of visitors per year (can reference `data/visitantes...csv`)*
*   *Data types and average string lengths.*
*Example: The `parks` table might have ~100 rows. With VARCHAR(255) for name/email, DATE, VARCHAR(10), DECIMAL, the row size might be around 300-400 bytes. Total size ~ 40KB + indexes. Perform similar rough estimates for major tables like `area_elements`, `visitors`, `personnel`.)*

### Index Proposal & Execution Plan Analysis (Additional Req 5)

*(Add your index proposals and analysis here.)*

**Proposed Indexes:**

*   **Foreign Keys:** Indexes are automatically created by InnoDB for foreign key constraints, which benefits JOIN performance (e.g., `park_provinces.park_id`, `park_provinces.province_id`, `area_elements.park_id`, `area_elements.area_number`, `area_elements.element_id`, etc.).
*   **Frequently Queried Columns:**
    *   `parks(code)`: Used in Functional Req 3 (`WHERE p.code IN (...)`). A UNIQUE index already exists, which is optimal.
    *   `provinces(name)`: Used for output in Functional Req 1. An index could speed up lookups if the table were very large, though the existing UNIQUE constraint might suffice.
    *   `natural_elements(scientific_name)`: Used for output/filtering in Functional Req 2 and Additional Reqs 3 & 4. The existing UNIQUE constraint helps.
    *   `vegetal_elements(element_id)`: Used in JOIN for Functional Req 2. Covered by the PK/FK.
    *   `visitors(park_id)`: Used in JOIN for Functional Req 3. Covered by the FK index.
    *   `area_elements(element_id)`: Used in JOINs/GROUP BY for Functional Req 2, Additional Reqs 3 & 4. Covered by PK/FK.
    *   `area_elements(park_id)`: Used in JOINs/GROUP BY for Functional Req 2, Additional Reqs 3 & 4. Covered by PK/FK.

**Execution Plan Analysis (Conceptual):**

*   **Func Req 1 (Province with most parks):** The query joins `provinces` and `park_provinces` (using FK indexes), groups by province (potentially using the `provinces.id` PK), counts, orders, and limits. Performance should be good with FK indexes.
*   **Func Req 2 (Vegetal species in >= half parks):** Joins `natural_elements`, `vegetal_elements`, `area_elements`. Groups by element. Needs efficient access via `element_id` (PK/FK indexes help). `COUNT(DISTINCT ae.park_id)` might require scanning grouped element data.
*   **Func Req 3 (Visitors in parks A, B):** Joins `visitors` and `parks`. Filters `parks` by `code` (uses UNIQUE index), then joins to `visitors` via `park_id` (uses FK index). Should be efficient.
*   **Add Req 3 (Species in all parks):** Joins `natural_elements` and `area_elements`. Groups by element. The `HAVING COUNT(DISTINCT ae.park_id) = total_parks` requires counting distinct parks per element. Performance depends on element distribution. Indexes on `area_elements(element_id)` and `area_elements(park_id)` are crucial.
*   **Add Req 4 (Species in one park):** Similar to Add Req 3, but `HAVING count = 1`. Indexes are equally important.

*(Optionally, add `EXPLAIN SELECT ...` output for these queries after populating data.)*

### Database Comparison Procedure (Additional Req 6)

A stored procedure named `compare_databases` has been implemented in `sql/setup.sql`. It accepts two database names as input parameters. Its purpose is to compare the schema definitions (tables, columns, indexes, constraints) between the two databases using queries against the `INFORMATION_SCHEMA`. The current implementation provides a basic skeleton and example comparison for table existence; further comparisons can be added as needed.

### Concurrency Control & Recovery Mechanisms (Additional Req 7)

*(Add your research and comparison here. Compare MySQL (InnoDB) with another engine like PostgreSQL.)*

**MySQL (InnoDB Engine):**

*   **Concurrency:** Uses Multi-Version Concurrency Control (MVCC) to allow readers non-blocking access to data even while writers are modifying it. Implements row-level locking for high concurrency. Supports standard transaction isolation levels (Read Uncommitted, Read Committed, Repeatable Read (default), Serializable). Uses mechanisms like gap locks and next-key locks to prevent phantom reads in Repeatable Read.
*   **Recovery:** Employs a write-ahead logging (WAL) mechanism using redo logs. Changes are first written to the redo log buffer and then flushed to disk. In case of a crash, InnoDB replays the redo logs from the last checkpoint to bring the database to a consistent state. Uses a doublewrite buffer to prevent data corruption from partial page writes during crashes.

**PostgreSQL:**

*   **Concurrency:** Also uses MVCC, similar in principle to InnoDB, providing high concurrency between readers and writers. Primarily uses row-level locking. Supports standard transaction isolation levels (Read Uncommitted, Read Committed (default), Repeatable Read, Serializable). Serializable isolation is implemented using Serializable Snapshot Isolation (SSI) which monitors dependencies between transactions.
*   **Recovery:** Uses Write-Ahead Logging (WAL). Changes are written to WAL segment files before data files are modified. Checkpoints periodically flush dirty data buffers to disk. On recovery, PostgreSQL replays WAL records from the last checkpoint forward to restore consistency. Offers Point-in-Time Recovery (PITR) capabilities using continuous archiving of WAL records.

**Comparison Points:**

*   Both use MVCC and WAL for high concurrency and reliable recovery.
*   Default isolation levels differ (Repeatable Read in InnoDB vs. Read Committed in PostgreSQL).
*   Specific locking strategies (e.g., InnoDB's gap locks vs. PostgreSQL's SSI for Serializable) differ in implementation details and performance characteristics.
*   Recovery mechanisms are conceptually similar, relying on WAL and checkpoints. PostgreSQL's PITR is often considered more flexible for fine-grained recovery scenarios.

## Trade-offs
- **Test Focus vs Implementation Speed:** By focusing on tests first, we ensure quality but may initially be slower than direct implementation.
- **Schema Complexity vs Requirement Fidelity:** Some relationships (mentioned in Simplifications) were omitted or simplified to reduce schema complexity and meet the "minimal effort" guideline. Some constraints (like element food rules) were implemented via triggers due to database engine limitations (MySQL CHECK constraints).
