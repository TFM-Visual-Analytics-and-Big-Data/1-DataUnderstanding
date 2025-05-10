from src.utils.file_operation import add_id_to_process_index, map_directory_to_dataframe
from src.utils.mongo_store import save_dict_to_mongo
from src.extraction.xml_parse import procesar_factura_desde_archivo
from src.transformation.factura_transformer import transformar_factura

import logging
from datetime import datetime
import subprocess
import sys


def main():
    """
    Punto de entrada principal del programa.
    """
    start_time = datetime.now()
    print("Ejecutando el pipeline...")
    print(f"Inicio del proceso: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. Levantar el directorio para extraer los archivos XML
    directory_contents = map_directory_to_dataframe("f:\\TFM-DATA")

    # log registro de los archivos que se van a procesar
    logging.basicConfig(
        filename="log/transactionProcess.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logTransacction = logging.getLogger("transactionProcess")

    # 2. Filtrar los archivos que no se encuentran procesados
    documento_to_process = directory_contents[directory_contents["process"] == False]

    total_documentos = len(documento_to_process)
    documento_estadistitica = {
        "contador_factura": 0,
        "contador_otros": 0,
        "contador_procesados": 0,
        "contador_no_procesados": 0,
    }
    percent_complete = 0
    # 3. Iteración para procesar los archivos
    for index, row in documento_to_process.iterrows():
        identifier = row["id"]
        logTransacction.info("=" * 50)
        logTransacction.info(f"{identifier} => Starting processing for file")
        logTransacction.info(f"{identifier} => Row data as JSON: {row.to_json()}")
        try:
            # 3.1 Procesamiento del archivo XML
            factura_data = procesar_factura_desde_archivo(row["path"])
            logTransacction.info(f"{identifier} => Successfully parsed XML file")

            # 3.2 Transformador del archivo XML a Json, tambien se extrae sólo datos relevantes
            transformed_data = transformar_factura(factura_data)
            logTransacction.info(
                f"{identifier} => Successfully transformed data to JSON"
            )

            # 3.3. Guardar el documneto en MongoDB
            status_mongo = save_dict_to_mongo(transformed_data)
            logTransacction.info(
                f"{identifier} => Saved data to MongoDB, status: {status_mongo}"
            )

            # 3.4. Actualizar estadisticas de procesamiento
            documento_estadistitica["contador_procesados"] += 1
            documento_estadistitica["contador_factura"] += 1
        except Exception as e:
            logTransacction.error(f"{identifier} => Error processing file : {e}")
            documento_estadistitica["contador_otros"] += 1
            documento_estadistitica["contador_no_procesados"] += 1
        finally:
            # 3.5. Actualizar el archivo de índice para marcar el archivo como procesado
            add_id_to_process_index(identifier)
            logTransacction.info(f"{identifier} => Update file for log process")
        logTransacction.info(f"{identifier} => End processing for file")
        # 3.6. Mostrar el progreso de procesamiento
        if index % 10 == 0:  # Print every 10 documents
            percent_complete = round((index + 1) / total_documentos * 100)
        print(
            f"{percent_complete}% - Procesando {index + 1} documentos de {total_documentos}...",
            end="\r",
        )

    # 4 Presentación de estadisticas de procesamiento
    print("=" * 50)
    print("Estadísticas de procesamiento:")
    print("=" * 50)
    print(
        f"Fin del proceso                            : {start_time.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(f"Total de documentos                        : {total_documentos}")
    print(
        f"Total de facturas                            : {documento_estadistitica['contador_factura']}"
    )
    print(
        f"Total de otros documentos                    : {documento_estadistitica['contador_otros']}"
    )
    print(
        f"Total de documentos procesados               : {documento_estadistitica['contador_procesados']}"
    )
    print(
        f"Total de documentos no procesadas            : {documento_estadistitica['contador_no_procesados']}"
    )


def check_and_install_requirements():
    """
    Check and install required packages from requirements.txt if not already installed.
    """
    try:
        with open("requirements.txt", "r") as req_file:
            requirements = req_file.readlines()
            for requirement in requirements:
                requirement = requirement.strip()
                if requirement:
                    try:
                        __import__(requirement.split("==")[0])
                    except ImportError:
                        print(f"Installing missing package: {requirement}")
                        subprocess.check_call(
                            [sys.executable, "-m", "pip", "install", requirement]
                        )
    except FileNotFoundError:
        print(
            "requirements.txt file not found. Please ensure it exists in the project directory."
        )
        sys.exit(1)


if __name__ == "__main__":
    # check_and_install_requirements()
    main()
