from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response,send_from_directory
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import surveys_sde,AttentionLog,WalletTransaction,ActionPlanReferences,DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Company,Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import CompanyMonitoring,ServiceChannel,CompanyStage,EnrollmentRecord,CompanyStatus,TrainingType,ModalityType,CourseManagers,Courses,catalogCategory,CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from models.diagnostico import Diagnosticos
from werkzeug.utils import secure_filename
from sqlalchemy import or_,not_
import pytz
from views.wallet import _update_wallet

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
import os

digitalcenter = Blueprint('digitalcenter', __name__, template_folder='templates', static_folder='static')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Python 3 code to demonstrate the
# working of MD5 (string - hexadecimal)
 
import hashlib

@digitalcenter.route('/hora/')
def __form_hora():
    default_timezone=pytz.timezone('America/Tegucigalpa')
    default = dt.now(default_timezone)
    print(default)
    print(default)
    app.logger.debug(default)
    return '9'


@digitalcenter.route('/demanda/v2',methods=['GET', 'POST'])
def _datos_describe_2_v2():
    servicios = []
    app.logger.debug('** SWING_CMS ** - ------------------')
    url = app.config.get('KOBOTOOLBOX_ALL')
    headers=app.config.get('KOBOTOOLBOX_TOKEN')
    resp = requests.get(url,headers=headers)
    api1 = json.loads(resp.content)
    api1['results'] = list(e for e in api1['results'] if e['_submitted_by']  in current_user.extra_info.kobotoolbox['kobotoolbox_access'] )
    for api in api1['results']:
        for resp in api:
            if api[resp] == '1':
                services = CatalogServices.query.filter(CatalogServices.diagnostic_questions.contains(resp)).all()
                if services:
                    for servicesx in services:
                        departamento =api['DEPARTAMENTO']
                        if departamento == '01':
                            name_de ='Atlantida'
                        elif departamento == '02':
                            name_de ='COLÓN'
                        elif departamento == '03':
                            name_de ='COMAYAGUA'
                        elif departamento == '04':
                            name_de ='COPÁN'
                        elif departamento == '05':
                            name_de ='CORTÉS'
                        elif departamento == '06':
                            name_de ='CHOLUTECA'
                        elif departamento == '07':
                            name_de ='EL PARAÍSO'
                        elif departamento == '08':
                            name_de ='FRANCISCO MORAZÁN'
                        elif departamento == '09':
                            name_de ='GRACIAS A DIOS'
                        elif departamento == '10':
                            name_de ='INTIBUCÁ'
                        elif departamento == '11':
                            name_de ='ISLAS DE LA BAHÍA'
                        elif departamento == '12':
                            name_de ='LA PAZ'
                        elif departamento == '13':
                            name_de ='LEMPIRA'
                        elif departamento == '14':
                            name_de ='OCOTEPEQUE'
                        elif departamento == '15':
                            name_de ='OLANCHO'
                        elif departamento == '16':
                            name_de ='SANTA BÁRBARA'
                        elif departamento == '17':
                            name_de ='VALLE'
                        elif departamento == '18':
                            name_de ='YORO'
                            
                        servi = str(servicesx.id) 
                        depart = []
                        if len(list(e for e in servicios if e['id']  == servi)) == 0:
                            depart.append({'name_de':name_de,'departamento':departamento,'total':1})
                            servicios.append({'id':servi,'titulo':servicesx.name,'departamentos':depart,'categoria':servicesx.catalog_category,'total':1,'anterior':api['_id']})
                        else:
                            varl = list(e for e in servicios if e['id']  == servi)[0]
                            index = servicios.index(varl)
                            
                            if servicios[index]['anterior'] != api['_id']:
                                if len(list(e for e in servicios[index]['departamentos'] if e['departamento']  == departamento))== 0:
                                    servicios[index]['departamentos'].append({'name_de':name_de,'departamento':departamento,'total':1})
                                else:
                                    dep = list(e for e in servicios[index]['departamentos'] if e['departamento']  == departamento)[0]
                                    index_departamento = servicios[index]['departamentos'].index(dep)
                                    servicios[index]['departamentos'][index_departamento]['total'] = servicios[index]['departamentos'][index_departamento]['total'] + 1 
                                servicios[index]['total'] = servicios[index]['total'] + 1
                                servicios[index]['anterior'] = api['_id']

                
    legalizacion = []
    administracion = []
    produccion = []
    financiera = []
    mercadeo = [] 
    for servicio in servicios:
        serviciox = servicio['categoria']
        if serviciox:
            if serviciox == 1:
                legalizacion.append(servicio)
            elif serviciox == 2:
                administracion.append(servicio)
                app.logger.debug(administracion)
            elif serviciox == 3:
                produccion.append(servicio)
            elif serviciox == 4:
                financiera.append(servicio)
            elif serviciox == 5:
                mercadeo.append(servicio)
        
    context = {
        'api': api,
        'legalizacion':legalizacion,
        'administracion':administracion,
        'produccion':produccion,
        'financiera':financiera,
        'mercadeo':mercadeo,

    }
   

    return render_template('datos_describe_2_v2.html',**context)


@digitalcenter.route('/ddd/',methods = ['GET', 'POST'])
def __form_perfil_emp2():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'upload-photo' not in request.files:
            return redirect(request.url)
        file = request.files['upload-photo']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # initializing string
            str2hash =  dt.now(tz.utc)
            # encoding GeeksforGeeks using encode()
            # then sending to md5()
            result = hashlib.md5(str(str2hash).encode())
            filename = str(current_user.id)+ '-' + str(result.hexdigest()) +'.'+ filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user = User.query.filter_by(id = current_user.id).first()
        if user.extra_info is None:
            user_extra = UserExtraInfo()
            user_extra.id = user.id
            user_extra.acceptterms = True
            db.session.add(user_extra)
            db.session.commit()
            db.session.refresh(user)
            app.logger.debug('** nooooo ** - API Appointment Detail')
            app.logger.debug('** SWING_CMS ** - API Appointment Detail')
        user.extra_info.avatar = filename
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home._home'))
    if request.method == 'GET':
        return 'hola'

@digitalcenter.route('/save/logo',methods = ['GET', 'POST'])
def __form_perfil_logo_emp2():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'upload-photo' not in request.files:
            return redirect(request.url)
        file = request.files['upload-photo']
        txt_company_id = request.form['txt_company_id']
        company = Company.query.filter_by(id = txt_company_id).first()
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # initializing string
            str2hash =  dt.now(tz.utc)
            # encoding GeeksforGeeks using encode()
            # then sending to md5()
            result = hashlib.md5(str(str2hash).encode())
            filename = str(current_user.id)+ '-' + str(result.hexdigest()) +'.'+ filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        company.avatar = filename
        db.session.add(company)
        db.session.commit()
        db.session.refresh(company)
        return redirect(url_for('digitalcenter._company_edit__form',company_id=txt_company_id))
    if request.method == 'GET':
        return 'hola'

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    

@digitalcenter.route('/form/sde/profile')
@login_required
def __form_profile_sde():
    app.logger.debug('** SWING_CMS ** - Welcome2')
    user = User.query.filter_by(id = current_user.id).first()
    professions = Professions.query.filter_by(enabled = True).all()
    app.logger.debug(professions)
    ctx = {'user':user,'professions':professions}
    return render_template('/digitalcenter/form_profile_sde.html',ctx=ctx)

@digitalcenter.route('/form/perfil/')
@login_required
def __form_perfil_emp():
    app.logger.debug('** SWING_CMS ** - Welcome2')
    user = User.query.filter_by(id = current_user.id).first()
    app.logger.debug('** SWING_CMS ** - Welcome2')
    ctx = {'user':user}
    return render_template('/digitalcenter/form_perfil_emp.html',ctx=ctx)
  

@digitalcenter.route('/form/category/')
@login_required
def __form_perfil_category():
        
    app.logger.debug('** SWING_CMS ** - Welcome2')

    user = User.query.filter_by(id = current_user.id).first()
    app.logger.debug('** SWING_CMS ** - Welcome2')

    ctx = {'user':user}
    return render_template('/digitalcenter/form_perfil_category.html',ctx=ctx)

@digitalcenter.route('/atencionempresarial/')
def _home_view():
    cur_oul = RTCOnlineUsers.query.with_for_update().order_by(RTCOnlineUsers.id.desc()).first()
    app.logger.debug('siiiiiiiiiiiiiiiiii *********')
    app.logger.debug(cur_oul.userlist)
    app.logger.debug('** siiiiiiiiiiiii varela')

    new_oul = cur_oul
    app.logger.debug(new_oul.userlist)    
    app.logger.debug('** yyyyyyy varela')   
    if current_user.is_authenticated:
        if current_user.is_user_role(['adm', 'emp']):
            x= new_oul.userlist.get('rtc_online_users', {}).get('emp_users')
        else:
            x= new_oul.userlist.get('rtc_online_users', {}).get('reg_users')
    else:
        x=  new_oul.userlist.get('rtc_online_users', {}).get('anon_users')
    x=  new_oul.userlist.get('rtc_online_users', {}).get('asesoras_user')
    if User.query.filter_by(id = 5).first():
        userRu = User.query.filter_by(id = 5).first()
    else:
        userRu = User.query.filter_by(id = 3).first()
    if User.query.filter_by(id = 6).first():
        userRi = User.query.filter_by(id = 6).first()
    else:
        userRi = User.query.filter_by(id = 3).first()
    if User.query.filter_by(id = 30).first():
        userAna = User.query.filter_by(id = 30).first()
    else:
        userAna = User.query.filter_by(id = 3).first()
    if User.query.filter_by(id = 15).first():
        userSPS = User.query.filter_by(id = 15).first()
    else:
        userSPS = User.query.filter_by(id = 3).first()
    if User.query.filter_by(id = 16).first():
        userLCB = User.query.filter_by(id = 16).first()
    else:
        userLCB = User.query.filter_by(id = 3).first()
    if User.query.filter_by(id = 17).first():
        userCholo = User.query.filter_by(id = 17).first()
    else:
        userCholo = User.query.filter_by(id = 3).first()
    if User.query.filter_by(id = 18).first():
        userCholu = User.query.filter_by(id = 18).first()
    else:
        userCholu = User.query.filter_by(id = 3).first()
   # if User.query.filter_by(id = 21).first():
   #     userTGU = User.query.filter_by(id = 21).first()
   # else:
   #     userTGU = User.query.filter_by(id = 3).first()
   # if User.query.filter_by(id = 20).first():
   #     userJuti = User.query.filter_by(id = 20).first()
   # else:
   #     userJuti = User.query.filter_by(id = 3).first()
    if User.query.filter_by(id = 24).first():
        userJefe = User.query.filter_by(id = 24).first()
    else:
        userJefe = User.query.filter_by(id = 3).first()

    if User.query.filter_by(id = 66).first():
        userAngie = User.query.filter_by(id = 66).first()
    else:
        userAngie = User.query.filter_by(id = 3).first()
        
    app.logger.debug('** varela')   
    app.logger.debug(x)
    app.logger.debug('** iiiiiiiiiiii varela')   
    new_userlist = new_oul.userlist
    app.logger.debug(new_userlist)    
    app.logger.debug('** xxxxxxxxxxxxx varela')    
    app.logger.debug('** SWING_CMS ** - Welcome2')
    context = {'userAngie':userAngie, 'userJefe':userJefe,'userAna':userAna, 'userRu':userRu,'userRi':userRi,'userLCB':userLCB,'userSPS':userSPS,'userCholo':userCholo,'userCholu':userCholu}
    return render_template('digitalcenter/home_view.html',**context)

@digitalcenter.route('/digitalcenter/chat/')
@login_required
def _dc_chat():
    app.logger.debug('** SWING_CMS ** - Try Chat')
    try:
        # Validate if the user has a Valid Session and Redirects
        response = isUserLoggedInRedirectDC('/digitalcenter/chat/', 'redirect')
        if response is not None:
            return response
        else:
            return render_template('chat.html')
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Try Chat Error: {}'.format(e))
        return jsonify({ 'status': 'error' })

@digitalcenter.route('/digitalcenter/chat/admin/')
def _dc_chat_admin():
    app.logger.debug('** SWING_CMS ** - Welcome2')
    #return render_template('/digitalcenter/dc_chat_admin.html')
    return render_template('/chatdc/chatadmin.html')

@digitalcenter.route('/digitalcenter/chat/home/')
def _dc_chat_home():
    app.logger.debug('** SWING_CMS ** - Welcome2')
    #return render_template('/digitalcenter/dc_chat_home.html')
    return render_template('/chatdc/chatuser.html')

@digitalcenter.route('/test/admin')
def _dc_chat_ad():
    app.logger.debug('** SWING_CMS ** - Welcome2')
    return render_template('/chatdc/chatadmin.html')

@digitalcenter.route('/test/user')
def _dc_chat_us():
    app.logger.debug('** SWING_CMS ** - Welcome2')
    return render_template('/chatdc/chatuser.html')

@digitalcenter.route('/sde/profile/1/example/')
def _sdeProfile():
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    return render_template('sdeProfile.html')

@digitalcenter.route('/sde/profile/<int:user_id>/',methods=['GET', 'POST'])
def _sdeProfileA(user_id):
    sdeProfile = User.query.filter_by(id = user_id).first()
    if sdeProfile:
        app.logger.debug('** SWING_CMS ** - Home Dashboard')
        context = {'sdeProfile':sdeProfile}
        return render_template('digitalcenter/sdeProfile.html',**context)
    else:
        return render_template('404.html')

@digitalcenter.route('/sde/appointments/<int:user_id>/create/old',methods=['GET', 'POST'])
def _dcappointments_create(title):
    app.logger.debug('** SWING_CMS ** -  appointments_create')    
    return render_template('digitalcenter/appointments_create.html')

@digitalcenter.route('/sde/admin/appointments/<int:user_id>/create',methods=['GET', 'POST'])
def _dcappointments_create_admin(user_id):
    app.logger.debug('** SWING_CMS ** -  appointments_create') 
    services = CatalogServices.query.filter_by(enabled = 1).all()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    context = {'services':services}  
    return render_template('digitalcenter/appointments_create_admin.html',**context)


@digitalcenter.route('/sde/appointments/config',methods=['GET', 'POST'])
def _dcconfig_calendar():
    app.logger.debug('** SWING_CMS ** -  appointments_create')    
    return render_template('digitalcenter/dcconfig_calendar.html')

#  configuracion
@digitalcenter.route('/sde/appointments/calendar/config',methods=['GET', 'POST'])
def _dcconfig_calendar_sde():
    app.logger.debug('** SWING_CMS ** -  appointments_create')    
    return render_template('digitalcenter/dcconfig_sde_calendar.html')

@digitalcenter.route('/sde/appointments/<int:user_id>/create',methods=['GET', 'POST'])
def _dcappointments_sde_create(user_id):
    sdeProfile = User.query.filter_by(id = user_id).first()
    dt_today = '2023-02-01 09:00:00'

    details = Appointments.query.join(UserXEmployeeAssigned).filter(
        Appointments.date_scheduled > dt_today,
        UserXEmployeeAssigned.user_id == Appointments.created_for,
        UserXEmployeeAssigned.employee_id == user_id,
        Appointments.cancelled == False
    ).order_by(Appointments.date_scheduled.asc()).all()
    for details in details:
        ('** SWING_CMS ** -  appointments_creaxxxxxte',details)  
        app.logger.debug(details.id)    
    if sdeProfile:
        app.logger.debug('** SWING_CMS ** - Home Dashboard')
        context = {'sdeProfile':sdeProfile}
        return render_template('digitalcenter/dcappointments_sde_create.html',**context)
    else:
        return render_template('404.html')


@digitalcenter.route('/webinar',methods=['GET', 'POST'])
def _webinar():
    return redirect('http://inscripciones.ciudadmujer.gob.hn/webinar')

@digitalcenter.route('/inscribite/list/web',methods=['GET', 'POST'])
def _webinarResultados():
    return redirect('http://inscripciones.ciudadmujer.gob.hn/inscribite/list/web')


@digitalcenter.route('/inscribite/',methods=['GET', 'POST'])
def _webinarInscribite():
    return redirect('http://inscripciones.ciudadmujer.gob.hn/inscribite/')
    
@digitalcenter.route('/reset/chat',methods=['GET', 'POST'])
def _re():
    nowdt = dt.now(tz.utc)
    operation = CatalogOperations.query.filter_by(name_short='ins').first()

    rtc_oul = RTCOnlineUsers()
    rtc_oul.id = nowdt
    rtc_oul.operation_id = operation.id
    rtc_oul.userlist = {
        'rtc_online_users': {
            'id': str(nowdt),
            'anon_users': [],
            'emp_users': [],
            'reg_users': [],
            'itc_users': [], 
            'dis_users': [],
            'mkt_users': []
        }
    }
    rtc_oul.enabled = True
    db.session.add(rtc_oul)

    db.session.commit()
    return render_template('404.html')



@digitalcenter.route('/plan/',methods=['GET', 'POST'])
def _plan_2():
    return render_template('plan.html')

@digitalcenter.route('/historial/',methods=['GET', 'POST'])
def _historial_2():
    return render_template('historial.html')


from sqlalchemy import desc
import requests
import json 
@digitalcenter.route('/diagnosticos/',methods=['GET', 'POST'])
@login_required
def _diagnosis_monitoring_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    try:
        url = app.config.get('KOBOTOOLBOX_ALL')
        headers=app.config.get('KOBOTOOLBOX_TOKEN')
        resp = requests.get(url,headers=headers)
        api = json.loads(resp.content)
        user = User.query.filter(User.id == current_user.id).first()
        api['results'] = list(e for e in api['results'] if e['_submitted_by']  in user.extra_info.kobotoolbox['kobotoolbox_access'] )
        context = {
            'api': api
        }
        return render_template('diagnosis_monitoring_list.html',**context)
    except Exception as e:
        return render_template('404.html')

@digitalcenter.route('/diagnosticos/comparativo',methods=['GET', 'POST'])
@login_required
def _diagnosis_monitoring_1_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    try:
        url = app.config.get('KOBOTOOLBOX_ALL')
        headers=app.config.get('KOBOTOOLBOX_TOKEN')
        resp = requests.get(url,headers=headers)
        api = json.loads(resp.content)
        user = User.query.filter(User.id == current_user.id).first()
        api['results'] = list(e for e in api['results'] if e['_submitted_by']  in user.extra_info.kobotoolbox['kobotoolbox_access'] )
        api2 = {}
        apix1 = []
        for apix in api['results']:
            identidad = apix['IDENTIDAD'].replace('-','')
            company =  Company.query.filter(Company.dni == identidad).first()
            if not company:
                apix1.append(apix)
            
        api2['results'] = apix1

        context = {
            'api': api2
        }
        return render_template('diagnosis_monitoring_list.html',**context)
    except Exception as e:
        return render_template('404.html')

@digitalcenter.route('/cartas/comparativo',methods=['GET', 'POST'])
@login_required
def _diagnosis_monitoring_2_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    try:
        diagnosis = DiagnosisCompany.query.filter_by(status=True).all()
        companys = []
        for diagnosi in diagnosis:
        
            ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
            ficha =  DocumentCompany.query.filter_by(company_id=diagnosi.company_id,documente_type_id=ficha.id,enabled=True).order_by(DocumentCompany.id.desc()).first()
            if not ficha:
                if diagnosi.company_id:
                    company = Company.query.filter_by(id=diagnosi.company_id,enabled=True).first()
                    if company:
                        companys.append(company)

        company_references = []
        context = {
            'apis': companys,
            'company_references':company_references
        }
        return render_template('company_monitoring_list.html',**context)
    except Exception as e:
        print(e)
        print(e)
        return render_template('404.html')
    
@digitalcenter.route('/planes/add/<int:user_uid>/',methods=['GET', 'POST'])
@login_required
def _plan_action_create(user_uid):
    app.logger.debug('** SWING_CMSx ** - ------------------')
    
    company =  Company.query.filter(Company.id == user_uid).first()
    diagnosis =  DiagnosisCompany.query.filter(DiagnosisCompany.company_id == company.id).first()
    plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).all()
    api = diagnosis.respuestas
    servicios = []
    if diagnosis.origin == 2:
        for resp in api:
            if resp['respuesta']  == '1' or resp['respuesta'] == '2':
                #print("Pregunta: {} respuesta: {}".format(resp,api[resp]))
                services = CatalogServices.query.filter(
                (CatalogServices.enabled == True) & 
                    CatalogServices.diagnostic_questions.contains(resp['id'])
                ).order_by(desc(CatalogServices.id)).all()
                for servicesx in services:
                    if len(list(e for e in servicios if e['id']  == servicesx.id)) == 0:
                        servicios.append({'id':servicesx.id,'tiempo_asesoria':servicesx.advisory_time,'tiempo_ejecucion':servicesx.execution_time,'costo':servicesx.cost,'titulo':servicesx.name,'categoria':servicesx.catalog_category})
    else:
        for resp in api:
            if api[resp] == '1' or api[resp] == '2':
                print("Pregunta: {} respuesta: {}".format(resp,api[resp]))
                services = CatalogServices.query.filter(
                (CatalogServices.enabled == True) & 
                    CatalogServices.diagnostic_questions.contains(resp)
                ).order_by(desc(CatalogServices.id)).all()
                for servicesx in services:
                    if len(list(e for e in servicios if e['id']  == servicesx.id)) == 0:
                        servicios.append({'id':servicesx.id,'tiempo_asesoria':servicesx.advisory_time,'tiempo_ejecucion':servicesx.execution_time,'costo':servicesx.cost,'titulo':servicesx.name,'categoria':servicesx.catalog_category})
    legalizacion = []
    administracion = []
    produccion = []
    financiera = []
    mercadeo = [] 
    for servicio in servicios:
        serviciox = servicio['categoria']
        if serviciox:
            if serviciox == 1:
                legalizacion.append(servicio)
            elif serviciox == 2:
                administracion.append(servicio)
                app.logger.debug(administracion)
            elif serviciox == 3:
                produccion.append(servicio)
            elif serviciox == 4:
                financiera.append(servicio)
            elif serviciox == 5:
                mercadeo.append(servicio)
    totalServicios = len(legalizacion) + len(administracion) + len(produccion) + len(financiera) + len(mercadeo)
    context = {
        'company':company,
        'plan':plan,
        'api': api,
        'legalizacion':legalizacion,
        'administracion':administracion,
        'produccion':produccion,
        'financiera':financiera,
        'mercadeo':mercadeo,
        'totalServicios':totalServicios

    }
   
    app.logger.debug(servicios)
    app.logger.debug(servicios)
    return render_template('plan_action_create.html',**context)

@digitalcenter.route('/planes/add/asesorias/<int:company_uid>/',methods=['GET', 'POST'])
@login_required
def _asesorias_puntuales(company_uid):
    company = Company.query.filter_by(id=company_uid).first()
    categoria = catalogCategory.query.filter_by().all()
    services = CatalogServices.query.filter_by(enabled=True).all()
    context = {'categoria':categoria,'services':services,'company':company} 
    return render_template('asesorias_puntuales.html',**context)

@digitalcenter.route('/activar/diagnostico/<int:company_uid>/plan/<servicio_uid>/',methods=['GET', 'POST'])
@login_required
def _plan_action_dianostico_plan(company_uid,servicio_uid):
    company = Company.query.filter_by(id=company_uid).first()
                #buscar si el diagnostico esta en plan de accion
    service_plan = CatalogServices.query.filter_by(name_short=servicio_uid).first()
    if not service_plan or not company:
        return render_template('404.html')
    actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service_plan.id,cancelled=False).first()
    if not actionplan:
        if request.method == 'POST':
            txt_start_date = request.form.get('txt_start_date') 
            txt_end_date = request.form.get('txt_end_date') 
            txt_descripcion = request.form.get('txt_descripcion') 
            actionplan = ActionPlan()
            actionplan.company_id = company.id
            actionplan.company = company
            actionplan.date_scheduled_start =txt_start_date
            actionplan.date_scheduled_end = txt_end_date
            actionplan.services_id = service_plan.id
            actionplan.created_by = current_user.id
            actionplan.fase = 0
            actionplan.descripcion = txt_descripcion
            db.session.add(actionplan)
            db.session.commit() 
            actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service_plan.id,cancelled=False).first()
            return redirect(url_for('digitalcenter._plan_action_bitacora',user_uid=actionplan.id))
    else:
        return redirect(url_for('digitalcenter._plan_action_bitacora',user_uid=actionplan.id))
    context = {'services':service_plan} 
    return render_template('plan_action_dianostico_plan.html',**context)

@digitalcenter.route('/admin/servicios',methods=['GET', 'POST'])
@login_required
def _admin_servicios():
    app.logger.debug('** SWING_CMS ** -  appointments_create') 
    services = CatalogServices.query.filter(CatalogServices.diagnostic_questions.contains("_6_2")).all()
    app.logger.debug('** busqua1 ** - ----')
    servicios = []
    for servicesx in services:
        servicios.append({'id':servicesx.id,'titulo':servicesx.name})
        app.logger.debug('** busqueda ** - ----')
        app.logger.debug(servicesx.id)
    app.logger.debug('** busqua2 ** - ----')
    for servicesx in services:
        app.logger.debug('** busquedax ** - ----')
        if next(x for x in servicios if x["id"] == 3 ):
            servicios.append({'id':servicesx.id,'titulo':servicesx.name})
            app.logger.debug('** busqueda ** - ----')
            app.logger.debug(servicesx.id)
    app.logger.debug(servicios)
    context = {'services':services} 
    return render_template('servicios.html',**context)


@digitalcenter.route('/update/innova',methods=['GET', 'POST'])
@login_required
def _valorar_servicios():
    servicios = CatalogServices.query.filter().all()
    for servicio in servicios:
        servicio.cost_innova = 250
        db.session.add(servicio)
        db.session.commit()
    return 'Listo'

@digitalcenter.route('/update/status',methods=['GET', 'POST'])
@login_required
def _init_status_company():
    companys = Company.query.filter_by(enabled=True).all()[0:200]
    for company in companys:
        update =  Company.query.filter(Company.id == company.id).first()
        ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
        ficha =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id).first()
        if ficha:
            diagnosis = DiagnosisCompany.query.filter(DiagnosisCompany.company_id == company.id).first()
            if  diagnosis:
                status = CompanyStatus.query.filter_by(name_short='6').first()
            else:
                status = CompanyStatus.query.filter_by(name_short='3').first()
            update.status_id = status.id
        else:
            status = CompanyStatus.query.filter_by(name_short='2').first()
            update.status_id = status.id
        db.session.add(update)
        db.session.commit()
    return 'listo'

@digitalcenter.route('/update/status/1',methods=['GET', 'POST'])
@login_required
def _init_status_company_2():
    companys = Company.query.filter_by(enabled=True).all()[200:400]
    for company in companys:
        update =  Company.query.filter(Company.id == company.id).first()
        ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
        ficha =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id).first()
        if ficha:
            diagnosis = DiagnosisCompany.query.filter(DiagnosisCompany.company_id == company.id).first()
            if  diagnosis:
                status = CompanyStatus.query.filter_by(name_short='6').first()
            else:
                status = CompanyStatus.query.filter_by(name_short='3').first()
            update.status_id = status.id
        else:
            status = CompanyStatus.query.filter_by(name_short='2').first()
            update.status_id = status.id
        db.session.add(update)
        db.session.commit()
    return 'listo'

@digitalcenter.route('/update/status/2',methods=['GET', 'POST'])
@login_required
def _init_status_company_3():
    companys = Company.query.filter_by(enabled=True).all()[400:600]
    for company in companys:
        update =  Company.query.filter(Company.id == company.id).first()
        ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
        ficha =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id).first()
        if ficha:
            diagnosis = DiagnosisCompany.query.filter(DiagnosisCompany.company_id == company.id).first()
            if  diagnosis:
                status = CompanyStatus.query.filter_by(name_short='6').first()
            else:
                status = CompanyStatus.query.filter_by(name_short='3').first()
            update.status_id = status.id
        else:
            status = CompanyStatus.query.filter_by(name_short='2').first()
            update.status_id = status.id
        db.session.add(update)
        db.session.commit()
    return 'listo'

@digitalcenter.route('/update/wallet',methods=['GET', 'POST'])
@login_required
def _init_wallet():
    companys = Company.query.filter_by(enabled=True).all()
    for company in companys:
        # Verificar si available_credit no existe o es menor o igual a cero
        if not company.available_credit or company.available_credit <= 0:
            # El código a ejecutar cuando la condición se cumple
            diagnostico = DiagnosisCompany.query.filter_by(company_id=company.id).first()
            #buscar si tiene diagnostico
            if diagnostico:
                #buscar si el diagnostico esta en plan de accion
                service_plan = CatalogServices.query.filter_by(name_short='a2').first()
                actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service_plan.id,cancelled=False).first()
                if not actionplan:
                    actionplan = ActionPlan()
                    actionplan.company_id = company.id
                    actionplan.company = company
                    actionplan.date_scheduled_start =diagnostico.date_created
                    actionplan.date_scheduled_end = diagnostico.date_created
                    actionplan.services_id = service_plan.id
                    actionplan.created_by = diagnostico.created_by
                    actionplan.fase = 0
                    actionplan.descripcion = ''
                    db.session.add(actionplan)
                    db.session.commit() 
                #buscar en wallet si esta el diagnostico
                wallet = WalletTransaction.query.filter_by(company_id = actionplan.company_id, services_id =service_plan.id).first()
                if not wallet:  
                    wallet = WalletTransaction()
                    wallet.amount = service_plan.cost_innova
                    wallet.company_id =company.id
                    wallet.services_id = service_plan.id
                    wallet.created_by = diagnostico.created_by
                    wallet.status = 1
                    wallet.type = 1
                    db.session.add(wallet)
                    db.session.commit() 
                #buscamos si tiene plan de accion
                service_plan = CatalogServices.query.filter_by(name_short='a3').first()
                actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service_plan.id,cancelled=False).first()
                if not actionplan:
                    #validamos que se encuentren servicios dentro del plan de accion
                    plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).order_by(asc(ActionPlan.date_scheduled_start)).first()
                    if plan:
                        plan = ActionPlan()
                        plan.company_id = company.id
                        plan.company = company
                        plan.date_scheduled_start =plan.date_scheduled_start
                        plan.date_scheduled_end = plan.date_scheduled_start
                        plan.services_id = service_plan.id
                        plan.created_by = diagnostico.created_by
                        plan.fase = 0
                        plan.descripcion = ''
                        db.session.add(plan)
                        db.session.commit() 
                        db.session.refresh(plan)
                wallet = WalletTransaction.query.filter_by(company_id = company.id, services_id =service_plan.id).first()
                if not wallet:  
                    wallet = WalletTransaction()
                    wallet.amount = service_plan.cost_innova
                    wallet.company_id =company.id
                    wallet.services_id = service_plan.id
                    wallet.created_by = diagnostico.created_by
                    wallet.status = 1
                    wallet.type = 1
                    db.session.add(wallet)
                    db.session.commit() 
            
                #recorre todos los servicios de la fase 1.
                plans = ActionPlan.query.filter(ActionPlan.company_id==company.id,ActionPlan.fase==1,ActionPlan.cancelled==False).order_by(asc(ActionPlan.date_scheduled_start)).all()
                #plans = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).order_by(asc(ActionPlan.date_scheduled_start)).all()
                if plans:
                    for plan in plans:
                        service_plan = CatalogServices.query.filter_by(id=plan.services_id).first()
                        wallet = WalletTransaction.query.filter_by(company_id = plan.company_id, services_id =service_plan.id).first()
                        if not wallet:  
                            wallet = WalletTransaction()
                            wallet.amount = service_plan.cost_innova
                            wallet.company_id =company.id
                            wallet.services_id = service_plan.id
                            wallet.created_by = plan.created_by
                            wallet.type = 1
                            if plan.progress == 100:
                                wallet.status = 1
                            else:
                                wallet.status = 2
                            db.session.add(wallet)
                            db.session.commit() 
                #recorre todos los servicios de la fase 2
                plans = ActionPlan.query.filter(ActionPlan.company_id==company.id,ActionPlan.fase==2,ActionPlan.cancelled==False).order_by(asc(ActionPlan.date_scheduled_start)).all()
                #plans = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).order_by(asc(ActionPlan.date_scheduled_start)).all()
                if plans:
                    for plan in plans:
                        service_plan = CatalogServices.query.filter_by(id=plan.services_id).first()
                        wallet = WalletTransaction.query.filter_by(company_id = plan.company_id, services_id =service_plan.id).first()
                        if wallet:  
                        # Si se encuentra un registro en la consulta, lo eliminamos
                            db.session.delete(wallet)
                            db.session.commit()
                service_planx = CatalogServices.query.filter_by(name_short='c1').first()
                wallet = WalletTransaction.query.filter_by(company_id = company.id, services_id =service_planx.id,status = 1).first()
                if wallet:  
                    # Si se encuentra un registro en la consulta, lo eliminamos
                    db.session.delete(wallet)
                    db.session.commit()
                if not wallet:  
                    wallet = WalletTransaction()
                    wallet.amount = service_planx.cost_innova
                    wallet.company_id =company.id
                    wallet.services_id = service_planx.id
                    wallet.created_by = diagnostico.created_by
                    wallet.type = 0
                    wallet.status = 1
                    db.session.add(wallet)
                    db.session.commit() 
                actualizar = _update_wallet(company.id)
                if actualizar:
                    print('empresa actulizada')

    return 'Listo'


@digitalcenter.route('/creditos/innova',methods=['GET', 'POST'])
@login_required
def _init_services_creditos():
    staff_it_role = CatalogUserRoles.query.filter_by(name_short='itc').first()
    websites = CatalogServices(name='Beca INNOVA', name_short='c1',cost_innova=4000,cost=4000, service_user_role=staff_it_role.id)
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Créditos INNOVA', name_short='c2',cost_innova=0,cost=0, service_user_role=staff_it_role.id)
    db.session.add(websites)
    db.session.commit()
    return 'Listo'

#----
@digitalcenter.route('/init/cursos',methods=['GET', 'POST'])
@login_required
def _init_cursos():
    #tipo de formacion
    TT1 = TrainingType(name='Formación Inicial', name_short='TT1')
    db.session.add(TT1)
    TT2 = TrainingType(name='Formación continua', name_short='TT2')
    db.session.add(TT2)
    #ModalityType
    MT1 = ModalityType(name='Presencial', name_short='MT1')
    db.session.add(MT1)
    MT2 = ModalityType(name='Virtual', name_short='MT2')
    db.session.add(MT2)
    #CourseManagers
    CM1 = CourseManagers(name='Laboratoria', name_short='Labo')
    db.session.add(CM1)
    CM2 = CourseManagers(name='Centro Nacional de Educación para el Trabajo', name_short='CENET')
    db.session.add(CM2)
    #CourseManagers
    CS1 = CompanyStatus(name='Elegible', name_short='1')
    db.session.add(CS1)
    CS2 = CompanyStatus(name='En proceso', name_short='2')
    db.session.add(CS2)
    CS3 = CompanyStatus(name='Inscrita', name_short='3')
    db.session.add(CS3)
    CS4 = CompanyStatus(name='Inactiva por decisión de la empresaria', name_short='4')
    db.session.add(CS4)
    CS5 = CompanyStatus(name='Inactiva por no cumplimiento de requisitos', name_short='5')
    db.session.add(CS5)
    db.session.commit()
    return 'Listo'

@digitalcenter.route('/init/activas',methods=['GET', 'POST'])
@login_required
def _init_activas():
    CS6 = CompanyStatus(name='Activa', name_short='6')
    db.session.add(CS6)
    db.session.commit()
    return 'Listo'

@digitalcenter.route('/insert/chat',methods=['GET', 'POST'])
@login_required
def _re1():
    staff_it_role = CatalogUserRoles.query.filter_by(name_short='itc').first()
    websites = CatalogServices(catalog_category=1,name='Asesoria para la formalizacion legal de la empresa', name_short='s1', service_user_role=staff_it_role.id,diagnostic_questions=[])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=1,name='Asesoria para gestión de registros legales', name_short='s2', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_9"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=1,name='Asesoria para adhesion al regimen de  facturacion, beneficios fiscales y legislación tributaria.', name_short='s3', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_9"},{"id": "_4_6"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=1,name='Acompañar en la gestión de solicitudes legales empresariales', name_short='s4', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_3"},{"id": "_2_8"},{"id": "_5_7"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=2,name='Acompañamiento en la elaboración de plan operativo y estratégico de desarrollo para la empresa.', name_short='s5', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_1_1"},{"id": "_1_2"},{"id": "_1_3"},{"id": "_1_4"},{"id": "_1_5"},{"id": "_1_7"},{"id": "_1_8"},{"id": "_1_8"},{"id": "_6_2"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=2,name='Asesoria en la gestión del talento humano.', name_short='s6', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_3_3"},{"id": "_5_6"},{"id": "_5_16"},{"id": "_5_17"},{"id": "_5_18"},{"id": "_6_1"},{"id": "_6_2"},{"id": "_6_3"},{"id": "_6_5"},{"id": "_6_6"},{"id": "_6_7"},{"id": "_6_8"},{"id": "_6_9"},{"id": "_6_10"},{"id": "_6_11"},{"id": "_6_12"},{"id": "_6_13"},{"id": "_6_14"},{"id": "_6_16"},{"id": "_6_17"}])
    db.session.add(websites)
    db.session.commit()

    websites = CatalogServices(catalog_category=2,name='Asesoria para implemetación de un sistema básico para el registro de las operaciones.', name_short='s8', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_8"},{"id": "_5_18"}])
    db.session.add(websites)
    db.session.commit()

    websites = CatalogServices(catalog_category=2,name='Elaboración de platillas para la elaboración de los Estados Financieros.', name_short='s10', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_5"},{"id": "_4_7"},{"id": "_4_10"},{"id": "_4_12"},{"id": "_4_17"}])
    db.session.add(websites)
    db.session.commit()
    #--
    websites = CatalogServices(catalog_category=3,name='Realizar la descripción y análisis de los procesos actuales para elaborar el diagrama de procesos.', name_short='s11', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_5_1"},{"id": "_5_5"},{"id": "_5_8"},{"id": "_5_12"},{"id": "_5_13"},{"id": "_5_14"},{"id": "_5_15"},{"id": "_5_19"},{"id": "_5_20"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=3,name='Acompañamiento en la elaboración de una guia para la gestión de calidad.', name_short='s12', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_5_8"},{"id": "_5_11"},{"id": "_5_13"},{"id": "_5_14"},{"id": "_5_17"},{"id": "_5_22"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=3,name='Asesoria para el desarrollo de red proveedores, cadena de sumistros y canales de distribución.', name_short='s13', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_14"},{"id": "_4_20"},{"id": "_5_3"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=3,name='Brindar estrategias y modelos para la mejora de la productividad.', name_short='s14', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_5_1"},{"id": "_5_21"},{"id": "_5_23"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=3,name='Asesoría en la formalización de productos y diseño de fichas técnicas.', name_short='s15', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_7"},{"id": "_5_2"},{"id": "_5_5"},{"id": "_5_8"},{"id": "_5_11"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=1,name='Asesoria para la afiliación y cotizaciones al IHSS, INFOP, RAP y gestiones legales de talento humano', name_short='s16', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_4"},{"id": "_4_19"},{"id": "_6_4"},{"id": "_6_9"},{"id": "_6_12"}])
    db.session.add(websites)
    db.session.commit()
    return render_template('404.html')


@digitalcenter.route('/insert/chat/2',methods=['GET', 'POST'])
@login_required
def _re2():
    staff_it_role = CatalogUserRoles.query.filter_by(name_short='itc').first()
    websites = CatalogServices(catalog_category=3,name='Asesoría en desarrollo de nuevos productos o mejora de los actuales y empaque.', name_short='s17', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_6"},{"id": "_5_2"},{"id": "_5_8"},{"id": "_5_9"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=4,name='Asesoria para el analisis de los riesgos financieros de la empresa.', name_short='s18', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_1"},{"id": "_4_7"},{"id": "_4_13"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=4,name='Elaboración de presupuestos.', name_short='s19', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_23"},{"id": "_4_14"},{"id": "_4_19"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=4,name='Asesoria para la Implementación de herramientas de control para registros de inventarios', name_short='s20', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_2"},{"id": "_4_3"},{"id": "_4_13"},{"id": "_4_14"},{"id": "_5_14"},{"id": "_5_21"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=4,name='Asesoria para los analisis de estados financieros e indicadores de productividad y gestión', name_short='s21', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_1"},{"id": "_4_5"},{"id": "_4_12"},{"id": "_4_17"},{"id": "_5_24"},{"id": "_6_17"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=4,name='Asesoría en analisis de costos y precios', name_short='s22', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_24"},{"id": "_2_25"},{"id": "_2_26"},{"id": "_4_1"},{"id": "_4_6"},{"id": "_4_18"},{"id": "_4_21"},{"id": "_5_19"},{"id": "_5_24"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoría para la adquisición de programas informáticos antivirus, ofis y sistemas operativos', name_short='s23', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_3_4"},{"id": "_3_7"},{"id": "_3_10'"},{"id": "3_11"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoría en requerimientos tecnológicos, contratos de servicios de internet y cuentas de correo', name_short='s24', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_9"},{"id": "_2_20"},{"id": "_3_1'"},{"id": "_3_2"},{"id": "_3_5"},{"id": "_3_6"},{"id": "_3_9"}])
    db.session.add(websites)
    db.session.commit()
    return render_template('404.html')

@digitalcenter.route('/insert/chat/3',methods=['GET', 'POST'])
@login_required
def _re3():
    staff_it_role = CatalogUserRoles.query.filter_by(name_short='itc').first()
    websites = CatalogServices(catalog_category=5,name='Elaboracion del plan de mercadeo para promocion e incremento de ventas.', name_short='s25', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_1"},{"id": "_5_23"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Analisis del entorno y la competencia para generación de estrategia de mejora.', name_short='s26', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_1_10'"},{"id": "_1_11"},{"id": "_2_9'"},{"id": "_2_26"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Acompañamiento en el uso de redes sociales (mercadeo digital)', name_short='s27', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_19'"},{"id": "_2_22"},{"id": "_3_9'"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoria en como realizar sondeos de mercado.', name_short='s28', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_1'"},{"id": "_2_6"},{"id": "_2_9'"},{"id": "_2_10'"},{"id": "_2_13'"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Acompañamiento en el desarrollo de estrategias de comercialización para captar y fidelizar clientes', name_short='s29', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_10'"},{"id": "_2_11"},{"id": "_2_12'"},{"id": "_2_19'"},{"id": "_2_20'"},{"id": "_2_18'"},{"id": "_2_21"},{"id": "_2_23'"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoría en el desarrollo de canales de distribución.', name_short='s30', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_15'"},{"id": "_2_16"},{"id": "_2_17'"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoria para uso de plataformas de desarrollo web.', name_short='s32', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_3_9'"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoramiento para la creacion e implementación de Página web personalizada.', name_short='s33', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_21'"},{"id": "_3_8"},{"id": "_3_9'"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoría para posicionar la empresa en Google.', name_short='s34', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_21'"},{"id": "_2_22"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoría en medios, pasarelas y botones de pagos.', name_short='s36', service_user_role=staff_it_role.id,diagnostic_questions=[])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoramiento en la generación de marca y línea gráfica.', name_short='s37', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_2'"},{"id": "_2_7"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoramiento en papeleria y productos promocionales bajo la guía de estilo', name_short='s38', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_4'"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Generación de contenido de valor empresarial para redes sociales', name_short='s39', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_19'"},{"id": "_2_22'"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoramiento en calendario de publicaciones para el contenido de valor en redes sociales', name_short='s40', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_22'"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=5,name='Asesoria en Herramientas básicas del diseño (aplicaciones)', name_short='s41', service_user_role=staff_it_role.id,diagnostic_questions=[])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(catalog_category=3,name='Elaboracion del Plan de inocuidad y seguridad industrial.', name_short='s42', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_5_5'"},{"id": "_5_7'"},{"id": "_5_8'"},{"id": "_5_13'"},{"id": "_5_14'"}])
    db.session.add(websites)
    db.session.commit()
    return render_template('404.html')

@digitalcenter.route('/insert/servicios/inciales',methods=['GET', 'POST'])
@login_required
def _re1_inicial():
    staff_it_role = CatalogUserRoles.query.filter_by(name_short='itc').first()
    websites = CatalogServices(name='Atención inicial', name_short='a1', service_user_role=staff_it_role.id,diagnostic_questions=[])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Diagnóstico Empresarial', name_short='a2', service_user_role=staff_it_role.id,diagnostic_questions=[])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Plan de acción', name_short='a3', service_user_role=staff_it_role.id,diagnostic_questions=[])
    db.session.add(websites)
    db.session.commit()
    return render_template('404.html')

@digitalcenter.route('/insert/catalogo/documentos',methods=['GET', 'POST'])
@login_required
def _re1_inicial_inicial():
    DOC1 = CatalogIDDocumentTypes(name='Ficha de inscripción', name_short='DOC1')
    db.session.add(DOC1)

    DOC2 = CatalogIDDocumentTypes(name='Carta de compromiso', name_short='DOC2')
    db.session.add(DOC2)
    db.session.commit()
    return render_template('404.html')



@digitalcenter.route('/insert/categias/',methods=['GET', 'POST'])
@login_required
def _re_categias():
    staff_it_role = CatalogUserRoles.query.filter_by(name_short='itc').first()
    websites = catalogCategory(name='LEGALIZACIÓN')
    db.session.add(websites)
    db.session.commit()
    websites = catalogCategory(name='ADMINISTRACIÓN')
    db.session.add(websites)
    db.session.commit()
    websites = catalogCategory(name='PRODUCCIÓN Y AMBIENTE')
    db.session.add(websites)
    db.session.commit()
    websites = catalogCategory(name='ANÁLISIS FINANCIERO')
    db.session.add(websites)
    db.session.commit()
    websites = catalogCategory(name='MERCADEO Y TICs')
    db.session.add(websites)
    db.session.commit()
    return render_template('404.html')


@digitalcenter.route('/demanda/',methods=['GET', 'POST'])
@login_required
def _datos_describe_12():
    servicios = []
    app.logger.debug('** SWING_CMS ** - ------------------')
    url = app.config.get('KOBOTOOLBOX_ALL')
    headers=app.config.get('KOBOTOOLBOX_TOKEN')
    resp = requests.get(url,headers=headers)
    api1 = json.loads(resp.content)
    api1['results'] = list(e for e in api1['results'] if e['_submitted_by']  in current_user.extra_info.kobotoolbox['kobotoolbox_access'] )
    for api in api1['results']:
        for resp in api:
            if api[resp] == '1':
                services = CatalogServices.query.filter(CatalogServices.diagnostic_questions.contains(resp)).all()
                if services:
                    for servicesx in services:
                        departamento =api['DEPARTAMENTO']
                        if departamento == '01':
                            name_de ='Atlantida'
                        elif departamento == '02':
                            name_de ='COLÓN'
                        elif departamento == '03':
                            name_de ='COMAYAGUA'
                        elif departamento == '04':
                            name_de ='COPÁN'
                        elif departamento == '05':
                            name_de ='CORTÉS'
                        elif departamento == '06':
                            name_de ='CHOLUTECA'
                        elif departamento == '07':
                            name_de ='EL PARAÍSO'
                        elif departamento == '08':
                            name_de ='FRANCISCO MORAZÁN'
                        elif departamento == '09':
                            name_de ='GRACIAS A DIOS'
                        elif departamento == '10':
                            name_de ='INTIBUCÁ'
                        elif departamento == '11':
                            name_de ='ISLAS DE LA BAHÍA'
                        elif departamento == '12':
                            name_de ='LA PAZ'
                        elif departamento == '13':
                            name_de ='LEMPIRA'
                        elif departamento == '14':
                            name_de ='OCOTEPEQUE'
                        elif departamento == '15':
                            name_de ='OLANCHO'
                        elif departamento == '16':
                            name_de ='SANTA BÁRBARA'
                        elif departamento == '17':
                            name_de ='VALLE'
                        elif departamento == '18':
                            name_de ='YORO'
                            
                        servi = str(servicesx.id) 
                        depart = []
                        if len(list(e for e in servicios if e['id']  == servi)) == 0:
                            depart.append({'name_de':name_de,'departamento':departamento,'total':1})
                            servicios.append({'id':servi,'titulo':servicesx.name,'departamentos':depart,'categoria':servicesx.catalog_category,'total':1,'anterior':api['_id']})
                        else:
                            varl = list(e for e in servicios if e['id']  == servi)[0]
                            index = servicios.index(varl)
                            
                            if servicios[index]['anterior'] != api['_id']:
                                if len(list(e for e in servicios[index]['departamentos'] if e['departamento']  == departamento))== 0:
                                    servicios[index]['departamentos'].append({'name_de':name_de,'departamento':departamento,'total':1})
                                else:
                                    dep = list(e for e in servicios[index]['departamentos'] if e['departamento']  == departamento)[0]
                                    index_departamento = servicios[index]['departamentos'].index(dep)
                                    servicios[index]['departamentos'][index_departamento]['total'] = servicios[index]['departamentos'][index_departamento]['total'] + 1 
                                servicios[index]['total'] = servicios[index]['total'] + 1
                                servicios[index]['anterior'] = api['_id']

                
    legalizacion = []
    administracion = []
    produccion = []
    financiera = []
    mercadeo = [] 
    for servicio in servicios:
        serviciox = servicio['categoria']
        if serviciox:
            if serviciox == 1:
                legalizacion.append(servicio)
            elif serviciox == 2:
                administracion.append(servicio)
                app.logger.debug(administracion)
            elif serviciox == 3:
                produccion.append(servicio)
            elif serviciox == 4:
                financiera.append(servicio)
            elif serviciox == 5:
                mercadeo.append(servicio)
        
    context = {
        'api': api,
        'legalizacion':legalizacion,
        'administracion':administracion,
        'produccion':produccion,
        'financiera':financiera,
        'mercadeo':mercadeo,

    }
   

    return render_template('datos_describe_2.html',**context)



@digitalcenter.route('/demanda/v1',methods=['GET', 'POST'])
@login_required
def _datos_describe_v1():

    servicios = []
    app.logger.debug('** SWING_CMS ** - ------------------')
    companys = Company.query.filter(Company.enabled==True).all()
    planes = 0
    lista = []
    for company in companys:
        print(company.id)
        #recorre todos los servicios de la fase 1.
        plans = ActionPlan.query.filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled==False).order_by(asc(ActionPlan.date_scheduled_start)).all()
        #plans = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).order_by(asc(ActionPlan.date_scheduled_start)).all()
        if plans:
            print('s')
            for plan in plans:
                servicesx = CatalogServices.query.filter(id==plan.services_id).first()
               
                if servicesx:
                                     
                    servi = str(servicesx.id) 
                    depart = []
                    if len(list(e for e in servicios if e['id']  == servi)) == 0:
        
                        servicios.append({'id':servi,'titulo':servicesx.name,'categoria':servicesx.catalog_category,'total':1,'anterior':company.id})
                    else:
                        varl = list(e for e in servicios if e['id']  == servi)[0]
                        index = servicios.index(varl)
                        if servicios[index]['anterior'] != company.id:
                            servicios[index]['total'] = servicios[index]['total'] + 1
                            servicios[index]['anterior'] = company.id

                
    legalizacion = []
    administracion = []
    produccion = []
    financiera = []
    mercadeo = [] 
    for servicio in servicios:
        print(servicio)
        print('servicio')
        print('s')
        serviciox = servicio['categoria']
        if serviciox:
            if serviciox == 1:
                legalizacion.append(servicio)
            elif serviciox == 2:
                administracion.append(servicio)
                app.logger.debug(administracion)
            elif serviciox == 3:
                produccion.append(servicio)
            elif serviciox == 4:
                financiera.append(servicio)
            elif serviciox == 5:
                mercadeo.append(servicio)
        
    context = {
        'api': companys,
        'legalizacion':legalizacion,
        'administracion':administracion,
        'produccion':produccion,
        'financiera':financiera,
        'mercadeo':mercadeo,

    }
   

    return render_template('datos_describe_3.html',**context)




@digitalcenter.route('/registros/im',methods=['GET', 'POST'])
def _registros_im():
    return render_template('registro_im.html')

@digitalcenter.route('/diagnostico/<int:user_uid>/',methods=['GET', 'POST'])
@login_required
def _diagnosis_dashboard(user_uid):
    app.logger.debug('** SWING_CMSx ** - ------------------')
    url = app.config.get('KOBOTOOLBOX_VIEW').format(user_uid)
    headers=  app.config.get('KOBOTOOLBOX_TOKEN')
    resp = requests.get(url,headers=headers)
    api = json.loads(resp.content)
    diagnostico = Diagnosticos()
    resultados  = diagnostico.calcular_area(api)
    company =  Company.query.filter(Company.dni == api['IDENTIDAD']).first()
    if company:
        diagnosis =  DiagnosisCompany.query.filter(DiagnosisCompany.company_id == company.id).first()
    else:
        diagnosis = None
    context = {
        "api":api,
        "diagnostico":resultados,
        "user_uid":user_uid,
        "company":company,
        "diagnosis":diagnosis,
    }
    return render_template('diagnosis_dashboard.html',**context)

@digitalcenter.route('/diagnosticos/view/<int:diagnosis_id>',methods=['GET', 'POST'])
@login_required
def _diagnosis_view_dashboard(diagnosis_id):
    app.logger.debug('** SWING_CMSx ** - ------------------')
    diagnosis = DiagnosisCompany.query.filter(DiagnosisCompany.id == diagnosis_id).first()
    company =  Company.query.filter(Company.id == diagnosis.company_id).first()

    context = {
        "api":"api",
        "diagnostico":diagnosis.resultados,
        "user_uid":"user_uid",
        "company":company,
        "diagnosis":diagnosis,
    }
    return render_template('diagnosis_dashboard.html',**context)

@digitalcenter.route('/elegibles/5',methods=['GET', 'POST'])
@login_required
def _registro_elegibles_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    inscripciones = Inscripciones.query.filter_by(elegible = True,cohorte=5).filter(or_(Inscripciones.status != 0, Inscripciones.status == None)).all()
    context = {
        'api': inscripciones
    }
    return render_template('digitalcenter/registro_elegibles_list.html',**context)

@digitalcenter.route('/view/si/5/<int:inscribe_id>',methods=['GET', 'POST'])
@login_required
def _registro_elegibles_panel(inscribe_id):
    app.logger.debug('** SWING_CMS ** - ------------------')
    inscripciones = Inscripciones.query.filter_by(id = inscribe_id).first()
    context = {
        'api': inscripciones
    }
    return render_template('digitalcenter/registro_elegibles_panel.html',**context)

@digitalcenter.route('/elegibles/no/5',methods=['GET', 'POST'])
@login_required
def _registro_no_elegibles_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    inscripciones = Inscripciones.query.filter_by(elegible = False,cohorte=5).filter(or_(Inscripciones.status != 0, Inscripciones.status == None)).all()
    context = {
        'api': inscripciones
    }
    return render_template('digitalcenter/registro_no_elegibles_list.html',**context)

@digitalcenter.route('/view/no/5/<int:inscribe_id>',methods=['GET', 'POST'])
@login_required
def _registro_no_eleibles_panel(inscribe_id):
    app.logger.debug('** SWING_CMS ** - ------------------')
    inscripciones = Inscripciones.query.filter_by(id = inscribe_id).first()
    context = {
        'api': inscripciones
    }
    return render_template('digitalcenter/registro_no_elegibles_panel.html',**context)




from sqlalchemy import desc,asc
@digitalcenter.route('/empresas/view/<int:user_uid>/',methods=['GET', 'POST'])
@login_required
def _plan_action_dashboard(user_uid):
    app.logger.debug('** SWING_CMSx ** - ------------------')

    company = Company.query.filter_by(id=user_uid).first()
    diagnos = DiagnosisCompany.query.filter_by(company_id=company.id,status=True).order_by(desc(DiagnosisCompany.date_created)).first()
    
    actions = ActionPlan.query.filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).all()
    actions_asesorias = ActionPlan.query.filter(ActionPlan.company_id==company.id,ActionPlan.espuntal==True).all()
    if diagnos:
        diagnostico = diagnos.resultados
    else:
        diagnostico = False
    users = User.query.join(UserXRole, User.id==UserXRole.user_id).filter(or_(UserXRole.user_role_id == 3, UserXRole.user_role_id == 4)).\
            filter(not_(User.id.in_([152, 144]))).all()
    context = {
        'users':users,
        'company': company,
        'actions':actions,
        "diagnostico":diagnostico,
        "actions_asesorias":actions_asesorias
    }
 
    return render_template('plan_action_dashboard.html',**context)
from functools import wraps
from flask import make_response
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache
@digitalcenter.route('/empresas/',methods=['GET', 'POST'])
@login_required
@nocache
def _company_monitoring_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    #diagnosis = DiagnosisCompany.query.filter_by(created_by=current_user.id)
    lista = []
    data = []
    categories = db.session.query(catalogCategory).all()
    #for diagnosi in diagnosis:
    #    lista.append(diagnosi.company_id)
    if current_user.id == 3 or current_user.id == 24 or current_user.id == 144 :


        # Consultar empresas que cumplan con las condiciones
        if current_user.id == 1445555:
            company = Company.query.join(User, User.id==Company.created_by)\
                .filter(Company.enabled==True,Company.status.has(CompanyStatus.name_short.in_([6])),Company.stage.has(CompanyStage.name_short.in_(['E2'])),)\
                .order_by(asc(Company.date_created))\
                .all()
            allowed_status_short_names = [1, 2, 3, 6]
            # Definir un alias para la relación con ActionPlan
            action_plan_alias = aliased(ActionPlan)
            companies = db.session.query(Company)\
                .filter(
                    Company.enabled == True,
                    Company.status.has(CompanyStatus.name_short.in_([6])),
                    Company.stage.has(CompanyStage.name_short.in_(['E2'])),
                    Company.action_plan_progress != None  # Agregar condición para action_plan_progress
                )\
                .join(action_plan_alias, action_plan_alias.company_id == Company.id)\
                .filter(action_plan_alias.fase == 1)\
                .distinct()\
                .all()
            data = []
        else:
            company = Company.query.join(User, User.id==Company.created_by)\
                .filter(Company.enabled==True)\
                .order_by(asc(Company.date_created))\
                .all()
            for company_data in company:
                actions = ActionPlan.query.filter(ActionPlan.company_id==company_data.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).all()
                if company_data.action_plan_progress is not None and actions:
                # Calcula la categoría según el valor de action_plan_progress
                    
                    if company_data.action_plan_progress :
                        category_start = int(company_data.action_plan_progress // 20) * 20
                        category_p = f"{category_start} de {category_start + 20}" if category_start < 100 else "80 de 100"
                    else:
                        category_p = "0 de 20"
                else:
                    category_p = "No tiene plan de acción"
                company_data.category_progress = category_p
            allowed_status_short_names = [1, 2, 3, 6]
            # Definir un alias para la relación con ActionPlan
            action_plan_alias = aliased(ActionPlan)
            companies = db.session.query(Company)\
                .filter(
                    Company.enabled == True,
                    Company.status.has(CompanyStatus.name_short.in_(allowed_status_short_names)),
                    Company.action_plan_progress != None  # Agregar condición para action_plan_progress
                )\
                .join(action_plan_alias, action_plan_alias.company_id == Company.id)\
                .filter(action_plan_alias.fase == 1)\
                .distinct()\
                .all()
            data = []
    



        for company_data in companies:  # Cambio el nombre de la variable a company_data
            if company_data.created_by_data:
                asignada = company_data.created_by_data.name
            else:
                asignada = ''
            if company_data.inscripcion:
                name = company_data.inscripcion.name
            else:
                name = ''
            company_info = {
                'company_id': company_data.id,  # Cambiado de company.id a company_data.id
                'company_name': company_data.name,  # Cambiado de company.name a company_data.name
                'date_action_plan': company_data.date_action_plan,
                'action_plan_progress': company_data.action_plan_progress,
                'days_since_action_plan': None,  # Inicialmente se establece en None
                'categories': {},
                'asignada':asignada,
                'name':name
                
            }

            if company_data.date_action_plan:
                # Calcular los días transcurridos desde date_action_plan hasta la fecha actual
                current_date = datetime.now()
                days_since_action_plan = (current_date - company_data.date_action_plan).days
                company_info['days_since_action_plan'] = days_since_action_plan

            for category in categories:
                action_plans = ActionPlan.query\
                    .filter(ActionPlan.company_id == company_data.id, ActionPlan.cancelled != True, ActionPlan.fase == 1)\
                    .join(CatalogServices, ActionPlan.services_id == CatalogServices.id)\
                    .filter(CatalogServices.catalog_category == category.id)\
                    .all()

                category_action_plans = []
                for action_plan in action_plans:
                    category_action_plans.append({
                        'action_plan_id': action_plan.id,
                        'description': action_plan.descripcion,
                        'progress': action_plan.progress,
                        'service_name': action_plan.services.name,
                        'service_name_short': action_plan.services.name_short
                    })

                company_info['categories'][category.name] = category_action_plans

            data.append(company_info)
    else:
        company = Company.query.join(User, User.id==Company.created_by).filter(Company.enabled==True, or_(Company.created_by == current_user.id,Company.id.in_(lista))).order_by(asc(Company.date_created)).all()
        for company_data in company:
            if company_data.action_plan_progress is not None:
            # Calcula la categoría según el valor de action_plan_progress
                actions = ActionPlan.query.filter(ActionPlan.company_id==company_data.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).all()
                if company_data.action_plan_progress and actions:

                    category_start = int(company_data.action_plan_progress // 20) * 20
                    category_p = f"{category_start} de {category_start + 20}" if category_start < 100 else "80 de 100"
                else:
                    category_p = "0 de 20"
            else:
                category_p = "No tiene plan de acción"
            company_data.category_progress = category_p
        allowed_status_short_names = [1, 2, 3, 6]
        # Definir un alias para la relación con ActionPlan
        action_plan_alias = aliased(ActionPlan)

        # Consultar empresas que cumplan con las condiciones
        companies = db.session.query(Company)\
            .filter(
                
                Company.enabled == True,
                or_(Company.created_by == current_user.id,Company.id.in_(lista)),
                Company.status.has(CompanyStatus.name_short.in_(allowed_status_short_names)),
                Company.action_plan_progress != None  # Agregar condición para action_plan_progress
            )\
            .join(action_plan_alias, action_plan_alias.company_id == Company.id)\
            .join(User, User.id==Company.created_by)\
            .filter(action_plan_alias.fase == 1)\
            .distinct()\
            .all()
        data = []
            

        # Obtener todas las categorías
        categories = db.session.query(catalogCategory).all()

        for company_data in companies:  # Cambio el nombre de la variable a company_data
            if company_data.created_by_data:
                asignada = company_data.created_by_data.name
            else:
                asignada = ''
            if company_data.inscripcion:
                name = company_data.inscripcion.name
            else:
                name = ''
            company_info = {
                'company_id': company_data.id,  # Cambiado de company.id a company_data.id
                'company_name': company_data.name,  # Cambiado de company.name a company_data.name
                'date_action_plan': company_data.date_action_plan,
                'action_plan_progress': company_data.action_plan_progress,
                'days_since_action_plan': None,  # Inicialmente se establece en None
                'categories': {},
                'asignada':asignada,
                'name':name
                
            }

            if company_data.date_action_plan:
                # Calcular los días transcurridos desde date_action_plan hasta la fecha actual
                current_date = datetime.now()
                days_since_action_plan = (current_date - company_data.date_action_plan).days
                company_info['days_since_action_plan'] = days_since_action_plan

            for category in categories:
                action_plans = ActionPlan.query\
                    .filter(ActionPlan.company_id == company_data.id, ActionPlan.cancelled != True, ActionPlan.fase == 1)\
                    .join(CatalogServices, ActionPlan.services_id == CatalogServices.id)\
                    .filter(CatalogServices.catalog_category == category.id)\
                    .all()

                category_action_plans = []
                for action_plan in action_plans:
                    category_action_plans.append({
                        'action_plan_id': action_plan.id,
                        'description': action_plan.descripcion,
                        'progress': action_plan.progress,
                        'service_name': action_plan.services.name,
                        'service_name_short': action_plan.services.name_short
                    })

                company_info['categories'][category.name] = category_action_plans

            data.append(company_info)  
    references = ActionPlanReferences.query.filter_by(employe_assigned=current_user.id).order_by(desc(ActionPlanReferences.id)).all()
    lista = []
    for reference in references:
        lista.append(reference.action_plan.company.id)
    company_references = Company.query.filter(Company.id.in_(lista)).all()
    context = {
        'apis': company,
        'company_references':company_references,
        'data':data,
        'categories':categories,
    }
    return render_template('company_monitoring_list.html',**context)


@digitalcenter.route('/empresas/proceso',methods=['GET', 'POST'])
@login_required
def _company_monitoring_proceso_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    #diagnosis = DiagnosisCompany.query.filter_by(created_by=current_user.id)
    lista = []
    data = []
    categories = db.session.query(catalogCategory).all()
    #for diagnosi in diagnosis:
    #    lista.append(diagnosi.company_id)
    allowed_status_short_names = [1, 2]
    if current_user.id == 3 or current_user.id == 24 or current_user.id == 144 :

        allowed_status_short_names = [1, 2]
        # Consultar empresas que cumplan con las condiciones
        if current_user.id == 1445555:
            company = Company.query.join(User, User.id==Company.created_by)\
                .filter(Company.enabled==True,Company.status.has(CompanyStatus.name_short.in_([6])),Company.stage.has(CompanyStage.name_short.in_(['E2'])),)\
                .filter(
                    Company.status.has(CompanyStatus.name_short.in_(allowed_status_short_names)),
                )\
                .order_by(asc(Company.date_created))\
                .all()
            allowed_status_short_names = [1, 2]
            # Definir un alias para la relación con ActionPlan
            action_plan_alias = aliased(ActionPlan)
            companies = db.session.query(Company)\
                .filter(
                    Company.enabled == True,
                    Company.status.has(CompanyStatus.name_short.in_([6])),
                    Company.stage.has(CompanyStage.name_short.in_(['E2'])),
                    Company.action_plan_progress != None  # Agregar condición para action_plan_progress
                )\
                .join(action_plan_alias, action_plan_alias.company_id == Company.id)\
                .filter(action_plan_alias.fase == 1)\
                .distinct()\
                .all()
            data = []
        else:
            company = Company.query.join(User, User.id==Company.created_by)\
                .filter(Company.enabled==True)\
                .filter(
                    Company.status.has(CompanyStatus.name_short.in_(allowed_status_short_names)),
                )\
                .order_by(asc(Company.date_created))\
                .all()
            allowed_status_short_names = [1, 2]
            # Definir un alias para la relación con ActionPlan
            action_plan_alias = aliased(ActionPlan)
            companies = db.session.query(Company)\
                .filter(
                    Company.enabled == True,
                    Company.status.has(CompanyStatus.name_short.in_(allowed_status_short_names)),
                    Company.action_plan_progress != None  # Agregar condición para action_plan_progress
                )\
                .join(action_plan_alias, action_plan_alias.company_id == Company.id)\
                .filter(action_plan_alias.fase == 1)\
                .distinct()\
                .all()
            data = []
    



        for company_data in companies:  # Cambio el nombre de la variable a company_data
            if company_data.created_by_data:
                asignada = company_data.created_by_data.name
            else:
                asignada = ''
            if company_data.inscripcion:
                name = company_data.inscripcion.name
            else:
                name = ''
            company_info = {
                'company_id': company_data.id,  # Cambiado de company.id a company_data.id
                'company_name': company_data.name,  # Cambiado de company.name a company_data.name
                'date_action_plan': company_data.date_action_plan,
                'action_plan_progress': company_data.action_plan_progress,
                'days_since_action_plan': None,  # Inicialmente se establece en None
                'categories': {},
                'asignada':asignada,
                'name':name
                
            }

            if company_data.date_action_plan:
                # Calcular los días transcurridos desde date_action_plan hasta la fecha actual
                current_date = datetime.now()
                days_since_action_plan = (current_date - company_data.date_action_plan).days
                company_info['days_since_action_plan'] = days_since_action_plan

            for category in categories:
                action_plans = ActionPlan.query\
                    .filter(ActionPlan.company_id == company_data.id, ActionPlan.cancelled != True, ActionPlan.fase == 1)\
                    .join(CatalogServices, ActionPlan.services_id == CatalogServices.id)\
                    .filter(CatalogServices.catalog_category == category.id)\
                    .all()

                category_action_plans = []
                for action_plan in action_plans:
                    category_action_plans.append({
                        'action_plan_id': action_plan.id,
                        'description': action_plan.descripcion,
                        'progress': action_plan.progress,
                        'service_name': action_plan.services.name,
                        'service_name_short': action_plan.services.name_short
                    })

                company_info['categories'][category.name] = category_action_plans

            data.append(company_info)
    else:
        company = Company.query.join(User, User.id==Company.created_by).filter(Company.enabled==True, or_(Company.created_by == current_user.id,Company.id.in_(lista))).order_by(asc(Company.date_created)).all()
        allowed_status_short_names = [1, 2, 3, 6]
        # Definir un alias para la relación con ActionPlan
        action_plan_alias = aliased(ActionPlan)

        # Consultar empresas que cumplan con las condiciones
        companies = db.session.query(Company)\
            .filter(
                
                Company.enabled == True,
                or_(Company.created_by == current_user.id,Company.id.in_(lista)),
                Company.status.has(CompanyStatus.name_short.in_(allowed_status_short_names)),
                Company.action_plan_progress != None  # Agregar condición para action_plan_progress
            )\
            .join(action_plan_alias, action_plan_alias.company_id == Company.id)\
            .join(User, User.id==Company.created_by)\
            .filter(action_plan_alias.fase == 1)\
            .distinct()\
            .all()
        data = []
            

        # Obtener todas las categorías
        categories = db.session.query(catalogCategory).all()

        for company_data in companies:  # Cambio el nombre de la variable a company_data
            if company_data.created_by_data:
                asignada = company_data.created_by_data.name
            else:
                asignada = ''
            if company_data.inscripcion:
                name = company_data.inscripcion.name
            else:
                name = ''
            company_info = {
                'company_id': company_data.id,  # Cambiado de company.id a company_data.id
                'company_name': company_data.name,  # Cambiado de company.name a company_data.name
                'date_action_plan': company_data.date_action_plan,
                'action_plan_progress': company_data.action_plan_progress,
                'days_since_action_plan': None,  # Inicialmente se establece en None
                'categories': {},
                'asignada':asignada,
                'name':name
                
            }

            if company_data.date_action_plan:
                # Calcular los días transcurridos desde date_action_plan hasta la fecha actual
                current_date = datetime.now()
                days_since_action_plan = (current_date - company_data.date_action_plan).days
                company_info['days_since_action_plan'] = days_since_action_plan

            for category in categories:
                action_plans = ActionPlan.query\
                    .filter(ActionPlan.company_id == company_data.id, ActionPlan.cancelled != True, ActionPlan.fase == 1)\
                    .join(CatalogServices, ActionPlan.services_id == CatalogServices.id)\
                    .filter(CatalogServices.catalog_category == category.id)\
                    .all()

                category_action_plans = []
                for action_plan in action_plans:
                    category_action_plans.append({
                        'action_plan_id': action_plan.id,
                        'description': action_plan.descripcion,
                        'progress': action_plan.progress,
                        'service_name': action_plan.services.name,
                        'service_name_short': action_plan.services.name_short
                    })

                company_info['categories'][category.name] = category_action_plans

            data.append(company_info)  
    references = ActionPlanReferences.query.filter_by(employe_assigned=current_user.id).order_by(desc(ActionPlanReferences.id)).all()
    lista = []
    for reference in references:
        lista.append(reference.action_plan.company.id)
    company_references = Company.query.filter(Company.id.in_(lista)).all()
    context = {
        'apis': company,
        'company_references':company_references,
        'data':data,
        'categories':categories,
    }
    return render_template('company_monitoring_list.html',**context)


@digitalcenter.route('/empresas/dn',methods=['GET', 'POST'])
@login_required
def _company_monitoring_list_id():
    app.logger.debug('** SWING_CMS ** - ------------------')
    #diagnosis = DiagnosisCompany.query.filter_by(created_by=current_user.id)
    lista = []
    #for diagnosi in diagnosis:
    #    lista.append(diagnosi.company_id)
    if current_user.id == 3 or current_user.id == 24:
        company = Company.query.join(User, User.id==Company.created_by)\
            .filter(Company.enabled==True).all()
   
    else:
        company = Company.query.join(User, User.id==Company.created_by).filter(Company.enabled==True, or_(Company.created_by == current_user.id,Company.id.in_(lista))).all()
    references = ActionPlanReferences.query.filter_by(employe_assigned=current_user.id).order_by(desc(ActionPlanReferences.id)).all()
    lista = []
    for reference in references:
        lista.append(reference.action_plan.company.id)
    company_references = Company.query.filter(Company.id.in_(lista)).all()
    context = {
        'apis': company,
        'company_references':company_references
    }
    return render_template('company_monitoring_list_id.html',**context)

@digitalcenter.route('/company/view/<int:user_uid>/',methods=['GET', 'POST'])
@login_required
def _company_dashboard(user_uid):
    app.logger.debug('** _company_dashboard ** - ------------------')

    company = Company.query.filter_by(id=user_uid).first()
    

    #buscamos la carta de compromiso DOC2
    carta = CatalogIDDocumentTypes.query.filter_by(name_short='DOC2').first()
    carta = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=carta.id,enabled=True).order_by(DocumentCompany.id.desc()).first()
    #buscamos la ficha de inscripcion DOC1
    ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
    ficha =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id,enabled=True).order_by(DocumentCompany.id.desc()).first()
    diagnos = DiagnosisCompany.query.filter_by(company_id=company.id,status=True).order_by(asc(DiagnosisCompany.date_created)).first()

    if diagnos:
        diagnostico = diagnos.resultados
    else:
        diagnostico = False
    enrolls = EnrollmentRecord.query.filter_by(company_id=company.id).all()
    satisfaccion = False
    impacto = False
    if company.action_plan_progress == 100:
        encuesta = surveys_sde.query.filter_by(company_id=company.id,catalog_surveys_id=1).first()
        if not encuesta:
            satisfaccion = True
        encuesta = surveys_sde.query.filter_by(company_id=company.id,catalog_surveys_id=2).first()
        if not encuesta:
            impacto = True
    actions = ActionPlan.query.filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).all()
    actions_asesorias = ActionPlan.query.filter(ActionPlan.company_id==company.id,ActionPlan.espuntal==True).all()
    if diagnos:
        diagnostico = diagnos.resultados
    else:
        diagnostico = False
    users = User.query.join(UserXRole, User.id==UserXRole.user_id).filter(or_(UserXRole.user_role_id == 3, UserXRole.user_role_id == 4)).\
            filter(not_(User.id.in_([152, 144]))).all()
    # Lista de identificadores cortos de tipo de documento
    document_type_ids = [1, 2, 3, 4]

    # Consulta para obtener los DocumentCompany que coinciden con los criterios
    documents = DocumentCompany.query.join(CatalogIDDocumentTypes).filter(
        DocumentCompany.company_id == company.id,
        CatalogIDDocumentTypes.name_short.in_(document_type_ids),
        DocumentCompany.enabled == True
    ).order_by(CatalogIDDocumentTypes.name_short.asc()).all()
    context = {
        'enrolls':enrolls,
        'carta':carta,
        'ficha':ficha,
        'company': company,
        'actions':actions,
        "diagnostico":diagnostico,
        "diagnos":diagnos,
        "satisfaccion":satisfaccion,
        "impacto":impacto,
        "actions_asesorias":actions_asesorias,
        "users":users,
        "documents":documents

    }
 
    return render_template('company_dashboard.html',**context)

@digitalcenter.route('/company/reference/view/<int:user_uid>/',methods=['GET', 'POST'])
@login_required
def _company_dashboard_action_plan_references(user_uid):
    app.logger.debug('** _company_dashboard_action_plan_references ** - ------------------')

    company = Company.query.filter_by(id=user_uid).first()
    #buscamos la carta de compromiso DOC2
    carta = CatalogIDDocumentTypes.query.filter_by(name_short='DOC2').first()
    carta = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=carta.id,enabled=True).first()
    #buscamos la ficha de inscripcion DOC1
    ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
    ficha =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id).first()
    diagnos = DiagnosisCompany.query.filter_by(company_id=company.id,status=True).order_by(desc(DiagnosisCompany.date_created)).first()
    actions = ActionPlan.query.filter_by(company_id=company.id).all()
    if diagnos:
        diagnostico = diagnos.resultados
    else:
        diagnostico = False
    references = ActionPlanReferences.query.join(ActionPlan, ActionPlan.id==ActionPlanReferences.action_plan_id).filter(ActionPlanReferences.employe_assigned==current_user.id,ActionPlan.company_id==company.id).order_by(desc(ActionPlanReferences.id)).all()

    context = {
        'carta':carta,
        'ficha':ficha,
        'company': company,
        'actions':actions,
        "diagnostico":diagnostico,
        "references":references
    }
 
    return render_template('company_dashboard_action_plan_references.html',**context)

@digitalcenter.route('/empresas/resumen/<int:user_uid>/',methods=['GET', 'POST'])
@login_required
def _plan_action_bitacora(user_uid):
    action = ActionPlan.query.filter_by(id=user_uid).first()
    history = ActionPlanHistory.query.filter_by(action_plan_id=action.id)
    lista = ['MT1','MT2']
    modalidad = ModalityType.query.filter(ModalityType.name_short.in_(lista)).all()

    context = {
        'action': action,
        'history':history,
        'modalidad':modalidad
    }
    return render_template('plan_action_bitacora.html',**context)


@digitalcenter.route('/empresas/resumen/update/<int:user_uid>/',methods=['GET', 'POST'])
@login_required
def _plan_action_bitacora_update(user_uid):
    action = ActionPlanHistory.query.filter_by(id=user_uid).first()
    lista = ['MT1','MT2']
    modalidad = ModalityType.query.filter(ModalityType.name_short.in_(lista)).all()
    context = {
        'action': action,
        'modalidad':modalidad,
       
    }
    return render_template('plan_action_bitacora_update.html',**context)


@digitalcenter.route('/empresas/resumen/bitecora/<int:user_uid>/',methods=['GET', 'POST'])
@login_required
def _plan_action_bitacora_atenciones(user_uid):
    history = ActionPlanHistory.query.filter_by(id=user_uid).first()
    context = {
        'history': history,
  
    }
    return render_template('plan_action_bitacora_atenciones.html',**context)


@digitalcenter.route('/empresas/view/user/<int:company_id>/',methods=['GET', 'POST'])
@login_required
def _company_user_list(company_id):
    app.logger.debug('** SWING_CMSx ** - ------------------')
    company = Company.query.filter_by(id=company_id).first()

    inscripciones =  Inscripciones.query.filter_by(id=company.inscripcion_id).all()

    users = User.query.join(UserExtraInfo, User.id==UserExtraInfo.id).filter(UserExtraInfo.company_id == company.id).all()
    
    context = {
        'users': users,
        'company':company,
        'inscripciones':inscripciones
    }
    return render_template('company_user_list.html',**context)


@digitalcenter.route('/save/carta/innova',methods = ['GET', 'POST'])
@login_required
def _form_carta_innova():
    if request.method == 'POST':
        txt_company_id = request.form['txt_company_id']
        txt_documente_id = request.form['txt_documente_id']
        txt_documente_version = request.form['txt_document_version']
        company = Company.query.filter_by(id=txt_company_id).first()
        document_type = CatalogIDDocumentTypes.query.filter_by(name_short=txt_documente_id).first()
        if txt_documente_version == "0":
            # check if the post request has the file part
            if 'upload-carta' not in request.files:
                return redirect(url_for('digitalcenter._company_dashboard',user_uid=company.id))
            file = request.files['upload-carta']
            #buscamos el tipo de documento
            carta = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=document_type.id,enabled = True).first()
            if not carta:
                # empty file without a filename.
                if file.filename == '':
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    documentoName = str(company.dni) + ' ' + str(document_type.name) 
                    filename =  documentoName.replace(" ", "_") +'.'+ filename.rsplit('.', 1)[1].lower()
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    carta = DocumentCompany()
                    carta.company_id = company.id
                    carta.documente_type_id = document_type.id
                    carta.complete = True
                    carta.signed = True
                    carta.signed_innova = True
                    carta.enabled = True
                    carta.document_local = filename
                    carta.created_by = current_user.id
                    db.session.add(carta)
                    if document_type.name_short == 'DOC1':
                        status  =   CompanyStatus.query.filter(CompanyStatus.name_short == 3).first()
                        company.status_id = status.id
                        db.session.add(company)
                    db.session.commit()
            return redirect(url_for('digitalcenter._company_dashboard',user_uid=company.id))
        elif txt_documente_version == "1" or txt_documente_version == "2":
            # check if the post request has the file part
            if 'upload-carta' not in request.files:
                return redirect(url_for('digitalcenter._company_dashboard',user_uid=company.id))
            file = request.files['upload-carta']
            #buscamos el tipo de documento
            carta = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=document_type.id,enabled = True).first()
            if carta:
                carta.enabled = False
                db.session.add(carta)   
                db.session.commit()
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                documentoName = str(company.dni) + ' ' + str(document_type.name)  + str(txt_documente_version)
                filename =  documentoName.replace(" ", "_") +'.'+ filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                carta = DocumentCompany()
                carta.company_id = company.id
                carta.documente_type_id = document_type.id
                carta.complete = True
                if txt_documente_version == "2":
                    carta.signed = True
                else:
                    carta.signed = True
                carta.signed_innova = True
                carta.enabled = True
                carta.document_local = filename
                carta.created_by = current_user.id
                if document_type.name_short == 'DOC1':
                    status  =   CompanyStatus.query.filter(CompanyStatus.name_short == 3).first()
                    company.status_id = status.id
                    db.session.add(company)
                db.session.add(carta)
                db.session.commit()
            if txt_documente_version == "2":
                return redirect(url_for('home._home'))
            else:
                return redirect(url_for('digitalcenter._company_dashboard',user_uid=company.id))
 
        print(current_user.id)
        return redirect(url_for('digitalcenter._home_view'))
    if request.method == 'GET':
        return redirect(url_for('digitalcenter._home_view'))


@digitalcenter.route('/formulario/documentos/<int:document_id>/inno',methods = ['GET', 'POST'])
@login_required
def _company_document_form(document_id):
    document = DocumentCompany.query.filter_by(id=document_id).first()
    context = {
        "document": document
    }
    return render_template('company_document_form.html',**context)

@digitalcenter.route('/formulario/documentos/<int:company_id>/add/<int:document_id>/',methods = ['GET', 'POST'])
@login_required
def _company_document_form_add(company_id,document_id):
    company = Company.query.filter_by(id=company_id).first()
    document_type = CatalogIDDocumentTypes.query.filter_by(id=document_id).first()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'upload-carta' not in request.files:
            return redirect(url_for('digitalcenter._company_document_form_add',company_id=company.id,document_id=document_type.id))
        
        file = request.files['upload-carta']
        #buscamos el tipo de documento
        document = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=document_type.id,enabled = True).first()
        n = 1
        if document:
            document.enabled = False
            n = document.id
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            documentoName = str(company.dni) + ' ' + str(document_type.name) + '-' + str(n)
            filename =  documentoName.replace(" ", "_") +'.'+ filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            carta = DocumentCompany()
            carta.company_id = company.id
            carta.documente_type_id = document_type.id
            carta.complete = True
            carta.signed = True
            carta.signed_innova = True
            carta.enabled = True
            carta.document_local = filename
            carta.created_by = current_user.id
            db.session.add(carta)

            if document_type.name_short == 'DOC1':
                update =  Company.query.filter(Company.id == company.id).first()
                status = CompanyStatus.query.filter_by(name_short='3').first()
                update.status_id = status.id
                db.session.add(update)
                db.session.commit()
            db.session.commit()
            return redirect(url_for('digitalcenter._company_dashboard',user_uid=company.id))

    context = {
        "company": company,
        "document_type":document_type
    }
    return render_template('company_document_form_add.html',**context)


@digitalcenter.route('/formulario/documentos/user/<int:document_id>/inno',methods = ['GET', 'POST'])
@login_required
def _company_document_user(document_id):
    document = DocumentCompany.query.filter_by(id=document_id).first()
    context = {
        "document": document
    }
    return render_template('company_document_user.html',**context)

@digitalcenter.route('/registros/inno/',methods = ['GET', 'POST'])
@login_required
def _registro_api_dashboard():
    return render_template('digitalcenter/registro_api_dashboard.html')



@digitalcenter.route('/diagnostico/update',methods=['GET', 'POST'])
@login_required
def _diagnosis_monitoring_1s_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    try:
        url = app.config.get('KOBOTOOLBOX_ALL')
        headers=app.config.get('KOBOTOOLBOX_TOKEN')
        resp = requests.get(url,headers=headers)
        api = json.loads(resp.content)
        user = User.query.filter(User.id == current_user.id).first()
        api['results'] = list(e for e in api['results'] if e['_submitted_by']  in user.extra_info.kobotoolbox['kobotoolbox_access'] )
        for diagnostico in api['results']:
            fecha_string = diagnostico['_submission_time']
            identidad = diagnostico['IDENTIDAD'].replace('-','')
            company =  Company.query.filter(Company.dni == identidad).first()
            fecha_datetime = convertir_a_datetime(fecha_string)
            if company:
                diagnos = DiagnosisCompany.query.filter_by(company_id=company.id).order_by(asc(DiagnosisCompany.date_created)).first()
                if diagnos:
                    if fecha_datetime:
                        diagnos.date_created = fecha_datetime
                        db.session.add(diagnos)
                        db.session.commit()
                        print("Fecha convertida:", fecha_datetime)
                    else:
                        print("Error: El formato del string es incorrecto.")
        context = {
            'api': api
        }
        return render_template('diagnosis_monitoring_list.html',**context)
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Try Chat Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


from datetime import datetime

def convertir_a_datetime(fecha_string):
    try:
        # Utilizamos strptime para analizar el string y obtener un objeto datetime
        fecha_datetime = datetime.strptime(fecha_string, "%Y-%m-%dT%H:%M:%S")
        return fecha_datetime
    except ValueError:
        # Si el formato del string no coincide con el esperado, manejar el error aquí
        return None
    

@digitalcenter.route('/update/l/1',methods=['GET', 'POST'])
@login_required
def _init1_status_company():
    companys = Company.query.filter_by(enabled=True).all()[0:200]
    for company in companys:
        update =  Company.query.filter(Company.id == company.id).first()

        if company.inscripcion:
            #buscamos el servicio de atencion inicial al plan de mejora como primer servicio de empresa
            service = CatalogServices.query.filter_by(name_short = 'a1').first()
            actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service.id,fase=0).first()
            if not actionplan:
                fecha = company.inscripcion.date_created
            else:
                if actionplan.date_created:
                    fecha = actionplan.date_created
                else:
                    fecha = company.inscripcion.date_created

            documento =  DocumentCompany.query.filter_by(company_id=company.id).order_by(asc(DocumentCompany.date_created)).first()
            if documento:
                fecha_documento = documento.date_created
                if fecha_documento:
                    if fecha > fecha_documento:
                        fecha = fecha_documento
            diagnostico = DiagnosisCompany.query.filter_by(company_id=company.id).order_by(asc(DiagnosisCompany.date_created)).first()
            if diagnostico:
                fecha_diagnostico = diagnostico.date_created
                if fecha_diagnostico:
                    if fecha > fecha_diagnostico:
                        fecha = fecha_diagnostico
            company.date_created =fecha
            db.session.add(update)
            db.session.commit()
    return 'listo'

@digitalcenter.route('/update/l/2',methods=['GET', 'POST'])
@login_required
def _init2_status_company():
    companys = Company.query.filter_by(enabled=True).all()[200:400]
    for company in companys:
        update =  Company.query.filter(Company.id == company.id).first()

        if company.inscripcion:
            #buscamos el servicio de atencion inicial al plan de mejora como primer servicio de empresa
            service = CatalogServices.query.filter_by(name_short = 'a1').first()
            actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service.id,fase=0).first()
            if not actionplan:
                fecha = company.inscripcion.date_created
            else:
                if actionplan.date_created:
                    fecha = actionplan.date_created
                else:
                    fecha = company.inscripcion.date_created

            documento =  DocumentCompany.query.filter_by(company_id=company.id).order_by(asc(DocumentCompany.date_created)).first()
            if documento:
                fecha_documento = documento.date_created
                if fecha_documento:
                    if fecha > fecha_documento:
                        fecha = fecha_documento
            diagnostico = DiagnosisCompany.query.filter_by(company_id=company.id).order_by(asc(DiagnosisCompany.date_created)).first()
            if diagnostico:
                fecha_diagnostico = diagnostico.date_created
                if fecha_diagnostico:
                    if fecha > fecha_diagnostico:
                        fecha = fecha_diagnostico
            company.date_created =fecha
            db.session.add(update)
            db.session.commit()
    return 'listo'

@digitalcenter.route('/update/l/3',methods=['GET', 'POST'])
@login_required
def _init3_status_company():
    companys = Company.query.filter_by(enabled=True).all()[400:700]
    for company in companys:
        update =  Company.query.filter(Company.id == company.id).first()

        if company.inscripcion:
            #buscamos el servicio de atencion inicial al plan de mejora como primer servicio de empresa
            service = CatalogServices.query.filter_by(name_short = 'a1').first()
            actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service.id,fase=0).first()
            if not actionplan:
                fecha = company.inscripcion.date_created
            else:
                if actionplan.date_created:
                    fecha = actionplan.date_created
                else:
                    fecha = company.inscripcion.date_created
            documento =  DocumentCompany.query.filter_by(company_id=company.id).order_by(asc(DocumentCompany.date_created)).first()
            if documento:
                fecha_documento = documento.date_created
                if fecha_documento:
                    if fecha > fecha_documento:
                        fecha = fecha_documento
            diagnostico = DiagnosisCompany.query.filter_by(company_id=company.id).order_by(asc(DiagnosisCompany.date_created)).first()
            if diagnostico:
                fecha_diagnostico = diagnostico.date_created
                if fecha_diagnostico:
                    if fecha > fecha_diagnostico:
                        fecha = fecha_diagnostico
            company.date_created =fecha
            db.session.add(update)
            db.session.commit()
    return 'listo'

@digitalcenter.route('/sde/service/',methods=['GET', 'POST'])
@login_required
def _asesoria_colectivas_service_list():
    app.logger.debug('** SWING_CMS ** -  appointments_create') 
    services = CatalogServices.query.filter_by(enabled=1).filter(
        or_(CatalogServices.fase != 0, CatalogServices.fase.is_(None))
    ).all()
    references = ActionPlanReferences.query.filter_by(employe_assigned=current_user.id).order_by(desc(ActionPlanReferences.id)).all()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    context = {'services':services,'references':references}  
    return render_template('digitalcenter/asesoria_colectivas_service_list.html',**context)


@digitalcenter.route('/sde/service/s/<int:service_id>/search',methods=['GET', 'POST'])
@login_required
def _asesoria_colectivas_service_search(service_id):
    filtro = False
    if request.method == 'POST':
        txt_start_date = int(request.form.get('txt_start_date') )
        txt_end_date = int(request.form.get('txt_end_date') )
        filtro = True

    current_date = datetime.now()
    app.logger.debug('** SWING_CMS ** -  appointments_create') 
    services = CatalogServices.query.filter_by(id = service_id).first()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    if current_user.id == 3 or current_user.id == 24:
        actions = ActionPlan.query.join(Company).filter(Company.enabled ==True,ActionPlan.services_id==services.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).all()
    else:
        actions = ActionPlan.query.join(Company).filter(
            or_(ActionPlan.created_by == current_user.id, Company.created_by == current_user.id),
            ActionPlan.services_id == services.id,
            ActionPlan.fase != 0,
            ActionPlan.cancelled == False
        ).all()
    # Suponiendo que tienes definidas las clases ActionPlan y ActionPlanReferences
    for action in actions:
        category = "No tiene plan de acción"
        if action.company.action_plan_progress is not None:
        # Calcula la categoría según el valor de action_plan_progress
        
            if action.company.action_plan_progress:
                category_start = int(action.company.action_plan_progress // 20) * 20
                category = f"{category_start} de {category_start + 20}" if category_start < 100 else "80 de 100"
            else:
                category = "0 de 20"
        action.company.avancepa = category
        if action.company.date_action_plan:
            days_since_action_plan = (current_date - action.company.date_action_plan).days
            
            action.days_since_action_plan = days_since_action_plan
        else:
            # Si date_scheduled_start es None, puedes establecer days_since_action_plan en None o un valor predeterminado
            action.days_since_action_plan = None  # Otra opción: action.days_since_action_plan = 0
    # Realizar la consulta
    if filtro:
        filtered_actions = []

        for action in actions:
            if action.days_since_action_plan > txt_start_date and action.days_since_action_plan < txt_end_date:
                print('xxxxxxxxxxxx')
                print(action.days_since_action_plan)
                filtered_actions.append(action)
        actions = filtered_actions
    action_plan_references = ActionPlanReferences.query.join(
        ActionPlan, ActionPlanReferences.action_plan_id == ActionPlan.id
    ).filter(
        ActionPlan.services_id == services.id,
        ActionPlanReferences.employe_assigned == current_user.id
    ).all()    
    # Suponiendo que tienes definidas las clases ActionPlan y ActionPlanReferences
    for action in action_plan_references:
        if action.action_plan.company.date_action_plan:
            days_since_action_plan = (current_date - action.action_plan.company.date_action_plan).days
            action.days_since_action_plan = days_since_action_plan
        else:
            # Si date_scheduled_start es None, puedes establecer days_since_action_plan en None o un valor predeterminado
            action.days_since_action_plan = None  # Otra opción: action.days_since_action_plan = 0
    if filtro:
        filtered_actions_2 = []

        for action in action_plan_references:
            if action.days_since_action_plan > txt_start_date and action.days_since_action_plan < txt_end_date:
                print('xxxxxxxxxxxx')
                filtered_actions.append(action)
        action_plan_references=filtered_actions_2
    context = {'actions':actions,'action_plan_references':action_plan_references}  
    return render_template('digitalcenter/asesoria_colectivas_service_search.html',**context)



@digitalcenter.route('/init/log/1',methods=['GET', 'POST'])
@login_required
def _init1_logs_company():
    companys = Company.query.filter_by(enabled=True).all()[0:200]
    for company in companys:
        atention = AttentionLog.query.filter_by(company_id=company.id).first()
        if not atention:
            update = AttentionLog()
            update.codigo = 1
            update.company_id = company.id
            update.description = "Inicio de atención"
            update.created_by = company.created_by
            update.date_attention = company.date_created
            db.session.add(update)
            db.session.commit() 
    return 'listo'

@digitalcenter.route('/init/log/2',methods=['GET', 'POST'])
@login_required
def _init2_logs_company():
    companys = Company.query.filter_by(enabled=True).all()[200:400]
    for company in companys:
        atention = AttentionLog.query.filter_by(company_id=company.id).first()
        if not atention:
            update = AttentionLog()
            update.codigo = 1
            update.company_id = company.id
            update.description = "Inicio de atención"
            update.created_by = company.created_by
            update.date_attention = company.date_created
            db.session.add(update)
            db.session.commit() 
    return 'listo'

@digitalcenter.route('/init/log/3',methods=['GET', 'POST'])
@login_required
def _init3_logs_company():
    companys = Company.query.filter_by(enabled=True).all()[400:700]
    for company in companys:
        atention = AttentionLog.query.filter_by(company_id=company.id).first()
        if not atention:
            update = AttentionLog()
            update.codigo = 1
            update.company_id = company.id
            update.description = "Inicio de atención"
            update.created_by = company.created_by
            update.date_attention = company.date_created
            db.session.add(update)
            db.session.commit() 
    return 'listo'


@digitalcenter.route('/init/log/4',methods=['GET', 'POST'])
@login_required
def _init4_logs_company():
    companys = Company.query.filter_by(enabled=True).all()[400:700]
    dato = []
    for company in companys:
        if not company.created_by or not company.date_created:
            dato.append(company.id)
    return str(dato)

@digitalcenter.route('/documentos/list',methods=['GET', 'POST'])
@login_required
def _company_document_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    #diagnosis = DiagnosisCompany.query.filter_by(created_by=current_user.id)
    lista = []
    #for diagnosi in diagnosis:
    #    lista.append(diagnosi.company_id)
    if current_user.id == 3 or current_user.id == 24:
        companys = Company.query.join(User, User.id==Company.created_by)\
            .filter(Company.enabled==True).all()
   
    else:
        companys = Company.query.join(User, User.id==Company.created_by).filter(Company.enabled==True, or_(Company.created_by == current_user.id,Company.id.in_(lista))).all()
    for company in companys:
        #buscamos la carta de compromiso DOC2
        
        carta = CatalogIDDocumentTypes.query.filter_by(name_short='DOC2').first()
        carta = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=carta.id,enabled=True).order_by(DocumentCompany.id.desc()).first()
        if carta:
            lista.append(carta.id)
        #buscamos la ficha de inscripcion DOC1
        ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
        ficha =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id,enabled=True).order_by(DocumentCompany.id.desc()).first()
        if carta:
            lista.append(ficha.id)
    lista = DocumentCompany.query.filter(DocumentCompany.id.in_(lista)).order_by(DocumentCompany.company_id).all()
    context = {
        'apis': lista,
      
    }
    return render_template('company_document_list.html',**context)



@digitalcenter.route('/update/stage/',methods=['GET', 'POST'])
@login_required
def _init_stage_company():
    print("hola")
    status = CompanyStage.query.filter_by(name_short='E1').first()
    companys = (
        db.session.query(Company)
        .filter(
            or_(Company.stage_id == None, Company.stage_id == ''),Company.enabled == True 
        )
        .all()
    )

    for company in companys:
        print("hola")
        print(company.id)
        update =  Company.query.filter(Company.id == company.id).first()
        ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
        ficha_doc =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id).first()
        carta = CatalogIDDocumentTypes.query.filter_by(name_short='DOC2').first()
        carta_doc =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=carta.id).first()
        diagnostico = DiagnosisCompany.query.filter_by(company_id=company.id).order_by(asc(DiagnosisCompany.date_created)).first()
        if diagnostico or ficha_doc or carta_doc:
            status = CompanyStage.query.filter_by(name_short='E2').first()
            update.stage_id = status.id
            if company.status:
                if company.status.name_short in ['4', '5']:
                    sumas = 2 +2
                else:
                    status = CompanyStatus.query.filter_by(name_short='6').first()
                    company.status_id = status.id                
            else:
                status = CompanyStatus.query.filter_by(name_short='6').first()
                company.status_id = status.id
        else:
            status = CompanyStage.query.filter_by(name_short='E1').first()
            update.stage_id = status.id

        db.session.add(update)
        db.session.commit()
    return 'listo'



@digitalcenter.route('/update/stage/x1',methods=['GET', 'POST'])
@login_required
def _init_stage_company32():
    print("hola")
    status = CompanyStage.query.filter_by(name_short='E1').first()
    # Realiza la unión entre Company y CompanyStatus
    companys = (
        db.session.query(Company)
        .join(Company.status)  # Realiza una unión con la relación "status" en Company
        .filter(
            Company.stage_id == status.id,
            Company.enabled == True,
            CompanyStatus.name_short.in_(['1', '2', '3','6'])  # Accede al atributo name_short de CompanyStatus
        )
        .all()
    )


    for company in companys:
        print("hola")
        print(company.id)
        update =  Company.query.filter(Company.id == company.id).first()
        ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
        ficha_doc =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id).first()
        carta = CatalogIDDocumentTypes.query.filter_by(name_short='DOC2').first()
        carta_doc =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=carta.id).first()
        diagnostico = DiagnosisCompany.query.filter_by(company_id=company.id).order_by(asc(DiagnosisCompany.date_created)).first()
        if diagnostico or ficha_doc or carta_doc:
            status = CompanyStage.query.filter_by(name_short='E2').first()
            update.stage_id = status.id
            if company.status:
                if company.status.name_short in ['4', '5']:
                    sumas = 2 +2
                else:
                    status = CompanyStatus.query.filter_by(name_short='6').first()
                    company.status_id = status.id                
            else:
                status = CompanyStatus.query.filter_by(name_short='6').first()
                company.status_id = status.id

        db.session.add(update)
        db.session.commit()
    return 'listo'


@digitalcenter.route('/update/stage/x2',methods=['GET', 'POST'])
@login_required
def _init_stage_company3():
    print("hola")
    status = CompanyStage.query.filter_by(name_short='E2').first()
    # Realiza la unión entre Company y CompanyStatus
    companys = (
        db.session.query(Company)
        .join(Company.status)  # Realiza una unión con la relación "status" en Company
        .filter(
            Company.stage_id == status.id,
            Company.enabled == True,
            CompanyStatus.name_short.in_(['1', '2', '3','6'])  # Accede al atributo name_short de CompanyStatus
        )
        .all()
    )


    for company in companys:
        print("hola")
        print(company.id)
        update =  Company.query.filter(Company.id == company.id).first()
        ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
        ficha_doc =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id).first()
        carta = CatalogIDDocumentTypes.query.filter_by(name_short='DOC2').first()
        carta_doc =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=carta.id).first()
        diagnostico = DiagnosisCompany.query.filter_by(company_id=company.id).order_by(asc(DiagnosisCompany.date_created)).first()
        if diagnostico or ficha_doc or carta_doc:
            status = CompanyStage.query.filter_by(name_short='E2').first()
            update.stage_id = status.id
            if company.status:
                if company.status.name_short in ['4', '5']:
                    sumas = 2 +2
                else:
                    status = CompanyStatus.query.filter_by(name_short='6').first()
                    company.status_id = status.id                
            else:
                status = CompanyStatus.query.filter_by(name_short='6').first()
                company.status_id = status.id

        db.session.add(update)
        db.session.commit()
    return 'listo'


@digitalcenter.route('/update/stage/x3',methods=['GET', 'POST'])
@login_required
def _init_stage_company4():
    print("hola")
    status = CompanyStage.query.filter_by(name_short='E3').first()
    # Realiza la unión entre Company y CompanyStatus
    companys = (
        db.session.query(Company)
        .join(Company.status)  # Realiza una unión con la relación "status" en Company
        .filter(
            Company.stage_id == status.id,
            Company.enabled == True,
            CompanyStatus.name_short.in_(['1', '2', '3'])  # Accede al atributo name_short de CompanyStatus
        )
        .all()
    )


    for company in companys:
        print("hola")
        print(company.id)
        update =  Company.query.filter(Company.id == company.id).first()
        ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
        ficha_doc =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id).first()
        carta = CatalogIDDocumentTypes.query.filter_by(name_short='DOC2').first()
        carta_doc =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=carta.id).first()
        diagnostico = DiagnosisCompany.query.filter_by(company_id=company.id).order_by(asc(DiagnosisCompany.date_created)).first()
        if diagnostico or ficha_doc or carta_doc:
            status = CompanyStage.query.filter_by(name_short='E2').first()
            update.stage_id = status.id
            if company.status:
                if company.status.name_short in ['4', '5']:
                    sumas = 2 +2
                else:
                    status = CompanyStatus.query.filter_by(name_short='6').first()
                    company.status_id = status.id                
            else:
                status = CompanyStatus.query.filter_by(name_short='6').first()
                company.status_id = status.id

        db.session.add(update)
        db.session.commit()
    return 'listo'

@digitalcenter.route('/update/stage/2',methods=['GET', 'POST'])
@login_required
def _init_stage_company_2():
    status = CompanyStage.query.filter_by(name_short='E1').first()
    companys = (
        db.session.query(Company)
        .filter(
            Company.enabled == True,  # Agrega esta condición
            Company.stage_id == status.id  # Agrega esta condición
        )
        .all()
    )

    for company in companys:
        update =  Company.query.filter(Company.id == company.id).first()
        ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
        ficha_doc =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id).first()
        carta = CatalogIDDocumentTypes.query.filter_by(name_short='DOC2').first()
        carta_doc =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=carta.id).first()
        diagnostico = DiagnosisCompany.query.filter_by(company_id=company.id).order_by(asc(DiagnosisCompany.date_created)).first()
        if diagnostico or ficha_doc or carta_doc:
                status = CompanyStage.query.filter_by(name_short='E2').first()
                update.stage_id = status.id
                db.session.add(update)
                db.session.commit()
    return 'listo'

@digitalcenter.route('/update/stage/3',methods=['GET', 'POST'])
@login_required
def _init_stage_3_company():
    companys = Company.query.filter_by(enabled=True).all()[420:670]
    for company in companys:
        update =  Company.query.filter(Company.id == company.id).first()
        ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
        ficha =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id).first()
        if ficha:
            if update.status_id == 1:                
                status = CompanyStage.query.filter_by(name_short='E1').first()
                update.stage_id = status.id
            else:
                status = CompanyStage.query.filter_by(name_short='E2').first()
                update.stage_id = status.id
        else:
            status = CompanyStage.query.filter_by(name_short='E1').first()
            update.stage_id = status.id
        db.session.add(update)
        db.session.commit()
    return 'listo'

@digitalcenter.route('/formulario/change/<int:company_id>/form/',methods = ['GET', 'POST'])
@login_required
def _company_change_form(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'upload-carta' not in request.files:
            return redirect(url_for('digitalcenter._company_document_form_add',company_id=company.id))
    status = CompanyStage.query.all()
    context = {
        "company": company,
        'status':status,
    }
    return render_template('company_change_form.html',**context)

@digitalcenter.route('/formulario/company/monitoring/<int:company_id>/form/',methods = ['GET', 'POST'])
@login_required
def _company_company_monitoring_form(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'upload-carta' not in request.files:
            return redirect(url_for('digitalcenter._company_company_monitoring_form',company_id=company.id))
        file = request.files['upload-carta']
        txt_date = request.form.get('txt_date') 
        txt_hours= request.form.get('txt_hours')
        selected_channel = request.form.get('selected_channel')
        txt_company_id = request.form.get('txt_company_id')
        txt_description =  request.form.get('txt_description')
        service_channel = ServiceChannel.query.filter_by(name_short=selected_channel).first()
 
        history = CompanyMonitoring()
        history.company_id = company.id
        history.created_by = current_user.id 
        history.id_service_channel = service_channel.id
        history.description = txt_description
        n = 1

        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            documentoName = str(company.dni) + ' ' +  str(txt_date) + '-' + str(n)
            filename =  documentoName.replace(" ", "_") +'.'+ filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        history.document_local = filename
        history.date = txt_date
        history.hour = txt_hours
        db.session.add(history)
        db.session.commit()

    channel = ServiceChannel.query.all()
    records = CompanyMonitoring.query.filter_by(company_id=company.id).all()
    context = {
        "company": company,
        "channel":channel,
        "records":records

    }
    return render_template('company_company_monitoring_form.html',**context)

@digitalcenter.route('/formulario/edit/<int:company_id>/form/',methods = ['GET', 'POST'])
@login_required
def _company_edit__form(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'upload-carta' not in request.files:
            return redirect(url_for('digitalcenter._company_document_form_add',company_id=company.id))
    status = CompanyStage.query.all()
    context = {
        "company": company,
        'status':status,

    }
    return render_template('company_edit__form.html',**context)

@digitalcenter.route('/blueberry/',methods=['GET', 'POST'])
@login_required
def _company_blueberry_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    company = Company.query.filter(Company.enabled==True).all()
    context = {
        'apis': company,
    }
    return render_template('company_list.html',**context)

@digitalcenter.route('/blueberry/<int:company_id>/',methods=['GET', 'POST'])
@login_required
def _company_blueberry_view(company_id):
    app.logger.debug('** SWING_CMS ** - ------------------')
    company = Company.query.filter_by(id=company_id).first()
    if request.method == 'POST':
        txt_departamento = request.form['txt_departamento']
        txt_municipios = request.form['txt_municipios']


    context = {
        'company': company,
    }
    return render_template('company_forms.html',**context)


from flask import Flask, jsonify
from sqlalchemy import func, and_
from sqlalchemy.orm import aliased

@digitalcenter.route('/get_action_plans', methods=['GET'])
@login_required
def get_action_plans():
    # Subconsulta para obtener el ID mínimo para cada company_id
    subquery = db.session.query(
        ActionPlan.company_id,
        func.min(ActionPlan.id).label('min_id')
    ).filter(ActionPlan.fase != 0).group_by(ActionPlan.company_id).subquery()


    # Consulta principal para obtener los registros completos
    result = db.session.query(ActionPlan).join(
        subquery,
        db.and_(
            ActionPlan.company_id == subquery.c.company_id,
            ActionPlan.id == subquery.c.min_id
        )
    ).all()

    # Crear una lista de diccionarios con los datos de result
    action_plans_data = []
    for action_plan in result:
        action_plans_data.append({
            'id': action_plan.id,
            'company_id': action_plan.company_id,
            'date_created': action_plan.date_created.strftime('%Y-%m-%d'),
            'date_scheduled_start': action_plan.date_scheduled_start.strftime('%Y-%m-%d') if action_plan.date_scheduled_start else None,
            # Agrega otros campos según sea necesario
        })

    # Retorna los datos en formato JSON
    return jsonify(action_plans_data)

@digitalcenter.route('/first_records_by_company', methods=['GET'])
@login_required
def first_records_by_company():
    # Realiza una subconsulta para obtener el primer registro creado por cada company_id
                
    subquery = db.session.query(
        func.min(DiagnosisCompany.date_created).label('min_date_created'),
        DiagnosisCompany.company_id.label('company_id')  # Asigna un alias a la columna company_id
    ).group_by(DiagnosisCompany.company_id).subquery()

    # Consulta principal que une la subconsulta para obtener los registros completos
    first_records = db.session.query(DiagnosisCompany).join(
        subquery,
        and_(
            DiagnosisCompany.company_id == subquery.c.company_id,
            DiagnosisCompany.date_created == subquery.c.min_date_created
        )
    ).all()

    # Crea una lista de diccionarios con los datos de los primeros registros
    data = []
    for record in first_records:
        data.append({
            'company_id': record.company_id,
            'date_created': record.date_created.strftime('%Y-%m-%d'),  # Convierte la fecha a una cadena
            'status': record.status,
            # Agrega otros campos según sea necesario
        })

    # Convierte la lista de diccionarios en formato JSON y la devuelve como respuesta
    return jsonify(data)


@digitalcenter.route('/get_companies', methods=['GET'])
@login_required
def get_companies():
    # Subconsulta para obtener el ID mínimo para cada company_id
    subquery = db.session.query(
        ActionPlan.company_id,
        func.min(ActionPlan.id).label('min_id')
    ).filter(ActionPlan.fase != 0).group_by(ActionPlan.company_id).subquery()


    # Consulta principal para obtener los registros completos
    result = db.session.query(ActionPlan).join(
        subquery,
        db.and_(
            ActionPlan.company_id == subquery.c.company_id,
            ActionPlan.id == subquery.c.min_id
        )
    ).all()

    # Crear una lista de diccionarios con los datos de result
    action_plans_data = []
    for action_plan in result:
        action_plans_data.append({
            'id': action_plan.id,
            'company_id': action_plan.company_id,
            'date_created': action_plan.date_created.strftime('%Y-%m-%d'),
            'date_scheduled_start': action_plan.date_scheduled_start.strftime('%Y-%m-%d') if action_plan.date_scheduled_start else None,
            # Agrega otros campos según sea necesario
        })

    # Retorna los datos en formato JSON
    return jsonify(action_plans_data)

# Ruta para la vista que retorna las empresas con ActionPlan no en fase 0
@digitalcenter.route('/companies_with_non_zero_phase', methods=['GET'])
@login_required
def companies_with_non_zero_phase():
    # Realiza una consulta que filtre las empresas en función de ActionPlan con fase no igual a 0
    companies = db.session.query(Company).\
        join(ActionPlan, Company.id == ActionPlan.company_id).\
        filter(ActionPlan.fase != 0).distinct().all()

    # Crea una lista de diccionarios con los datos de las empresas
    data = []
    for company in companies:
        data.append({
            'id': company.id,
            'name': company.name,
            # Agrega otros campos de la empresa según sea necesario
        })

    # Convierte la lista de diccionarios en formato JSON y la devuelve como respuesta
    return jsonify(data)


from datetime import datetime, timedelta
from sqlalchemy.orm import aliased

@digitalcenter.route('/empresas/en/pausa/',methods=['GET', 'POST'])
@login_required
def _company_pausa_list():
    # Obtener la fecha actual y la fecha hace 60 días
    fecha_actual = datetime.now()
    fecha_limite = fecha_actual - timedelta(days=60)
    lista  = []
    listado = []
    allowed_status_short_names = [6]
    allowed_stage_short_names = ['E2']
    if current_user.id == 3 or current_user.id == 24:
        companies = Company.query.join(User, User.id==Company.created_by)\
            .filter(Company.enabled==True,Company.status.has(CompanyStatus.name_short.in_(allowed_status_short_names)),Company.stage.has(CompanyStage.name_short.in_(allowed_stage_short_names))).all()
    else:
        companies = Company.query.join(User, User.id==Company.created_by).filter(Company.enabled==True, or_(Company.created_by == current_user.id,Company.id.in_(lista))).all()
    for company in companies:
        action_plan_history_records = (
        db.session.query(ActionPlanHistory)
        .join(ActionPlan, ActionPlanHistory.action_plan_id == ActionPlan.id)
        
        .filter(ActionPlan.company_id == company.id)
        
        .order_by(desc(ActionPlanHistory.date_created)).first()
        )

        if action_plan_history_records:
            fecha_ultima = action_plan_history_records.date_created
            if fecha_limite > fecha_ultima:
                listado.append(company.id)
    company = Company.query.filter(Company.id.in_(listado)).order_by(Company.id).all()
    categories = db.session.query(catalogCategory).all()
    context = {
        'apis': company,
        'company_references':company,
        'data':[],
        'categories':categories,
    }
    return render_template('company_pausa_list.html',**context)

@digitalcenter.route('/empresas/rango/',methods=['GET', 'POST'])
@login_required
def _company_rango_list():
    # Obtener la fecha actual y la fecha hace 60 días

    # POST: Save Appointment
    if request.method == 'POST':
        fecha_actual_str = request.form['txt_startDate']
        fecha_limite_str = request.form['txt_endDate']
        # Convertir las cadenas a objetos datetime
        fecha_a = datetime.strptime(fecha_actual_str, '%Y-%m-%d')
        fecha_b = datetime.strptime(fecha_limite_str, '%Y-%m-%d')

    else:
        fecha_a = datetime.now()
        fecha_b = fecha_a - timedelta(days=60)


    # Consulta para obtener las compañías con historial de planes de acción entre las fechas A y B
    company = (
        db.session.query(Company)
        .join(ActionPlan)
        .join(ActionPlanHistory)
        .filter(
            ActionPlanHistory.date_created.between(fecha_a, fecha_b)
        )
        .all()
    )
    categories = db.session.query(catalogCategory).all()
    context = {
        'apis': company,
        'company_references':company,
        'data':[],
        'categories':categories,
        'fecha_a':fecha_a,
        'fecha_b':fecha_b,
    }
    return render_template('monitoreo/company_rango_list.html',**context)

# Define el filtro personalizado para formatear fechas
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d'):
    return value.strftime(format) if value else ''


@digitalcenter.route('/empresas/diagnostico/<int:company_id>/',methods=['GET', 'POST'])
@login_required
def _company_diagnostic(company_id):
    company = Company.query.filter_by(id = company_id).first()
    diagnostico = Diagnosticos()

    direccion = [pregunta for pregunta in diagnostico.preguntas if pregunta['id_categoria'] == 1]
    mercadeo = [pregunta for pregunta in diagnostico.preguntas if pregunta['id_categoria'] == 2]
    madurez = [pregunta for pregunta in diagnostico.preguntas if pregunta['id_categoria'] == 3]
    financiera = [pregunta for pregunta in diagnostico.preguntas if pregunta['id_categoria'] == 4]
    produccion = [pregunta for pregunta in diagnostico.preguntas if pregunta['id_categoria'] == 5]
    organizacion = [pregunta for pregunta in diagnostico.preguntas if pregunta['id_categoria'] == 6]
    legalizacion = [pregunta for pregunta in diagnostico.preguntas if pregunta['id_categoria'] == 7]

    context = {
        'company': company,
        'direccion':direccion,
        'mercadeo':mercadeo,
        'madurez':madurez,
        'financiera':financiera,
        'produccion':produccion,
        'organizacion':organizacion,
        'legalizacion':legalizacion
    }
    return render_template('digitalcenter/company_diagnostic.html',**context)


@digitalcenter.route('/formulario/documentos/<int:company_id>/add/other/',methods = ['GET', 'POST'])
@login_required
def _company_document_others_add(company_id):
    company = Company.query.filter_by(id=company_id).first()

    document_type = document_type = CatalogIDDocumentTypes.query.filter(
                            CatalogIDDocumentTypes.name_short.in_([1, 2, 3, 4])
                        ).order_by(CatalogIDDocumentTypes.name_short.asc()).all()

    if request.method == 'POST':
        # check if the post request has the file part
        if 'upload-carta' not in request.files:
            return redirect(url_for('digitalcenter._company_document_form_add',company_id=company.id,document_id=document_type.id))
        
        file = request.files['upload-carta']
        txt_document_id = request.form['txt_document_id']

        #buscamos el tipo de documento
        document_type = CatalogIDDocumentTypes.query.filter_by(id=txt_document_id).first() 
        document = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=document_type.id,enabled = True).first()

        n = 1
        if document:
            document.enabled = False
            n = document.id
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            documentoName = str(company.dni) + ' ' + str(document_type.name) + '-' + str(n)
            filename =  documentoName.replace(" ", "_") +'.'+ filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            carta = DocumentCompany()
            carta.company_id = company.id
            carta.documente_type_id = document_type.id
            carta.complete = True
            carta.signed = True
            carta.signed_innova = True
            carta.enabled = True
            carta.document_local = filename
            carta.created_by = current_user.id
            if document:
                db.session.add(document)
            db.session.add(carta)
            db.session.commit()
            return redirect(url_for('digitalcenter._company_dashboard',user_uid=company.id))

    context = {
        "company": company,
        "document_type":document_type
    }
    return render_template('company_document_others_add.html',**context)


@digitalcenter.route('/gpeg/search/attentions',methods=['GET', 'POST'])
@login_required
def _gpeg_search_attentions():
    filtro = False
    if request.method == 'POST':
        start_date = request.form.get('txt_start_date')
        end_date = request.form.get('txt_end_date')

        filtro = True
    else:
        # Definir las fechas de inicio y fin
        start_date = datetime.now() - timedelta(days=30)
        end_date =datetime.now()
        current_date = datetime.now()
    app.logger.debug('** SWING_CMS ** -  appointments_create') 

    app.logger.debug('** SWING_CMS ** - Home Dashboard')
 
    actions = ActionPlan.query.join(Company).filter(Company.enabled ==False,ActionPlan.fase!=0,ActionPlan.cancelled ==False).all()



    # Execute the three queries and store results in sets
    companies_history_set = set(
        company for company in Company.query.join(ActionPlan, ActionPlan.company_id == Company.id)
                            .join(ActionPlanHistory, ActionPlanHistory.action_plan_id == ActionPlan.id)
                            .filter(ActionPlanHistory.date_created >= start_date,
                                    ActionPlanHistory.date_created < end_date)
                            .distinct()
    )

    companies_action_plan_set = set(
        company for company in Company.query.filter(Company.date_action_plan >= start_date,
                                                    Company.date_action_plan < end_date)
    )

    companies_diagnosis_set = set(
        company for company in Company.query.join(DiagnosisCompany)
                            .filter(DiagnosisCompany.date_created >= start_date,
                                    DiagnosisCompany.date_created < end_date)
                            .distinct()
    )

    # Combine the results using set union
    all_companies_set = companies_history_set.union(companies_action_plan_set).union(companies_diagnosis_set)

    # Apply distinct to eliminate duplicates even when present in multiple sets
    all_companies_set = all_companies_set.union({company for company in all_companies_set if company not in all_companies_set})

    # Option 2: Iterate directly over the set if you only need to access the companies
    for company in all_companies_set:
        print(company.name)  # Or access other company attributes


    context = {'all_companies_set':all_companies_set, 'start_date':start_date,'end_date':end_date}  
    return render_template('gpeg_search_attentions.html',**context)


