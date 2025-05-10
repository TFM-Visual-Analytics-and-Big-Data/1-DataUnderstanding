import xml.etree.ElementTree as ET
import xmlschema
import json
import re
import os

from decimal import Decimal
from pathlib import Path


def leer_contenido_xml(path_xml: str) -> str:
    """Lee el contenido de un archivo XML."""
    with open(path_xml, "r", encoding="utf-8") as f:
        return f.read()


def clean_keys(data):
    """Limpia las claves de un diccionario o lista, eliminando '@' y '$'."""
    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            # Quitar '@' si está al inicio
            if k.startswith("@"):
                k = k[1:]
            # Cambiar '$' por 'value'
            if k == "$":
                k = "value"
            new_data[k] = clean_keys(v)
        return new_data
    elif isinstance(data, list):
        return [clean_keys(item) for item in data]
    elif isinstance(data, Decimal):
        return float(data)
    else:
        return data


def extraer_comprobante_xml(contenido_xml: str) -> str:
    """Extrae y decodifica el XML contenido en el tag <comprobante>."""
    match = re.search(
        r"<comprobante>(<!\[CDATA\[)?(.*?)(\]\]>)?</comprobante>",
        contenido_xml,
        re.DOTALL,
    )
    if not match:
        raise ValueError("No se encontró el contenido del tag <comprobante>")

    comprobante = match.group(2).replace("&lt;", "<").replace("&gt;", ">").strip()
    return comprobante


def obtener_version_factura(comprobante_xml: str) -> str:
    """Parses el XML del comprobante y obtiene la versión del tag <factura>."""
    root = ET.fromstring(comprobante_xml)
    # ds:Signature
    root.remove(root.find("{http://www.w3.org/2000/09/xmldsig#}Signature"))
    if root.tag != "factura":
        raise ValueError("El contenido no contiene un tag <factura> como raíz")

    version = root.attrib.get("version")
    if not version:
        raise ValueError("No se encontró el atributo 'version' en el tag <factura>")

    return version, root


def validar_y_convertir_a_json(
    root: ET.Element, version: str, base_xsd_path: str = "xsd"
) -> str:
    """Valida el XML contra el XSD y lo convierte a JSON."""

    xsd_path = Path(os.path.join(base_xsd_path, f"facturaV{version}.xsd"))

    if not xsd_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo XSD para la versión {version}: {xsd_path}"
        )

    schema = xmlschema.XMLSchema(xsd_path)

    if not schema.is_valid(root):
        raise ValueError("El XML no es válido contra el XSD")

    data_dict = schema.to_dict(root) 
    # value = json.dumps(cleaned_data, indent=2, ensure_ascii=False)
    # return json.dumps(data_dict, indent=2, ensure_ascii=False)
    return clean_keys(data_dict)


def procesar_factura_desde_archivo(path_xml: str) -> str:
    """Función principal para procesar un archivo XML y devolver su contenido en JSON."""

    root_path = os.getcwd()
    base_xsd_path = os.path.join(root_path, "src/XSD/factura/")

    contenido_xml = leer_contenido_xml(path_xml)
    comprobante_xml = extraer_comprobante_xml(contenido_xml)
    version, root = obtener_version_factura(comprobante_xml)
    return validar_y_convertir_a_json(root, version, base_xsd_path)
