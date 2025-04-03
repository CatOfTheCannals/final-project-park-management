# Final Project Report

## Introduction
This project aims to develop a database system for managing information about natural parks and protected areas in Argentina. The system will provide tools for tracking ecological data, visitor statistics, and park management activities.

## Design Approach
1. **Test-Driven Development:** We follow a test-first approach to ensure all requirements are clearly defined and met.
2. **Modular Implementation:** Implement core functionalities first, progressively adding more features while maintaining test coverage.
3. **Documentation:** Keep detailed records of design decisions and trade-offs.

## Current Status
### Implemented Requirements:
- Complete database schema with all required tables and relationships
- Data validation constraints via foreign keys, unique constraints, and triggers
- Functional queries for all required reporting needs
- Comprehensive test suite verifying all requirements

## Assumptions
1. We are using **MySQL** as the database engine.
2. 

## Design Decisions & Simplifications
- **Visitors:** Visitors are directly associated with the park they are visiting (`visitors.park_id`), even though they stay in accommodations. This simplifies querying visitor counts per park.
- **Research Element Link:** Implemented via `research_projects.element_id` foreign key, assuming a project focuses on one primary element.
- **Conservation Area Link:** Implemented via `conservation_personnel.park_id` and `conservation_personnel.area_number` composite foreign key, assuming a conservation staff member is assigned to one specific area.
- **Element Food Constraints:** The constraints preventing minerals from being food (`check_mineral_not_food`) and preventing plants from feeding (`check_vegetal_not_feeding`) are implemented using `BEFORE INSERT` and `BEFORE UPDATE` triggers on the `element_food` table. This approach was chosen because MySQL does not support subqueries within `CHECK` constraints.


### Index Proposal & Execution Plan Analysis 

#### Index Proposal



### Indexing Strategy

The indexes are finely tuned to support the join and aggregation operations with minimal overhead.

- **Table: natural_elements**
  - **Primary Key:** `id`
  - **Unique Constraint:** `scientific_name`

- **Table: area_elements**
  - **Composite Primary Key:** `(park_id, area_number, element_id)`
  - **Dedicated Index:** `idx_area_elements_element_id` on `element_id`

##### Performance Highlights

- **Efficient Joins:**  
  The dedicated index on `area_elements.element_id` enables the query optimizer to quickly locate matching rows. The EXPLAIN output confirms that only 136 rows are scanned using this index.

- **Optimized Lookups:**  
  The primary key on `natural_elements.id` supports an `eq_ref` lookup, ensuring a one-to-one match per join iteration. This guarantees rapid retrieval of the necessary rows.

- **Smooth Aggregation:**  
  The grouping on `natural_elements.id` and `scientific_name` is handled efficiently, even with the temporary table and filesort operations. The existing indexes make the grouping and HAVING clause (filtering for a distinct count of 1) cost-effective.

**Execution Plan Analysis:**
You can find the explanations for the query plans at pre_computed_results/analysis/execution_plans_output.txt

**Species in all parks:**
   ```sql
   EXPLAIN SELECT ne.scientific_name
   FROM natural_elements ne
   JOIN area_elements ae ON ne.id = ae.element_id
   GROUP BY ne.id, ne.scientific_name
   HAVING COUNT(DISTINCT ae.park_id) = (SELECT COUNT(*) FROM parks);
   ```
The index on area_elements.element_id (idx_area_elements_element_id) is key. The EXPLAIN shows that MySQL uses a nested-loop join:

• Area_elements lookup:
The engine scans 136 rows using the idx_area_elements_element_id index. It accesses only the indexed columns (park_id, area_number, element_id) so it avoids a full table scan, keeping the cost low (read_cost 0.25, eval_cost 13.60).

• Natural_elements lookup:
For each row from area_elements, it performs an eq_ref lookup in natural_elements using the primary key. This means it gets exactly one matching row quickly (rows_examined_per_scan is 1), benefiting from the unique primary key.

• Grouping and filesort:
The query groups by natural_elements.id and scientific_name, so MySQL creates a temporary table and does a filesort. Although that adds some cost (sort_cost 136.00), the efficient index usage minimizes the overhead.

• HAVING subquery:
The subquery on parks uses its index (key "code") to quickly count rows, further keeping the query efficient.

Overall, the index choice minimizes row scans and leverages fast, indexed lookups, which makes the join and group-by operations lean and fast.

4. **Species in only one park:**
   ```sql
   EXPLAIN SELECT ne.scientific_name
   FROM natural_elements ne
   JOIN area_elements ae ON ne.id = ae.element_id
   GROUP BY ne.id, ne.scientific_name
   HAVING COUNT(DISTINCT ae.park_id) = 1;
   ```
The plan shows MySQL scanning 136 rows from area_elements via the dedicated index on element_id (idx_area_elements_element_id), which means it doesn’t need to scan the full composite primary key. Each row then triggers an eq_ref lookup in natural_elements using its primary key (id), ensuring a fast one-row fetch.

After the join, MySQL groups by natural_elements.id and scientific_name using a temporary table and filesort (sort_cost 136.00). Finally, it applies the HAVING filter (COUNT(DISTINCT ae.park_id) = 1).

Overall, the dedicated index on area_elements.element_id is optimal because it directly supports the join. The natural_elements table uses its primary key efficiently. For the current workload, the indexes are well-chosen.

##### Conclusion

The indexes in place are optimal for the current queries, as they minimize row scans and support fast, efficient joins and aggregations. This robust indexing design not only maintains excellent performance with the current dataset but is also scalable as data volume increases.

### Database Comparison Procedure

A stored procedure named `compare_databases` has been implemented in `sql/setup.sql`. It accepts two database names as input parameters and compares their schema definitions using queries against the `INFORMATION_SCHEMA`.

The procedure compares:
1. Tables that exist in one database but not the other
2. Tables with the same name but different structures
3. Differences in indexes and constraints

This tool is valuable for:
- Verifying that development and production environments are in sync
- Comparing before/after states during schema migrations
- Troubleshooting issues related to schema differences

To use the procedure:
```sql
-- Example call:
CALL compare_databases('park_management', 'park_management_backup'); 
```
*(Replace 'park_management_backup' with the name of the second database you want to compare)*

#### Analysis of Comparison Results (`schema_comparison_output.txt`)

The execution of `scripts/run_db_comparison.sh` generates the comparison output in `results/comparison/schema_comparison_output.txt`. Analyzing this output reveals the following discrepancies between the `park_management` (main) and `park_management_alt` (alternative) schemas, reflecting the intentional differences introduced in `sql/setup_alternative_db.sql`:

*   **Table Differences:**
    *   The `email_log` table exists only in `park_management`. This was intentionally omitted from `park_management_alt`.
    *   The tables `adventure_trails` and `eco_innovations` exist only in `park_management_alt`, as they were added specifically to the alternative schema script.

*   **Index Differences (on common tables):**
    *   The comparison highlights differences in index naming and potentially implicit vs. explicit index creation. For example, `park_management` might have implicitly created indexes for foreign keys or parts of primary keys (like `element_id`, `province_id`, `park_id`), while `park_management_alt` has explicitly named indexes (`idx_...`).
    *   Crucially, the `UNIQUE` index on `provinces.name` is missing in `park_management_alt` (as intended), which is reflected in the constraint differences.
    *   The `UNIQUE` index on `natural_elements.common_name` exists only in `park_management_alt` (as intended).
    *   The index `idx_parks_code` was intentionally omitted in `park_management_alt`, although the comparison output might not list it directly if the `UNIQUE` constraint on `code` implicitly created a usable index structure in both.

*   **Constraint Differences (on common tables):**
    *   The `UNIQUE` constraint on `provinces.name` exists only in `park_management`. This was intentionally removed in `park_management_alt`.
    *   The foreign key constraint `visitors_ibfk_2` (linking `visitors.park_id` to `parks.id`) exists only in `park_management`. This was intentionally omitted in `park_management_alt`.
    *   A `UNIQUE` constraint on `natural_elements.common_name` exists only in `park_management_alt`. This was an intentional addition to the alternative schema.

These results confirm that the `compare_databases` procedure successfully identifies variations in tables, indexes, and constraints between two database schemas, matching the deliberate modifications made in the setup scripts.

### Concurrency Control & Recovery Mechanisms

**MySQL (InnoDB Engine):**

**Concurrency Control:**
- Uses Multi-Version Concurrency Control (MVCC) to allow readers non-blocking access to data while writers are modifying it
- Implements row-level locking for high concurrency
- Supports standard transaction isolation levels:
  - READ UNCOMMITTED: Allows dirty reads
  - READ COMMITTED: Prevents dirty reads
  - REPEATABLE READ (default): Prevents dirty reads and non-repeatable reads
  - SERIALIZABLE: Prevents all concurrency anomalies
- Uses gap locks and next-key locks to prevent phantom reads in REPEATABLE READ
- Deadlock detection automatically rolls back transactions with fewer changes

**Recovery Mechanisms:**
- Employs a write-ahead logging (WAL) mechanism using redo logs
- Changes are first written to the redo log buffer and then flushed to disk
- Uses a doublewrite buffer to prevent data corruption from partial page writes
- In case of a crash, InnoDB replays the redo logs from the last checkpoint
- Maintains undo logs for transaction rollback and MVCC
- Supports binary logging for point-in-time recovery and replication

**PostgreSQL:**

**Concurrency Control:**
- Also uses MVCC, providing high concurrency between readers and writers
- Primarily uses row-level locking
- Supports standard transaction isolation levels:
  - READ COMMITTED (default): Prevents dirty reads
  - REPEATABLE READ: Prevents dirty reads and non-repeatable reads
  - SERIALIZABLE: Prevents all concurrency anomalies
- Serializable isolation is implemented using Serializable Snapshot Isolation (SSI)
- SSI monitors transaction dependencies and aborts transactions that could violate serializability
- Explicit locking commands (SELECT FOR UPDATE, LOCK TABLE) for special cases
- Deadlock detection with configurable timeout

**Recovery Mechanisms:**
- Uses Write-Ahead Logging (WAL)
- Changes are written to WAL segment files before data files are modified
- Checkpoints periodically flush dirty data buffers to disk
- On recovery, replays WAL records from the last checkpoint forward
- Offers Point-in-Time Recovery (PITR) using continuous archiving of WAL records
- WAL archiving allows restoration to any point in time
- Supports streaming replication for high availability

**Comparison:**

| Feature | MySQL (InnoDB) | PostgreSQL |
|---------|----------------|------------|
| Concurrency Model | MVCC | MVCC |
| Default Isolation | REPEATABLE READ | READ COMMITTED |
| Phantom Prevention | Gap locks, next-key locks | Serializable Snapshot Isolation |
| Recovery Logging | Redo logs, undo logs | Write-Ahead Logs (WAL) |
| Point-in-Time Recovery | Binary logs | WAL archiving |
| Deadlock Handling | Automatic detection and rollback | Detection with timeout |
| Locking Granularity | Row-level, table-level | Row-level, table-level |
| Special Features | Doublewrite buffer | PITR, streaming replication |

Both systems provide robust concurrency control and recovery mechanisms, with PostgreSQL offering more advanced point-in-time recovery options and MySQL providing slightly better performance in high-concurrency OLTP workloads due to its optimized implementation of MVCC.

## Trade-offs
- **Test Focus vs Implementation Speed:** By focusing on tests first, we ensure quality but may initially be slower than direct implementation.
- **Schema Complexity vs Requirement Fidelity:** Some relationships (mentioned in Simplifications) were omitted or simplified to reduce schema complexity and meet the "minimal effort" guideline. Some constraints (like element food rules) were implemented via triggers due to database engine limitations (MySQL CHECK constraints).
- **Data Volume vs Performance:** The current schema is optimized for the expected data volume. For significantly larger datasets, additional denormalization or specialized indexes might be needed.
