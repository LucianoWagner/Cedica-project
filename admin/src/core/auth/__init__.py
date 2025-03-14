from sqlalchemy.orm import aliased, joinedload

from .permission import Permission
from .role import Role
from .user import User
from .role_permission import role_permissions_association
from ..bcrypt import bcrypt
from ..database import db
from sqlalchemy import asc, desc

from ..people import Person, Member


def find_user_by_email_and_password(email, password):
    """
    Encuentra un usuario por su correo electrónico y contraseña.

    Args:
        email (str): El correo electrónico del usuario.
        password (str): La contraseña del usuario.

    Returns:
        User: El usuario encontrado o None si no se encuentra.
    """
    found_user = User.query.filter_by(email=email).first()
    if found_user and bcrypt.check_password_hash(found_user.password, password):
        return found_user
    return None


def find_user_by_email(email):
    """
    Encuentra un usuario por su correo electrónico.

    Args:
        email (str): El correo electrónico del usuario.

    Returns:
        User: El usuario encontrado o None si no se encuentra.
    """
    return User.query.filter_by(email=email).first()


def find_user_by_id(id):
    """
    Encuentra un usuario por su ID.

    Args:
        id (int): El ID del usuario.

    Returns:
        User: El usuario encontrado o None si no se encuentra.
    """
    return User.query.filter_by(id=id).first()


def encode_password(password):
    """
    Codifica una contraseña.

    Args:
        password (str): La contraseña a codificar.

    Returns:
        str: La contraseña codificada.
    """
    hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    return hash.decode("utf-8")


def create_user(**kwargs):
    """
    Crea un nuevo usuario.

    Args:
        **kwargs: Los atributos del usuario.

    Returns:
        None
    """
    if kwargs.get("password") is not None:
        kwargs["password"] = encode_password(kwargs["password"])
    new_user = User(**kwargs)
    db.session.add(new_user)
    db.session.commit()


def create_role(**kwargs):
    """
    Crea un nuevo rol.

    Args:
        **kwargs: Los atributos del rol.

    Returns:
        Role: El rol creado.
    """
    new_role = Role(**kwargs)
    db.session.add(new_role)
    db.session.commit()
    return new_role


def get_all_roles():
    """
    Obtiene todos los roles.

    Returns:
        list: Una lista de todos los roles.
    """
    return Role.query.all()


def get_role_by_name(name):
    """
    Obtiene un rol por su nombre.

    Args:
        name (str): El nombre del rol.

    Returns:
        Role: El rol encontrado o None si no se encuentra.
    """
    return Role.query.filter_by(name=name).first()


def get_permission_by_name(name):
    """
    Obtiene un permiso por su nombre.

    Args:
        name (str): El nombre del permiso.

    Returns:
        Permission: El permiso encontrado o None si no se encuentra.
    """
    return Permission.query.filter_by(name=name).first()


def create_permission(**kwargs):
    """
    Crea un nuevo permiso.

    Args:
        **kwargs: Los atributos del permiso.

    Returns:
        None
    """
    new_permission = Permission(**kwargs)
    db.session.add(new_permission)
    db.session.commit()


def get_users(page=1, per_page=10, sort_by="created_at", order="desc", email=None, active=None, roles=None):
    """
    Obtiene una lista paginada de usuarios.

    Args:
        page (int): El número de página.
        per_page (int): El número de usuarios por página.
        sort_by (str): El campo por el cual ordenar.
        order (str): El orden de la ordenación ("asc" o "desc").
        email (str, optional): El correo electrónico para filtrar.
        active (str, optional): El estado activo para filtrar.
        roles (str, optional): Los roles para filtrar.

    Returns:
        Pagination: Un objeto de paginación con los usuarios.
    """
    sort_columns = {
        "email": User.email,
        "created_at": User.created_at
    }

    users = None
    if order == "asc":
        users = User.query.order_by(asc(sort_columns[sort_by]))
    else:
        users = User.query.order_by(desc(sort_columns[sort_by]))

    if email:
        users = users.filter(User.email.ilike(f"%{email}%"))

    if active is not None:
        if active == "true":
            print("entre true")
            users = users.filter(User.active == True)
        else:
            print("entre false")
            users = users.filter(User.active == False)

    if roles:
        # Roles has the ids, separated by comma, user has only one role
        roles = roles.split(",")
        users = users.filter(User.role_id.in_(roles))

    # devuelve un objeto de paginacion
    return users.paginate(page=page, per_page=per_page, error_out=False)


def get_users_quantity(email=None, active=None, roles=None):
    """
    Obtiene la cantidad de usuarios.

    Args:
        email (str, optional): El correo electrónico para filtrar.
        active (str, optional): El estado activo para filtrar.
        roles (str, optional): Los roles para filtrar.

    Returns:
        int: La cantidad de usuarios.
    """
    users = User.query

    if email:
        users = users.filter(User.email.ilike(f"%{email}%"))

    if active is not None:
        if active == "true":
            users = users.filter(User.active == True)
        else:
            users = users.filter(User.active == False)

    if roles:
        # Roles has the ids, separated by comma, user has only one role
        roles = roles.split(",")
        users = users.filter(User.role_id.in_(roles))

    return users.count()


def delete_user(user_id):
    """
    Elimina un usuario por su ID.

    Args:
        user_id (int): El ID del usuario a eliminar.

    Returns:
        bool: True si el usuario fue eliminado, False si no se encontró.
    """
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return True
    return False


def get_profile_data(user_id):
    """
    Obtiene los datos del perfil de un usuario.

    Args:
        user_id (int): El ID del usuario.

    Returns:
        dict: Un diccionario con los datos del perfil del usuario o None si no se encuentra.
    """
    # Aliasing the models for cleaner joins
    MemberAlias = aliased(Member)
    PersonAlias = aliased(Person)

    print(user_id)

    # Query to fetch the user with the associated member and person data
    user_query = (
        User.query
        .options(
            # Eagerly load both Member and Person relationships
            joinedload(User.member).joinedload(Member.person)
        )
        .join(MemberAlias, User.member_id == MemberAlias.id)
        # Join the Person model via member
        .join(PersonAlias, MemberAlias.person_id == PersonAlias.id)
        .filter(User.id == user_id)
    )

    user = user_query.first()

    if not user:
        return None

    # Debugging the fetched user and member
    print(
        f"User fetched: {user.email}, Member: {user.member.person.name} {user.member.person.surname}")

    # Construct the user data dictionary
    user_data = {
        "id": user.id,
        "email": user.email,
        "alias": user.alias,
        "role": user.role.name,  # Assuming there's a role relationship
        "active": user.active,
        "member": {
            "name": user.member.person.name,  # Accessing name from Person
            "surname": user.member.person.surname,  # Accessing surname from Person
        }
    }

    return user_data
