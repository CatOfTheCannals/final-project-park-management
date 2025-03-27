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
- **Element Food Constraints:** The `CHECK` constraints (`check_mineral_not_food`, `check_vegetal_not_feeding`) intended for the `element_food` table were removed from the DDL (`sql/setup.sql`). MySQL does not support subqueries within `CHECK` constraints. This logic (preventing minerals as food, preventing plants from feeding) is currently **not enforced** at the database level and would need to be handled by application logic or triggers if required.

## Trade-offs
- **Test Focus vs Implementation Speed:** By focusing on tests first, we ensure quality but may initially be slower than direct implementation.
- **Schema Complexity vs Requirement Fidelity:** Some relationships (mentioned in Simplifications) were omitted or simplified to reduce schema complexity and meet the "minimal effort" guideline. Some constraints (like element food rules) were removed due to database engine limitations, shifting enforcement responsibility.
