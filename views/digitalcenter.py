from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response,send_from_directory
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import AttentionLog,WalletTransaction,ActionPlanReferences,DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Company,Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import EnrollmentRecord,CompanyStatus,TrainingType,ModalityType,CourseManagers,Courses,catalogCategory,CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from models.diagnostico import Diagnosticos
from werkzeug.utils import secure_filename
from sqlalchemy import or_
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
    if User.query.filter_by(id = 21).first():
        userTGU = User.query.filter_by(id = 21).first()
    else:
        userTGU = User.query.filter_by(id = 3).first()
    if User.query.filter_by(id = 20).first():
        userJuti = User.query.filter_by(id = 20).first()
    else:
        userJuti = User.query.filter_by(id = 3).first()
    if User.query.filter_by(id = 24).first():
        userJefe = User.query.filter_by(id = 24).first()
    else:
        userJefe = User.query.filter_by(id = 3).first()
    app.logger.debug('** varela')   
    app.logger.debug(x)
    app.logger.debug('** iiiiiiiiiiii varela')   
    new_userlist = new_oul.userlist
    app.logger.debug(new_userlist)    
    app.logger.debug('** xxxxxxxxxxxxx varela')    
    app.logger.debug('** SWING_CMS ** - Welcome2')
    context = {'userJefe':userJefe,  'userJuti':userJuti, 'userTGU':userTGU, 'userRu':userRu,'userRi':userRi,'userLCB':userLCB,'userSPS':userSPS,'userCholo':userCholo,'userCholu':userCholu}
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
def _plan_action_create(user_uid):
    app.logger.debug('** SWING_CMSx ** - ------------------')
    
    company =  Company.query.filter(Company.id == user_uid).first()
    diagnosis =  DiagnosisCompany.query.filter(DiagnosisCompany.company_id == company.id).first()
    plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).all()
    api = diagnosis.respuestas
    servicios = []
    for resp in api:
        if api[resp] == '1' or api[resp] == '2':
            print("Pregunta: {} respuesta: {}".format(resp,api[resp]))
            services = CatalogServices.query.filter(CatalogServices.diagnostic_questions.contains(resp)).all()
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
def _asesorias_puntuales(company_uid):
    company = Company.query.filter_by(id=company_uid).first()
    categoria = catalogCategory.query.filter_by().all()
    services = CatalogServices.query.filter_by(enabled=True).all()
    context = {'categoria':categoria,'services':services,'company':company} 
    return render_template('asesorias_puntuales.html',**context)

@digitalcenter.route('/activar/diagnostico/<int:company_uid>/plan/<servicio_uid>/',methods=['GET', 'POST'])
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
def _valorar_servicios():
    servicios = CatalogServices.query.filter().all()
    for servicio in servicios:
        servicio.cost_innova = 250
        db.session.add(servicio)
        db.session.commit()
    return 'Listo'

@digitalcenter.route('/update/status',methods=['GET', 'POST'])
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
def _init_wallet():
    companys = Company.query.filter_by(enabled=True).all()
    for company in companys:
        if not company.available_credit:
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
                plans = ActionPlan.query.filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled==False).order_by(asc(ActionPlan.date_scheduled_start)).all()
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
                service_plan = CatalogServices.query.filter_by(name_short='c1').first()
                wallet = WalletTransaction.query.filter_by(company_id = company.id, services_id =service_plan.id).first()
                if not wallet:  
                    wallet = WalletTransaction()
                    wallet.amount = service_plan.cost_innova
                    wallet.company_id =company.id
                    wallet.services_id = service_plan.id
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
def _init_activas():
    CS6 = CompanyStatus(name='Activa', name_short='6')
    db.session.add(CS6)
    db.session.commit()
    return 'Listo'

@digitalcenter.route('/insert/chat',methods=['GET', 'POST'])
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
def _re1_inicial_inicial():
    DOC1 = CatalogIDDocumentTypes(name='Ficha de inscripción', name_short='DOC1')
    db.session.add(DOC1)

    DOC2 = CatalogIDDocumentTypes(name='Carta de compromiso', name_short='DOC2')
    db.session.add(DOC2)
    db.session.commit()
    return render_template('404.html')



@digitalcenter.route('/insert/categias/',methods=['GET', 'POST'])
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

@digitalcenter.route('/elegibles/5',methods=['GET', 'POST'])
def _registro_elegibles_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    inscripciones = Inscripciones.query.filter_by(elegible = True,cohorte=5).all()
    context = {
        'api': inscripciones
    }
    return render_template('digitalcenter/registro_elegibles_list.html',**context)

@digitalcenter.route('/view/si/5/<int:inscribe_id>',methods=['GET', 'POST'])
def _registro_elegibles_panel(inscribe_id):
    app.logger.debug('** SWING_CMS ** - ------------------')
    inscripciones = Inscripciones.query.filter_by(id = inscribe_id).first()
    context = {
        'api': inscripciones
    }
    return render_template('digitalcenter/registro_elegibles_panel.html',**context)

@digitalcenter.route('/elegibles/no/5',methods=['GET', 'POST'])
def _registro_no_elegibles_list():
    app.logger.debug('** SWING_CMS ** - ------------------')
    inscripciones = Inscripciones.query.filter_by(elegible = False,cohorte=5).all()
    context = {
        'api': inscripciones
    }
    return render_template('digitalcenter/registro_no_elegibles_list.html',**context)

@digitalcenter.route('/view/no/5/<int:inscribe_id>',methods=['GET', 'POST'])
def _registro_no_eleibles_panel(inscribe_id):
    app.logger.debug('** SWING_CMS ** - ------------------')
    inscripciones = Inscripciones.query.filter_by(id = inscribe_id).first()
    context = {
        'api': inscripciones
    }
    return render_template('digitalcenter/registro_no_elegibles_panel.html',**context)




from sqlalchemy import desc,asc
@digitalcenter.route('/empresas/view/<int:user_uid>/',methods=['GET', 'POST'])
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
    users = User.query.join(UserXRole, User.id==UserXRole.user_id).filter(UserXRole.user_role_id == 3).all()
    context = {
        'users':users,
        'company': company,
        'actions':actions,
        "diagnostico":diagnostico,
        "actions_asesorias":actions_asesorias
    }
 
    return render_template('plan_action_dashboard.html',**context)


@digitalcenter.route('/empresas/',methods=['GET', 'POST'])
def _company_monitoring_list():
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
    return render_template('company_monitoring_list.html',**context)

@digitalcenter.route('/empresas/dn',methods=['GET', 'POST'])
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
def _company_dashboard(user_uid):
    app.logger.debug('** sexo ** - ------------------')

    company = Company.query.filter_by(id=user_uid).first()
    

    #buscamos la carta de compromiso DOC2
    carta = CatalogIDDocumentTypes.query.filter_by(name_short='DOC2').first()
    carta = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=carta.id,enabled=True).order_by(DocumentCompany.id.desc()).first()
    #buscamos la ficha de inscripcion DOC1
    ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
    ficha =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id,enabled=True).order_by(DocumentCompany.id.desc()).first()
    diagnos = DiagnosisCompany.query.filter_by(company_id=company.id,status=True).order_by(desc(DiagnosisCompany.date_created)).first()
    actions = ActionPlan.query.filter_by(company_id=company.id,cancelled=False).all()
    if diagnos:
        diagnostico = diagnos.resultados
    else:
        diagnostico = False
    enrolls = EnrollmentRecord.query.filter_by(company_id=company.id).all()
    context = {
        'enrolls':enrolls,
        'carta':carta,
        'ficha':ficha,
        'company': company,
        'actions':actions,
        "diagnostico":diagnostico,
    }
 
    return render_template('company_dashboard.html',**context)

@digitalcenter.route('/company/reference/view/<int:user_uid>/',methods=['GET', 'POST'])
def _company_dashboard_action_plan_references(user_uid):
    app.logger.debug('** sexo ** - ------------------')

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
def _plan_action_bitacora(user_uid):
    action = ActionPlan.query.filter_by(id=user_uid).first()
    history = ActionPlanHistory.query.filter_by(action_plan_id=action.id)
    context = {
        'action': action,
        'history':history
    }
    return render_template('plan_action_bitacora.html',**context)


@digitalcenter.route('/empresas/resumen/update/<int:user_uid>/',methods=['GET', 'POST'])
def _plan_action_bitacora_update(user_uid):
    action = ActionPlanHistory.query.filter_by(id=user_uid).first()
    context = {
        'action': action,
       
    }
    return render_template('plan_action_bitacora_update.html',**context)


@digitalcenter.route('/empresas/resumen/bitecora/<int:user_uid>/',methods=['GET', 'POST'])
def _plan_action_bitacora_atenciones(user_uid):
    history = ActionPlanHistory.query.filter_by(id=user_uid).first()
    context = {
        'history': history,
  
    }
    return render_template('plan_action_bitacora_atenciones.html',**context)


@digitalcenter.route('/empresas/view/user/<int:company_id>/',methods=['GET', 'POST'])
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
def _company_document_form(document_id):
    document = DocumentCompany.query.filter_by(id=document_id).first()
    context = {
        "document": document
    }
    return render_template('company_document_form.html',**context)

@digitalcenter.route('/formulario/documentos/<int:company_id>/add/<int:document_id>/',methods = ['GET', 'POST'])
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
def _company_document_user(document_id):
    document = DocumentCompany.query.filter_by(id=document_id).first()
    context = {
        "document": document
    }
    return render_template('company_document_user.html',**context)

@digitalcenter.route('/registros/inno/',methods = ['GET', 'POST'])
def _registro_api_dashboard():
    return render_template('digitalcenter/registro_api_dashboard.html')



@digitalcenter.route('/diagnostico/update',methods=['GET', 'POST'])
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
def _asesoria_colectivas_service_list():
    app.logger.debug('** SWING_CMS ** -  appointments_create') 
    services = CatalogServices.query.filter_by(enabled = 1).all()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    context = {'services':services}  
    return render_template('digitalcenter/asesoria_colectivas_service_list.html',**context)


@digitalcenter.route('/sde/service/<int:service_id>/search',methods=['GET', 'POST'])
def _asesoria_colectivas_service_search(service_id):
    app.logger.debug('** SWING_CMS ** -  appointments_create') 
    services = CatalogServices.query.filter_by(id = service_id).first()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    actions = ActionPlan.query.filter(ActionPlan.created_by==current_user.id,ActionPlan.services_id==services.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).all()
    context = {'actions':actions}  
    return render_template('digitalcenter/asesoria_colectivas_service_search.html',**context)



@digitalcenter.route('/init/log/1',methods=['GET', 'POST'])
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
def _init4_logs_company():
    companys = Company.query.filter_by(enabled=True).all()[400:700]
    dato = []
    for company in companys:
        if not company.created_by or not company.date_created:
            dato.append(company.id)
    return str(dato)