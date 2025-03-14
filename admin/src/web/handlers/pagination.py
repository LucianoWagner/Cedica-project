def generate_pagination(current_page: int, total_pages: int) -> list:
    """
    Genera una lista de números de página para la paginación basada en la página actual y el total de páginas.

    Args:
        current_page (int): La página actual.
        total_pages (int): El número total de páginas.

    Returns:
        list: Una lista de números de página para mostrar en el control de paginación.
    """
    if total_pages <= 7:
        return list(range(1, total_pages + 1))

    if current_page <= 3:
        return [1, 2, 3, '...', total_pages - 1, total_pages]

    if current_page >= total_pages - 2:
        return [1, 2, '...', total_pages - 2, total_pages - 1, total_pages]

    return [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]


def get_total_pages(count, per_page):
    """
    Calcula el número total de páginas basado en el conteo total de elementos y el número de elementos por página.

    Args:
        count (int): El conteo total de elementos.
        per_page (int): El número de elementos por página.

    Returns:
        int: El número total de páginas.
    """
    return (count + per_page - 1) // per_page


def paginate(query_func, count_func, sort_by, order, page, per_page=10, **filters):
    """
    Maneja la lógica de paginación, incluyendo la obtención de elementos paginados y la generación de metadatos de paginación.

    Args:
        query_func (function): La función para obtener los elementos paginados.
        count_func (function): La función para obtener el conteo total de elementos.
        sort_by (str): El campo por el cual ordenar.
        order (str): El orden de la ordenación (ascendente o descendente).
        page (int): La página actual.
        per_page (int, optional): El número de elementos por página. Por defecto es 10.
        **filters: Filtros adicionales para la consulta.

    Returns:
        dict: Un diccionario con los elementos paginados, el conteo total, el número total de páginas y la paginación.
    """
    # Get total count without pagination
    total_count = count_func(**filters)

    # Get paginated items
    pagination_result = query_func(
        page=page, per_page=per_page, sort_by=sort_by, order=order, **filters)
    items = pagination_result.items
    total_pages = get_total_pages(total_count, per_page)
    pagination = generate_pagination(page, total_pages)

    return {
        'items': items,  # Paginated items
        'count': total_count,  # Total count without pagination
        'total_pages': total_pages,
        'pagination': pagination
    }
