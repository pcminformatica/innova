from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response,send_from_directory
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import EnrollmenWorkshops,Workshops,AttentionLog,WalletTransaction,ActionPlanReferences,DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Company,Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import CompanyMonitoring,ServiceChannel,CompanyStage,EnrollmentRecord,CompanyStatus,TrainingType,ModalityType,CourseManagers,Courses,catalogCategory,CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from models.diagnostico import Diagnosticos
from werkzeug.utils import secure_filename
from sqlalchemy import or_,not_
import pytz
from views.wallet import _update_wallet

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
import os

mae = Blueprint('mae', __name__, template_folder='templates', static_folder='static')

#entry



@mae.route('/mae/workshops/bitacora/<int:enrolls_id>')
def _workshops_bitacora(enrolls_id):
    enrolls = EnrollmenWorkshops.query.filter_by(id=enrolls_id).first()
    context = {
        'enrolls':enrolls,

    }
    return render_template('/mae/workshops_bitacora.html',**context)

@mae.route('/mae/create')
def _create_company():
    return render_template('/mae/create_company.html')

@mae.route('/mae/workshops')
def _workshops_dashboard():
    courses  = Courses.query.filter_by(isworkshop=1).all()
    context = {
        'courses':courses,

    }
    return render_template('/mae/workshops_dashboard.html',**context)

@mae.route('/mae/workshops/creation')
def _workshops_creation_admin():
    training = TrainingType.query.filter_by(enabled=True).all()
   
    modality = ModalityType.query.filter_by(enabled=True).all()
    manager = CourseManagers.query.filter_by(enabled=True).all()
    context = {
        'training':training,
        'modality':modality,
        'manager':manager,
    }

    return render_template('/mae/workshops_creation_admin.html',**context)

@mae.route('/mae/workshops/attendance')
def _workshops_attendance():
    training = TrainingType.query.filter_by(enabled=True).all()
   
    modality = ModalityType.query.filter_by(enabled=True).all()
    manager = CourseManagers.query.filter_by(enabled=True).all()
    context = {
        'training':training,
        'modality':modality,
        'manager':manager,
    }

    return render_template('/mae/workshops_attendance.html',**context)

@mae.route('/mae/workshops/joinis/<int:courses_id>')
def _workshops_joins(courses_id):
    courses  = Courses.query.filter_by(code=courses_id).first()
    training = TrainingType.query.filter_by(enabled=True).all()
   
    modality = ModalityType.query.filter_by(enabled=True).all()
    manager = CourseManagers.query.filter_by(enabled=True).all()
    context = {
        'training':training,
        'modality':modality,
        'manager':manager,
        'courses':courses
    }

    return render_template('/mae/workshops_joins.html',**context)
#process
@mae.route('/mae/home')
def _mae_home():
    return render_template('/mae/home.html')

@mae.route('/mae/list')
def _mae_list():
    # Consulta para traer las Company con inscripción cohorte igual a 10

    # Consulta para traer las Company con inscripción cohorte igual a 10
    companies = Company.query.join(Inscripciones).filter(Inscripciones.cohorte == 10).all()

    context = {
        'companies':companies
    }

    return render_template('/mae/mae_list.html',**context)

@mae.route('/mae/workshops/list')
def _workshops_list():
    return render_template('/mae/workshops_list.html')

#    return render_template('/digitalcenter/form_profile_sde.html')

#output
@mae.route('/mae/perfil/<int:company_id>')
def _mae_perfil(company_id):
    company = Company.query.filter_by(id=company_id).first()
    enroles = EnrollmenWorkshops.query.filter_by(company_id=company.id).all()
    taller_conocimiento = False 
    for enrol in enroles:
        if enrol.workshop.course.code == '101':
            taller_conocimiento = enrol.id
    
    if  taller_conocimiento:
        taller_conocimiento = EnrollmenWorkshops.query.filter_by(id=taller_conocimiento).first()

    mentalidad_emprendedora  = False 
    for enrol in enroles:
        if enrol.workshop.course.code == '102':
            mentalidad_emprendedora = enrol.id
    
    if  mentalidad_emprendedora:
        mentalidad_emprendedora = EnrollmenWorkshops.query.filter_by(id=mentalidad_emprendedora).first()

    canvas_exploratorio  = False 
    for enrol in enroles:
        if enrol.workshop.course.code == '103':
            canvas_exploratorio = enrol.id
    
    if  canvas_exploratorio:
        canvas_exploratorio = EnrollmenWorkshops.query.filter_by(id=canvas_exploratorio).first()

    canvas_base   = False 
    for enrol in enroles:
        if enrol.workshop.course.code == '104':
            canvas_base = enrol.id
    
    if  canvas_base:
        canvas_base = EnrollmenWorkshops.query.filter_by(id=canvas_base).first()

    context = {
        'company':company,
        'enroles':enroles,
        'taller_conocimiento':taller_conocimiento,
        'mentalidad_emprendedora':mentalidad_emprendedora,
        'canvas_exploratorio':canvas_exploratorio,
        'canvas_base':canvas_base

    }
    return render_template('/mae/perfil.html',**context)

@mae.route('/mae/word/perfil/<int:company_id>/<int:courses_id>')
def _workshops_register(company_id,courses_id):
    company = Company.query.filter_by(id=company_id).first()
    courses  = Courses.query.filter_by(code=courses_id).first()
    workshops = Workshops.query.filter_by(id_course =courses.id).all()

    context = {
        'company':company,
        'courses':courses,
        'workshops':workshops
    }
    return render_template('/mae/workshops_creation.html',**context)
