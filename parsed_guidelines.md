I’m working on a final project (trabajo practico) for my last course in my masters. We need to get this project working with minimal effort

Requisitos previos a rendir el examen libre de Base de Datos

1. Se deberá entregar el TP correspondiente al primer cuatrimestre del 2019 con las siguientes
modificaciones/agregados
a. Previo a diseñar el modelo verificar si hay información pública que pueda ser utilizada
en el mismo (for example un listado de los parques nacionales) (Additional Requirements 1)
b. Efectuar una estimación del tamaño de las tablas que resulten del modelo (Additional Requirements 2)
c. Agregar a las consultas solicitadas en el trabajo práctico las siguientes
i. Las especies que se encuentran en todos los parques (Additional Requirements 3)
ii. Las especies que se encuentran en un único parque (Additional Requirements 4)
d. Proponer un conjunto de índices adecuados para resolver las consultas planteadas en
el punto c) y analizar el plan de ejecución correspondiente. (Additional Requirements 5)

2. Elegir un motor de base de datos and sobre el mismo crear un procedimiento que reciba como
parámetro el nombre de 2 bases de datos and compare las tablas, los índices and los constraints de
las mismas. (Additional Requirements 6)
3. Investigar el funcionamiento del control de concurrencia and del recovery en 2 motores
comerciales de base de datos. La comparación debe centrarse, fundamentalmente en los
aspectos técnicos de los mismos. (Additional Requirements 7)
Para los puntos 2 and 3 se deberá confeccionar un informe.
En el momento del examen final se tomará un coloquio sobre los puntos anteriores.

A continuacion, las consignas del tp de 2019

Introducción y Objetivos

El objetivo de esta primera parte es que, dado un problema de mediana comple-
jidad, los alumnos puedan implementar una solución utilizando las herramientas
de modelado and diseño vistas desde el punto de vista lógico and completar, dando un
cierre, el aspecto físico utilizando algún motor de base de datos. El motor en el
que se va a efectuar la entrega puede elegirse entre:
• MySQL / MariaDB (General Requirements 3)
• PostgreSQL (General Requirements 3)
• SQL Server (General Requirements 3)
En todos los casos los alumnos deberán asegurarse de contar con el software
necesario para poder mostrar el trabajo práctico en las fechas and lugar de entrega.

Consignas: Al momento de la corrección se tendrán en cuenta tanto la correcti-
tud de la solución como el uso de las herramientas disponibles en el motor elegido.

La entrega deberá constar, como mínimo, de la siguiente documentación:
• Carátula. Con tabla de contenidos, título del trabajo, fecha and nombre de los
autores. (General Requirements 5)
• Introducción and explicación del problema a resolver. (General Requirements 5)
• Modelo de Entidad Relación and Modelo Relacional derivado, utilizados para
implementar la solución. (General Requirements 5)
• Detalle de los supuestos asumidos para la resolución del problema. (General Requirements 5)
• Diseño físico correspondiente a la solución, implementado en el motor de base
de datos elegido por el grupo. (General Requirements 5)
• Código correspondiente a las consultas/stored procedures/ triggers que se
piden en el punto Funcionalidades a Implementar (General Requirements 5)
• Conclusiones (General Requirements 5)
La base que se utilice para efectuar la demostración deberá contener datos de
prueba cargados, de forma de poder evaluar el funcionamiento de las consultas in-
cluidas en los requerimientos. (General Requirements 4)
No es necesario entregar una interfaz para ejecutar
las consultas; las mismas podrán ser ejecutadas directamente desde la interfaz del
motor de base de datos elegido.
Recomendamos revisar el avance del trabajo con el tutor asignado antes de la
fecha de entrega.

1 Enunciado del Problema
Se desea crear un sistema que almacena información sobre los parques naturales
gestionados por las provincias (General Requirements 1)

Se sabe lo siguiente:
Una Provincia puede tener varios parques naturales.
En toda Provincia existe uno and sólo un organismo responsable de los parques. (Data Requirements 1)
Un parque puede estar compartido por más de una Provincia. (Data Requirements X)
Un parque natural se identifica por un nombre, (Data Requirements 2)
fue declarado en una fecha, (Data Requirements 2)
tiene un email de contacto, (Data Requirements 2)
se compone de varias áreas identificadas por un nombre (Data Requirements 3)
and caracterizadas por una determinada extensión. (Data Requirements 3)

Por motivos de eficiencia se desea favorecer las consultas referentes al número
de parques existentes en cada Provincia and la superficie total declarada parque nat-
ural en cada Provincia. (Data Requirements 14)

En cada área forzosamente residen elementos naturales que pueden ser de tres
tipos: vegetales, animales and minerales.
Cada elemento natural tiene una denominación científica, (Data Requirements 4)
una denominación vulgar (Data Requirements 4)
and un número inventariado de individuos por área. (Data Requirements 4)
De los elementos vegetales se desea saber si tienen floración and en qué
periodo se produce ésta; (Data Requirements 5)
de los animales se desea saber su tipo de alimentación (herbívora, carnívora u omnívora) (Data Requirements 6)
and sus periodos de celo; (Data Requirements 6)
de los minerales se desea saber si se trata de cristales o de rocas. (Data Requirements 7)
Además, interesa registrar qué elementos sirven de alimento a otros elementos, (Data Requirements 8)
teniendo en cuenta que ningún mineral se considera alimento and que un vegetal no
se alimenta de ningún otro elemento.
Del personal del parque se guarda el DNI, (Data Requirements 9)
número de CUIL, (Data Requirements 9)
nombre, (Data Requirements 9)
dirección, (Data Requirements 9)
teléfonos (domicilio, móvil) (Data Requirements 9)
and sueldo. (Data Requirements 9)
Se distinguen los siguientes tipos de personal: (Data Requirements 10)

Personal de gestión: registra los datos de los visitantes del parque and están des-
tinados en una entrada del parque (las entradas se identifican por un número).

Personal de vigilancia: vigila un área determinada del parque que recorre en
un vehículo (tipo and matrícula). Puede ocurrir que use el mismo vehículo para mas
de un área, pero siempre es el mismo en cada área que vigila.

Personal investigador: Tiene una titulación que ha de recogerse and pueden re-
alizar (incluso conjuntamente) proyectos de investigación sobre un determinado
elemento. Un proyecto de investigación tiene un presupuesto and un periodo de real-
ización.

Personal de conservación: mantiene and conserva un área determinada del par-
que. Cada uno lo realiza en una especialidad determinada (limpieza, caninos).

Un visitante (DNI, (Data Requirements 11)
nombre, (Data Requirements 11)
domicilio (Data Requirements 11)
and profesión) (Data Requirements 11)
debe alojarse dentro de los
alojamientos de que dispone el parque; (Data Requirements 12)
éstos tienen una capacidad limitada (Data Requirements 12)
and tienen una determinada categoría. (Data Requirements 12)

Los alojamientos organizan excursiones al parque, en vehículo o a pie, en deter-
minados días de la semana (Data Requirements 13)
and a una hora determinada. (Data Requirements 13)
A estas excursiones puede
acudir cualquier visitante del parque (independientemente del alojamiento en que
este). Un visitante tiene, obligatoriamente, que alojarse en el parque. Una excur-
sión puede ser organizada por más de un alojamiento.

2 Funcionalidades a Implementar
Lo siguiente es un listado mínimo de consultas que deben resolver sobre la base
implementada. Además debe cumplir con modelar correctamente el dominio del
problema
• ¿Cúal es la provincia con más parques naturales? (Functional Requirements 1)
• ¿Qué especies vegetales se encuentran en al menos la mitad de los parques? (Functional Requirements 2)
• ¿Cuántos visitantes estuvieron en los parques cuyos codigos son A and B? (Functional Requirements 3)
Diseñar un trigger para que cuando se disminuye la cantidad de alguna especie
registrada en un parque envíe automáticamente un email al email de contacto de
ese parque (Functional Requirements 4)
Se deberán implementar en la base de datos todas las restricciones que surgen
del problema utilizando las herramientas apropiadas. (Functional Requirements 5)

Las consultas deben devolver datos significativos, no solamente los identifi-
Cadores.
