-- Sample data for park_management database
-- Run this script AFTER running setup.sql

USE park_management;

-- Provinces (Add a few more distinct ones)
INSERT INTO provinces (name, responsible_organization) VALUES
('Mendoza', 'Secretaría de Ambiente y Ordenamiento Territorial'),
('Río Negro', 'Secretaría de Ambiente y Desarrollo Sustentable'),
('Misiones', 'Ministerio de Ecología y RNR');
-- Add province IDs from functional tests if needed for consistency, or query them later.
-- SELECT id INTO @ba_id FROM provinces WHERE name = 'Buenos Aires'; -- Example

-- Parks (Add a few more, maybe one shared)
INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES
('Aconcagua Provincial Park', '1983-11-28', 'aconcagua@mendoza.gov.ar', 'AP', 71000),
('Nahuel Huapi National Park', '1934-09-29', 'nahuelhuapi@apn.gob.ar', 'NH', 717261),
('Iguazú National Park', '1934-10-09', 'iguazu@apn.gob.ar', 'IG', 67620);
-- Get Park IDs
-- SELECT id INTO @ap_id FROM parks WHERE code = 'AP'; -- Example

-- Park Provinces (Link new parks/provinces)
-- Assuming Mendoza ID = 4, Rio Negro ID = 5, Misiones ID = 6 (adjust based on actual IDs)
-- Assuming Aconcagua ID = 4, Nahuel Huapi ID = 5, Iguazu ID = 6 (adjust based on actual IDs)
INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES
(4, 4, 71000), -- Aconcagua in Mendoza
(5, 5, 717261), -- Nahuel Huapi in Rio Negro (Simplified - actually shared with Neuquén)
(6, 6, 67620); -- Iguazu in Misiones

-- Park Areas (Add areas for new parks)
INSERT INTO park_areas (park_id, area_number, name, extension) VALUES
(4, 1, 'Horcones Valley', 30000),
(4, 2, 'Plaza de Mulas Base Camp Area', 1000),
(5, 1, 'Circuito Chico Area', 50000),
(5, 2, 'Tronador Area', 100000),
(6, 1, 'Garganta del Diablo Circuit Area', 5000),
(6, 2, 'Macuco Trail Area', 10000);

-- Natural Elements (Add diverse examples)
INSERT INTO natural_elements (scientific_name, common_name) VALUES
('Vultur gryphus', 'Andean Condor'),
('Puma concolor', 'Puma'),
('Lama guanicoe', 'Guanaco'),
('Nothofagus pumilio', 'Lenga Beech'),
('Berberis microphylla', 'Calafate'),
('Quartz', 'Quartz Crystal'),
('Granite', 'Granite Rock'),
('Panthera onca', 'Jaguar'),
('Euterpe edulis', 'Palmito Palm');
-- Get Element IDs
-- SELECT id INTO @condor_id FROM natural_elements WHERE scientific_name = 'Vultur gryphus'; -- Example

-- Element Subtypes (Link new elements)
INSERT INTO animal_elements (element_id, diet, mating_season) VALUES
((SELECT id FROM natural_elements WHERE scientific_name = 'Vultur gryphus'), 'carnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Puma concolor'), 'carnivore', 'Varies'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Lama guanicoe'), 'herbivore', 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Panthera onca'), 'carnivore', 'Year-round');

INSERT INTO vegetal_elements (element_id, flowering_period) VALUES
((SELECT id FROM natural_elements WHERE scientific_name = 'Nothofagus pumilio'), 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Berberis microphylla'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Euterpe edulis'), 'Spring/Summer');

INSERT INTO mineral_elements (element_id, crystal_or_rock) VALUES
((SELECT id FROM natural_elements WHERE scientific_name = 'Quartz'), 'crystal'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Granite'), 'rock');

-- Area Elements (Distribute new elements across new areas)
INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES
(4, 1, (SELECT id FROM natural_elements WHERE scientific_name = 'Vultur gryphus'), 50),
(4, 1, (SELECT id FROM natural_elements WHERE scientific_name = 'Lama guanicoe'), 200),
(4, 1, (SELECT id FROM natural_elements WHERE scientific_name = 'Quartz'), 1000), -- Representing presence
(5, 1, (SELECT id FROM natural_elements WHERE scientific_name = 'Nothofagus pumilio'), 5000),
(5, 2, (SELECT id FROM natural_elements WHERE scientific_name = 'Puma concolor'), 20),
(6, 1, (SELECT id FROM natural_elements WHERE scientific_name = 'Panthera onca'), 15),
(6, 2, (SELECT id FROM natural_elements WHERE scientific_name = 'Euterpe edulis'), 1000);

-- Personnel (Add examples for different roles)
INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES
('P111222', '20-111222-3', 'Ana Garcia', 'Calle Falsa 123', '555-1111', 60000.00),
('P333444', '27-333444-5', 'Juan Perez', 'Av Siempreviva 742', '555-2222', 55000.00),
('P555666', '20-555666-7', 'Maria Lopez', 'Boulevard Roto 456', '555-3333', 70000.00),
('P777888', '23-777888-9', 'Carlos Sanchez', 'Pasaje Seguro 789', '555-4444', 58000.00);
-- Get Personnel IDs
-- SELECT id INTO @ana_id FROM personnel WHERE DNI = 'P111222'; -- Example

-- Personnel Subtypes (Assign roles)
INSERT INTO management_personnel (personnel_id, entrance_number) VALUES
((SELECT id FROM personnel WHERE DNI = 'P111222'), 1); -- Ana Garcia is management at entrance 1

INSERT INTO surveillance_personnel (personnel_id, vehicle_type, vehicle_registration) VALUES
((SELECT id FROM personnel WHERE DNI = 'P333444'), '4x4 Pickup', 'AE567FG'); -- Juan Perez is surveillance

INSERT INTO research_personnel (personnel_id, project_id, title) VALUES
((SELECT id FROM personnel WHERE DNI = 'P555666'), 1, 'Biologist'); -- Maria Lopez is research (assuming project_id 1 exists from tests or add one)

INSERT INTO conservation_personnel (personnel_id, specialty, park_id, area_number) VALUES
((SELECT id FROM personnel WHERE DNI = 'P777888'), 'Trail Maintenance', 5, 1); -- Carlos Sanchez is conservation in Nahuel Huapi Area 1

-- Visitors (Add some visitors to new parks/accommodations)
-- First add accommodations
INSERT INTO accommodations (capacity, category) VALUES
(8, 'Mountain Lodge'),
(2, 'Riverside Cabin');
-- Get Accommodation IDs
-- SELECT id INTO @lodge_id FROM accommodations WHERE category = 'Mountain Lodge'; -- Example

INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES
('V101010', 'Laura Gomez', 'Some Street 1', 'Engineer', (SELECT id FROM accommodations WHERE category = 'Mountain Lodge'), 4), -- Visitor in Aconcagua
('V202020', 'Pedro Martinez', 'Other Street 2', 'Doctor', (SELECT id FROM accommodations WHERE category = 'Riverside Cabin'), 5), -- Visitor in Nahuel Huapi
('V303030', 'Sofia Rodriguez', 'Another Street 3', 'Teacher', (SELECT id FROM accommodations WHERE category = 'Riverside Cabin'), 5); -- Visitor in Nahuel Huapi

-- Excursions (Add examples)
INSERT INTO excursions (day_of_week, time, type) VALUES
('Saturday', '08:00:00', 'foot'),
('Sunday', '14:00:00', 'vehicle');
-- Get Excursion IDs
-- SELECT id INTO @hike_id FROM excursions WHERE day_of_week = 'Saturday'; -- Example

-- Accommodation Excursions (Link accommodations to excursions)
INSERT INTO accommodation_excursions (accommodation_id, excursion_id) VALUES
((SELECT id FROM accommodations WHERE category = 'Mountain Lodge'), (SELECT id FROM excursions WHERE day_of_week = 'Saturday')),
((SELECT id FROM accommodations WHERE category = 'Riverside Cabin'), (SELECT id FROM excursions WHERE day_of_week = 'Sunday'));

-- Visitor Excursions (Link visitors to excursions)
INSERT INTO visitor_excursions (visitor_id, excursion_id) VALUES
((SELECT id FROM visitors WHERE DNI = 'V101010'), (SELECT id FROM excursions WHERE day_of_week = 'Saturday')),
((SELECT id FROM visitors WHERE DNI = 'V202020'), (SELECT id FROM excursions WHERE day_of_week = 'Sunday'));

-- Element Food (Example: Puma eats Guanaco)
INSERT INTO element_food (element_id, food_element_id) VALUES
((SELECT id FROM natural_elements WHERE scientific_name = 'Puma concolor'), (SELECT id FROM natural_elements WHERE scientific_name = 'Lama guanicoe'));

-- Add more data as needed...
SELECT 'Sample data population complete.' AS status;
