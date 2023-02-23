from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response,send_from_directory
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
import os

digitalcenter = Blueprint('digitalcenter', __name__, template_folder='templates', static_folder='static')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            filename = str(current_user.id) +'.'+ filename.rsplit('.', 1)[1].lower()
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
        return redirect(url_for('digitalcenter.__form_profile_sde'))
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
        userRu = User.query.filter_by(id = 1).first()
    if User.query.filter_by(id = 6).first():
        userRi = User.query.filter_by(id = 6).first()
    else:
        userRi = User.query.filter_by(id = 1).first()
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
    app.logger.debug('** varela')   
    app.logger.debug(x)
    app.logger.debug('** iiiiiiiiiiii varela')   
    new_userlist = new_oul.userlist
    app.logger.debug(new_userlist)    
    app.logger.debug('** xxxxxxxxxxxxx varela')    
    app.logger.debug('** SWING_CMS ** - Welcome2')
    context = {'userJuti':userJuti, 'userTGU':userTGU, 'userRu':userRu,'userRi':userRi,'userLCB':userLCB,'userSPS':userSPS,'userCholo':userCholo,'userCholu':userCholu}
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


@digitalcenter.route('/servicios/',methods=['GET', 'POST'])
def _servicios_1():
    return render_template('servicios.html')

@digitalcenter.route('/plan/',methods=['GET', 'POST'])
def _plan_2():
    return render_template('plan.html')

@digitalcenter.route('/historial/',methods=['GET', 'POST'])
def _historial_2():
    return render_template('historial.html')

@digitalcenter.route('/servi/',methods=['GET', 'POST'])
def _servi():
    services = CatalogServices.query.filter_by(enabled = 1).all()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    context = {'services':services}  
    return render_template('servi.html',**context)

import requests
import json 
@digitalcenter.route('/datos/',methods=['GET', 'POST'])
def _datos():
    app.logger.debug('** SWING_CMS ** - ------------------')
    url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/?format=json"
    #url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/202116860/?format=json"
    headers={'Authorization':'token 5690e59a570b717402ac2bcdba1fe02afc8abd85'}
    resp = requests.get(url,headers=headers)
    api = json.loads(resp.content)
    context = {
        'api': api
    }
    return render_template('datos.html',**context)

@digitalcenter.route('/datos/<int:user_uid>/',methods=['GET', 'POST'])
def _datos_describe(user_uid):
    app.logger.debug('** SWING_CMSx ** - ------------------')
    #url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/?format=json"
    url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/{}/?format=json".format(user_uid)
    headers={'Authorization':'token 5690e59a570b717402ac2bcdba1fe02afc8abd85'}
    resp = requests.get(url,headers=headers)
    api = json.loads(resp.content)
    servicios = []
    for resp in api:
        if api[resp] == '1':
            print("Pregunta: {} respuesta: {}".format(resp,api[resp]))
            services = CatalogServices.query.filter(CatalogServices.diagnostic_questions.contains(resp)).all()

            for servicesx in services:
                print('....')
                if len(list(e for e in servicios if e['id']  == servicesx.id)) == 0:
                    servicios.append({'id':servicesx.id,'titulo':servicesx.name})
                
    context = {
        'api': api,
        'servicios':servicios
    }
    app.logger.debug(servicios)
    app.logger.debug(servicios)
    app.logger.debug(servicios)
    return render_template('datos_describe.html',**context)


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


@digitalcenter.route('/insert/chat',methods=['GET', 'POST'])
def _re1():
    staff_it_role = CatalogUserRoles.query.filter_by(name_short='itc').first()
    websites = CatalogServices(name='Asesoria para la formalizacion legal de la empresa', name_short='s1', service_user_role=staff_it_role.id,diagnostic_questions=[])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Asesoria para gestión de registros legales', name_short='s2', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_9"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Asesoria para adhesion al regimen de  facturacion, beneficios fiscales y legislación tributaria.', name_short='s3', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_9"},{"id": "_4_6"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Acompañar en la gestión de solicitudes legales empresariales', name_short='s4', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_3"},{"id": "_2_8"},{"id": "_5_7"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Acompañamiento en la elaboración de plan operativo y estratégico de desarrollo para la empresa.', name_short='s5', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_1_1"},{"id": "_1_2"},{"id": "_1_3"},{"id": "_1_4"},{"id": "_1_5"},{"id": "_1_7"},{"id": "_1_8"},{"id": "_1_8"},{"id": "_6_2"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Asesoria en la gestión del talento humano.', name_short='s6', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_3_3"},{"id": "_5_6"},{"id": "_5_16"},{"id": "_5_17"},{"id": "_5_18"},{"id": "_6_1"},{"id": "_6_2"},{"id": "_6_3"},{"id": "_6_5"},{"id": "_6_6"},{"id": "_6_7"},{"id": "_6_8"},{"id": "_6_9"},{"id": "_6_10"},{"id": "_6_11"},{"id": "_6_12"},{"id": "_6_13"},{"id": "_6_14"},{"id": "_6_16"},{"id": "_6_17"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Guia para manual de funciones.', name_short='s7', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_5_16"},{"id": "_5_17"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Asesoria para implemetación de un sistema básico para el registro de las operaciones.', name_short='s8', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_8"},{"id": "_5_18"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Generación de redes y trabajo coloraborativo.', name_short='s9', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_5_3"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Elaboración de platillas para la elaboración de los Estados Financieros.', name_short='s10', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_5"},{"id": "_4_7"},{"id": "_4_10"},{"id": "_4_12"},{"id": "_4_17"}])
    db.session.add(websites)
    db.session.commit()
    #--
    websites = CatalogServices(name='Realizar la descripción y análisis de los procesos actuales para elaborar el diagrama de flujo de procesos', name_short='s11', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_5_1"},{"id": "_5_5"},{"id": "_5_8"},{"id": "_5_12"},{"id": "_5_13"},{"id": "_5_14"},{"id": "_5_15"},{"id": "_5_19"},{"id": "_5_20"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Acompañamiento en la elaboración de una guia para la gestión de calidad', name_short='s12', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_5_8"},{"id": "_5_11"},{"id": "_5_13"},{"id": "_5_14"},{"id": "_5_17"},{"id": "_5_22"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Asesoria para el desarrollo de red proveedores, cadena de sumistros y canales de distribución.', name_short='s13', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_14"},{"id": "_4_20"},{"id": "_5_3"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Brindar estrategias y modelos para la mejora de la productividad.', name_short='s14', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_5_1"},{"id": "_5_21"},{"id": "_5_23"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Asesoría en la formalización de productos y diseño de fichas técnicas.', name_short='s15', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_7"},{"id": "_5_2"},{"id": "_5_5"},{"id": "_5_8"},{"id": "_5_11"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Asesoría en la formalización de productos y diseño de fichas técnicas.', name_short='s16', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_7"},{"id": "_5_2"},{"id": "_5_5"},{"id": "_5_8"},{"id": "_5_11"}])
    db.session.add(websites)
    db.session.commit()
    return render_template('404.html')


@digitalcenter.route('/insert/chat/2',methods=['GET', 'POST'])
def _re2():
    staff_it_role = CatalogUserRoles.query.filter_by(name_short='itc').first()
    websites = CatalogServices(name='Asesoria para la formalizacion legal de la empresa', name_short='s1', service_user_role=staff_it_role.id,diagnostic_questions=[])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Asesoria para gestión de registros legales', name_short='s2', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_9"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Asesoria para adhesion al regimen de  facturacion, beneficios fiscales y legislación tributaria.', name_short='s3', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_4_9"},{"d": "_4_6"}])
    db.session.add(websites)
    db.session.commit()
    websites = CatalogServices(name='Acompañar en la gestión de solicitudes legales empresariales (permisos, licencias, registros, certificados y otros)', name_short='s4', service_user_role=staff_it_role.id,diagnostic_questions=[{"id": "_2_3"},{"d": "_2_8"},{"d": "_5_7"}])
    db.session.add(websites)
    db.session.commit()
    return render_template('404.html')