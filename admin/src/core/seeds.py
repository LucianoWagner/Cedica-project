from datetime import datetime, timedelta
import random

import click
from flask.cli import with_appcontext

from core.auth import create_user, create_role, create_permission, get_role_by_name, Role, get_permission_by_name
from core.database import db
from core.horses import create_horse
from core.people import create_member, create_person, create_jya
from core.finance import create_charge
from core.public import Message
from web.templates.payments import create_payment


def random_date():
    """
        Genera una fecha aleatoria dentro del último año.

        Returns:
            datetime: Una fecha aleatoria.
    """
    days_ago = random.randint(1, 365)
    return datetime.now() - timedelta(days_ago)


def seed_payments_for_member(member_id):
    """
        Genera pagos aleatorios para un miembro específico.

        Args:
            member_id (int): El ID del miembro.

        Returns:
            list: Una lista de pagos generados.
    """
    payments = []
    for _ in range(10):
        # Random amount between 10 and 100
        amount = round(random.uniform(10.0, 100.0), 2)
        date = random_date()  # Random date within the last year
        payment_type = random.choice(payment_types)
        description = random.choice(payment_descriptions)

        payment = create_payment(
            member_id=member_id,
            amount=amount,
            date=date,
            type=payment_type,
            description=description
        )
        payments.append(payment)
    return payments


# Payment types and descriptions to randomize
payment_types = ["Honorarios", "Proveedor", "Gastos Varios"]
payment_descriptions = ["Pago mensual",
                        "Donación", "Cuota de evento", "Suscripción"]


def seed_charges_for_member(jya_id, member_id):
    """
        Genera cargos aleatorios para un miembro específico.

        Args:
            jya_id (int): El ID del JYA.
            member_id (int): El ID del miembro.

        Returns:
            list: Una lista de cargos generados.
    """
    charges = []
    # Random amount between 10 and 100
    amount = round(random.uniform(10.0, 100.0), 2)
    date = random_date()  # Random date within the last year
    payment_method = random.choice(charge_methods)
    observations = random.choice(charge_observations)

    charge = create_charge(
        jya_id=jya_id,
        amount=amount,
        date=date,
        payment_method=payment_method,
        observations=observations,
        member_id=member_id
    )
    charges.append(charge)
    return charges


def random_date():
    """
    Generates a random date within the last year.

    Returns:
        datetime: A random date.
    """
    days_ago = random.randint(1, 365)
    return datetime.now() - timedelta(days_ago)


def seed_messages():
    """
    Generates random messages and saves them to the database.
    """
    full_names = ["John Doe", "Jane Smith",
                  "Alice Johnson", "Bob Brown", "Charlie Davis"]
    emails = ["john@example.com", "jane@example.com",
              "alice@example.com", "bob@example.com", "charlie@example.com"]
    bodies = ["Cuando", "Donde", "Por que", "Como", "Quien"]
    comments = ["Comentario 1", "Comentario 2",
                "Comentario 3", "Comentario 4", "Comentario 5"]

    messages = []
    for _ in range(10):
        message = Message(
            full_name=random.choice(full_names),
            email=random.choice(emails),
            body=random.choice(bodies),
            status=random.choice(['Pendiente', 'Contestada']),
            comment=random.choice(comments)
        )
        messages.append(message)
        db.session.add(message)
    db.session.commit()


charge_methods = ["Efectivo", "Tarjeta de Crédito",
                  "Transferencia Bancaria", "Cheque"]
charge_observations = ["Pago mensual",
                       "Donación", "Cuota de evento", "Suscripción"]
seed_person_data = [
    {
        "name": "Mateo",
        "surname": "Spinetti",
        "dni": 12345678,
        "address": "123 Main St, New York, NY",
        "telephone": "+1-234-567-8901",
        "emergency_contact": "+1-234-567-8902"
    },
    {
        "name": "jyane",
        "surname": "Smith",
        "dni": 23456789,
        "address": "456 Elm St, Los Angeles, CA",
        "telephone": "+1-234-567-8903",
        "emergency_contact": "+1-234-567-8904"
    },
    {
        "name": "Mike",
        "surname": "Johnson",
        "dni": 34567890,
        "address": "789 Oak St, Chicago, IL",
        "telephone": "+1-234-567-8905",
        "emergency_contact": "+1-234-567-8906"
    },
    {
        "name": "Lucy",
        "surname": "Brown",
        "dni": 45678901,
        "address": "101 Pine St, Houston, TX",
        "telephone": "+1-234-567-8907",
        "emergency_contact": "+1-234-567-8908"
    },
    {
        "name": "David",
        "surname": "Wilson",
        "dni": 56789012,
        "address": "202 Maple St, San Francisco, CA",
        "telephone": "+1-234-567-8909",
        "emergency_contact": "+1-234-567-8910"
    },
]
seed_members = [
    {
        "email": "mateospinetti1@gmail.com",
        "locality": "New York",
        "profession": "Software Engineer",
        "job_position": "Backend Developer",
        "start_date": datetime(2020, 1, 15),
        "end_date": None,  # Current job, no end date
        "medical_insurance": "HealthPlus",
        "insurance_number": "HP123456789",
        "job_condition": "Full-time",
        "active": True
    },
    {

        "email": "jyane.smith@example.com",
        "locality": "Los Angeles",
        "profession": "Data Scientist",
        "job_position": "Senior Data Analyst",
        "start_date": datetime(2019, 6, 10),
        "end_date": None,  # Current job, no end date
        "medical_insurance": "WellCare",
        "insurance_number": "WC987654321",
        "job_condition": "Full-time",
        "active": True
    },
    {

        "email": "mike.johnson@example.com",
        "locality": "Chicago",
        "profession": "Graphic Designer",
        "job_position": "Lead Designer",
        "start_date": datetime(2018, 4, 20),
        "end_date": datetime(2023, 8, 1),  # Job ended
        "medical_insurance": "CareHealth",
        "insurance_number": "CH112233445",
        "job_condition": "Part-time",
        "active": False
    },
    {

        "email": "lucy.brown@example.com",
        "locality": "Houston",
        "profession": "Project Manager",
        "job_position": "Senior Project Manager",
        "start_date": datetime(2021, 2, 5),
        "end_date": None,  # Current job, no end date
        "medical_insurance": "LifeSecure",
        "insurance_number": "LS556677889",
        "job_condition": "Full-time",
        "active": True
    },
    {
        "email": "david.wilson@example.com",
        "locality": "San Francisco",
        "profession": "Web Developer",
        "job_position": "Frontend Developer",
        "start_date": datetime(2022, 7, 15),
        "end_date": None,  # Current job, no end date
        "medical_insurance": "HealthGuard",
        "insurance_number": "HG998877665",
        "job_condition": "Full-time",
        "active": True
    },
]

seed_user_data = [
    {
        "email": "mateospinetti1@gmail.com",
        "alias": "johnny",
        "password": "123456",  # Make sure to hash your passwords in a real application

    },
    {
        "email": "lucianowagner@gmail.com",
        "alias": "jyane123",
        "password": "123456",

    },
    {
        "email": "mike.johnson@example.com",
        "alias": "mike2021",
        "password": "hashed_password_3",

    },
    {
        "email": "lucy.brown@example.com",
        "alias": "lucy_b",
        "password": "hashed_password_4",

    },
    {
        "email": "david.wilson@example.com",
        "alias": "david_w",
        "password": "hashed_password_5",

    },
]

seed_horse_data = [
    {
        "name": "Thunder",
        "birth_date": datetime(2015, 5, 20),
        "sex": "Masculino",
        "race": "Thoroughbred",
        "fur": "Bay",
        "origin": "Donacion",
        "entry_date": datetime(2020, 6, 15),
        "headquarter": "New York",
        "trainers": None,  # Will be set later
        "riders": None,  # Will be set later
        "jya_type": "Hipoterapia",
        "files": []
    },
    {
        "name": "Lightning",
        "birth_date": datetime(2017, 3, 14),
        "sex": "Femenino",
        "race": "Arabian",
        "fur": "Chestnut",
        "origin": "Compra",
        "entry_date": datetime(2021, 4, 10),
        "headquarter": "Los Angeles",
        "trainers": None,  # Will be set later
        "riders": None,  # Will be set later
        "jya_type": "Monta Terapéutica",
        "files": []
    },
    {
        "name": "Storm",
        "birth_date": datetime(2016, 8, 30),
        "sex": "Masculino",
        "race": "Quarter Horse",
        "fur": "Black",
        "origin": "Donacion",
        "entry_date": datetime(2019, 9, 5),
        "headquarter": "Chicago",
        "trainers": None,  # Will be set later
        "riders": None,  # Will be set later
        "jya_type": "Deporte Ecuestre",
        "files": []
    },
    {
        "name": "Blaze",
        "birth_date": datetime(2018, 1, 25),
        "sex": "Femenino",
        "race": "Morgan",
        "fur": "Palomino",
        "origin": "Compra",
        "entry_date": datetime(2022, 2, 20),
        "headquarter": "Houston",
        "trainers": None,  # Will be set later
        "riders": None,  # Will be set later
        "jya_type": "Actividades Recreativas",
        "files": []
    },
    {
        "name": "Shadow",
        "birth_date": datetime(2014, 11, 11),
        "sex": "Masculino",
        "race": "Appaloosa",
        "fur": "Gray",
        "origin": "Donacion",
        "entry_date": datetime(2018, 12, 1),
        "headquarter": "San Francisco",
        "trainers": None,  # Will be set later
        "riders": None,  # Will be set later
        "jya_type": "Equitación",
        "files": []
    }
]

seed_jya_data = [
    {
        "age": 25,
        "birth_date": datetime(1998, 5, 20),
        "birth_place": "Buenos Aires",
        "granted": True,
        "grant_percentage": 75.0,
        "behind_payment": False
    },
    {
        "age": 30,
        "birth_date": datetime(1993, 8, 15),
        "birth_place": "Córdoba",
        "granted": False,
        "grant_percentage": 0.0,
        "behind_payment": True
    },
    {
        "age": 45,
        "birth_date": datetime(2001, 4, 23),
        "birth_place": "Buenos Aires",
        "granted": False,
        "grant_percentage": 3.0,
        "behind_payment": True
    }
]


def seed_data():
    """
        Genera datos de ejemplo para la base de datos.
    """
    permissions = [
        'user_index', 'user_create', 'user_destroy', 'user_update', 'user_show', 'user_approve',
        'team_index', 'team_create', 'team_destroy', 'team_update', 'team_show',
        'payment_index', 'payment_create', 'payment_destroy', 'payment_update', 'payment_show',
        'jya_index', 'jya_create', 'jya_destroy', 'jya_update', 'jya_show',
        'horse_index', 'horse_create', 'horse_destroy', 'horse_update', 'horse_show',
        'charge_index', 'charge_create', 'charge_destroy', 'charge_update', 'charge_show',
        'publication_index', 'publication_create', 'publication_destroy', 'publication_update', 'publication_show',
        'report_index', 'report_create', 'report_destroy', 'report_update', 'report_show',
        'message_index', 'message_create', 'message_destroy', 'message_update', 'message_show'
    ]

    for perm_name in permissions:
        perm = create_permission(name=perm_name)

    # Crear roles y asignar permisos
    roles_permissions = {
        'system-admin': permissions,
        'tecnica': ['jya_index', 'jya_create', 'jya_update', 'jya_show', 'jya_destroy',
                    'charge_index', 'charge_show',
                    'horse_index', 'horse_show',
                    'report_index', 'report_show'],
        'ecuestre': ['jya_index', 'jya_show',
                     'horse_index', 'horse_show', 'horse_update', 'horse_create', 'horse_destroy'],
        'administracion': ['team_index', 'team_create', 'team_update', 'team_show', 'team_destroy',
                           'payment_index', 'payment_create', 'payment_show', 'payment_update', 'payment_destroy',
                           'jya_index', 'jya_create', 'jya_update', 'jya_show', 'jya_destroy',
                           'charge_index', 'charge_create', 'charge_destroy', 'charge_update', 'charge_show',
                           'horse_index', 'horse_show',
                           'user_approve',
                           'publication_index', 'publication_create', 'publication_update', 'publication_show',
                           'publication_destroy',
                           'report_index', 'report_show',
                           'message_index', 'message_create', 'message_update', 'message_show', 'message_destroy'],

        'editor': ['publication_index', 'publication_create', 'publication_update', 'publication_show'],
    }

    for role_name, role_permissions in roles_permissions.items():
        role = Role(name=role_name)
        for perm_name in role_permissions:
            perm = get_permission_by_name(name=perm_name)
            role.permissions.append(perm)
        db.session.add(role)

    db.session.commit()

    role_sysadmin = get_role_by_name(name="system-admin")
    role_ecuestre = get_role_by_name(name="ecuestre")
    person_mateo = create_person(**seed_person_data[0])
    member_mateo = create_member(person_id=person_mateo.id, **seed_members[0])
    user_mateo = create_user(member_id=member_mateo.id,
                             role_id=role_sysadmin.id, **seed_user_data[0], is_approved=True)

    seed_payments_for_member(member_mateo.id)
    person_jane = create_person(**seed_person_data[1])
    member_jane = create_member(person_id=person_jane.id, **seed_members[1])
    user_jane = create_user(member_id=member_jane.id,
                            role_id=role_ecuestre.id, **seed_user_data[1], is_approved=True)
    seed_payments_for_member(member_jane.id)
    person_mike = create_person(**seed_person_data[2])
    member_mike = create_member(person_id=person_mike.id, **seed_members[2])
    seed_payments_for_member(member_mike.id)
    print("Data seeded successfully")

    for horse_data in seed_horse_data:
        horse_data["trainers"] = [member_mateo, member_jane]
        horse_data["riders"] = [member_jane, member_mike]
        create_horse(**horse_data)

    person_lucy = create_person(**seed_person_data[3])
    lucy_jya = create_jya(person_id=person_lucy.id, **seed_jya_data[0])
    seed_charges_for_member(lucy_jya.id, member_mateo.id)

    person_david = create_person(**seed_person_data[4])
    david_jya = create_jya(person_id=person_david.id, **seed_jya_data[1])
    seed_charges_for_member(david_jya.id, member_mike.id)
    seed_messages()


@click.command(name="seed")
@with_appcontext
def run_seed():
    """
        Comando de Flask para ejecutar la función de generación de datos.
    """
    seed_data()
