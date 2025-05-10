def modificar_dict(d, campos_a_remover=None, campos_a_agregar=None):
    """
    Modifica un diccionario eliminando y agregando campos.
    Args:
        d (dict): El diccionario a modificar.
        campos_a_remover (list): Lista de claves a eliminar del diccionario.
        campos_a_agregar (dict): Diccionario con claves y valores a agregar.
    Returns:
        dict: El diccionario modificado.
    """
    # Remover campos
    for campo in campos_a_remover or []:
        d.pop(campo, None)

    # Agregar campos
    for k, v in (campos_a_agregar or {}).items():
        d[k] = v

    return d


def remover_dict(d, campos_a_remover=None):
    """
    Elimina campos de un diccionario.
    Args:
        d (dict): El diccionario a modificar.
        campos_a_remover (list): Lista de claves a eliminar del diccionario.
    Returns:
        dict: El diccionario modificado.
    """
    # Remover campos
    for campo in campos_a_remover or []:
        d.pop(campo, None)

    return d


def sumar_campo_valor(
    esquema: dict, campo_lista: str = "totalImpuesto", campo_suma: str = "valor"
) -> float:
    """
    Suma los valores de un campo numérico dentro de una lista de diccionarios en un esquema anidado.

    Args:
        esquema (dict): El diccionario que contiene la lista.
        campo_lista (str): El nombre de la clave que contiene la lista.
        campo_suma (str): El campo cuyo valor se quiere sumar.

    Returns:
        float: La suma de todos los valores del campo_suma en los elementos de la lista.
    """
    try:
        return sum(item.get(campo_suma, 0) for item in esquema.get(campo_lista, []))
    except (TypeError, AttributeError):
        return 0.0
