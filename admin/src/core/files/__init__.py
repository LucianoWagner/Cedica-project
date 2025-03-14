from datetime import datetime
import datetime as dt

from os import fstat

import ulid
from click import clear
from flask import current_app, request
from minio import S3Error
from minio.commonconfig import CopySource
from werkzeug.datastructures import FileStorage

from datetime import datetime
import datetime as dt
from os import fstat

import ulid
from click import clear
from flask import current_app, request
from minio import S3Error
from werkzeug.datastructures import FileStorage

from .files import File
from .horse_file import horse_file_association
from .jya_file import jya_file_association
from .member_file import member_file_association
from ..database import db


def create_file(url, title, type, isLink):
    file = File(url=url, title=title, type=type, isLink=isLink)
    return file


def extract_files_data():
    """Extract file data for each uploaded file, excluding file_upload from JSON."""
    return [
        {
            "file_name": request.form.getlist('file_name[]')[i],
            "file_type": request.form.getlist('file_type[]')[i],
            "file_id": generate_ulid(),
            "content_type": file.content_type,
            "content_length": file.content_length,
            # Do not include file_upload in the dictionary
        }
        for i, file in enumerate(request.files.getlist('file_upload[]'))
        if isinstance(file, FileStorage)  # Ensure file is valid
    ]


def extract_link_data():
    """Extract link data from the form."""
    return [
        {
            "link_name": request.form.getlist('link_name[]')[i],
            "link_type": request.form.getlist('link_type[]')[i],
            "link_url": request.form.getlist('link_url[]')[i]
        } for i in range(len(request.form.getlist('link_name[]')))
    ]


def upload_file(client, file_data, file_upload):
    """Upload a single file to storage."""
    file_name_with_ulid = f"{file_data['file_id']}_{file_data['file_name']}"

    client.put_object(
        current_app.config.get("STORAGE_BUCKET"),
        file_name_with_ulid,
        file_upload,  # Use the actual FileStorage object for upload
        fstat(file_upload.stream.fileno()).st_size,
        file_upload.content_type,
    )
    return create_file(file_name_with_ulid, file_data["file_name"], file_data['file_type'], False)


def update_file_key(client, bucket_name, old_key, new_key):
    """
    Update the key of a file in MinIO by copying it to a new key and deleting the old key.

    :param client: Minio client instance
    :param bucket_name: Name of the bucket
    :param old_key: The current key of the file
    :param new_key: The new key for the file
    """
    try:
        # Copy the file to the new key
        copy_result = client.copy_object(
            bucket_name,
            new_key,
            f"/{bucket_name}/{old_key}"
        )
        print(f"File copied to new key: {copy_result.object_name}")

        # Delete the old key
        client.remove_object(bucket_name, old_key)
        print(f"Old key deleted: {old_key}")

    except S3Error as err:
        print(f"Error occurred: {err}")


def upload_files(client, files_data, files_array):
    """Upload files directly to storage in a streaming fashion."""
    for file_data in files_data:
        # Retrieve the actual file upload based on the index
        file_upload = request.files.getlist('file_upload[]')[
            files_data.index(file_data)]
        uploaded_file = upload_file(client, file_data, file_upload)
        files_array.append(uploaded_file)


def generate_ulid():
    """Generate a unique ULID string."""
    return str(ulid.new())


def generate_presigned_url(object_name):
    client = current_app.storage.client
    return client.presigned_get_object(current_app.config.get("STORAGE_BUCKET"), object_name,
                                       expires=dt.timedelta(minutes=10))


def delete_file(file_to_delete, from_storage=True, from_db=True):
    if file_to_delete:
        # Delete the file itself
        if from_storage and not file_to_delete.isLink:
            current_app.storage.client.remove_object(
                current_app.config.get("STORAGE_BUCKET"), file_to_delete.url)
        if from_db:
            db.session.delete(file_to_delete)


def create_file(url, title, type, isLink):
    """
    Crea un archivo.

    Args:
        url (str): La URL del archivo.
        title (str): El título del archivo.
        type (str): El tipo de archivo.
        isLink (bool): Indica si es un enlace.

    Returns:
        File: El archivo creado.
    """
    file = File(url=url, title=title, type=type, isLink=isLink)
    return file


def extract_files_data():
    """
    Extrae los datos de los archivos subidos, excluyendo file_upload del JSON.

    Returns:
        list: Una lista de diccionarios con los datos de los archivos.
    """
    return [
        {
            "file_name": request.form.getlist('file_name[]')[i],
            "file_type": request.form.getlist('file_type[]')[i],
            "file_id": generate_ulid(),
            "content_type": file.content_type,
            "content_length": file.content_length,
        }
        for i, file in enumerate(request.files.getlist('file_upload[]'))
        if isinstance(file, FileStorage)
    ]


def extract_link_data():
    """
    Extrae los datos de los enlaces del formulario.

    Returns:
        list: Una lista de diccionarios con los datos de los enlaces.
    """
    return [
        {
            "link_name": request.form.getlist('link_name[]')[i],
            "link_type": request.form.getlist('link_type[]')[i],
            "link_url": request.form.getlist('link_url[]')[i]
        } for i in range(len(request.form.getlist('link_name[]')))
    ]


def upload_file(client, file_data, file_upload):
    """
    Sube un archivo a almacenamiento.

    Args:
        client (Minio): El cliente de Minio.
        file_data (dict): Los datos del archivo.
        file_upload (FileStorage): El archivo a subir.

    Returns:
        File: El archivo subido.
    """
    file_name_with_ulid = f"{file_data['file_id']}_{file_data['file_name']}"

    client.put_object(
        current_app.config.get("STORAGE_BUCKET"),
        file_name_with_ulid,
        file_upload,
        fstat(file_upload.stream.fileno()).st_size,
        file_upload.content_type,
    )
    return create_file(file_name_with_ulid, file_data["file_name"], file_data['file_type'], False)


def update_file_key(client, bucket_name, old_key, new_key):
    """
    Actualiza la clave de un archivo en MinIO copiándolo a una nueva clave y eliminando la clave antigua.

    Args:
        client (Minio): El cliente de Minio.
        bucket_name (str): El nombre del bucket.
        old_key (str): La clave actual del archivo.
        new_key (str): La nueva clave para el archivo.
    """
    try:
        source = CopySource(bucket_name, old_key)

        copy_result = client.copy_object(
            bucket_name,
            new_key,
            source
        )
        print(f"File copied to new key: {copy_result.object_name}")

        client.remove_object(bucket_name, old_key)
        print(f"Old key deleted: {old_key}")

    except S3Error as err:
        print(f"Error occurred: {err}")


def upload_files(client, files_data, files_array):
    """
    Sube archivos directamente a almacenamiento de manera continua.

    Args:
        client (Minio): El cliente de Minio.
        files_data (list): Los datos de los archivos.
        files_array (list): La lista donde se agregarán los archivos subidos.
    """
    for file_data in files_data:
        file_upload = request.files.getlist('file_upload[]')[
            files_data.index(file_data)]
        uploaded_file = upload_file(client, file_data, file_upload)
        files_array.append(uploaded_file)


def generate_ulid():
    """
    Genera una cadena ULID única.

    Returns:
        str: La cadena ULID generada.
    """
    return str(ulid.new())


def generate_presigned_url(object_name):
    """
    Genera una URL pre-firmada para un objeto.

    Args:
        object_name (str): El nombre del objeto.

    Returns:
        str: La URL pre-firmada.
    """
    client = current_app.storage.client
    return client.presigned_get_object(current_app.config.get("STORAGE_BUCKET"), object_name,
                                       expires=dt.timedelta(minutes=10))


def delete_file(file_to_delete, from_storage=True, from_db=True):
    """
    Elimina un archivo.

    Args:
        file_to_delete (File): El archivo a eliminar.
        from_storage (bool): Indica si se debe eliminar del almacenamiento.
        from_db (bool): Indica si se debe eliminar de la base de datos.
    """
    if file_to_delete:
        if from_storage and not file_to_delete.isLink:
            current_app.storage.client.remove_object(
                current_app.config.get("STORAGE_BUCKET"), file_to_delete.url)
        if from_db:
            db.session.delete(file_to_delete)


def process_edit_files(file, validated_data, client):
    """
    Procesa la edición de archivos.

    Args:
        file (File): El archivo a editar.
        validated_data (dict): Los datos validados.
        client (Minio): El cliente de Minio.
    """
    if file.url not in [link['link_url'] for link in validated_data["links"]]:
        delete_file(file, from_storage=True, from_db=True)
    else:
        old_title = file.title
        old_url = file.url
        new_title = [link['link_name']
                     for link in validated_data["links"] if link['link_url'] == file.url][0]

        if old_title != new_title and not file.isLink:
            new_url = f"{generate_ulid()}_{new_title}"
            update_file_key(client, current_app.config.get(
                "STORAGE_BUCKET"), file.url, new_url)
            file.url = new_url

        file.title = new_title
        file.type = [link['link_type']
                     for link in validated_data["links"] if link['link_url'] == old_url][0]

        validated_data["links"] = [
            link for link in validated_data["links"] if link['link_url'] != old_url]
        db.session.commit()


def get_filtered_files_data(object, title=None, type=None):
    """
    Obtiene los datos de los archivos filtrados.

    Args:
        object (object): El objeto que contiene los archivos.
        title (str, optional): El título para filtrar.
        type (str, optional): El tipo para filtrar.

    Returns:
        list: Una lista de datos de los archivos filtrados.
    """
    files = object.files.filter(
        File.title.startswith(title) if title else True,
        File.type.startswith(type) if type else True
    ).all()
    return [file.get_show_data() for file in files]
