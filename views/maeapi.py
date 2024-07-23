from . import auth,crypto_key, db, removeItemFromList, updateItemFromList

from datetime import datetime as dt
from datetime import timezone as tz
from flask import Blueprint, request, url_for, jsonify, make_response
from flask import current_app as app
from flask_login import current_user, login_required
from models.models import EnrollmenWorkshops,EnrollmentRecord,Workshops,ContactCenter,AttentionLog,CourseManagers,TrainingType,ActionPlanReferences,WalletTransaction,DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Appointments, CatalogIDDocumentTypes, CatalogUserRoles, CatalogServices
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
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con','code':company.id })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@maeapi.route('/api/mae/save/workshops/', methods = ['POST'])
# @login_required
def _api_mae_workshops():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            courses_id = request.json['txt_company_id']
            workshops_id = request.json['txt_formacion']

            company  = Company.query.filter_by(id=courses_id).first()
            workshops = Workshops.query.filter_by(id =workshops_id).first()
            inscripcion = EnrollmenWorkshops()
            inscripcion.id_workshop = workshops.id
            inscripcion.company_id = company.id 
            inscripcion.created_by = current_user.id

            db.session.add(inscripcion)
            db.session.commit()


            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@maeapi.route('/api/mae/save/workshops/create', methods = ['POST'])
# @login_required
def _api_mae_workshops_create():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            courses_id = request.json['curso']
            txt_lugar = request.json['txt_lugar']

            txt_fecha_inicio = request.json['txt_fecha_inicio']
            txt_fecha_final = request.json['txt_fecha_final']
            txt_descripcion = request.json['txt_descripcion']



            courses  = Courses.query.filter_by(id=courses_id).first()
            workshop = Workshops()
            workshop.course = courses
            workshop.created_by = current_user.id 
            workshop.date_end =txt_fecha_final
            workshop.date_start =txt_fecha_inicio
            workshop.description =txt_descripcion
            workshop.lugar = txt_lugar
            db.session.add(workshop)
            db.session.commit()


            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })
    
@maeapi.route('/api/mae/saves/workshops/finalizo', methods = ['POST'])
# @login_required
def _api_mae_workshops_fin():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            enrolls_id = request.json['txt_enrolls']
            chx_finalizo = request.json['chx_finalizo']

            enrolls  = EnrollmenWorkshops.query.filter_by(id=enrolls_id).first()
            enrolls.complete = chx_finalizo
            db.session.add(enrolls)
            db.session.commit()


            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })