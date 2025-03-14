from sqlalchemy import text

from .message import Message
from .publication import Publication


def get_publications_quantity():
    """
    Obtiene la cantidad total de publicaciones.

    Returns:
        int: La cantidad total de publicaciones.
    """
    return Publication.query.count()


def get_publications(page=1, per_page=10, sort_by="created_at", order="desc"):
    """
    Obtiene una lista paginada de publicaciones.

    Args:
        page (int): El número de página a recuperar.
        per_page (int): La cantidad de elementos por página.
        sort_by (str): El campo por el cual ordenar.
        order (str): El orden de clasificación.

    Returns:
        Pagination: Una lista paginada de publicaciones.
    """
    order_clause = text(f"{sort_by} {order}")
    return Publication.query.order_by(order_clause).paginate(page=page, per_page=per_page, error_out=False)


def get_messages_quantity():
    """
    Obtiene la cantidad total de mensajes.

    Returns:
        int: La cantidad total de mensajes.
    """
    return Message.query.count()


def get_messages(page=1, per_page=10, sort_by="created_at", order="desc", status=None):
    """
    Obtiene una lista paginada de mensajes.

    Args:
        page (int): El número de página a recuperar.
        per_page (int): La cantidad de elementos por página.
        sort_by (str): El campo por el cual ordenar.
        order (str): El orden de clasificación.
        status (str): El estado de los mensajes a recuperar.

    Returns:
        Pagination: Una lista paginada de mensajes.
    """
    query = Message.query
    if status:
        query = query.filter(Message.status == status)
    order_clause = text(f"{sort_by} {order}")
    return query.order_by(order_clause).paginate(page=page, per_page=per_page, error_out=False)
