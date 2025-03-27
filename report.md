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
- **Surveillance Vehicle:** The `surveillance_personnel` table links a vehicle directly to the personnel member. The requirement nuance "siempre es el mismo en cada área que vigila" (always the same in each area they watch) is simplified; we assume one primary vehicle per surveillance staff member rather than tracking vehicle assignments per area vigilated.
- **Research Element Link:** The relationship between research projects/personnel and the specific `natural_elements` being researched (Requirement 10.c.1) is not implemented in the current schema to maintain simplicity.
- **Conservation Area Link:** The relationship between `conservation_personnel` and the specific `park_areas` they maintain (Requirement 10.d) is not implemented in the current schema for simplicity.

## Trade-offs
- **Test Focus vs Implementation Speed:** By focusing on tests first, we ensure quality but may initially be slower than direct implementation.
- **Schema Complexity vs Requirement Fidelity:** Some relationships (mentioned in Simplifications) were omitted to reduce schema complexity and meet the "minimal effort" guideline, potentially limiting some complex queries not explicitly listed in the requirements.
