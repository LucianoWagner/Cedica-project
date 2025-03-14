from sqlalchemy.orm import joinedload
from datetime import datetime

from sqlalchemy import desc, asc, cast, String
from sqlalchemy.orm import aliased

from .member import Member
from .people import Person
from .jya_professional_association import jya_professional_association
from .jya import Jya
from ..database import db
from ..files import delete_file


def create_member(files=None, **kwargs):
    """
    Crea un nuevo miembro.

    Args:
        files (list, optional): Archivos asociados al miembro.
        **kwargs: Argumentos adicionales para el miembro.

    Returns:
        Member: El nuevo miembro creado.
    """
    if files is None:
        files = []
    new_member = Member(files=files, **kwargs)
    db.session.add(new_member)
    db.session.commit()
    return new_member


def create_jya(files=None, **kwargs):
    """
    Crea un nuevo JYA (Jinete y Amazona).

    Args:
        files (list, optional): Archivos asociados al JYA.
        **kwargs: Argumentos adicionales para el JYA.

    Returns:
        Jya: El nuevo JYA creado.
    """
    if files is None:
        files = []

    if "person" in kwargs:
        created_person = create_person(**kwargs["person"])
        kwargs.pop("person")

        new_jya = Jya(files=files, person=created_person, **kwargs)
    else:
        new_jya = Jya(files=files, **kwargs)
    db.session.add(new_jya)
    db.session.commit()
    return new_jya


def create_person(**kwargs):
    """
    Crea una nueva persona.

    Args:
        **kwargs: Argumentos adicionales para la persona.

    Returns:
        Person: La nueva persona creada.
    """
    new_person = Person(**kwargs)
    db.session.add(new_person)
    db.session.commit()
    return new_person


def find_member_by_id(member_id):
    """
    Encuentra un miembro por su ID.

    Args:
        member_id (int): El ID del miembro.

    Returns:
        Member: El miembro encontrado.
    """
    return Member.query.get(member_id)


def find_jya_by_id(jya_id):
    """
    Encuentra un JYA por su ID.

    Args:
        jya_id (int): El ID del JYA.

    Returns:
        Jya: El JYA encontrado.
    """
    return Jya.query.get(jya_id)


def get_members_without_user():
    """
    Obtiene todos los miembros que no tienen usuario asociado.

    Returns:
        list: Lista de miembros sin usuario.
    """
    return Member.query.filter(Member.user == None).all()


def get_all_members():
    """
    Obtiene todos los miembros.

    Returns:
        list: Lista de todos los miembros.
    """
    return Member.query.all()


def get_all_jyas():
    """
    Obtiene todos los JYAs.

    Returns:
        list: Lista de todos los JYAs.
    """
    return Jya.query.all()


def get_members_quantity():
    """
    Obtiene la cantidad total de miembros.

    Returns:
        int: Cantidad de miembros.
    """
    return Member.query.count()


def get_members(page=1, per_page=10, sort_by="created_at", order="desc", criteria=None, search=None, job_position=None):
    """
    Obtiene una lista paginada de miembros.

    Args:
        page (int): Número de página.
        per_page (int): Cantidad de elementos por página.
        sort_by (str): Campo por el cual ordenar.
        order (str): Orden de la lista (asc o desc).
        criteria (str, optional): Criterio de búsqueda.
        search (str, optional): Término de búsqueda.
        job_position (str, optional): Posición de trabajo.

    Returns:
        Pagination: Lista paginada de miembros.
    """
    PersonAlias = aliased(Person)

    # Define the columns for sorting using the aliased Person model
    sort_columns = {
        "nombre": PersonAlias.name,  # Referencing PersonAlias
        "apellido": PersonAlias.surname,
        "dni": PersonAlias.dni,
        "email": Member.email,
        "created_at": Member.createdAt
    }

    # Start the query and join with the aliased Person
    members_query = (
        Member.query
        # Eagerly load the Person relationship
        .options(joinedload(Member.person))
        .join(PersonAlias, Member.person_id == PersonAlias.id)
    )

    # Apply ordering
    if order == "asc":
        members_query = members_query.order_by(asc(sort_columns[sort_by]))
    else:
        members_query = members_query.order_by(desc(sort_columns[sort_by]))

    # Apply search filter if provided
    if search:
        if criteria:
            if criteria == "dni":
                members_query = members_query.filter(
                    cast(sort_columns[criteria], String).ilike(f"%{search}%"))
            else:
                members_query = members_query.filter(
                    sort_columns[criteria].ilike(f"%{search}%"))
        else:
            members_query = members_query.filter(
                db.or_(
                    PersonAlias.name.ilike(f"%{search}%"),
                    PersonAlias.surname.ilike(f"%{search}%"),
                    cast(PersonAlias.dni, String).ilike(f"%{search}%"),
                    Member.email.ilike(f"%{search}%"),
                )
            )

    # Apply job position filter if provided
    if job_position:
        formatted_job_positions = [pos.replace(
            "+", " ") for pos in job_position.split(",")]
        filters = [Member.job_position.ilike(
            f"%{pos}%") for pos in formatted_job_positions]
        members_query = members_query.filter(db.or_(*filters))

    # Paginate the results
    paginated_members = members_query.paginate(
        page=page, per_page=per_page, error_out=False)

    return paginated_members  # Return the paginated results


def get_all_job_positions():
    """
    Obtiene todas las posiciones de trabajo distintas.

    Returns:
        list: Lista de posiciones de trabajo.
    """
    return db.session.query(Member.job_position).distinct().all()


def get_member_by_id(member_id):
    """
    Obtiene un miembro por su ID.

    Args:
        member_id (int): El ID del miembro.

    Returns:
        Member: El miembro encontrado.
    """
    return Member.query.get(member_id)


def delete_member(member):
    """
    Elimina un miembro por su ID.

    Args:
        member_id (int): El ID del miembro.

    Returns:
        Member: El miembro eliminado.
    """
    for file in member.files:
        delete_file(file)

    db.session.delete(member)
    db.session.commit()
    return member


def get_jyas(page=1, per_page=10, sort_by="name", order="asc", criteria=None, search=None, professionals=None):
    """
    Obtiene una lista paginada de JYAs.

    Args:
        page (int): Número de página.
        per_page (int): Cantidad de elementos por página.
        sort_by (str): Campo por el cual ordenar.
        order (str): Orden de la lista (asc o desc).
        criteria (str, optional): Criterio de búsqueda.
        search (str, optional): Término de búsqueda.
        professionals (str, optional): Profesionales asociados.

    Returns:
        Pagination: Lista paginada de JYAs.
    """
    PersonAlias = aliased(Person)

    # Define the columns for sorting using the aliased Person model
    sort_columns = {
        "name": PersonAlias.name,
        "surname": PersonAlias.surname,
        "dni": PersonAlias.dni,
        "created_at": Jya.createdAt  # Assuming JyA model has a createdAt field
    }

    # Start the query and join with the aliased Person
    jyas_query = (
        Jya.query
        # Eagerly load the Person relationship
        .options(joinedload(Jya.person))
        # Eagerly load the professionals relationship
        .options(joinedload(Jya.professionals))
        .join(PersonAlias, Jya.person_id == PersonAlias.id)
    )

    # Apply ordering
    if order == "asc":
        jyas_query = jyas_query.order_by(asc(sort_columns[sort_by]))
    else:
        jyas_query = jyas_query.order_by(desc(sort_columns[sort_by]))

    # Apply filters for name, surname, dni if provided
    if search:
        if criteria:
            if criteria == "dni":
                jyas_query = jyas_query.filter(
                    cast(sort_columns[criteria], String).ilike(f"%{search}%"))
            elif criteria == "nombre":
                jyas_query = jyas_query.filter(
                    sort_columns["name"].ilike(f"%{search}%"))
            else:
                jyas_query = jyas_query.filter(
                    sort_columns["surname"].ilike(f"%{search}%"))
        else:
            jyas_query = jyas_query.filter(
                db.or_(
                    PersonAlias.name.ilike(f"%{search}%"),
                    PersonAlias.surname.ilike(f"%{search}%"),
                    cast(PersonAlias.dni, String).ilike(f"%{search}%"),
                )
            )

    # Apply professionals filter if provided
    if professionals:
        # Convert the professionals string to a list of integers
        professionals_list = professionals.split(",")
        jyas_query = jyas_query.filter(
            Jya.professionals.any(Member.id.in_(professionals_list)))

    # Paginate the results
    paginated_jyas = jyas_query.paginate(
        page=page, per_page=per_page, error_out=False)

    return paginated_jyas  # Return the paginated results


def get_jyas_quantity(criteria=None, search=None, professionals=None):
    """
    Obtiene la cantidad de JYAs.

    Args:
        criteria (str, optional): Criterio de búsqueda.
        search (str, optional): Término de búsqueda.
        professionals (str, optional): Profesionales asociados.

    Returns:
        int: Cantidad de JYAs.
    """
    PersonAlias = aliased(Person)

    jyas_query = (
        Jya.query
        .join(PersonAlias, Jya.person_id == PersonAlias.id)
    )

    if search:
        if criteria:
            if criteria == "dni":
                jyas_query = jyas_query.filter(
                    cast(PersonAlias.dni, String).ilike(f"%{search}%"))
            elif criteria == "nombre":
                jyas_query = jyas_query.filter(
                    PersonAlias.name.ilike(f"%{search}%"))
            else:
                jyas_query = jyas_query.filter(
                    PersonAlias.surname.ilike(f"%{search}%"))
        else:
            jyas_query = jyas_query.filter(
                db.or_(
                    PersonAlias.name.ilike(f"%{search}%"),
                    PersonAlias.surname.ilike(f"%{search}%"),
                    cast(PersonAlias.dni, String).ilike(f"%{search}%"),
                )
            )

    if professionals:
        professionals_list = professionals.split(",")
        jyas_query = jyas_query.filter(
            Jya.professionals.any(Member.id.in_(professionals_list)))

    return jyas_query.count()


def get_all_professionals():
    """
    Obtiene todos los profesionales que no son veterinarios.

    Returns:
        list: Lista de profesionales.
    """
    return db.session.query(Member).filter(Member.profession != 'Veterinario').all()
