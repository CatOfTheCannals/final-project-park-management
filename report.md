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

Based on our database schema and the expected data volumes, here are the estimated sizes for the main tables:

| Table | Rows | Row Size (approx.) | Total Size | Notes |
|-------|------|-------------------|------------|-------|
| provinces | 24 | 300 bytes | 7.2 KB | Based on Argentina's 23 provinces + CABA |
| parks | 50-100 | 400 bytes | 20-40 KB | National and provincial parks |
| park_provinces | 60-120 | 24 bytes | 1.5-3 KB | Some parks span multiple provinces |
| park_areas | 250-500 | 300 bytes | 75-150 KB | Assuming 5 areas per park |
| natural_elements | 100-200 | 520 bytes | 52-104 KB | Various species and minerals |
| area_elements | 1000-2000 | 24 bytes | 24-48 KB | Distribution of elements across areas |
| personnel | 100-200 | 600 bytes | 60-120 KB | Staff across all parks |
| visitors | 5000-10000 | 500 bytes | 2.5-5 MB | Based on visitor statistics |
| accommodations | 50-100 | 300 bytes | 15-30 KB | Various lodging options |
| excursions | 50-100 | 100 bytes | 5-10 KB | Different tour options |

**Total estimated database size:** Approximately 3-6 MB for data + 1-2 MB for indexes = 4-8 MB

**Assumptions:**
- VARCHAR fields average 50% of their maximum length in actual usage
- Each foreign key and index adds approximately 20-30% overhead
- The visitor count is based on a sample of annual visitors, not the total historical record
- The estimation doesn't include potential growth over time

### Index Proposal & Execution Plan Analysis (Additional Req 5)

**Proposed Indexes:**

1. **Foreign Keys:** InnoDB automatically creates indexes for foreign key constraints, which benefits JOIN performance. These include:
   - `park_provinces.park_id`, `park_provinces.province_id`
   - `area_elements.park_id`, `area_elements.area_number`, `area_elements.element_id`
   - `visitors.park_id`, `visitors.accommodation_id`
   - All other foreign key relationships

2. **Additional Recommended Indexes:**
   - `CREATE INDEX idx_natural_elements_scientific_name ON natural_elements(scientific_name);` - For species lookups by name
   - `CREATE INDEX idx_area_elements_element_id ON area_elements(element_id);` - For finding all areas containing a specific element
   - `CREATE INDEX idx_area_elements_park_id ON area_elements(park_id);` - For finding all elements in a specific park
   - `CREATE INDEX idx_visitors_park_id ON visitors(park_id);` - For counting visitors by park

**Execution Plan Analysis:**

1. **Func Req 1 (Province with most parks):**
   ```sql
   EXPLAIN SELECT p.name, COUNT(pp.park_id) AS park_count
   FROM provinces p
   JOIN park_provinces pp ON p.id = pp.province_id
   GROUP BY p.id, p.name
   ORDER BY park_count DESC
   LIMIT 1;
   ```
   - Uses the index on `pp.province_id` for the JOIN
   - Performs a GROUP BY on `p.id` (primary key)
   - The ORDER BY and LIMIT make this efficient even with many provinces

2. **Func Req 2 (Vegetal species in at least half of parks):**
   ```sql
   EXPLAIN SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count
   FROM natural_elements ne
   JOIN vegetal_elements ve ON ne.id = ve.element_id
   JOIN area_elements ae ON ne.id = ae.element_id
   GROUP BY ne.id, ne.scientific_name
   HAVING park_count >= (SELECT COUNT(*)/2 FROM parks);
   ```
   - Uses indexes on `ve.element_id` and `ae.element_id` for JOINs
   - The GROUP BY operation benefits from the index on `ne.id`
   - The COUNT(DISTINCT) operation may require a temporary table
   - The proposed `idx_area_elements_element_id` index would improve performance

3. **Add Req 3 (Species in all parks):**
   ```sql
   EXPLAIN SELECT ne.scientific_name
   FROM natural_elements ne
   JOIN area_elements ae ON ne.id = ae.element_id
   GROUP BY ne.id, ne.scientific_name
   HAVING COUNT(DISTINCT ae.park_id) = (SELECT COUNT(*) FROM parks);
   ```
   - Similar execution plan to Func Req 2
   - The HAVING clause with COUNT(DISTINCT) and subquery may be expensive
   - The proposed indexes on `area_elements` would significantly improve performance

4. **Add Req 4 (Species in only one park):**
   ```sql
   EXPLAIN SELECT ne.scientific_name
   FROM natural_elements ne
   JOIN area_elements ae ON ne.id = ae.element_id
   GROUP BY ne.id, ne.scientific_name
   HAVING COUNT(DISTINCT ae.park_id) = 1;
   ```
   - Similar execution plan to Add Req 3
   - Simpler HAVING condition makes this slightly more efficient

   **Análisis Específico (Punto 1.c y 1.d):**

   *   **Consulta "Especies en todos los parques" (Add Req 3):** Esta consulta requiere agregar los datos de `area_elements` por `element_id` para contar los parques únicos (`COUNT(DISTINCT ae.park_id)`). El plan de ejecución (visible en `results/analysis/execution_plans_output.txt`) muestra que se utiliza el índice `idx_area_elements_element_id` para agrupar eficientemente las filas por elemento antes de contar los parques. La unión con `natural_elements` se realiza mediante la clave primaria. La comparación final se hace contra una subconsulta que cuenta el total de parques. Gracias a los datos añadidos en `data/load/area_elements.csv` (específicamente, asegurando que el Puma, ID 2, esté en todos los parques), esta consulta ahora devuelve el resultado esperado.

   *   **Consulta "Especies en un único parque" (Add Req 4):** Similar a la anterior, agrupa por elemento usando `idx_area_elements_element_id` y cuenta los parques distintos. La condición `HAVING COUNT(DISTINCT ae.park_id) = 1` filtra los resultados. El plan de ejecución es eficiente gracias al índice propuesto. Los datos de ejemplo incluyen varias especies que solo existen en un parque, permitiendo que esta consulta devuelva resultados significativos.

   Los índices propuestos (`idx_area_elements_element_id`, `idx_area_elements_park_id`, `idx_natural_elements_scientific_name`, `idx_parks_code`, `idx_visitors_park_id`, además de los índices automáticos de claves primarias y foráneas) son adecuados para optimizar el conjunto completo de consultas requeridas, incluyendo las del punto 1.c.

### Database Comparison Procedure (Additional Req 6)

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
CALL compare_databases('database1', 'database2');
```

### Concurrency Control & Recovery Mechanisms (Additional Req 7)

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
