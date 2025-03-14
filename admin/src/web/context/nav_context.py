from flask import session


def inject_nav_links():
    """
        Inyecta los enlaces de navegación basados en los permisos del usuario almacenados en la sesión.

        Recupera los permisos del usuario desde la sesión y genera una lista de enlaces de navegación
        para los módulos asociados a esos permisos. Se asegura de crear enlaces únicos para cada módulo
        y pluraliza los nombres de los módulos según sea necesario.

        Returns:
            dict: Un diccionario con la clave 'nav_links' que contiene una lista de enlaces de navegación,
            donde cada enlace tiene un 'name' (nombre del módulo) y un 'href' (enlace a la vista correspondiente).
    """
    # Recuperar permisos desde la sesión
    permissions = session.get("permissions", [])

    # Crear un conjunto para almacenar los módulos únicos
    unique_modules = set()

    # Extraer módulos de los permisos
    for perm in permissions:
        parts = perm.name.split("_")
        if len(parts) >= 2:  # Asegúrate de que haya al menos un módulo y una acción
            module_name = parts[0]  # Obtiene el nombre del módulo
            unique_modules.add(module_name)  # Agrega el módulo al conjunto

    # Crear el array de nav_links
    nav_links = []

    # Generar enlaces para cada módulo
    for module in unique_modules:
        if module == "team":
            module_name = "member"
        else:
            module_name = module

        # Pluralize the name of the module using the mapping
        # Pluralize the name of the module
        plural_module_name = f"{module_name.capitalize()}s"
        # Mapping dictionary for module name conversion
        module_name_mapping = {
            "charge": "Cobros",
            "horse": "Ecuestre",
            "user": "Usuarios",
            "jya": "J&As",
            "member": "Miembros",
            "payment": "Pagos",
            "publication": "Publicaciones",
            "message": "Mensajes",
            "report": "Reportes"
        }

        real_module_name = module_name_mapping.get(
            module_name, module_name.capitalize() + "s")
        # Generate href as pluralized.module.CapitalizedNameResource
        href = f"{module_name}s.{plural_module_name}Resource"

        nav_link = {
            "name": real_module_name,  # Pluralized name for the nav_link
            "href": href  # Set the href in the correct format
        }
        nav_links.append(nav_link)

    return dict(nav_links=nav_links)
