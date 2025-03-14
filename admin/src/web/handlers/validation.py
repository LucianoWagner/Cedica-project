from flask import current_app

from core.files import upload_files, create_file, process_edit_files
from core.people import find_member_by_id


def validate_schema_with_files(schema, data, object=None, is_edit=False):
    """
    Valida los datos del esquema y maneja la carga de archivos y la creación de enlaces.

    Args:
        schema (Schema): El esquema de validación.
        data (dict): Los datos a validar.
        object (Object, optional): El objeto a editar, si es una edición. Por defecto es None.
        is_edit (bool, optional): Indica si es una operación de edición. Por defecto es False.

    Returns:
        tuple: Una tupla que contiene los datos filtrados, los enlaces creados y los archivos subidos.
    """
    validated_data = schema.load({key: value for key, value in data.items()})
    client = current_app.storage.client
    if is_edit:
        for file in object.files:
            process_edit_files(file, validated_data, client)

    links = [create_file(link["link_url"], link['link_name'],
                         link['link_type'], True)
             for link in validated_data["links"]]

    files = []

    upload_files(client, validated_data['files'], files)
    filtered_data = {key: value for key, value in validated_data.items() if
                     key not in ["files", "links"]}
    return filtered_data, links, files
