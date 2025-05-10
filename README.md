<p align="center">
  <img src="https://raw.githubusercontent.com/TFM-Visual-Analytics-and-Big-Data/.about/master/src/img/unir.png" alt="UNIR - Universidad Internacional de La Rioja" width="250"/>
</p>
<h1 align="center">Máster Universitario en Análisis y Visualización de Datos Masivos/ Visual Analytics and Big Data</h1> 
<h1 align="center">Trabajo de Fin de Máster</h1>
<h2 align="center">Modelo Predictivo para Estimar Ventas y Estacionalidad a partir de Facturación Electrónica</h2>
<p align="center">
  <strong>Autor:</strong><br/>Edwin Rafael Larrea Buste<br/> 
  <strong>Director:</strong><br/>Hugo Alberto Xochicale Rojas
</p>


# Data Understanding -  (Pipeline ETL en Python para procesar los archivos XML)

## Tabla de Contenidos

- [Introducción](#introducción)
- [Objetivo](#objetivo)
- [Herramientas](#herramientas)
- [Dependencias](#dependencias)
- [Algoritmo](#algoritmo)
- [Arquitectura](#arquitectura)
- [Componentes Principales](#directorio-src)

## Introducción
El repositorio es un pipeline ETL en Python para procesar los archivos XML, es el primer paso para el desarrollo del trabajo fin de master (Modelo Predictivo para Estimar Ventas y Estacionalidad a partir de Facturación Electrónica).


## Objetivo

El objetivo principal de este proyecto python es desarrollar un pipeline ETL que permita procesar archivos XML de facturación electrónica, extrayendo información clave como fechas, montos, pagos y productos. Este pipeline está diseñado para transformar los datos en un formato estructurado (JSON) y almacenarlos en una base de datos MongoDB, facilitando su análisis posterior. Además, se busca garantizar la modularidad y escalabilidad del código, permitiendo su reutilización en otros proyectos similares.

## Herramientas

En este proyecto se han utilizado las siguientes herramientas y tecnologías:

- **Python**: Lenguaje principal para el desarrollo del pipeline ETL.
- **MongoDB**: Base de datos NoSQL utilizada para almacenar los datos estructurados.
- **Git**: Control de versiones para el seguimiento de cambios en el código.
- **Pandas**: Para la manipulación y análisis de datos estructurados.

## Dependencias

A continuación, se detallan las dependencias utilizadas en este proyecto y su propósito:

| Dependencia               | Versión   | Descripción                                                                 |
|---------------------------|-----------|-----------------------------------------------------------------------------|
| xml.etree.ElementTree / lxml / xmltodict | 2.5.0       | Para el análisis y procesamiento de archivos XML.                          |
| pymongo                   | 4.5.0       | Para la conexión y manipulación de la base de datos MongoDB.               |
| pandas                    | >=2.2.0       | Para la manipulación y análisis de datos estructurados.                    |
| python-dotenv             | 1.0.0        | Para la gestión de variables de entorno desde un archivo `.env`.           |
| logging                   | -       | Para la configuración y manejo de logs personalizados.                     |
| jsonschema                | -       | Para la validación de estructuras JSON.                                    |
| os / shutil               | -       | Para operaciones de sistema de archivos.                                   |
| argparse                  | -       | Para la gestión de argumentos en la línea de comandos.                     |

Estas dependencias están listadas en el archivo `requirements.txt` para facilitar su instalación.

## Algoritmo

A continuación, se describe el paso a paso del pipeline ETL implementado:

1. **Inicio del Pipeline**  
    - Se registra la hora de inicio del proceso.
    - Se imprime un mensaje indicando que el pipeline está en ejecución.

2. **Carga de Archivos XML**  
    - Se utiliza la función `map_directory_to_dataframe` para mapear el contenido del directorio en un DataFrame, donde cada fila representa un archivo XML.
    - Usando el archivo `process.index`, se verifica si el archivo xml ya fueron procesados anteriormente agregando una bandera de control en  el dataframe.

3. **Filtrado de Archivos No Procesados**  
    - Se filtran los archivos que aún no han sido procesados (`process == False`) para obtener una lista de documentos pendientes.

4. **Inicialización de Estadísticas**  
    - Se inicializan contadores para llevar estadísticas del procesamiento, como el número de facturas procesadas, otros documentos, y documentos no procesados.

5. **Iteración Sobre los Archivos**

    5.1 **Procesamiento del Archivo XML**
        - Se llama a la función `procesar_factura_desde_archivo` para extraer los datos del archivo XML.
        - se hace una validacion de la estructura de los archivos XML de facturación electrónica con archivos XSD (XML Schema Definition). Estos esquemas son proporcionados por el Servicio de Rentas Internas (SRI) y garantizan que los XML cumplan con los estándares requeridos. 
        - Se hace una limpieza del archivo, excluyendo etiquetas pertenecinente a firma electronica. 
    
    5.2 **Transformación de Datos**  
        - Se transforma el contenido del archivo XML en un formato JSON estructurado mediante la función `transformar_factura`.        
        - Se hace una limpieza del documento JSON, excluyendo datos de la empresa y cliente. 

    5.3 **Almacenamiento en MongoDB**  
        - Los datos transformados se guardan en una base de datos MongoDB utilizando la función `save_dict_to_mongo`.

    5.4 **Actualización de Estadísticas**  
        - Se actualizan los contadores de documentos procesados y categorizados.

    5.5 **Actualización del Índice de Procesamiento**  
        - Se marca el archivo xml como procesado en log índice (`process.index`) mediante la función `add_id_to_process_index`.

    5.6 **Progreso del Procesamiento**  
        - Cada 10 documentos procesados, se imprime el porcentaje de progreso.

6. **Presentación de Estadísticas Finales**  
    - Al finalizar el procesamiento, se imprimen las estadísticas del pipeline, incluyendo el total de documentos procesados, facturas, otros documentos, y documentos no procesados.

Este flujo asegura que los archivos XML sean procesados de manera eficiente, transformados en datos estructurados, y almacenados en una base de datos para su posterior análisis.

## Arquitectura

```markdown
1-DataUnderstanding/
│
├── src/
│   ├── extraction/             # Módulos de extracción
│   │   ├── xml_parser.py         
│   │
│   ├── transformation/         # Transformación de datos
│   │   ├── dict_transformer.py
│   │   └── factura_transformer.py
│   │
│   ├── utils/                 # Utilidades
│   │   ├── file_operation.py
│   │   ├── logger.py
│   │   ├── logger_decorator.py
│   │   └── mongo_store.py
│   └── xsd/                   # SCHEMA de los xml 
│       └── factura/
│           ├── facturaV1.0.0.xsd 
│           ├── facturaV1.1.0.xsd
│           ├── facturaV2.0.0.xsd
│           └── facturaV2.1.0.xsd
│
├── requirements.txt         # Dependencias
├── README.md                # Documentación
├── main.py                  # Punto de entrada principal
├── .env.template            # Configuración del entorno
└── .gitignore

```

Explicación de los componentes principales:

### **Directorio `src/`**
Este directorio contiene el código fuente organizado en submódulos según su funcionalidad:

#### a. **`extraction/` (Módulos de extracción)**
- **`xml_parser.py`**: Implementa la lógica para leer y parsear archivos XML. Usa librerías como `xml.etree.ElementTree`, `lxml` o `xmltodict` para convertir los datos XML en estructuras manejables como diccionarios u objetos Python.

#### b. **`transformation/` (Transformación de datos)**
- **`dict_transformer.py`**: Realiza transformaciones en datos representados como diccionarios. Puede limpiar, normalizar o mapear datos a un formato intermedio.
- **`factura_transformer.py`**: Específicamente diseñado para transformar datos relacionados con facturas. Incluye lógica para interpretar campos específicos o convertir datos a un formato estándar.

#### c. **`utils/` (Utilidades)**
- **`file_operation.py`**: Contiene funciones auxiliares para operaciones con archivos, como lectura, escritura o manejo de rutas.
- **`logger.py`**: Implementa un sistema de registro (logging) para rastrear eventos, errores o información relevante durante la ejecución del pipeline.
- **`logger_decorator.py`**: Proporciona decoradores para añadir automáticamente capacidades de logging a funciones o métodos.
- **`mongo_store.py`**: Maneja la interacción con una base de datos MongoDB, como guardar o recuperar datos.

#### d. **`xsd/` (Schemas de validación XML)**
- Contiene archivos `.xsd` (XML Schema Definition) que definen las reglas y estructura esperada de los archivos XML. Los subdirectorios como `factura/` agrupan esquemas específicos para diferentes versiones de facturas:
  - **`facturaV1.0.0.xsd`**, **`facturaV1.1.0.xsd`**, etc.: Esquemas para validar facturas en distintas versiones.

### **Archivos raíz**
- **`requirements.txt`**: Lista las dependencias del proyecto (librerías y versiones necesarias) que se instalan con `pip install -r requirements.txt`.
- **`README.md`**: Documentación del proyecto, incluyendo instrucciones de uso, descripción de los módulos y cualquier información relevante.
- **`main.py`**: Punto de entrada principal del pipeline. Coordina la ejecución de los diferentes módulos.
- **`.env.template`**: Plantilla para configurar variables de entorno, como credenciales o configuraciones específicas.
- **`.gitignore`**: Define qué archivos o directorios deben ser ignorados por Git (por ejemplo, archivos temporales, credenciales, etc.).
