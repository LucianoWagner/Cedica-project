from sqlalchemy import asc, desc

from .horse import Horse
from .horse_rider import horse_rider_association
from .horse_trainer import horse_trainer_association
from ..database import db
from ..files import delete_file


def get_horses(page=1, per_page=10, sort_by='entry_date', order='desc', name=None, types=None):
    """
    Obtiene una lista paginada de caballos.

    Args:
        page (int): Número de página.
        per_page (int): Cantidad de elementos por página.
        sort_by (str): Campo por el cual ordenar.
        order (str): Orden de la lista (asc o desc).
        name (str, optional): Nombre del caballo.
        types (str, optional): Tipos de caballos.

    Returns:
        Pagination: Lista paginada de caballos.
    """
    sort_columns = {
        'entry_date': Horse.entry_date,
        'name': Horse.name,
        'birth_date': Horse.birth_date,
    }
    horses = None
    if order == "asc":
        horses = Horse.query.order_by(asc(sort_columns[sort_by]))
    else:
        horses = Horse.query.order_by(desc(sort_columns[sort_by]))

    if name:
        horses = horses.filter(Horse.name.ilike(f"%{name}%"))

    if types:
        types = types.split(",")

        horses = horses.filter(Horse.jya_type.in_(types))

    return horses.paginate(page=page, per_page=per_page, error_out=False)


def get_horses_quantity(name=None, types=None):
    """
    Obtiene la cantidad de caballos.

    Args:
        name (str, optional): Nombre del caballo.
        types (str, optional): Tipos de caballos.

    Returns:
        int: Cantidad de caballos.
    """
    horses = Horse.query
    if name:
        horses = horses.filter(Horse.name.ilike(f"%{name}%"))

    if types:
        types = types.split(",")
        horses = horses.filter(Horse.jya_type.in_(types))
    return horses.count()


def create_horse(files, trainers, riders, **kwargs):
    """
    Crea un nuevo caballo.

    Args:
        files (list): Archivos asociados al caballo.
        trainers (list): Entrenadores asociados al caballo.
        riders (list): Jinetes asociados al caballo.
        **kwargs: Argumentos adicionales para el caballo.

    Returns:
        Horse: El nuevo caballo creado.
    """
    horse = Horse(files=files, trainers=trainers, riders=riders, **kwargs)
    db.session.add(horse)
    db.session.commit()
    return horse


def delete_horse(horse_id):
    """
    Elimina un caballo por su ID.

    Args:
        horse_id (int): El ID del caballo.

    Returns:
        bool: True si se eliminó, False en caso contrario.
    """
    horse_to_delete = Horse.query.get(horse_id)
    if horse_to_delete:
        # Eliminar archivos asociados
        for file in horse_to_delete.files:
            delete_file(file)

        # Eliminar el caballo
        db.session.delete(horse_to_delete)
        db.session.commit()
        return True
    return False


def find_horse_by_id(horse_id):
    """
    Encuentra un caballo por su ID.

    Args:
        horse_id (int): El ID del caballo.

    Returns:
        Horse: El caballo encontrado.
    """
    return Horse.query.get(horse_id)
