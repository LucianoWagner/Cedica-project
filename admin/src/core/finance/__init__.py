from sqlalchemy import asc, desc

from .payments import Payment
from .charges import Charge
from ..database import db
from ..people import Member, jya_professional_association
from ..people import Person
from ..people import Jya


def create_charge(**kwargs):
    """
    Crea un nuevo cargo.

    Args:
        **kwargs: Argumentos del cargo.

    Returns:
        Charge: El nuevo cargo creado.
    """
    new_charge = charges.Charge(**kwargs)
    db.session.add(new_charge)
    db.session.commit()
    return new_charge


def create_jya_with_person(**kwargs):
    """
    Crea un nuevo JYA con una persona asociada.

    Args:
        **kwargs: Argumentos para crear la persona y el JYA.

    Returns:
        None
    """
    new_person = Person(
        name=kwargs["name"],
        surname=kwargs["surname"],
        dni=kwargs["dni"],
        address=kwargs["current_address"],
        telephone=kwargs["telephone"],
        emergency_contact=kwargs["emergency_contact"]
    )
    db.session.add(new_person)
    db.session.commit()

    scholarship_percentage = kwargs.get("scholarship_percentage", 0)
    granted = scholarship_percentage > 0

    new_jya = Jya(
        person_id=new_person.id,
        age=kwargs["age"],
        birth_date=kwargs["birthdate"],
        birth_place=kwargs.get("birth_place"),
        granted=granted,
        grant_percentage=scholarship_percentage,
        behind_payment=kwargs.get("behind_payment")
    )
    db.session.add(new_jya)
    db.session.commit()

    if "professionals" in kwargs and kwargs["professionals"]:
        for professional_id in kwargs["professionals"]:
            db.session.execute(
                jya_professional_association.insert().values(
                    jya_id=new_jya.id, member_id=professional_id)
            )
        db.session.commit()


def get_charges(page=1, per_page=10, sort_by="date", order="desc", payment_method=None, member_name=None,
                member_surname=None, start_date=None, end_date=None):
    """
    Obtiene una lista paginada de cargos.

    Args:
        page (int): Número de página.
        per_page (int): Cantidad de elementos por página.
        sort_by (str): Campo por el cual ordenar.
        order (str): Orden de la lista (asc o desc).
        payment_method (str, optional): Metodo de pago.
        member_name (str, optional): Nombre del miembro.
        member_surname (str, optional): Apellido del miembro.
        start_date (datetime, optional): Fecha de inicio.
        end_date (datetime, optional): Fecha de fin.

    Returns:
        Pagination: Lista paginada de cargos.
    """
    sort_columns = {
        "date": Charge.date
    }
    charges = None

    if order == "asc":
        charges = Charge.query.order_by(asc(sort_columns[sort_by]))
    else:
        charges = Charge.query.order_by(desc(sort_columns[sort_by]))

    if member_name or member_surname:
        member_query = Member.query.join(Person, Member.person_id == Person.id)
        if member_name:
            member_query = member_query.filter(
                Person.name.ilike(f"%{member_name}%"))
        if member_surname:
            member_query = member_query.filter(
                Person.surname.ilike(f"%{member_surname}%"))

        member_ids = [member.id for member in member_query.all()]
        charges = charges.filter(Charge.member_id.in_(member_ids))

    if payment_method:
        payment_methods = payment_method.split(',')
        payment_method_mapping = {
            "Tarjeta-Credito": "Tarjeta de Crédito",
            "Tarjeta-Debito": "Tarjeta de Débito",
        }
        payment_methods = [payment_method_mapping.get(
            method, method.replace("-", " ")) for method in payment_methods]
        charges = charges.filter(Charge.payment_method.in_(payment_methods))

    if start_date:
        charges = charges.filter(Charge.date >= start_date)

    if end_date:
        charges = charges.filter(Charge.date <= end_date)

    return charges.paginate(page=page, per_page=per_page, error_out=False)


def get_payments(page=1, per_page=10, sort_by="date", order="desc", type=None, start_date=None, end_date=None):
    """
    Obtiene una lista paginada de pagos.

    Args:
        page (int): Número de página.
        per_page (int): Cantidad de elementos por página.
        sort_by (str): Campo por el cual ordenar.
        order (str): Orden de la lista (asc o desc).
        type (str, optional): Tipo de pago.
        start_date (datetime, optional): Fecha de inicio.
        end_date (datetime, optional): Fecha de fin.

    Returns:
        Pagination: Lista paginada de pagos.
    """
    sort_columns = {
        "date": Payment.date
    }

    payments = None
    if order == "asc":
        payments = Payment.query.order_by(asc(sort_columns[sort_by]))
    else:
        payments = Payment.query.order_by(desc(sort_columns[sort_by]))

    if type:
        type_list = type.split(',')
        print(type_list)
        payments = payments.filter(Payment.type.in_(type_list))

    if start_date:
        payments = payments.filter(Payment.date >= start_date)

    if end_date:
        payments = payments.filter(Payment.date <= end_date)

    return payments.paginate(page=page, per_page=per_page, error_out=False)


def get_charges_quantity(payment_method, member_name=None, member_surname=None, start_date=None, end_date=None):
    """
    Obtiene la cantidad de cargos.

    Args:
        payment_method (str): Metodo de pago.
        member_name (str, optional): Nombre del miembro.
        member_surname (str, optional): Apellido del miembro.
        start_date (datetime, optional): Fecha de inicio.
        end_date (datetime, optional): Fecha de fin.

    Returns:
        int: Cantidad de cargos.
    """
    charges = Charge.query

    if member_name or member_surname:
        member_query = Member.query.join(Person, Member.person_id == Person.id)
        if member_name and member_surname:
            member_query = member_query.filter(Person.name.ilike(f"%{member_name}%"),
                                               Person.surname.ilike(f"%{member_surname}%"))
        elif member_name:
            member_query = member_query.filter(
                Person.name.ilike(f"%{member_name}%"))
        elif member_surname:
            member_query = member_query.filter(
                Person.surname.ilike(f"%{member_surname}%"))

        member_ids = [member.id for member in member_query.all()]
        if member_ids:
            charges = charges.filter(Charge.member_id.in_(member_ids))

    if payment_method:
        charges = charges.filter(Charge.payment_method == payment_method)

    if start_date:
        charges = charges.filter(Charge.date >= start_date)

    if end_date:
        charges = charges.filter(Charge.date <= end_date)

    return charges.count()


def get_payments_quantity(type=None, start_date=None, end_date=None):
    """
    Obtiene la cantidad de pagos.

    Args:
        type (str, optional): Tipo de pago.
        start_date (datetime, optional): Fecha de inicio.
        end_date (datetime, optional): Fecha de fin.

    Returns:
        int: Cantidad de pagos.
    """
    payments = Payment.query

    if type:
        payments = payments.filter(Payment.type == type)

    if start_date:
        payments = payments.filter(Payment.date >= start_date)

    if end_date:
        payments = payments.filter(Payment.date <= end_date)

    return payments.count()


def delete_charge(charge_id):
    """
    Elimina un cargo por su ID.

    Args:
        charge_id (int): El ID del cargo.

    Returns:
        bool: True si se eliminó, False en caso contrario.
    """
    charge_to_delete = Charge.query.get(charge_id)
    if charge_to_delete:
        db.session.delete(charge_to_delete)
        db.session.commit()
        return True
    return False


def delete_payment(payment_id):
    """
    Elimina un pago por su ID.

    Args:
        payment_id (int): El ID del pago.

    Returns:
        bool: True si se eliminó, False en caso contrario.
    """
    payment_to_delete = Payment.query.get(payment_id)
    if payment_to_delete:
        db.session.delete(payment_to_delete)
        db.session.commit()
        return True
    return False


def find_charge_by_id(charge_id):
    """
    Encuentra un cargo por su ID.

    Args:
        charge_id (int): El ID del cargo.

    Returns:
        Charge: El cargo encontrado.
    """
    return Charge.query.get(charge_id)


def find_payment_by_id(payment_id):
    """
    Encuentra un pago por su ID.

    Args:
        payment_id (int): El ID del pago.

    Returns:
        Payment: El pago encontrado.
    """
    return Payment.query.get(payment_id)
