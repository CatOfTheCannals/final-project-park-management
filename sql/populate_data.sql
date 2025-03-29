-- Comprehensive data for park_management database
-- Run this script AFTER running setup.sql

USE park_management;

-- =============================================
-- PROVINCES
-- Based on data/areas_protegidas_nacionales_y_provinciales_por_jurisdiccion.csv
-- =============================================
INSERT INTO provinces (name, responsible_organization) VALUES
('Buenos Aires', 'Organismo Provincial para el Desarrollo Sostenible'),
('Catamarca', 'Secretaría de Estado del Ambiente y Desarrollo Sustentable'),
('Ciudad A. de Buenos Aires', 'Agencia de Protección Ambiental'),
('Chaco', 'Ministerio de Planificación, Ambiente e Innovación Tecnológica'),
('Chubut', 'Ministerio de Ambiente y Control del Desarrollo Sustentable'),
('Córdoba', 'Secretaría de Ambiente y Cambio Climático'),
('Corrientes', 'Instituto de Conservación del Iberá'),
('Entre Ríos', 'Secretaría de Ambiente'),
('Formosa', 'Ministerio de la Producción y Ambiente'),
('Jujuy', 'Ministerio de Ambiente'),
('La Pampa', 'Subsecretaría de Ambiente'),
('La Rioja', 'Secretaría de Ambiente'),
('Mendoza', 'Secretaría de Ambiente y Ordenamiento Territorial'),
('Misiones', 'Ministerio de Ecología y Recursos Naturales Renovables'),
('Neuquén', 'Secretaría de Desarrollo Territorial y Ambiente'),
('Río Negro', 'Secretaría de Ambiente y Desarrollo Sustentable'),
('Salta', 'Ministerio de Producción y Desarrollo Sustentable'),
('San Juan', 'Secretaría de Estado de Ambiente y Desarrollo Sustentable'),
('San Luis', 'Ministerio de Medio Ambiente, Campo y Producción'),
('Santa Cruz', 'Secretaría de Estado de Ambiente'),
('Santa Fe', 'Ministerio de Ambiente y Cambio Climático'),
('Santiago del Estero', 'Dirección General de Bosques y Fauna'),
('Tierra del Fuego', 'Secretaría de Ambiente, Desarrollo Sostenible y Cambio Climático'),
('Tucumán', 'Secretaría de Estado de Medio Ambiente');

-- =============================================
-- PARKS
-- =============================================
INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES
-- National Parks
('Nahuel Huapi', '1934-04-29', 'nahuelhuapi@parquesnacionales.gob.ar', 'NH', 717261),
('Iguazú', '1934-10-09', 'iguazu@parquesnacionales.gob.ar', 'IG', 67620),
('El Palmar', '1966-06-23', 'elpalmar@parquesnacionales.gob.ar', 'EP', 8500),
('Los Glaciares', '1937-05-11', 'glaciares@parquesnacionales.gob.ar', 'LG', 726927),
('Tierra del Fuego', '1960-10-15', 'tierradelfuego@parquesnacionales.gob.ar', 'TF', 68909),
('Talampaya', '1997-07-11', 'talampaya@parquesnacionales.gob.ar', 'TA', 215000),
('Sierra de las Quijadas', '1991-12-10', 'quijadas@parquesnacionales.gob.ar', 'SQ', 73785),
('Calilegua', '1979-07-19', 'calilegua@parquesnacionales.gob.ar', 'CA', 76306),
('El Rey', '1948-05-24', 'elrey@parquesnacionales.gob.ar', 'ER', 44162),
('Los Cardones', '1996-12-11', 'cardones@parquesnacionales.gob.ar', 'LC', 64117),
-- Provincial Parks
('Aconcagua', '1983-11-28', 'aconcagua@mendoza.gob.ar', 'AC', 71000),
('Iberá', '2018-12-05', 'ibera@corrientes.gob.ar', 'IB', 159800),
('Pereyra Iraola', '1967-11-01', 'pereyrairaola@buenosaires.gob.ar', 'PI', 10248),
('Islas de Santa Fe', '1999-12-29', 'islasdesantafe@santafe.gob.ar', 'IS', 4096),
('Chancaní', '1986-07-15', 'chancani@cordoba.gob.ar', 'CH', 4920),
('Ernesto Tornquist', '1958-06-01', 'tornquist@buenosaires.gob.ar', 'ET', 6700),
('Laguna de Mar Chiquita', '1991-01-05', 'marchiquita@cordoba.gob.ar', 'LM', 80000),
('Península Valdés', '1983-09-29', 'peninsulavaldes@chubut.gob.ar', 'PV', 360000),
('Parque Luro', '1997-05-12', 'parqueluro@lapampa.gob.ar', 'PL', 7600),
('Bañados del Río Dulce', '2008-11-21', 'riodulce@santiago.gob.ar', 'RD', 9000);

-- =============================================
-- PARK PROVINCES (Link parks to provinces)
-- =============================================
-- Get province IDs - using SET to avoid output in console
SET @ba_id = (SELECT id FROM provinces WHERE name = 'Buenos Aires');
SET @catamarca_id = (SELECT id FROM provinces WHERE name = 'Catamarca');
SET @chaco_id = (SELECT id FROM provinces WHERE name = 'Chaco');
SET @ct_id = (SELECT id FROM provinces WHERE name = 'Chubut');
SET @co_id = (SELECT id FROM provinces WHERE name = 'Córdoba');
SET @cr_id = (SELECT id FROM provinces WHERE name = 'Corrientes');
SET @entre_rios_id = (SELECT id FROM provinces WHERE name = 'Entre Ríos');
SET @ju_id = (SELECT id FROM provinces WHERE name = 'Jujuy');
SET @lp_id = (SELECT id FROM provinces WHERE name = 'La Pampa');
SET @lr_id = (SELECT id FROM provinces WHERE name = 'La Rioja');
SET @me_id = (SELECT id FROM provinces WHERE name = 'Mendoza');
SET @mi_id = (SELECT id FROM provinces WHERE name = 'Misiones');
SET @ne_id = (SELECT id FROM provinces WHERE name = 'Neuquén');
SET @rn_id = (SELECT id FROM provinces WHERE name = 'Río Negro');
SET @sa_id = (SELECT id FROM provinces WHERE name = 'Salta');
SET @sj_id = (SELECT id FROM provinces WHERE name = 'San Juan');
SET @sl_id = (SELECT id FROM provinces WHERE name = 'San Luis');
SET @sc_id = (SELECT id FROM provinces WHERE name = 'Santa Cruz');
SET @sf_id = (SELECT id FROM provinces WHERE name = 'Santa Fe');
SET @se_id = (SELECT id FROM provinces WHERE name = 'Santiago del Estero');
SET @tf_id = (SELECT id FROM provinces WHERE name = 'Tierra del Fuego');
SET @tu_id = (SELECT id FROM provinces WHERE name = 'Tucumán');

-- Get park IDs - using SET to avoid output in console
SET @nh_id = (SELECT id FROM parks WHERE code = 'NH');
SET @ig_id = (SELECT id FROM parks WHERE code = 'IG');
SET @ep_id = (SELECT id FROM parks WHERE code = 'EP');
SET @lg_id = (SELECT id FROM parks WHERE code = 'LG');
SET @tf_park_id = (SELECT id FROM parks WHERE code = 'TF');
SET @ta_id = (SELECT id FROM parks WHERE code = 'TA');
SET @sq_id = (SELECT id FROM parks WHERE code = 'SQ');
SET @calilegua_id = (SELECT id FROM parks WHERE code = 'CA');
SET @el_rey_id = (SELECT id FROM parks WHERE code = 'ER');
SET @lc_id = (SELECT id FROM parks WHERE code = 'LC');
SET @ac_id = (SELECT id FROM parks WHERE code = 'AC');
SET @ib_id = (SELECT id FROM parks WHERE code = 'IB');
SET @pi_id = (SELECT id FROM parks WHERE code = 'PI');
SET @is_id = (SELECT id FROM parks WHERE code = 'IS');
SET @chancani_id = (SELECT id FROM parks WHERE code = 'CH');
SET @et_id = (SELECT id FROM parks WHERE code = 'ET');
SET @lm_id = (SELECT id FROM parks WHERE code = 'LM');
SET @pv_id = (SELECT id FROM parks WHERE code = 'PV');
SET @pl_id = (SELECT id FROM parks WHERE code = 'PL');
SET @rd_id = (SELECT id FROM parks WHERE code = 'RD');

-- Link parks to provinces
INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES
-- National Parks
(@nh_id, @rn_id, 500000), -- Nahuel Huapi in Rio Negro
(@nh_id, @ne_id, 217261), -- Nahuel Huapi in Neuquén (shared)
(@ig_id, @mi_id, 67620),  -- Iguazú in Misiones
(@ep_id, @entre_rios_id, 8500),   -- El Palmar in Entre Ríos
(@lg_id, @sc_id, 726927), -- Los Glaciares in Santa Cruz
(@tf_park_id, @tf_id, 68909), -- Tierra del Fuego in Tierra del Fuego
(@ta_id, @lr_id, 215000), -- Talampaya in La Rioja
(@sq_id, @sl_id, 73785),  -- Sierra de las Quijadas in San Luis
(@calilegua_id, @ju_id, 76306),  -- Calilegua in Jujuy
(@el_rey_id, @sa_id, 44162),  -- El Rey in Salta
(@lc_id, @sa_id, 64117),  -- Los Cardones in Salta
-- Provincial Parks
(@ac_id, @me_id, 71000),  -- Aconcagua in Mendoza
(@ib_id, @cr_id, 159800), -- Iberá in Corrientes
(@pi_id, @ba_id, 10248),  -- Pereyra Iraola in Buenos Aires
(@is_id, @sf_id, 4096),   -- Islas de Santa Fe in Santa Fe
(@chancani_id, @co_id, 4920),   -- Chancaní in Córdoba
(@et_id, @ba_id, 6700),   -- Ernesto Tornquist in Buenos Aires
(@lm_id, @co_id, 80000),  -- Laguna de Mar Chiquita in Córdoba
(@pv_id, @ct_id, 360000), -- Península Valdés in Chubut
(@pl_id, @lp_id, 7600),   -- Parque Luro in La Pampa
(@rd_id, @se_id, 9000);   -- Bañados del Río Dulce in Santiago del Estero

-- =============================================
-- PARK AREAS
-- =============================================
-- Create areas for each park (at least 2-3 per park)
INSERT INTO park_areas (park_id, area_number, name, extension) VALUES
-- Nahuel Huapi areas
(@nh_id, 1, 'Circuito Chico', 50000),
(@nh_id, 2, 'Tronador', 100000),
(@nh_id, 3, 'Isla Victoria', 30000),
(@nh_id, 4, 'Valle del Manso', 80000),
-- Iguazú areas
(@ig_id, 1, 'Garganta del Diablo', 5000),
(@ig_id, 2, 'Circuito Superior', 10000),
(@ig_id, 3, 'Circuito Inferior', 8000),
(@ig_id, 4, 'Isla San Martín', 2000),
-- El Palmar areas
(@ep_id, 1, 'Palmeral', 5000),
(@ep_id, 2, 'Río Uruguay', 2000),
-- Los Glaciares areas
(@lg_id, 1, 'Perito Moreno', 100000),
(@lg_id, 2, 'Upsala', 150000),
(@lg_id, 3, 'Cerro Chaltén', 80000),
-- Tierra del Fuego areas
(@tf_park_id, 1, 'Bahía Lapataia', 20000),
(@tf_park_id, 2, 'Lago Roca', 15000),
-- Talampaya areas
(@ta_id, 1, 'Cañón de Talampaya', 50000),
(@ta_id, 2, 'Ciudad Perdida', 30000),
-- Sierra de las Quijadas areas
(@sq_id, 1, 'Potrero de la Aguada', 20000),
(@sq_id, 2, 'Sierra del Gigante', 25000),
-- Calilegua areas
(@calilegua_id, 1, 'Selva Pedemontana', 25000),
(@calilegua_id, 2, 'Selva Montana', 30000),
-- El Rey areas
(@el_rey_id, 1, 'Selva de Yungas', 20000),
(@el_rey_id, 2, 'Río Popayán', 15000),
-- Los Cardones areas
(@lc_id, 1, 'Valle Encantado', 30000),
(@lc_id, 2, 'Quebrada de Cajón', 25000),
-- Aconcagua areas
(@ac_id, 1, 'Valle de Horcones', 30000),
(@ac_id, 2, 'Plaza de Mulas', 20000),
-- Iberá areas
(@ib_id, 1, 'Laguna Iberá', 50000),
(@ib_id, 2, 'Esteros del Iberá', 70000),
-- Pereyra Iraola areas
(@pi_id, 1, 'Sector Santa Rosa', 5000),
(@pi_id, 2, 'Sector San Juan', 4000),
-- Islas de Santa Fe areas
(@is_id, 1, 'Isla El Chapetón', 2000),
(@is_id, 2, 'Isla Los Mellados', 1500),
-- Chancaní areas
(@chancani_id, 1, 'Bosque Chaqueño', 3000),
(@chancani_id, 2, 'Quebradas', 1500),
-- Ernesto Tornquist areas
(@et_id, 1, 'Sierra de la Ventana', 4000),
(@et_id, 2, 'Cerro Tres Picos', 2000),
-- Laguna de Mar Chiquita areas
(@lm_id, 1, 'Bañados del Río Dulce', 40000),
(@lm_id, 2, 'Costa de la Laguna', 30000),
-- Península Valdés areas
(@pv_id, 1, 'Punta Norte', 80000),
(@pv_id, 2, 'Caleta Valdés', 70000),
(@pv_id, 3, 'Puerto Pirámides', 50000),
-- Parque Luro areas
(@pl_id, 1, 'Caldenal', 5000),
(@pl_id, 2, 'Salitral', 2000),
-- Bañados del Río Dulce areas
(@rd_id, 1, 'Bañados Norte', 5000),
(@rd_id, 2, 'Bañados Sur', 4000);

-- =============================================
-- NATURAL ELEMENTS
-- Based on data/representatividad_de_las_especies_en_areas_protegidas_nacionales.csv
-- =============================================
-- ANIMALS
INSERT INTO natural_elements (scientific_name, common_name) VALUES
-- Mammals
('Panthera onca', 'Jaguar'),
('Puma concolor', 'Puma'),
('Hippocamelus bisulcus', 'Huemul'),
('Lama guanicoe', 'Guanaco'),
('Myrmecophaga tridactyla', 'Oso Hormiguero'),
('Tapirus terrestris', 'Tapir'),
('Chrysocyon brachyurus', 'Aguará Guazú'),
('Lontra longicaudis', 'Lobito de Río'),
('Leopardus geoffroyi', 'Gato Montés'),
('Dolichotis patagonum', 'Mara'),
-- Birds
('Vultur gryphus', 'Cóndor Andino'),
('Rhea americana', 'Ñandú'),
('Phoenicopterus chilensis', 'Flamenco Austral'),
('Eudromia elegans', 'Martineta'),
('Cyanoliseus patagonus', 'Loro Barranquero'),
('Gubernatrix cristata', 'Cardenal Amarillo'),
('Spheniscus magellanicus', 'Pingüino de Magallanes'),
('Harpia harpyja', 'Águila Harpía'),
('Ara chloropterus', 'Guacamayo Rojo'),
('Ramphastos toco', 'Tucán Toco'),
-- Reptiles
('Caiman latirostris', 'Yacaré Overo'),
('Chelonoidis chilensis', 'Tortuga Terrestre Argentina'),
('Bothrops alternatus', 'Yarará Grande'),
('Tupinambis merianae', 'Lagarto Overo'),
('Boa constrictor occidentalis', 'Boa de las Vizcacheras'),
-- Amphibians
('Ceratophrys ornata', 'Escuerzo'),
('Melanophryniscus stelzneri', 'Sapito de Colores'),
('Leptodactylus latrans', 'Rana Criolla'),
-- Fish
('Salminus brasiliensis', 'Dorado'),
('Pseudoplatystoma corruscans', 'Surubí');

-- PLANTS
INSERT INTO natural_elements (scientific_name, common_name) VALUES
('Araucaria araucana', 'Pehuén'),
('Prosopis caldenia', 'Caldén'),
('Austrocedrus chilensis', 'Ciprés de la Cordillera'),
('Nothofagus pumilio', 'Lenga'),
('Nothofagus antarctica', 'Ñire'),
('Prosopis flexuosa', 'Algarrobo Dulce'),
('Schinopsis balansae', 'Quebracho Colorado'),
('Ceiba chodatii', 'Palo Borracho'),
('Handroanthus impetiginosus', 'Lapacho Rosado'),
('Fitzroya cupressoides', 'Alerce Patagónico'),
('Podocarpus parlatorei', 'Pino del Cerro'),
('Polylepis australis', 'Tabaquillo'),
('Bulnesia sarmientoi', 'Palo Santo'),
('Aspidosperma quebracho-blanco', 'Quebracho Blanco'),
('Jacaranda mimosifolia', 'Jacarandá'),
('Erythrina crista-galli', 'Ceibo'),
('Celtis ehrenbergiana', 'Tala'),
('Geoffroea decorticans', 'Chañar'),
('Schinus molle', 'Aguaribay'),
('Victoria cruziana', 'Irupé');

-- MINERALS
INSERT INTO natural_elements (scientific_name, common_name) VALUES
('Quartz', 'Cuarzo'),
('Granite', 'Granito'),
('Calcite', 'Calcita'),
('Rhodochrosite', 'Rodocrosita'),
('Pyrite', 'Pirita'),
('Basalt', 'Basalto'),
('Gypsum', 'Yeso'),
('Fluorite', 'Fluorita'),
('Obsidian', 'Obsidiana'),
('Marble', 'Mármol');

-- =============================================
-- ELEMENT SUBTYPES
-- =============================================
-- Animal Elements
INSERT INTO animal_elements (element_id, diet, mating_season) VALUES
((SELECT id FROM natural_elements WHERE scientific_name = 'Panthera onca'), 'carnivore', 'Year-round'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Puma concolor'), 'carnivore', 'Spring-Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Hippocamelus bisulcus'), 'herbivore', 'Autumn'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Lama guanicoe'), 'herbivore', 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Myrmecophaga tridactyla'), 'insectivore', 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Tapirus terrestris'), 'herbivore', 'Spring-Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Chrysocyon brachyurus'), 'omnivore', 'Autumn-Winter'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Lontra longicaudis'), 'carnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Leopardus geoffroyi'), 'carnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Dolichotis patagonum'), 'herbivore', 'Spring-Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Vultur gryphus'), 'carnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Rhea americana'), 'omnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Phoenicopterus chilensis'), 'omnivore', 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Eudromia elegans'), 'omnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Cyanoliseus patagonus'), 'herbivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Gubernatrix cristata'), 'omnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Spheniscus magellanicus'), 'carnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Harpia harpyja'), 'carnivore', 'Spring-Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Ara chloropterus'), 'herbivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Ramphastos toco'), 'omnivore', 'Spring-Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Caiman latirostris'), 'carnivore', 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Chelonoidis chilensis'), 'herbivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Bothrops alternatus'), 'carnivore', 'Autumn'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Tupinambis merianae'), 'omnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Boa constrictor occidentalis'), 'carnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Ceratophrys ornata'), 'carnivore', 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Melanophryniscus stelzneri'), 'insectivore', 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Leptodactylus latrans'), 'insectivore', 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Salminus brasiliensis'), 'carnivore', 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Pseudoplatystoma corruscans'), 'carnivore', 'Spring-Summer');

-- Vegetal Elements
INSERT INTO vegetal_elements (element_id, flowering_period) VALUES
((SELECT id FROM natural_elements WHERE scientific_name = 'Araucaria araucana'), 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Prosopis caldenia'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Austrocedrus chilensis'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Nothofagus pumilio'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Nothofagus antarctica'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Prosopis flexuosa'), 'Spring-Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Schinopsis balansae'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Ceiba chodatii'), 'Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Handroanthus impetiginosus'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Fitzroya cupressoides'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Podocarpus parlatorei'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Polylepis australis'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Bulnesia sarmientoi'), 'Spring-Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Aspidosperma quebracho-blanco'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Jacaranda mimosifolia'), 'Spring-Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Erythrina crista-galli'), 'Spring-Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Celtis ehrenbergiana'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Geoffroea decorticans'), 'Spring'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Schinus molle'), 'Spring-Summer'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Victoria cruziana'), 'Summer');

-- Mineral Elements
INSERT INTO mineral_elements (element_id, crystal_or_rock) VALUES
((SELECT id FROM natural_elements WHERE scientific_name = 'Quartz'), 'crystal'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Granite'), 'rock'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Calcite'), 'crystal'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Rhodochrosite'), 'crystal'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Pyrite'), 'crystal'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Basalt'), 'rock'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Gypsum'), 'crystal'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Fluorite'), 'crystal'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Obsidian'), 'rock'),
((SELECT id FROM natural_elements WHERE scientific_name = 'Marble'), 'rock');

-- =============================================
-- AREA ELEMENTS (Distribute elements across areas)
-- =============================================
-- Helper function to get random number of individuals
DELIMITER //
CREATE FUNCTION random_individuals(min_val INT, max_val INT) 
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN FLOOR(min_val + RAND() * (max_val - min_val));
END //
DELIMITER ;

-- Get element IDs for distribution - using SET to avoid output in console
SET @jaguar_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Panthera onca');
SET @puma_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Puma concolor');
SET @huemul_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Hippocamelus bisulcus');
SET @guanaco_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Lama guanicoe');
SET @hormiguero_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Myrmecophaga tridactyla');
SET @tapir_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Tapirus terrestris');
SET @aguara_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Chrysocyon brachyurus');
SET @lobito_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Lontra longicaudis');
SET @gatomontes_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Leopardus geoffroyi');
SET @mara_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Dolichotis patagonum');
SET @condor_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Vultur gryphus');
SET @nandu_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Rhea americana');
SET @flamenco_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Phoenicopterus chilensis');
SET @martineta_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Eudromia elegans');
SET @loro_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Cyanoliseus patagonus');
SET @cardenal_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Gubernatrix cristata');
SET @pinguino_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Spheniscus magellanicus');
SET @aguila_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Harpia harpyja');
SET @guacamayo_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Ara chloropterus');
SET @tucan_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Ramphastos toco');

-- Plant IDs
SET @pehuen_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Araucaria araucana');
SET @calden_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Prosopis caldenia');
SET @cipres_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Austrocedrus chilensis');
SET @lenga_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Nothofagus pumilio');
SET @nire_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Nothofagus antarctica');
SET @algarrobo_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Prosopis flexuosa');
SET @quebracho_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Schinopsis balansae');
SET @paloborracho_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Ceiba chodatii');
SET @lapacho_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Handroanthus impetiginosus');
SET @alerce_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Fitzroya cupressoides');

-- Mineral IDs
SET @quartz_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Quartz');
SET @granite_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Granite');
SET @calcite_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Calcite');
SET @rhodochrosite_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Rhodochrosite');
SET @basalt_id = (SELECT id FROM natural_elements WHERE scientific_name = 'Basalt');

-- Distribute elements across areas
-- Nahuel Huapi (Patagonia)
INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES
(@nh_id, 1, @puma_id, random_individuals(10, 30)),
(@nh_id, 1, @huemul_id, random_individuals(50, 100)),
(@nh_id, 1, @condor_id, random_individuals(20, 40)),
(@nh_id, 1, @lenga_id, random_individuals(5000, 10000)),
(@nh_id, 1, @cipres_id, random_individuals(3000, 6000)),
(@nh_id, 1, @granite_id, random_individuals(1000, 5000)),
(@nh_id, 2, @puma_id, random_individuals(5, 15)),
(@nh_id, 2, @huemul_id, random_individuals(30, 70)),
(@nh_id, 2, @condor_id, random_individuals(15, 30)),
(@nh_id, 2, @lenga_id, random_individuals(8000, 15000)),
(@nh_id, 2, @nire_id, random_individuals(4000, 8000)),
(@nh_id, 2, @alerce_id, random_individuals(500, 1000)),
(@nh_id, 3, @lobito_id, random_individuals(30, 60)),
(@nh_id, 3, @lenga_id, random_individuals(3000, 6000)),
(@nh_id, 3, @cipres_id, random_individuals(2000, 4000)),
(@nh_id, 4, @puma_id, random_individuals(8, 20)),
(@nh_id, 4, @guanaco_id, random_individuals(100, 200)),
(@nh_id, 4, @lenga_id, random_individuals(6000, 12000));

-- Iguazú (Subtropical)
INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES
(@ig_id, 1, @jaguar_id, random_individuals(5, 10)),
(@ig_id, 1, @tapir_id, random_individuals(20, 40)),
(@ig_id, 1, @tucan_id, random_individuals(50, 100)),
(@ig_id, 1, @lapacho_id, random_individuals(500, 1000)),
(@ig_id, 1, @paloborracho_id, random_individuals(200, 400)),
(@ig_id, 2, @jaguar_id, random_individuals(3, 8)),
(@ig_id, 2, @hormiguero_id, random_individuals(15, 30)),
(@ig_id, 2, @guacamayo_id, random_individuals(30, 60)),
(@ig_id, 2, @lapacho_id, random_individuals(300, 600)),
(@ig_id, 3, @tapir_id, random_individuals(15, 30)),
(@ig_id, 3, @tucan_id, random_individuals(40, 80)),
(@ig_id, 3, @lapacho_id, random_individuals(400, 800)),
(@ig_id, 4, @lobito_id, random_individuals(10, 20)),
(@ig_id, 4, @tucan_id, random_individuals(20, 40));

-- Los Glaciares (Patagonia)
INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES
(@lg_id, 1, @puma_id, random_individuals(10, 25)),
(@lg_id, 1, @condor_id, random_individuals(30, 60)),
(@lg_id, 1, @lenga_id, random_individuals(4000, 8000)),
(@lg_id, 1, @nire_id, random_individuals(3000, 6000)),
(@lg_id, 1, @basalt_id, random_individuals(2000, 5000)),
(@lg_id, 2, @huemul_id, random_individuals(40, 80)),
(@lg_id, 2, @condor_id, random_individuals(25, 50)),
(@lg_id, 2, @lenga_id, random_individuals(5000, 10000)),
(@lg_id, 3, @puma_id, random_individuals(8, 20)),
(@lg_id, 3, @guanaco_id, random_individuals(150, 300)),
(@lg_id, 3, @lenga_id, random_individuals(3000, 6000));

-- Aconcagua (Mountain)
INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES
(@ac_id, 1, @puma_id, random_individuals(5, 15)),
(@ac_id, 1, @guanaco_id, random_individuals(200, 400)),
(@ac_id, 1, @condor_id, random_individuals(20, 40)),
(@ac_id, 1, @quartz_id, random_individuals(1000, 3000)),
(@ac_id, 1, @granite_id, random_individuals(5000, 10000)),
(@ac_id, 2, @condor_id, random_individuals(15, 30)),
(@ac_id, 2, @guanaco_id, random_individuals(50, 100)),
(@ac_id, 2, @granite_id, random_individuals(3000, 6000));

-- Iberá (Wetlands)
INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES
(@ib_id, 1, @aguara_id, random_individuals(20, 40)),
(@ib_id, 1, @lobito_id, random_individuals(50, 100)),
(@ib_id, 1, @gatomontes_id, random_individuals(200, 400)),
(@ib_id, 2, @aguara_id, random_individuals(15, 30)),
(@ib_id, 2, @gatomontes_id, random_individuals(150, 300));

-- Add more elements to other parks to ensure good distribution for queries
-- Make sure some elements appear in many parks (for "at least half" query)
-- Make sure some elements appear in all parks (for "in all parks" query)
-- Make sure some elements appear in only one park (for "only one park" query)

-- Common elements (in most parks)
INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES
-- Puma in many parks
(@ep_id, 1, @puma_id, random_individuals(5, 15)),
(@ta_id, 1, @puma_id, random_individuals(8, 20)),
(@sq_id, 1, @puma_id, random_individuals(6, 18)),
(@ca_id, 1, @puma_id, random_individuals(7, 17)),
(@er_id, 1, @puma_id, random_individuals(9, 22)),
(@lc_id, 1, @puma_id, random_individuals(10, 25)),
(@ch_id, 1, @puma_id, random_individuals(4, 12)),
(@et_id, 1, @puma_id, random_individuals(3, 10)),
-- Condor in many parks
(@ep_id, 1, @condor_id, random_individuals(10, 30)),
(@ta_id, 1, @condor_id, random_individuals(15, 35)),
(@sq_id, 1, @condor_id, random_individuals(20, 40)),
(@ca_id, 1, @condor_id, random_individuals(12, 28)),
(@er_id, 1, @condor_id, random_individuals(18, 36)),
(@lc_id, 1, @condor_id, random_individuals(25, 45)),
-- Granite in many parks
(@ep_id, 1, @granite_id, random_individuals(1000, 3000)),
(@ta_id, 1, @granite_id, random_individuals(2000, 5000)),
(@sq_id, 1, @granite_id, random_individuals(1500, 4000)),
(@ca_id, 1, @granite_id, random_individuals(1200, 3500)),
(@er_id, 1, @granite_id, random_individuals(1800, 4500)),
(@lc_id, 1, @granite_id, random_individuals(2500, 6000));

-- Rare elements (in only one park)
INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES
(@nh_id, 1, @alerce_id, random_individuals(100, 300)), -- Only in Nahuel Huapi
(@ig_id, 1, @guacamayo_id, random_individuals(40, 80)), -- Only in Iguazú
(@lg_id, 1, @pinguino_id, random_individuals(500, 1000)), -- Only in Los Glaciares
(@ac_id, 1, @rhodochrosite_id, random_individuals(200, 500)); -- Only in Aconcagua

-- =============================================
-- ELEMENT FOOD (Predator-prey relationships)
-- =============================================
INSERT INTO element_food (element_id, food_element_id) VALUES
-- Predator-prey relationships
(@jaguar_id, @tapir_id),
(@jaguar_id, @carpincho_id),
(@puma_id, @guanaco_id),
(@puma_id, @huemul_id),
(@puma_id, @nandu_id),
(@puma_id, @martineta_id),
(@aguila_id, @martineta_id),
(@aguila_id, @loro_id),
(@condor_id, @guanaco_id), -- Scavenging
(@tucan_id, @lapacho_id), -- Fruit eating
(@guacamayo_id, @lapacho_id), -- Fruit/seed eating
(@nandu_id, @calden_id), -- Seed eating
(@tapir_id, @lapacho_id), -- Fruit eating
(@guanaco_id, @lenga_id), -- Browsing
(@guanaco_id, @nire_id), -- Browsing
(@huemul_id, @lenga_id), -- Browsing
(@huemul_id, @nire_id); -- Browsing

-- =============================================
-- PERSONNEL
-- =============================================
INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES
-- Management Personnel
('P100001', '20-100001-1', 'Carlos Gómez', 'Av. Rivadavia 1234, CABA', '11-1234-5678', 85000.00),
('P100002', '27-100002-2', 'María Rodríguez', 'Calle San Martín 567, Mendoza', '261-234-5678', 82000.00),
('P100003', '20-100003-3', 'Juan Pérez', 'Av. Colón 890, Córdoba', '351-234-5678', 83000.00),
('P100004', '27-100004-4', 'Laura Fernández', 'Calle Mitre 123, Bariloche', '294-234-5678', 81000.00),
('P100005', '20-100005-5', 'Roberto Sánchez', 'Av. Belgrano 456, Salta', '387-234-5678', 84000.00),
-- Surveillance Personnel
('P200001', '20-200001-1', 'Miguel Torres', 'Calle Laprida 789, Mendoza', '261-345-6789', 75000.00),
('P200002', '27-200002-2', 'Ana González', 'Av. San Martín 234, Bariloche', '294-345-6789', 76000.00),
('P200003', '20-200003-3', 'Diego Martínez', 'Calle Belgrano 567, Puerto Iguazú', '3757-34-5678', 74000.00),
('P200004', '27-200004-4', 'Lucía Díaz', 'Av. Córdoba 890, El Calafate', '2902-34-5678', 77000.00),
('P200005', '20-200005-5', 'Fernando López', 'Calle San Lorenzo 123, Salta', '387-345-6789', 73000.00),
('P200006', '27-200006-6', 'Valeria Romero', 'Av. Urquiza 456, Corrientes', '379-345-6789', 72000.00),
('P200007', '20-200007-7', 'Martín Silva', 'Calle Alvear 789, San Luis', '266-345-6789', 71000.00),
('P200008', '27-200008-8', 'Carolina Acosta', 'Av. Independencia 234, Córdoba', '351-345-6789', 78000.00),
-- Research Personnel
('P300001', '20-300001-1', 'Alejandro Molina', 'Calle Alem 567, CABA', '11-456-7890', 90000.00),
('P300002', '27-300002-2', 'Gabriela Vargas', 'Av. Libertador 890, Mendoza', '261-456-7890', 92000.00),
('P300003', '20-300003-3', 'Sebastián Ríos', 'Calle Sarmiento 123, Córdoba', '351-456-7890', 91000.00),
('P300004', '27-300004-4', 'Natalia Pereyra', 'Av. Mitre 456, Bariloche', '294-456-7890', 93000.00),
('P300005', '20-300005-5', 'Javier Gutiérrez', 'Calle Belgrano 789, Puerto Iguazú', '3757-45-6789', 94000.00),
('P300006', '27-300006-6', 'Mariana Castro', 'Av. San Martín 234, El Calafate', '2902-45-6789', 95000.00),
('P300007', '20-300007-7', 'Pablo Núñez', 'Calle Rivadavia 567, Salta', '387-456-7890', 96000.00),
('P300008', '27-300008-8', 'Daniela Ortiz', 'Av. Corrientes 890, Corrientes', '379-456-7890', 97000.00),
-- Conservation Personnel
('P400001', '20-400001-1', 'Ricardo Medina', 'Calle Florida 123, CABA', '11-567-8901', 80000.00),
('P400002', '27-400002-2', 'Silvia Rojas', 'Av. Las Heras 456, Mendoza', '261-567-8901', 79000.00),
('P400003', '20-400003-3', 'Eduardo Paz', 'Calle Colón 789, Córdoba', '351-567-8901', 78000.00),
('P400004', '27-400004-4', 'Cecilia Vega', 'Av. Bustillo 234, Bariloche', '294-567-8901', 77000.00),
('P400005', '20-400005-5', 'Gustavo Campos', 'Calle Victoria 567, Puerto Iguazú', '3757-56-7890', 76000.00),
('P400006', '27-400006-6', 'Marcela Flores', 'Av. Libertad 890, El Calafate', '2902-56-7890', 75000.00),
('P400007', '20-400007-7', 'Hernán Soto', 'Calle Alberdi 123, Salta', '387-567-8901', 74000.00),
('P400008', '27-400008-8', 'Verónica Ramos', 'Av. 9 de Julio 456, Corrientes', '379-567-8901', 73000.00);

-- =============================================
-- RESEARCH PROJECTS
-- =============================================
INSERT INTO research_projects (budget, duration, element_id) VALUES
(250000.00, '24 months', @jaguar_id), -- Jaguar conservation project
(180000.00, '18 months', @puma_id), -- Puma tracking project
(300000.00, '36 months', @huemul_id), -- Huemul recovery program
(220000.00, '24 months', @condor_id), -- Condor monitoring project
(150000.00, '12 months', @lenga_id), -- Lenga forest health assessment
(280000.00, '30 months', @alerce_id), -- Alerce growth study
(200000.00, '24 months', @lapacho_id), -- Lapacho phenology research
(350000.00, '48 months', @tapir_id), -- Tapir habitat use study
(190000.00, '18 months', @guanaco_id), -- Guanaco population dynamics
(230000.00, '24 months', @pinguino_id); -- Penguin breeding success

-- Get project IDs - using SET to avoid output in console
SET @jaguar_project_id = (SELECT id FROM research_projects WHERE element_id = @jaguar_id);
SET @puma_project_id = (SELECT id FROM research_projects WHERE element_id = @puma_id);
SET @huemul_project_id = (SELECT id FROM research_projects WHERE element_id = @huemul_id);
SET @condor_project_id = (SELECT id FROM research_projects WHERE element_id = @condor_id);
SET @lenga_project_id = (SELECT id FROM research_projects WHERE element_id = @lenga_id);
SET @alerce_project_id = (SELECT id FROM research_projects WHERE element_id = @alerce_id);
SET @lapacho_project_id = (SELECT id FROM research_projects WHERE element_id = @lapacho_id);
SET @tapir_project_id = (SELECT id FROM research_projects WHERE element_id = @tapir_id);
SET @guanaco_project_id = (SELECT id FROM research_projects WHERE element_id = @guanaco_id);
SET @pinguino_project_id = (SELECT id FROM research_projects WHERE element_id = @pinguino_id);

-- =============================================
-- PERSONNEL SUBTYPES
-- =============================================
-- Management Personnel
INSERT INTO management_personnel (personnel_id, entrance_number) VALUES
((SELECT id FROM personnel WHERE DNI = 'P100001'), 1),
((SELECT id FROM personnel WHERE DNI = 'P100002'), 2),
((SELECT id FROM personnel WHERE DNI = 'P100003'), 1),
((SELECT id FROM personnel WHERE DNI = 'P100004'), 3),
((SELECT id FROM personnel WHERE DNI = 'P100005'), 2);

-- Surveillance Personnel
INSERT INTO surveillance_personnel (personnel_id, vehicle_type, vehicle_registration) VALUES
((SELECT id FROM personnel WHERE DNI = 'P200001'), '4x4 Toyota Hilux', 'AA123BB'),
((SELECT id FROM personnel WHERE DNI = 'P200002'), '4x4 Ford Ranger', 'AC456DE'),
((SELECT id FROM personnel WHERE DNI = 'P200003'), 'Motocicleta Honda XR', 'AF789GH'),
((SELECT id FROM personnel WHERE DNI = 'P200004'), '4x4 Chevrolet S10', 'AI012JK'),
((SELECT id FROM personnel WHERE DNI = 'P200005'), '4x4 Toyota Land Cruiser', 'AL345MN'),
((SELECT id FROM personnel WHERE DNI = 'P200006'), 'Motocicleta Yamaha XT', 'AO678PQ'),
((SELECT id FROM personnel WHERE DNI = 'P200007'), '4x4 Volkswagen Amarok', 'AR901ST'),
((SELECT id FROM personnel WHERE DNI = 'P200008'), '4x4 Nissan Frontier', 'AU234VW');

-- Research Personnel
INSERT INTO research_personnel (personnel_id, project_id, title) VALUES
((SELECT id FROM personnel WHERE DNI = 'P300001'), @jaguar_project_id, 'Biólogo'),
((SELECT id FROM personnel WHERE DNI = 'P300002'), @puma_project_id, 'Zoóloga'),
((SELECT id FROM personnel WHERE DNI = 'P300003'), @huemul_project_id, 'Veterinario'),
((SELECT id FROM personnel WHERE DNI = 'P300004'), @condor_project_id, 'Ornitóloga'),
((SELECT id FROM personnel WHERE DNI = 'P300005'), @lenga_project_id, 'Botánico'),
((SELECT id FROM personnel WHERE DNI = 'P300006'), @alerce_project_id, 'Dendrocronóloga'),
((SELECT id FROM personnel WHERE DNI = 'P300007'), @tapir_project_id, 'Ecólogo'),
((SELECT id FROM personnel WHERE DNI = 'P300008'), @guanaco_project_id, 'Bióloga de Conservación'),
-- Some researchers work on multiple projects
((SELECT id FROM personnel WHERE DNI = 'P300001'), @tapir_project_id, 'Biólogo'),
((SELECT id FROM personnel WHERE DNI = 'P300004'), @pinguino_project_id, 'Ornitóloga'),
((SELECT id FROM personnel WHERE DNI = 'P300005'), @lapacho_project_id, 'Botánico');

-- Conservation Personnel
INSERT INTO conservation_personnel (personnel_id, specialty, park_id, area_number) VALUES
((SELECT id FROM personnel WHERE DNI = 'P400001'), 'Mantenimiento de Senderos', @nh_id, 1),
((SELECT id FROM personnel WHERE DNI = 'P400002'), 'Restauración de Hábitat', @ig_id, 1),
((SELECT id FROM personnel WHERE DNI = 'P400003'), 'Control de Especies Invasoras', @lg_id, 1),
((SELECT id FROM personnel WHERE DNI = 'P400004'), 'Monitoreo de Calidad de Agua', @tf_park_id, 1),
((SELECT id FROM personnel WHERE DNI = 'P400005'), 'Prevención de Incendios', @ta_id, 1),
((SELECT id FROM personnel WHERE DNI = 'P400006'), 'Educación Ambiental', @sq_id, 1),
((SELECT id FROM personnel WHERE DNI = 'P400007'), 'Reforestación', @calilegua_id, 1),
((SELECT id FROM personnel WHERE DNI = 'P400008'), 'Conservación de Humedales', @ib_id, 1);

-- =============================================
-- ACCOMMODATIONS
-- =============================================
INSERT INTO accommodations (capacity, category) VALUES
(4, 'Cabaña Estándar'),
(2, 'Habitación Doble'),
(6, 'Cabaña Familiar'),
(8, 'Cabaña Grande'),
(2, 'Habitación Matrimonial'),
(4, 'Suite'),
(10, 'Albergue'),
(3, 'Habitación Triple'),
(5, 'Cabaña Mediana'),
(12, 'Dormitorio Compartido'),
(2, 'Carpa Equipada'),
(4, 'Carpa Familiar'),
(6, 'Domo'),
(2, 'Refugio de Montaña'),
(8, 'Casa Rodante');

-- =============================================
-- EXCURSIONS
-- =============================================
INSERT INTO excursions (day_of_week, time, type) VALUES
('Monday', '09:00:00', 'foot'),
('Monday', '14:00:00', 'vehicle'),
('Tuesday', '08:30:00', 'foot'),
('Tuesday', '15:00:00', 'vehicle'),
('Wednesday', '09:30:00', 'foot'),
('Wednesday', '13:30:00', 'vehicle'),
('Thursday', '08:00:00', 'foot'),
('Thursday', '14:30:00', 'vehicle'),
('Friday', '09:00:00', 'foot'),
('Friday', '15:30:00', 'vehicle'),
('Saturday', '08:00:00', 'foot'),
('Saturday', '10:00:00', 'foot'),
('Saturday', '14:00:00', 'vehicle'),
('Saturday', '16:00:00', 'vehicle'),
('Sunday', '08:30:00', 'foot'),
('Sunday', '10:30:00', 'foot'),
('Sunday', '13:30:00', 'vehicle'),
('Sunday', '15:30:00', 'vehicle');

-- Get accommodation IDs - using SET to avoid output in console
SET @cabana_std_id = (SELECT id FROM accommodations WHERE category = 'Cabaña Estándar');
SET @hab_doble_id = (SELECT id FROM accommodations WHERE category = 'Habitación Doble');
SET @cabana_fam_id = (SELECT id FROM accommodations WHERE category = 'Cabaña Familiar');
SET @cabana_grande_id = (SELECT id FROM accommodations WHERE category = 'Cabaña Grande');
SET @hab_matrim_id = (SELECT id FROM accommodations WHERE category = 'Habitación Matrimonial');
SET @suite_id = (SELECT id FROM accommodations WHERE category = 'Suite');
SET @albergue_id = (SELECT id FROM accommodations WHERE category = 'Albergue');
SET @hab_triple_id = (SELECT id FROM accommodations WHERE category = 'Habitación Triple');
SET @cabana_med_id = (SELECT id FROM accommodations WHERE category = 'Cabaña Mediana');
SET @dorm_comp_id = (SELECT id FROM accommodations WHERE category = 'Dormitorio Compartido');

-- Get excursion IDs - using SET to avoid output in console
SET @exc_mon_am_id = (SELECT id FROM excursions WHERE day_of_week = 'Monday' AND time = '09:00:00');
SET @exc_mon_pm_id = (SELECT id FROM excursions WHERE day_of_week = 'Monday' AND time = '14:00:00');
SET @exc_tue_am_id = (SELECT id FROM excursions WHERE day_of_week = 'Tuesday' AND time = '08:30:00');
SET @exc_tue_pm_id = (SELECT id FROM excursions WHERE day_of_week = 'Tuesday' AND time = '15:00:00');
SET @exc_wed_am_id = (SELECT id FROM excursions WHERE day_of_week = 'Wednesday' AND time = '09:30:00');
SET @exc_wed_pm_id = (SELECT id FROM excursions WHERE day_of_week = 'Wednesday' AND time = '13:30:00');
SET @exc_sat_am1_id = (SELECT id FROM excursions WHERE day_of_week = 'Saturday' AND time = '08:00:00');
SET @exc_sat_am2_id = (SELECT id FROM excursions WHERE day_of_week = 'Saturday' AND time = '10:00:00');
SET @exc_sat_pm1_id = (SELECT id FROM excursions WHERE day_of_week = 'Saturday' AND time = '14:00:00');
SET @exc_sat_pm2_id = (SELECT id FROM excursions WHERE day_of_week = 'Saturday' AND time = '16:00:00');
SET @exc_sun_am1_id = (SELECT id FROM excursions WHERE day_of_week = 'Sunday' AND time = '08:30:00');
SET @exc_sun_am2_id = (SELECT id FROM excursions WHERE day_of_week = 'Sunday' AND time = '10:30:00');
SET @exc_sun_pm1_id = (SELECT id FROM excursions WHERE day_of_week = 'Sunday' AND time = '13:30:00');
SET @exc_sun_pm2_id = (SELECT id FROM excursions WHERE day_of_week = 'Sunday' AND time = '15:30:00');

-- =============================================
-- ACCOMMODATION EXCURSIONS
-- =============================================
INSERT INTO accommodation_excursions (accommodation_id, excursion_id) VALUES
-- Cabaña Estándar offers several excursions
(@cabana_std_id, @exc_mon_am_id),
(@cabana_std_id, @exc_wed_am_id),
(@cabana_std_id, @exc_sat_am1_id),
(@cabana_std_id, @exc_sun_am1_id),
-- Habitación Doble offers some excursions
(@hab_doble_id, @exc_tue_am_id),
(@hab_doble_id, @exc_sat_am2_id),
(@hab_doble_id, @exc_sun_am2_id),
-- Cabaña Familiar offers vehicle excursions
(@cabana_fam_id, @exc_mon_pm_id),
(@cabana_fam_id, @exc_wed_pm_id),
(@cabana_fam_id, @exc_sat_pm1_id),
(@cabana_fam_id, @exc_sun_pm1_id),
-- Cabaña Grande offers all weekend excursions
(@cabana_grande_id, @exc_sat_am1_id),
(@cabana_grande_id, @exc_sat_am2_id),
(@cabana_grande_id, @exc_sat_pm1_id),
(@cabana_grande_id, @exc_sat_pm2_id),
(@cabana_grande_id, @exc_sun_am1_id),
(@cabana_grande_id, @exc_sun_am2_id),
(@cabana_grande_id, @exc_sun_pm1_id),
(@cabana_grande_id, @exc_sun_pm2_id),
-- Suite offers premium excursions
(@suite_id, @exc_tue_pm_id),
(@suite_id, @exc_sat_am2_id),
(@suite_id, @exc_sun_am2_id),
-- Albergue offers group excursions
(@albergue_id, @exc_mon_am_id),
(@albergue_id, @exc_wed_am_id),
(@albergue_id, @exc_sat_am1_id),
(@albergue_id, @exc_sun_am1_id),
-- Some excursions are offered by multiple accommodations
(@hab_triple_id, @exc_sat_am1_id),
(@hab_triple_id, @exc_sun_am1_id),
(@cabana_med_id, @exc_sat_pm1_id),
(@cabana_med_id, @exc_sun_pm1_id),
(@dorm_comp_id, @exc_mon_am_id),
(@dorm_comp_id, @exc_sat_am1_id);

-- =============================================
-- VISITORS
-- =============================================
-- Based on data/visitantes_registrados_en_los_parques_nacionales.csv for ratio of residents/non-residents
INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES
-- Visitors to Nahuel Huapi
('V100001', 'Jorge Martínez', 'Av. Corrientes 1234, CABA', 'Ingeniero', @cabana_std_id, @nh_id),
('V100002', 'Marta Gómez', 'Calle Mitre 567, Rosario', 'Médica', @cabana_std_id, @nh_id),
('V100003', 'Luis Rodríguez', 'Av. San Martín 890, Mendoza', 'Abogado', @hab_doble_id, @nh_id),
('V100004', 'Ana Fernández', 'Calle Belgrano 123, Córdoba', 'Arquitecta', @hab_doble_id, @nh_id),
('V100005', 'Carlos Sánchez', 'Av. Rivadavia 456, CABA', 'Contador', @cabana_fam_id, @nh_id),
('V100006', 'Laura Pérez', 'Calle Sarmiento 789, La Plata', 'Profesora', @cabana_fam_id, @nh_id),
('V100007', 'Roberto López', 'Av. Belgrano 234, Tucumán', 'Comerciante', @cabana_fam_id, @nh_id),
('V100008', 'Silvia Torres', 'Calle San Martín 567, Salta', 'Enfermera', @cabana_fam_id, @nh_id),
('V100009', 'Miguel González', 'Av. 9 de Julio 890, CABA', 'Estudiante', @hab_triple_id, @nh_id),
('V100010', 'Patricia Díaz', 'Calle Urquiza 123, Paraná', 'Psicóloga', @hab_triple_id, @nh_id),
('V100011', 'Fernando Acosta', 'Av. Colón 456, Córdoba', 'Periodista', @hab_triple_id, @nh_id),
('V100012', 'Claudia Romero', 'Calle Lavalle 789, CABA', 'Diseñadora', @albergue_id, @nh_id),
('V100013', 'Gustavo Vargas', 'Av. Independencia 234, Mar del Plata', 'Profesor', @albergue_id, @nh_id),
('V100014', 'Marcela Castro', 'Calle Alvear 567, Rosario', 'Contadora', @albergue_id, @nh_id),
('V100015', 'Javier Molina', 'Av. Córdoba 890, CABA', 'Programador', @albergue_id, @nh_id),
-- International visitors to Nahuel Huapi
('E100001', 'John Smith', '123 Main St, New York, USA', 'Engineer', @suite_id, @nh_id),
('E100002', 'Emma Johnson', '45 Park Avenue, London, UK', 'Doctor', @suite_id, @nh_id),
('E100003', 'Hans Müller', 'Hauptstrasse 78, Berlin, Germany', 'Architect', @cabana_grande_id, @nh_id),
('E100004', 'Sophie Dubois', '34 Rue de Rivoli, Paris, France', 'Teacher', @cabana_grande_id, @nh_id),
('E100005', 'Marco Rossi', 'Via Roma 56, Rome, Italy', 'Chef', @cabana_grande_id, @nh_id),

-- Visitors to Iguazú
('V200001', 'Diego Martínez', 'Av. Santa Fe 1234, CABA', 'Médico', @cabana_std_id, @ig_id),
('V200002', 'Valeria Gómez', 'Calle Córdoba 567, Rosario', 'Abogada', @cabana_std_id, @ig_id),
('V200003', 'Martín Rodríguez', 'Av. Las Heras 890, Mendoza', 'Ingeniero', @hab_doble_id, @ig_id),
('V200004', 'Carolina Fernández', 'Calle San Jerónimo 123, Córdoba', 'Profesora', @hab_doble_id, @ig_id),
('V200005', 'Sebastián Sánchez', 'Av. Callao 456, CABA', 'Contador', @cabana_fam_id, @ig_id),
('V200006', 'Natalia Pérez', 'Calle 7 789, La Plata', 'Arquitecta', @cabana_fam_id, @ig_id),
('V200007', 'Alejandro López', 'Av. 24 de Septiembre 234, Tucumán', 'Comerciante', @cabana_fam_id, @ig_id),
('V200008', 'Gabriela Torres', 'Calle Caseros 567, Salta', 'Enfermera', @cabana_fam_id, @ig_id),
-- International visitors to Iguazú
('E200001', 'David Wilson', '78 Oxford St, London, UK', 'Photographer', @suite_id, @ig_id),
('E200002', 'Maria García', 'Calle Mayor 23, Madrid, Spain', 'Journalist', @suite_id, @ig_id),
('E200003', 'Hiroshi Tanaka', '5-2-1 Ginza, Tokyo, Japan', 'Engineer', @cabana_grande_id, @ig_id),
('E200004', 'Luisa Ferreira', 'Rua Augusta 45, São Paulo, Brazil', 'Lawyer', @cabana_grande_id, @ig_id),

-- Visitors to Los Glaciares
('V300001', 'Pablo Gutiérrez', 'Av. Cabildo 1234, CABA', 'Fotógrafo', @cabana_med_id, @lg_id),
('V300002', 'Lucía Morales', 'Calle Entre Ríos 567, Rosario', 'Bióloga', @cabana_med_id, @lg_id),
('V300003', 'Hernán Suárez', 'Av. Godoy Cruz 890, Mendoza', 'Geólogo', @dorm_comp_id, @lg_id),
('V300004', 'Daniela Ortiz', 'Calle Dean Funes 123, Córdoba', 'Estudiante', @dorm_comp_id, @lg_id),
('V300005', 'Mariano Paz', 'Av. Santa Fe 456, CABA', 'Guía de Montaña', @dorm_comp_id, @lg_id),
-- International visitors to Los Glaciares
('E300001', 'Thomas Brown', '45 Queen St, Sydney, Australia', 'Geologist', @hab_matrim_id, @lg_id),
('E300002', 'Anna Schmidt', 'Friedrichstrasse 10, Munich, Germany', 'Photographer', @hab_matrim_id, @lg_id),
('E300003', 'Pierre Dupont', '12 Avenue Victor Hugo, Paris, France', 'Writer', @hab_matrim_id, @lg_id),

-- Add more visitors to other parks
-- Aconcagua
('V400001', 'Ramiro Vega', 'Av. Pueyrredón 1234, CABA', 'Montañista', @cabana_med_id, @ac_id),
('V400002', 'Cecilia Rojas', 'Calle Pellegrini 567, Rosario', 'Fotógrafa', @cabana_med_id, @ac_id),
('V400003', 'Gonzalo Medina', 'Av. Colón 890, Córdoba', 'Ingeniero', @dorm_comp_id, @ac_id),
('E400001', 'Michael Johnson', '34 Mountain View, Denver, USA', 'Climber', @hab_matrim_id, @ac_id),

-- Iberá
('V500001', 'Florencia Núñez', 'Av. Corrientes 1234, CABA', 'Bióloga', @cabana_med_id, @ib_id),
('V500002', 'Matías Soto', 'Calle San Luis 567, Rosario', 'Fotógrafo', @cabana_med_id, @ib_id),
('V500003', 'Verónica Campos', 'Av. Vélez Sarsfield 890, Córdoba', 'Veterinaria', @dorm_comp_id, @ib_id),
('E500001', 'Robert Davis', '56 Riverside Dr, Chicago, USA', 'Wildlife Photographer', @hab_matrim_id, @ib_id);

-- =============================================
-- VISITOR EXCURSIONS
-- =============================================
-- Link visitors to excursions
INSERT INTO visitor_excursions (visitor_id, excursion_id) VALUES
-- Nahuel Huapi visitors on excursions
((SELECT id FROM visitors WHERE DNI = 'V100001'), @exc_mon_am_id),
((SELECT id FROM visitors WHERE DNI = 'V100001'), @exc_wed_am_id),
((SELECT id FROM visitors WHERE DNI = 'V100002'), @exc_mon_am_id),
((SELECT id FROM visitors WHERE DNI = 'V100003'), @exc_tue_am_id),
((SELECT id FROM visitors WHERE DNI = 'V100004'), @exc_tue_am_id),
((SELECT id FROM visitors WHERE DNI = 'V100005'), @exc_mon_pm_id),
((SELECT id FROM visitors WHERE DNI = 'V100006'), @exc_mon_pm_id),
((SELECT id FROM visitors WHERE DNI = 'V100007'), @exc_wed_pm_id),
((SELECT id FROM visitors WHERE DNI = 'V100008'), @exc_wed_pm_id),
((SELECT id FROM visitors WHERE DNI = 'V100009'), @exc_sat_am1_id),
((SELECT id FROM visitors WHERE DNI = 'V100010'), @exc_sat_am1_id),
((SELECT id FROM visitors WHERE DNI = 'V100011'), @exc_sun_am1_id),
((SELECT id FROM visitors WHERE DNI = 'V100012'), @exc_mon_am_id),
((SELECT id FROM visitors WHERE DNI = 'V100013'), @exc_sat_am1_id),
((SELECT id FROM visitors WHERE DNI = 'V100014'), @exc_sun_am1_id),
((SELECT id FROM visitors WHERE DNI = 'V100015'), @exc_mon_am_id),
((SELECT id FROM visitors WHERE DNI = 'E100001'), @exc_tue_pm_id),
((SELECT id FROM visitors WHERE DNI = 'E100002'), @exc_sat_am2_id),
((SELECT id FROM visitors WHERE DNI = 'E100003'), @exc_sat_am1_id),
((SELECT id FROM visitors WHERE DNI = 'E100004'), @exc_sun_am1_id),
((SELECT id FROM visitors WHERE DNI = 'E100005'), @exc_sat_pm1_id),

-- Iguazú visitors on excursions
((SELECT id FROM visitors WHERE DNI = 'V200001'), @exc_mon_am_id),
((SELECT id FROM visitors WHERE DNI = 'V200002'), @exc_wed_am_id),
((SELECT id FROM visitors WHERE DNI = 'V200003'), @exc_tue_am_id),
((SELECT id FROM visitors WHERE DNI = 'V200004'), @exc_tue_am_id),
((SELECT id FROM visitors WHERE DNI = 'V200005'), @exc_mon_pm_id),
((SELECT id FROM visitors WHERE DNI = 'V200006'), @exc_wed_pm_id),
((SELECT id FROM visitors WHERE DNI = 'V200007'), @exc_sat_pm1_id),
((SELECT id FROM visitors WHERE DNI = 'V200008'), @exc_sun_pm1_id),
((SELECT id FROM visitors WHERE DNI = 'E200001'), @exc_tue_pm_id),
((SELECT id FROM visitors WHERE DNI = 'E200002'), @exc_sat_am2_id),
((SELECT id FROM visitors WHERE DNI = 'E200003'), @exc_sat_am1_id),
((SELECT id FROM visitors WHERE DNI = 'E200004'), @exc_sun_am1_id),

-- Los Glaciares visitors on excursions
((SELECT id FROM visitors WHERE DNI = 'V300001'), @exc_sat_pm1_id),
((SELECT id FROM visitors WHERE DNI = 'V300002'), @exc_sun_pm1_id),
((SELECT id FROM visitors WHERE DNI = 'V300003'), @exc_mon_am_id),
((SELECT id FROM visitors WHERE DNI = 'V300004'), @exc_sat_am1_id),
((SELECT id FROM visitors WHERE DNI = 'V300005'), @exc_mon_am_id),
((SELECT id FROM visitors WHERE DNI = 'E300001'), @exc_tue_pm_id),
((SELECT id FROM visitors WHERE DNI = 'E300002'), @exc_sat_am2_id),
((SELECT id FROM visitors WHERE DNI = 'E300003'), @exc_sun_am2_id),

-- Aconcagua visitors on excursions
((SELECT id FROM visitors WHERE DNI = 'V400001'), @exc_sat_pm1_id),
((SELECT id FROM visitors WHERE DNI = 'V400002'), @exc_sun_pm1_id),
((SELECT id FROM visitors WHERE DNI = 'V400003'), @exc_mon_am_id),
((SELECT id FROM visitors WHERE DNI = 'E400001'), @exc_tue_pm_id),

-- Iberá visitors on excursions
((SELECT id FROM visitors WHERE DNI = 'V500001'), @exc_sat_pm1_id),
((SELECT id FROM visitors WHERE DNI = 'V500002'), @exc_sun_pm1_id),
((SELECT id FROM visitors WHERE DNI = 'V500003'), @exc_mon_am_id),
((SELECT id FROM visitors WHERE DNI = 'E500001'), @exc_tue_pm_id);

-- Clean up temporary function
DROP FUNCTION IF EXISTS random_individuals;

-- Verify data population
SELECT 'Comprehensive data population complete.' AS status;
SELECT COUNT(*) AS provinces_count FROM provinces;
SELECT COUNT(*) AS parks_count FROM parks;
SELECT COUNT(*) AS park_provinces_count FROM park_provinces;
SELECT COUNT(*) AS park_areas_count FROM park_areas;
SELECT COUNT(*) AS natural_elements_count FROM natural_elements;
SELECT COUNT(*) AS animal_elements_count FROM animal_elements;
SELECT COUNT(*) AS vegetal_elements_count FROM vegetal_elements;
SELECT COUNT(*) AS mineral_elements_count FROM mineral_elements;
SELECT COUNT(*) AS area_elements_count FROM area_elements;
SELECT COUNT(*) AS element_food_count FROM element_food;
SELECT COUNT(*) AS personnel_count FROM personnel;
SELECT COUNT(*) AS research_projects_count FROM research_projects;
SELECT COUNT(*) AS accommodations_count FROM accommodations;
SELECT COUNT(*) AS visitors_count FROM visitors;
SELECT COUNT(*) AS excursions_count FROM excursions;
SELECT COUNT(*) AS accommodation_excursions_count FROM accommodation_excursions;
SELECT COUNT(*) AS visitor_excursions_count FROM visitor_excursions;
