from . import auth,crypto_key, db, removeItemFromList, updateItemFromList

from datetime import datetime as dt
from datetime import timezone as tz
from flask import Blueprint, request, url_for, jsonify, make_response
from flask import current_app as app
from flask_login import current_user, login_required
from models.models import ContactCenter,AttentionLog,CourseManagers,TrainingType,ActionPlanReferences,WalletTransaction,DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Appointments, CatalogIDDocumentTypes, CatalogUserRoles, CatalogServices
from models.models import CompanyMonitoring,ServiceChannel,surveys_sde,catalog_surveys_sde,Evaluations,ModalityType,CompanyStage,EnrollmentRecord,Courses,CompanyStatus,User, UserExtraInfo, UserXEmployeeAssigned, UserXRole,Company
from models.formatjson import JsonPhone, JsonSocial,JsonConfigProfile
from models.diagnostico import Diagnosticos
from sqlalchemy import or_,desc,asc
from views.wallet import _update_wallet
from views.digitalcenter import convertir_a_datetime
import json
from views.email_app import send_email  # Importar la función send_email desde email_app.py
from models.models import default_timezone
maeapi = Blueprint('maeapi', __name__, template_folder='templates', static_folder='static')

# Set the Appointment's Details
@maeapi.route('/api/mae/save/101/', methods = ['POST'])
# @login_required
def _api_mae_inscripciones():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            preguntas = request.json['preguntas']

            inscripcion = Inscripciones()
            dni = list(e for e in preguntas if e['id']  == 'txt_identidad')[0]['respuesta']
            nombres = list(e for e in preguntas if e['id']  == 'txt_name')[0]['respuesta']
            apellidos = list(e for e in preguntas if e['id']  == 'txt_apellidos')[0]['respuesta']
            inscripcion.name = nombres + ' ' + apellidos
            inscripcion.company_name = list(e for e in preguntas if e['id']  == 'txt_company_name')[0]['respuesta']
            inscripcion.correo = list(e for e in preguntas if e['id']  == 'txt_correo_electronico')[0]['respuesta']
            inscripcion.phone = list(e for e in preguntas if e['id']  == 'txt_celular')[0]['respuesta']
            inscripcion.cohorte = 10
            inscripcion.dni = dni.replace("-", "").strip()
            inscripcion.departamento = list(e for e in preguntas if e['id']  == 'txt_departamento')[0]['respuesta']
            inscripcion.municipio = list(e for e in preguntas if e['id']  == 'txt_municipio')[0]['respuesta']
            inscripcion.rtn = dni.strip()
            inscripcion.respuestas = preguntas
            inscripcion.status = 1
            db.session.add(inscripcion)
            db.session.commit()
            company =  Company.query.filter(Company.dni == dni).first()
            status  =   CompanyStatus.query.filter(CompanyStatus.name_short == 2).first()
            #creamos la empresa
            if not company:
                company = Company()
                company.name = inscripcion.company_name.strip()
                company.rtn = inscripcion.rtn
                company.dni = dni.strip()
                company.address = inscripcion.departamento + ' - ' + inscripcion.municipio
                company.created_by = current_user.id
                company.inscripcion_id = inscripcion.id
                company.status_id = status.id
                db.session.add(company)
                db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })
