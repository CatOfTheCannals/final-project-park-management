I’m working on a final project (trabajo practico) for my last course in my masters. We need to get this project working with minimal effort


Requisitos previos a rendir el examen libre de Base de Datos


1. Se deberá entregar el TP correspondiente al primer cuatrimestre del 2019 con las siguientes
modificaciones/agregados
a. Previo a diseñar el modelo verificar si hay información pública que pueda ser utilizada
en el mismo (por ejemplo un listado de los parques nacionales)
b. Efectuar una estimación del tamaño de las tablas que resulten del modelo
c. Agregar a las consultas solicitadas en el trabajo práctico las siguientes
i. Las especies que se encuentran en todos los parques
ii. Las especies que se encuentran en un único parque
d. Proponer un conjunto de índices adecuados para resolver las consultas planteadas en
el punto c) y analizar el plan de ejecución correspondiente.


2. Elegir un motor de base de datos y sobre el mismo crear un procedimiento que reciba como
parámetro el nombre de 2 bases de datos y compare las tablas, los índices y los constraints de
las mismas.
3. Investigar el funcionamiento del control de concurrencia y del recovery en 2 motores
comerciales de base de datos. La comparación debe centrarse, fundamentalmente en los
aspectos técnicos de los mismos.
Para los puntos 2 y 3 se deberá confeccionar un informe.
En el momento del examen final se tomará un coloquio sobre los puntos anteriores.


A continuacion, las consignas del tp de 2019


Introducción y Objetivos


El objetivo de esta primera parte es que, dado un problema de mediana comple-
jidad, los alumnos puedan implementar una solución utilizando las herramientas


de modelado y diseño vistas desde el punto de vista lógico y completar, dando un
cierre, el aspecto físico utilizando algún motor de base de datos. El motor en el
que se va a efectuar la entrega puede elegirse entre:
• MySQL / MariaDB
• PostgreSQL
• SQL Server
En todos los casos los alumnos deberán asegurarse de contar con el software
necesario para poder mostrar el trabajo práctico en las fechas y lugar de entrega.


Consignas: Al momento de la corrección se tendrán en cuenta tanto la correcti-
tud de la solución como el uso de las herramientas disponibles en el motor elegido.


La entrega deberá constar, como mínimo, de la siguiente documentación:
• Carátula. Con tabla de contenidos, título del trabajo, fecha y nombre de los
autores.
• Introducción y explicación del problema a resolver.
• Modelo de Entidad Relación y Modelo Relacional derivado, utilizados para
implementar la solución.
• Detalle de los supuestos asumidos para la resolución del problema.
• Diseño físico correspondiente a la solución, implementado en el motor de base
de datos elegido por el grupo.
• Código correspondiente a las consultas/stored procedures/ triggers que se
piden en el punto Funcionalidades a Implementar
• Conclusiones
La base que se utilice para efectuar la demostración deberá contener datos de


prueba cargados, de forma de poder evaluar el funcionamiento de las consultas in-
cluidas en los requerimientos. No es necesario entregar una interfaz para ejecutar


las consultas; las mismas podrán ser ejecutadas directamente desde la interfaz del
motor de base de datos elegido.
Recomendamos revisar el avance del trabajo con el tutor asignado antes de la
fecha de entrega.




1 Enunciado del Problema
Se desea crear un sistema que almacena información sobre los parques naturales
gestionados por las provincias
Se sabe lo siguiente: Una Provincia puede tener varios parques naturales. En
toda Provincia existe uno y sólo un organismo responsable de los parques. Un
parque puede estar compartido por más de una Provincia.
Un parque natural se identifica por un nombre, fue declarado en una fecha,
tiene un email de contacto, se compone de varias áreas identificadas por un nombre
y caracterizadas por una determinada extensión.
Por motivos de eficiencia se desea favorecer las consultas referentes al número


de parques existentes en cada Provincia y la superficie total declarada parque nat-
ural en cada Provincia.


En cada área forzosamente residen elementos naturales que pueden ser de tres


tipos: vegetales, animales y minerales. Cada elemento natural tiene una denomi-
nación científica, una denominación vulgar y un número inventariado de individuos


por área. De los elementos vegetales se desea saber si tienen floración y en qué
periodo se produce ésta; de los animales se desea saber su tipo de alimentación
(herbívora, carnívora u omnívora) y sus periodos de celo; de los minerales se desea
saber si se trata de cristales o de rocas.
Además, interesa registrar qué elementos sirven de alimento a otros elementos,
teniendo en cuenta que ningún mineral se considera alimento y que un vegetal no
se alimenta de ningún otro elemento.
Del personal del parque se guarda el DNI, número de CUIL, nombre, dirección,
teléfonos (domicilio, móvil) y sueldo. Se distinguen los siguientes tipos de personal:


Personal de gestión: registra los datos de los visitantes del parque y están des-
tinados en una entrada del parque (las entradas se identifican por un número).


Personal de vigilancia: vigila un área determinada del parque que recorre en
un vehículo (tipo y matrícula). Puede ocurrir que use el mismo vehículo para mas
de un área, pero siempre es el mismo en cada área que vigila.


Personal investigador: Tiene una titulación que ha de recogerse y pueden re-
alizar (incluso conjuntamente) proyectos de investigación sobre un determinado


elemento. Un proyecto de investigación tiene un presupuesto y un periodo de real-
ización.


Personal de conservación: mantiene y conserva un área determinada del par-
que. Cada uno lo realiza en una especialidad determinada (limpieza, caninos).


Un visitante (DNI, nombre, domicilio y profesión) debe alojarse dentro de los
alojamientos de que dispone el parque; éstos tienen una capacidad limitada y
tienen una determinada categoría.


Los alojamientos organizan excursiones al parque, en vehículo o a pie, en deter-
minados días de la semana y a una hora determinada. A estas excursiones puede


acudir cualquier visitante del parque (independientemente del alojamiento en que


este). Un visitante tiene, obligatoriamente, que alojarse en el parque. Una excur-
sión puede ser organizada por más de un alojamiento.





2 Funcionalidades a Implementar
Lo siguiente es un listado mínimo de consultas que deben resolver sobre la base
implementada. Además debe cumplir con modelar correctamente el dominio del
problema
• ¿Cúal es la provincia con más parques naturales?
• ¿Qué especies vegetales se encuentran en al menos la mitad de los parques?
• ¿Cuántos visitantes estuvieron en los parques cuyos codigos son A y B?
Diseñar un trigger para que cuando se disminuye la cantidad de alguna especie
registrada en un parque envíe automáticamente un email al email de contacto de
ese parque
Se deberán implementar en la base de datos todas las restricciones que surgen
del problema utilizando las herramientas apropiadas.


Las consultas deben devolver datos significativos, no solamente los identifi-
Cadores.


So, those are the tasks. Now before anything, let’s craft a plan. For reference, in the data directory you have some official files that can serve as a template for creating our mock data sources. The teacher told me that we for the purposes of the assignment, we should invent data that is not contained in the source files


