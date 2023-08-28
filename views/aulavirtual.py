from . import credentials,auth,changePassword, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app

from flask_login import logout_user, current_user, login_required
from models.models import CompanyStatus,Inscripciones,EnrollmentRecord,Courses,TrainingType,ModalityType,CourseManagers,WalletTransaction,catalogCategory,DocumentCompany,Company, DiagnosisCompany,ActionPlan, Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
aulavirtual = Blueprint('aulavirtual', __name__, template_folder='templates', static_folder='static')


# Creates Timestamps without UTC for JavaScript handling:
# utcDate.replace(tzinfo=tz.utc).timestamp()
#
# Creates Dates witout UTC for Python handling:
# utcDate.replace(tzinfo=tz.utc).astimezone(tz=None)
import json


@aulavirtual.route('/formulario/')
def _curso_created():
    training = TrainingType.query.filter_by(enabled=True).all()
   
    modality = ModalityType.query.filter_by(enabled=True).all()
    manager = CourseManagers.query.filter_by(enabled=True).all()
    context = {
        'training':training,
        'modality':modality,
        'manager':manager,
    }
    return render_template('aulavirtual/curso_created.html',**context)

@aulavirtual.route('/enroll/<int:company_id>//')
def _curso_enroll(company_id):
    company = Company.query.filter_by(id=company_id).first()
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    cursos = Courses.query.filter_by(enabled=True).all()
    context = {
        'company':company,
        'cursos':cursos,
    }
    return render_template('aulavirtual/curso_enroll.html',**context)

@aulavirtual.route('/cursos/list/')
def _curso_list():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    cursos = Courses.query.filter_by(enabled=True).all()
    context = {
        'cursos':cursos,
   
    }
    return render_template('aulavirtual/curso_list.html',**context)
import os
import pandas as pd
@aulavirtual.route('/cursos/list/<int:courses_id>/',methods = ['GET', 'POST'])
def _curso_enroll_list(courses_id):
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    cursos = Courses.query.filter_by(id=courses_id).first()
    enrolls = EnrollmentRecord.query.filter_by(id_course=courses_id).all()
    data = []

    if request.method == 'POST':
        txt_id_company = request.form.get('txt_id_company') 
        if 'file-excel' not in request.files:
            return "No se seleccionó ningún archivo."
        
        file = request.files['file-excel']
        
        if file.filename == '':
            return "No se seleccionó ningún archivo."
        
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            
            file.save(filename)
            
            df = pd.read_excel(filename)
            
            required_columns = ['DNI', 'Correo']
            if not all(column in df.columns for column in required_columns):
                return "El archivo no contiene todas las columnas requeridas."
            linea = 1
            for index, row in df.iterrows():
                identity = row['DNI']
                correo = row['Correo']
                dni = identity.strip().replace("-", "").replace(" ", "")
                inscripcion =  Inscripciones.query.filter(Inscripciones.dni == dni).first()
                if inscripcion:
                    company =  Company.query.filter(Company.dni == inscripcion.dni).first()
                    #creamos la empresa
                    if company:                       
                        enroll = EnrollmentRecord.query.filter_by(id_course = txt_id_company,company_id=company.id).first()
                        if not enroll:
                            courses = EnrollmentRecord()
                            courses.id_course = txt_id_company
                            courses.company_id = company.id
                            courses.created_by = current_user.id
                            db.session.add(courses)         
                            db.session.commit()
                    else:
                        data.append({'linea':index+2, 'dni': dni, 'correo': correo})
                else:
                    data.append({'linea':index+2, 'dni': dni, 'correo': correo})
                
    
    
    context = {
        'enrolls':enrolls,
        'cursos':cursos,
        'data':data
   
    }
    return render_template('aulavirtual/curso_enroll_list.html',**context)