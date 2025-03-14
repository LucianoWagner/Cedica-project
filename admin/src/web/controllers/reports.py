from datetime import datetime, timedelta

from flask import render_template, jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint

from core.database import db
from core.finance import Payment, Charge
from core.people import Jya, Member
from core.public import Message
from web.handlers.auth import login_required, permission_required

from dateutil.relativedelta import relativedelta

reports_blueprint = Blueprint("reports", __name__, url_prefix="/reports")


@reports_blueprint.route("/")
class ReportsResource(MethodView):
    @login_required
    @permission_required('report_index')
    def get(self):
        """
        Maneja la solicitud GET para obtener una lista de publicaciones.

        Returns:
            Response: Renderiza la plantilla con la lista de publicaciones y la paginación.
        """
        return render_template("reports/reports.html")


@login_required
@permission_required('report_show')
@reports_blueprint.route('/behind-payments', methods=['GET'])
def get_behind_payment_jyas():
    """
    Fetches all J&As behind on payments.

    Returns:
        JSON response with J&As who are behind on payments.
    """
    try:
        jyas = Jya.query.filter_by(behind_payment=True).all()

        if not jyas:
            return jsonify({"message": "No hay J&As con deudas."}), 200

        result = [jya.to_dict() for jya in jyas]

        return jsonify(result), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Se produjo un error al buscar los datos requeridos"}), 500


@reports_blueprint.route('/payments-distribution', methods=['GET'])
@login_required
@permission_required('report_show')
def payments_distribution():
    try:
        # Get the start_date and end_date from the request arguments
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        # Ensure that both start_date and end_date are provided
        if not start_date_str or not end_date_str:
            return jsonify({"error": "Both start_date and end_date are required."}), 400

        # Convert the start_date and end_date strings from dd/mm/yyyy format to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        except ValueError:
            return jsonify({"error": "Formato de fechas invalido, por favor utilizar dd/mm/aaaa."}), 400

        print(start_date, end_date)

        # Filter the payments based on the date range
        payments = db.session.query(
            Payment.type,
            db.func.sum(Payment.amount).label('total')
        ).filter(
            Payment.date >= start_date,
            Payment.date <= end_date
        ).group_by(Payment.type).all()

        # If no data found
        if not payments:
            return jsonify({"message": "No hay información disponible en este rango de fechas"}), 200

        # Return the result
        result = [{"type": payment.type, "total": float(
            payment.total)} for payment in payments]
        return jsonify(result), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while fetching the data."}), 500


@reports_blueprint.route('/job-and-profession-reports', methods=['GET'])
@login_required
@permission_required('report_show')
def job_and_profession_reports():
    try:
        # Query active members and group by job position and profession
        job_positions = db.session.query(Member.job_position, db.func.count(Member.id).label('count')) \
            .filter(Member.active == True) \
            .group_by(Member.job_position).all()

        professions = db.session.query(Member.profession, db.func.count(Member.id).label('count')) \
            .filter(Member.active == True) \
            .group_by(Member.profession).all()

        # If no data is found, return a message
        if not job_positions and not professions:
            return jsonify({"message": "No active members found."}), 200

        # Format the results
        job_position_data = [
            {"job_position": jp.job_position, "count": jp.count} for jp in job_positions]
        profession_data = [{"profession": prof.profession,
                            "count": prof.count} for prof in professions]

        return jsonify({"job_positions": job_position_data, "professions": profession_data}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while fetching the data."}), 500


@reports_blueprint.route('/monthly-income', methods=['GET'])
@login_required
@permission_required('report_show')
def monthly_income():
    try:
        start_month = int(request.args.get('start_month'))
        start_year = int(request.args.get('start_year'))
        end_month = int(request.args.get('end_month'))
        end_year = int(request.args.get('end_year'))

        # Validate the inputs
        if not (1 <= start_month <= 12) or not (1 <= end_month <= 12):
            return jsonify({"error": "Invalid month provided."}), 400

        if start_year > end_year or (start_year == end_year and start_month > end_month):
            return jsonify({"error": "Invalid date range."}), 400

        # Build date range
        start_date = datetime(start_year, start_month, 1)
        end_date = datetime(end_year, end_month, 1) + \
            relativedelta(months=1, days=-1)

        # Query income by month
        results = db.session.query(
            db.func.date_trunc('month', Charge.date).label('month'),
            db.func.sum(Charge.amount).label('total')
        ).filter(
            Charge.date >= start_date,
            Charge.date <= end_date
        ).group_by(
            db.func.date_trunc('month', Charge.date)
        ).order_by(
            db.func.date_trunc('month', Charge.date)
        ).all()

        # Format results
        data = [{"month": month.strftime('%B %Y'), "total": float(
            total)} for month, total in results]

        return jsonify(data), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while fetching the data."}), 500


@reports_blueprint.route('/wordcloud-data', methods=['GET'])
@login_required
@permission_required('report_show')
def get_wordcloud_data():
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        print(start_date_str, end_date_str)

        if not start_date_str or not end_date_str:
            return jsonify({"error": "Both start_date and end_date are required."}), 400

        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

        messages = Message.query.filter(
            Message.created_at.between(start_date, end_date)).all()

        word_count = {}
        for message in messages:
            if message.body:
                words = message.body.split()
                for word in words:
                    word_count[word] = word_count.get(word, 0) + 1

        word_data = [{"text": word, "weight": count} for word, count in
                     sorted(word_count.items(), key=lambda x: x[1], reverse=True)]
        return jsonify(word_data), 200

    except ValueError:
        return jsonify({"error": "Invalid date format. Use dd/mm/yyyy."}), 400
    except Exception as e:
        return jsonify({"error": "Error processing the request.", "details": str(e)}), 500
