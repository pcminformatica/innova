from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response,send_from_directory
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import DiagnosisCompany,Inscripciones,ActionPlan,Company,Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import catalogCategory,CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from werkzeug.utils import secure_filename
from sqlalchemy import or_
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


from sqlalchemy import desc
@digitalcenter.route('/servi/',methods=['GET', 'POST'])
def _servi():
    services = CatalogServices.query.filter_by(enabled = 1).order_by(desc(CatalogServices.name_short)).all()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    context = {'services':services}  
    return render_template('servi.html',**context)

@digitalcenter.route('/servi/<int:user_uid>',methods=['GET', 'POST'])
def _servi_detalle(user_uid):
    services = catalogCategory.query.all()
    service = CatalogServices.query.filter_by(id = user_uid).first()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    context = {'services':services,'service':service}  
    return render_template('admindash/formservicios.html',**context)

@digitalcenter.route('/servi/delete/<int:service_id>',methods=['GET', 'POST'])
def _servi_detalle_delete(service_id):
    service = CatalogServices.query.filter_by(id = service_id).delete()
    db.session.commit()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    return redirect(url_for('digitalcenter._servi'))


import requests
import json 
@digitalcenter.route('/diagnosticos/',methods=['GET', 'POST'])
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
                if len(list(e for e in servicios if e['id']  == servicesx.id)) == 0:
                    servicios.append({'id':servicesx.id,'titulo':servicesx.name,'categoria':servicesx.catalog_category})
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
    nombre = api['NOMBRE_EMPRESA']
    rtn = api['RTN']
    company =  Company.query.filter(or_(Company.name == nombre, Company.rtn == rtn)).first()
    if company:

        plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id).all()
        
    else:
        plan = []
    context = {
        'plan':plan,
        'api': api,
        'legalizacion':legalizacion,
        'administracion':administracion,
        'produccion':produccion,
        'financiera':financiera,
        'mercadeo':mercadeo,

    }
   
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


@digitalcenter.route('/datos/12/<int:user_uid>/',methods=['GET', 'POST'])
def _datos_describe_12(user_uid):
    app.logger.debug('** SWING_CMSx ** - ------------------')
    #url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/?format=json"
    url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/{}/?format=json".format(user_uid)
    headers={'Authorization':'token 5690e59a570b717402ac2bcdba1fe02afc8abd85'}
    resp = requests.get(url,headers=headers)
    api = json.loads(resp.content)
    servicios = []
    app.logger.debug('** SWING_CMS ** - ------------------')
    url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/?format=json"
    #url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/202116860/?format=json"
    headers={'Authorization':'token 5690e59a570b717402ac2bcdba1fe02afc8abd85'}
    resp = requests.get(url,headers=headers)
    api1 = json.loads(resp.content)
    for api in api1['results']:
        for resp in api:
            if api[resp] == '1':
                print("Pregunta: {} respuesta: {}".format(resp,api[resp]))
                services = CatalogServices.query.filter(CatalogServices.diagnostic_questions.contains(resp)).all()
                if services:
                    for servicesx in services:
                        departamento =api['DEPARTAMENTO']
                        servi = str(servicesx.id) + '-' + str(departamento)
                        if len(list(e for e in servicios if e['id']  == servi)) == 0:
                            servicios.append({'id':servi,'departamento':departamento,'titulo':servicesx.name + ' ' ,'categoria':servicesx.catalog_category,'total':1,'anterior':api['_id']})
                        else:
                            varl = list(e for e in servicios if e['id']  == servi)[0]
                            index = servicios.index(varl)
                            if servicios[index]['anterior'] != api['_id']:
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

@digitalcenter.route('/registros/im',methods=['GET', 'POST'])
def _registros_im():
    return render_template('registro_im.html')

@digitalcenter.route('/diagnostico/<int:user_uid>/',methods=['GET', 'POST'])
def _datos_diagnostico(user_uid):
    app.logger.debug('** SWING_CMSx ** - ------------------')
    #url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/?format=json"
    url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/{}/?format=json".format(user_uid)
    headers={'Authorization':'token 5690e59a570b717402ac2bcdba1fe02afc8abd85'}
    resp = requests.get(url,headers=headers)
    api = json.loads(resp.content)
    servicios = []
    #preguntas
    direccion_estrategica = ["_1_1","_1_2","_1_3","_1_4","_1_5","_1_6","_1_7","_1_8","_1_9","_1_10","_1_11"]
    mercadeo_ventas = ["_2_1","_2_2","_2_3","_2_4","_2_5","_2_6","_2_7","_2_8", "_2_9", "_2_10", "_2_11", "_2_12","_2_13","_2_14","_2_15","_2_16","_2_17","_2_18","_2_19","_2_20","_2_21","_2_22","_2_23","_2_24","_2_25","_2_26"]
    madurez_digital = ["_3_1","_3_2","_3_3","_3_4","_3_5","_3_6","_3_7","_3_8","_3_9","_3_10","_3_11"]
    gestion_financiera = ["_4_1","_4_2","_4_3","_4_4","_4_5","_4_6","_4_7","_4_8","_4_9","_4_10","_4_11","_4_12","_4_13","_4_14","_4_15","_4_16","_4_17","_4_18","_4_19","_4_20","_4_21" ]
    gestion_produccion = ["_5_1","_5_2","_5_3","_5_4","_5_5","_5_6","_5_7","_5_8","_5_9","_5_10","_5_11","_5_12","_5_13","_5_14","_5_15","_5_16","_5_17","_5_18","_5_19","_5_20","_5_21","_5_22","_5_23","_5_24",]
    organizacion_gestion = ["_6_1","_6_2","_6_3","_6_4","_6_5","_6_6","_6_7","_6_8","_6_9","_6_10","_6_11","_6_12","_6_13","_6_14","_6_15","_6_16" ,"_6_17"]
    
    #1
    respuestas_direccion_estrategica = []
    total_direccion_estrategica = 0
    for clave in direccion_estrategica:
        respuestas_direccion_estrategica.append({clave:api[clave]})
        total_direccion_estrategica = total_direccion_estrategica + int(api[clave])
        print("Pregunta: {} respuesta: {}".format(clave,api[clave]))
    resultado_direccion_estrategica = total_direccion_estrategica/(len(direccion_estrategica)*3) * 0.10 * 100
    resultado_direccion_estrategica = round(resultado_direccion_estrategica, 2)
    #2
    respuestas_mercadeo_ventas = []
    total_mercadeo_ventas = 0
    for clave in mercadeo_ventas:
        respuestas_mercadeo_ventas.append({clave:api[clave]})
        total_mercadeo_ventas = total_mercadeo_ventas + int(api[clave])
        print("Pregunta: {} respuesta: {}".format(clave,api[clave]))
    resultado_mercadeo_ventas = total_mercadeo_ventas/(len(mercadeo_ventas)*3) * 0.25 * 100
    resultado_mercadeo_ventas = round(resultado_mercadeo_ventas, 2)
    #3
    respuestas_madurez_digital = []
    total_madurez_digital = 0
    for clave in madurez_digital:
        respuestas_madurez_digital.append({clave:api[clave]})
        total_madurez_digital = total_madurez_digital + int(api[clave])
        print("Pregunta: {} respuesta: {}".format(clave,api[clave]))
    resultado_madurez_digital = total_madurez_digital/(len(madurez_digital)*3) * 0.10 * 100
    resultado_madurez_digital = round(resultado_madurez_digital, 2)
    #4
    respuestas_gestion_financiera = []
    total_gestion_financiera = 0
    for clave in gestion_financiera:
        respuestas_gestion_financiera.append({clave:api[clave]})
        total_gestion_financiera = total_gestion_financiera + int(api[clave])
        print("Pregunta: {} respuesta: {}".format(clave,api[clave]))
    resultado_gestion_financiera = total_gestion_financiera/(len(gestion_financiera)*3) * 0.25 * 100
    resultado_gestion_financiera = round(resultado_gestion_financiera, 2)
    #5
    respuestas_gestion_produccion = []
    total_gestion_produccion = 0
    for clave in gestion_produccion:
        respuestas_gestion_produccion.append({clave:api[clave]})
        total_gestion_produccion = total_gestion_produccion + int(api[clave])
        print("Pregunta: {} respuesta: {}".format(clave,api[clave]))
    resultado_gestion_produccion = total_gestion_produccion/(len(gestion_produccion)*3) * 0.20 * 100
    resultado_gestion_produccion = round(resultado_gestion_produccion, 2)

    #6
    respuestas_organizacion_gestion = []
    total_organizacion_gestion = 0
    for clave in organizacion_gestion:
        respuestas_organizacion_gestion.append({clave:api[clave]})
        total_organizacion_gestion = total_organizacion_gestion + int(api[clave])
        print("Pregunta: {} respuesta: {}".format(clave,api[clave]))
    resultado_organizacion_gestion = total_organizacion_gestion/(len(organizacion_gestion)*3) * 0.10 * 100
    resultado_organizacion_gestion = round(resultado_organizacion_gestion, 2)

    totaldiagnostico = resultado_direccion_estrategica + resultado_mercadeo_ventas + resultado_madurez_digital + resultado_gestion_financiera + resultado_gestion_produccion + resultado_organizacion_gestion
    totaldiagnostico = round(totaldiagnostico, 2) 
    totalarea =  total_direccion_estrategica + total_mercadeo_ventas + total_madurez_digital + total_gestion_financiera + total_gestion_produccion + total_organizacion_gestion 
    tipo_empresa = "EMPRESA D"
    if totaldiagnostico <= 60:
        tipo_empresa = "EMPRESA D"
    elif totaldiagnostico <= 70:
        tipo_empresa = "EMPRESA C"
    elif totaldiagnostico <= 90:
        tipo_empresa = "EMPRESA B"
    elif totaldiagnostico <= 100:
        tipo_empresa = "EMPRESA D"
    context = {
        'api': api,
        "respuestas_direccion_estrategica":respuestas_direccion_estrategica,
        "total_direccion_estrategica":total_direccion_estrategica,
        "respuestas_mercadeo_ventas":respuestas_mercadeo_ventas,
        "total_mercadeo_ventas":total_mercadeo_ventas,
        "respuestas_madurez_digital":respuestas_madurez_digital,
        "total_madurez_digital":total_madurez_digital,
        "respuestas_gestion_financiera":respuestas_gestion_financiera,
        "total_gestion_financiera":total_gestion_financiera,
        "respuestas_gestion_produccion":respuestas_gestion_produccion,
        "total_gestion_produccion":total_gestion_produccion,
        "respuestas_organizacion_gestion":respuestas_organizacion_gestion,
        "total_organizacion_gestion":total_organizacion_gestion,
        "resultado_direccion_estrategica":resultado_direccion_estrategica,
        "resultado_mercadeo_ventas":resultado_mercadeo_ventas,
        "resultado_madurez_digital":resultado_madurez_digital,
        "resultado_gestion_financiera":resultado_gestion_financiera,
        "resultado_gestion_produccion":resultado_gestion_produccion,
        "resultado_organizacion_gestion":resultado_organizacion_gestion,
        "totaldiagnostico":totaldiagnostico,
        "totalarea":totalarea,
        "tipo_empresa":tipo_empresa
    }
   
    app.logger.debug(servicios)
    app.logger.debug(servicios)
    return render_template('diagnostico.html',**context)

@digitalcenter.route('/elegibles/5',methods=['GET', 'POST'])
def _elegibles_5():
    app.logger.debug('** SWING_CMS ** - ------------------')
    inscripciones = Inscripciones.query.filter_by(elegible = True,cohorte=5).all()
    context = {
        'api': inscripciones
    }
    return render_template('elegibles.html',**context)