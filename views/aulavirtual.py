from . import credentials,auth,changePassword, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from sqlalchemy import not_,or_
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app

from flask_login import logout_user, current_user, login_required
from models.models import CompanyStatus,Inscripciones,EnrollmentRecord,Courses,TrainingType,ModalityType,CourseManagers,WalletTransaction,catalogCategory,DocumentCompany,Company, DiagnosisCompany,ActionPlan, Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
aulavirtual = Blueprint('aulavirtual', __name__, template_folder='templates', static_folder='static')


from werkzeug.utils import secure_filename
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
import hashlib
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
            try:
                filename = secure_filename(file.filename)
                # initializing string
                str2hash =  dt.now(tz.utc)
                # encoding GeeksforGeeks using encode()
                # then sending to md5()
                result = hashlib.md5(str(str2hash).encode())
                filename = str(current_user.id)+ '-' + str(result.hexdigest()) +'.'+ filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                df = pd.read_excel(file)
                
                required_columns = ['DNI', 'Correo']
                if not all(column in df.columns for column in required_columns):
                    return "El archivo no contiene todas las columnas requeridas."
                linea = 1
        
                for index, row in df.iterrows():
                    identity = str(row['DNI'])
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
                
            except Exception as e:
                return jsonify({'status': 'error', 'msg': str(e)}) 
    
    context = {
        'enrolls':enrolls,
        'cursos':cursos,
        'data':data
   
    }
    return render_template('aulavirtual/curso_enroll_list.html',**context)


@aulavirtual.route('/cursos/list/inscritas/',methods = ['GET', 'POST'])
def _curso_enroll_list_inscritas():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    companies = EnrollmentRecord.query.join(
        Courses, Courses.id==EnrollmentRecord.id_course).join(
        TrainingType, Courses.id_training_type==TrainingType.id).join(
        Company,Company.id == EnrollmentRecord.company_id).join(
        Inscripciones,Inscripciones.id == Company.inscripcion_id
        ).filter(
                TrainingType.name_short == 'TT1'
        ).all()
    print(len(companies))
    # Accede a las Inscripciones.id a través de la relación en EnrollmentRecord
    inscripciones_ids_distintas = [company.company.inscripcion.id for company in companies]
    # Realiza la consulta para obtener las Inscripciones que no están en la lista
    inscripciones_no_en_lista = Inscripciones.query.filter(
        not_(Inscripciones.id.in_(inscripciones_ids_distintas))
    ).all()
    app.logger.debug('** SWING_CMS ** - ------------------')
    inscripciones = Inscripciones.query.filter_by(elegible = True,cohorte=5).filter(
    not_(Inscripciones.id.in_(inscripciones_ids_distintas))
    ).filter(or_(Inscripciones.status != 0, Inscripciones.status == None)).all()
    context = {
        'api': inscripciones
    }
    return render_template('digitalcenter/registro_elegibles_list.html',**context)