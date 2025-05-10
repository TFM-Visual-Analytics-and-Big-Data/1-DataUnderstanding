

from .dict_transformer import modificar_dict, remover_dict, sumar_campo_valor


def transformar_factura(doc):
    """
    Transforma un documento de factura XML a un formato JSON simplificado.

    Args:
        doc (dict): Documento de factura en formato JSON.

    Returns:
        dict: Documento de factura transformado.
    """
    doc = procesar_info_tributaria(doc)
    doc = procesar_info_factura(doc)
    doc = procesar_detalles(doc)
    doc = procesar_info_adicional(doc)
    return doc

def extraer_forma_pago_y_total(pagos_dict):
    """
    Extrae una lista de diccionarios con solo 'formaPago' y 'total' desde un esquema de pagos.

    Args:
        pagos_dict (dict): Diccionario con la clave 'pago' que contiene una lista de pagos.

    Returns:
        list[dict]: Lista de diccionarios con 'formaPago' y 'total'.
    """
    pagos = pagos_dict.get('pago', [])
    return [{'formaPago': p.get('formaPago'), 'total': p.get('total')} for p in pagos]

def transformar_detalles(detalles_dict):
    """
    Transforma una estructura de 'detalles' extrayendo campos clave y sumando los impuestos.

    Args:
        detalles_dict (dict): Diccionario con clave 'detalle' que contiene una lista de productos.

    Returns:
        list[dict]: Lista de productos con campos simplificados.
    """
    resultado = []
    for item in detalles_dict.get('detalle', []):
        total_impuesto = sumar_campo_valor(item["impuestos"], 'impuesto', 'valor')
        resultado.append({
            'codigoPrincipal': item.get('codigoPrincipal'),
            'codigoAuxiliar': item.get('codigoAuxiliar'),
            'descripcion': item.get('descripcion'),
            'unidadMedida': item.get('unidadMedida'),
            'cantidad': item.get('cantidad'),
            'precioUnitario': item.get('precioUnitario'),
            'precioTotalSinImpuesto': item.get('precioTotalSinImpuesto'),
            'totalImpuesto': total_impuesto
        })
    return resultado

def procesar_info_tributaria(doc):
    """
    Procesa la información tributaria del documento de factura.
    """
    tmp = doc['infoTributaria']
    infoTributaria = {
        '_id': tmp['claveAcceso'],
        'ambiente': tmp['ambiente'],
        'codigoDocumento': tmp['codDoc'],
        'establecimiento': tmp['estab'],
        'puntoEmisor': tmp['ptoEmi'],
        'secuencial': tmp['secuencial']
    }
    return modificar_dict(
        doc,
        campos_a_remover=["infoTributaria"],
        campos_a_agregar=infoTributaria
    )

def procesar_info_factura(doc):
    """
    Procesa la información de la factura del documento.
    """
    tmp = doc['infoFactura']
    infoFactura = {
        'fechaEmision': tmp['fechaEmision'],
        'direccionEstablecimiento': tmp['dirEstablecimiento'],
        'direccionComprador': tmp['direccionComprador'],
        'totalSinImpuestos': tmp['totalSinImpuestos'],
        'totalDescuento': tmp['totalDescuento'],
        'propina': tmp['propina'],
        'importeTotal': tmp['importeTotal'],
        'moneda': tmp['moneda'],
        'totalConImpuestos': sumar_campo_valor( tmp['totalConImpuestos']),
        'pagos': extraer_forma_pago_y_total(tmp['pagos']),
    }
    return modificar_dict(
        doc,
        campos_a_remover=["infoFactura"],
        campos_a_agregar=infoFactura
    )

def procesar_detalles(doc):
    """
    Procesa los detalles de la factura del documento.
    """
    tmp = doc['detalles']
    detalles = transformar_detalles(tmp)
    return modificar_dict(
        doc,
        campos_a_remover=["detalles", "id", "version"],
        campos_a_agregar={"detalles": detalles}
    )

def procesar_info_adicional(doc): 
    """
    Procesa la información adicional del documento de factura.
    """
    return remover_dict(
        doc,
        campos_a_remover=["infoAdicional"] 
    )