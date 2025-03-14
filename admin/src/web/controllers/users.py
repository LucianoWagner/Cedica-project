from flask import render_template, session, abort, request, flash, redirect, url_for, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError
from pyexpat.errors import messages

from core.auth import get_users, get_users_quantity, delete_user, get_all_roles, find_user_by_email, create_user, \
    find_user_by_id, encode_password, get_profile_data
from core.bcrypt import bcrypt
from core.database import db
from core.people import get_members_without_user
from web.handlers.auth import is_authenticated, login_required, permission_required
from web.handlers.pagination import generate_pagination, get_total_pages, paginate
from web.schemas.users import UserAddSchema, UserEditSchema, UserApprovalSchema

users_blueprint = Blueprint("users", __name__, url_prefix="/users")


@users_blueprint.route("/<int:user_id>")
class UserResource(MethodView):

    @permission_required('user_destroy')
    def delete(self, user_id):
        """
        Maneja la solicitud DELETE para eliminar un usuario específico.

        Args:
            user_id (int): ID del usuario a eliminar.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        print(user_id)
        if delete_user(user_id):
            return '', 204
        else:
            abort(404, description="User not found")

    @permission_required('user_update')
    def put(self, user_id):
        """
        Maneja la solicitud PUT para actualizar un usuario específico.

        Args:
            user_id (int): ID del usuario a actualizar.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        form_data = request.form.to_dict()
        schema = UserEditSchema()
        try:
            validated_data = schema.load(form_data)
            user = find_user_by_id(user_id)
            if user is None:
                return jsonify({"error": "No existe un usuario con el id indicado"}), 400

            existing_user_email = find_user_by_email(validated_data["email"])
            if (existing_user_email is not None and existing_user_email.id != user_id):
                return jsonify(
                    {"error": "El mail ingresado ya pertenece a otro usuario registrado en el sistema "}), 400

            user.email = validated_data["email"]
            user.alias = validated_data["alias"]
            user.role_id = validated_data["role_id"]
            user.active = validated_data.get("active")

            if validated_data['change_password']:
                user.password = encode_password(validated_data["password"])

            db.session.commit()

            return jsonify({"message": "Usuario actualizado con exito"}), 200

        except ValidationError as err:
            print(err)
            return jsonify(err.messages), 400


@users_blueprint.route("/")
class UsersResource(MethodView):
    @permission_required('user_index')
    def get(self):
        """
        Maneja la solicitud GET para obtener una lista de usuarios.

        Returns:
            Response: Devuelve una lista de usuarios en formato JSON.
        """
        page = request.args.get("page", 1, type=int)
        sort_by = request.args.get("sort_by", "created_at")
        order = request.args.get("order", "desc")
        email = request.args.get("email")
        active = request.args.get("active")
        filter_roles = request.args.get("roles")

        per_page = 10

        users_data = paginate(lambda **kwargs: get_users(**kwargs), lambda **kwargs: get_users_quantity(**kwargs),
                              sort_by, order, page, per_page, email=email,
                              active=active, roles=filter_roles)

        columns = [
            {"name": "email", "label": "Email", "sortable": True},
            {"name": "active", "label": "Activo", "sortable": False},
            {"name": "role", "label": "Rol", "sortable": False},
            {"name": "created_at", "label": "Fecha de Creacion", "sortable": True}]

        roles = get_all_roles()
        members_without_users = get_members_without_user()

        return render_template(
            "users/users.html",
            data=users_data['items'],
            count=users_data['count'],
            sort_by=sort_by,
            order=order,
            per_page=per_page,
            page=page,
            total_pages=users_data['total_pages'],
            pagination=users_data['pagination'],
            columns=columns,
            roles=roles,
            members_without_users=members_without_users
        )

    @permission_required("user_create")
    def post(self):
        """
        Maneja la solicitud POST para crear un nuevo usuario.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        form_data = request.form.to_dict()
        schema = UserAddSchema()

        try:
            validated_data = schema.load(form_data)
            user = find_user_by_email(validated_data["email"])
            if user:
                return jsonify({"error": "El email ya esta en uso"}), 400

            create_user(**validated_data, is_approved=True)

            return jsonify({"message": "Usuario creado exitosamente"}), 201

        except ValidationError as err:
            return jsonify(err.messages), 400

        except Exception as e:
            print(e)
            return jsonify({"error": "Error al crear el usuario"}), 500


@users_blueprint.route("/profile")
class UserResource(MethodView):
    def get(self):
        """
        Maneja la solicitud GET para obtener el perfil del usuario autenticado.

        Returns:
            Response: Devuelve los datos del perfil del usuario en formato JSON.
        """
        user_id = session.get("user")
        print(user_id)
        user_data = get_profile_data(user_id)
        if not user_data:
            return jsonify({"error": "No se pudo obtener su información"}), 404
        return user_data, 200

    def post(self):
        """
        Maneja la solicitud POST para actualizar el perfil del usuario autenticado.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        # Get user ID from session
        user_id = session.get("user")
        if not user_id:
            return jsonify({"message": "Usuario no autenticado"}), 401

        # Find the user by ID
        found_user = find_user_by_id(user_id)
        if not found_user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Get the request data (alias, original password, new password)
        data = request.get_json()
        alias = data.get("alias")
        original_password = data.get("original_password")
        new_password = data.get("new_password")

        # Update alias if provided
        if alias:
            found_user.alias = alias

        # Check if the user is trying to change the password
        if original_password:
            # Verify that the original password is correct
            if not bcrypt.check_password_hash(found_user.password, original_password):
                return jsonify({"message": "La contraseña actual es incorrecta"}), 400

            # Validate new password
            if new_password:
                # Hash the new password and update the user
                found_user.password = encode_password(new_password)

        # Save changes to the database
        try:
            db.session.commit()
            return jsonify({"message": "Perfil actualizado exitosamente"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error al actualizar el perfil"}), 500


@users_blueprint.route("/<int:user_id>/approve")
class ApproveUserResource(MethodView):
    @permission_required("user_approve")
    def post(self, user_id):
        """
        Maneja la solicitud POST para aprobar un usuario.

        Args:
            user_id (int): ID del usuario a aprobar.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        form_data = request.form.to_dict()
        schema = UserApprovalSchema()

        try:
            validated_data = schema.load(form_data)
            user = find_user_by_id(user_id)
            if not user:
                return jsonify({"error": "Usuario no encontrado"}), 404

            user.is_approved = True
            user.role_id = validated_data["role_id"]
            user.member_id = validated_data["member_id"]

            db.session.commit()

            return jsonify({"message": "Usuario aprobado exitosamente"}), 200
        except ValidationError as err:
            return jsonify(err.messages), 400
        except Exception as e:
            print(e)
            return jsonify({"error": "Error al aprobar el usuario"}), 500
