from . import credentials,auth,changePassword, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app

from flask_login import logout_user, current_user, login_required
from models.models import Company, DiagnosisCompany,ActionPlan, Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

# Creates Timestamps without UTC for JavaScript handling:
# utcDate.replace(tzinfo=tz.utc).timestamp()
#
# Creates Dates witout UTC for Python handling:
# utcDate.replace(tzinfo=tz.utc).astimezone(tz=None)
import json
@home.route('/te/')
def pasw3():
    app.logger.debug('** SWING_CMS ** - pasw2')
#    auth.ActionCodeSettings(
#        url='innovamujer.ciudadmujer.gob.hn'
#    )
#    va = auth.generate_password_reset_link('consultorvarela@gmail.com')

#    app.logger.debug(va)    

    return render_template("pasw2.html")
import requests

    
@home.route('/pasw2/')
def pasw2():
    app.logger.debug('** SWING_CMS ** - pasw2')
    va = changePassword()
    app.logger.debug(va)    
    return render_template('pasw2.html')

@home.route('/')
def _index():
    app.logger.debug('** SWING_CMS ** - Index')
    return redirect(url_for('home._welcome'))

@home.route('/escuelaempresarial/')
def _aulavirtual():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    return render_template('aulavirtual/home.html')

@home.route('/comunidaddenegocios/')
def _comunidadempresarial():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    return render_template('comunidadempresarial/home.html')

@home.route('/preguntasfrecuentes/')
def _preguntasfrecuentes():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    return render_template('preguntasfrecuentes.html')


@home.route('/acercade/')
def _acercade():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    return render_template('acercade.html')

# Create appointment response
def _appointment_response(details, apptList, cmd = 'for'):
    app.logger.debug('** SWING_CMS ** - Citas Crear Response')
    try:
        if details is not None:
            for record in details:
                usr_for = User.query.filter_by(id = record.created_for).first()
                emp_crt = User.query.filter_by(id = record.created_by).first()
                emp_tab = UserXEmployeeAssigned.query.filter_by(id = record.emp_assigned).first()
                emp_asg = User.query.filter_by(id = emp_tab.employee_id).first()
                service = CatalogServices.query.filter_by(id = record.service_id).first()
                time_sf = record.date_scheduled + td(minutes = service.duration_minutes)
                time_end_local = time_sf.replace(tzinfo=tz.utc).astimezone(tz=None)
                time_start_local = record.date_scheduled.replace(tzinfo=tz.utc).astimezone(tz=None)
                daytime = None
                if time_start_local.hour >= 0 and time_start_local.hour < 6:
                    daytime = 'dawn'
                elif time_start_local.hour >= 6 and time_start_local.hour < 12:
                    daytime = 'morning'
                elif time_start_local.hour >= 12 and time_start_local.hour < 18:
                    daytime = 'evening'
                elif time_start_local.hour >= 18 and time_start_local.hour <= 23:
                    daytime = 'night'
                
                apptList.append({
                    'id': record.id,
                    'appointment_type': cmd,
                    'cancelled': record.cancelled,
                    'created_by': {
                        'name': emp_crt.name
                    },
                    'created_for': {
                        'attended': record.usr_attendance,
                        'name': usr_for.name
                    },
                    'date_created': record.date_created,
                    'date_timestamp': int(record.date_scheduled.replace(tzinfo=tz.utc).timestamp() * 1000),
                    'date_scheduled': format_date(time_start_local, "EEEE, dd 'de' MMMM 'del' yyyy", locale='es').capitalize(),
                    'time_scheduled_start': format_time(time_start_local, "hh:mm a", locale='en'),
                    'time_scheduled_end': format_time(time_end_local, "hh:mm a", locale='en'),
                    'emp_assigned': {
                        'accepted': record.emp_accepted,
                        'attended': record.emp_attendance,
                        'name': emp_asg.name
                    },
                    'service': {
                        'duration': service.duration_minutes,
                        'name': service.name,
                        'name_short': service.name_short,
                        'time_of_day': daytime
                    }
                })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Citas Crear Response Error: {}'.format(e))
        return jsonify({ 'status': 'error' })

@home.route('/appointments/')
@login_required
def _appointments():
    app.logger.debug('** SWING_CMS ** - Citas')
    try:
        dt_today = dt.now(tz.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        response = {
            'appointments_created_by': [],
            'appointments_created_for_e': [],
            'appointments_created_for_u': [],
            'datetime': str(dt_today)
        }

        if current_user.is_user_role(['adm', 'emp']):
            # Get Appointments for Employees (Assigned and Created By)

            # Appointments - created_by
            details_by = Appointments.query.filter(
                Appointments.created_by == current_user.id,
                Appointments.cancelled == False,
                Appointments.date_scheduled >= dt_today
            ).order_by(Appointments.date_scheduled.asc())

            _appointment_response(details_by, response['appointments_created_by'], 'by')

            # Appointments - created_for_e (emp_assigned)
            details_for = Appointments.query.join(UserXEmployeeAssigned).filter(
                Appointments.date_scheduled >= dt_today,
                UserXEmployeeAssigned.user_id == Appointments.created_for,
                UserXEmployeeAssigned.employee_id == current_user.id,
                Appointments.cancelled == False
            ).order_by(Appointments.date_scheduled.asc())

            _appointment_response(details_for, response['appointments_created_for_e'], 'assigned')
        else:
            # Get Appointments for Users (Created For)
            
            # Appointments - created_for_u
            details = Appointments.query.filter(
                Appointments.created_for == current_user.id,
                Appointments.cancelled == False,
                Appointments.date_scheduled >= dt_today
            ).order_by(Appointments.date_scheduled.asc())

            _appointment_response(details, response['appointments_created_for_u'])

        return render_template('appointments.html', appointments=response)
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Citas Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


@home.route('/appointments/create/')
@login_required
def _appointmentscreate():
    app.logger.debug('** SWING_CMS ** - Crear Citas')
    return render_template('appointments_create.html')


@home.route('/appointments/create/admin/')
@login_required
def _appointmentscreateadmin():
    app.logger.debug('** SWING_CMS ** - Crear Citas Admin')
    try:
        srv = CatalogServices.query.filter_by(enabled = True).order_by(CatalogServices.name.asc())
        ids = CatalogIDDocumentTypes.query.filter_by(enabled = True).order_by(CatalogIDDocumentTypes.name.asc())
        return render_template('appointments_create_admin.html', services=srv, ids_docs_types=ids)
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Crear Citas Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


@home.route('/chat/')
def _chat():
    app.logger.debug('** SWING_CMS ** - Try Chat')
    try:
        # Validate if the user has a Valid Session and Redirects
        response = isUserLoggedInRedirect('chat', 'redirect')
        if response is not None:
            return response
        else:
            return render_template('chat.html')
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Try Chat Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


@home.route('/chat/admin/')
@login_required
def _chat_admin():
    app.logger.debug('** SWING_CMS ** - Chat Admin')
    return render_template('chat_admin.html')


@home.route('/chat/home/')
@login_required
def _chat_home():
    app.logger.debug('** SWING_CMS ** - Chat Home')
    return render_template('chat_home.html')


@home.route('/digitalcenter/old')
def _digitalcenter():
    app.logger.debug('** SWING_CMS ** - Digital Center')
    return render_template('digitalcenter.html')



@home.route('/home/')
@login_required
def _home():
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    if current_user.is_authenticated:
        if current_user.is_user_role(['usr']):
            if current_user.extra_info is None or current_user.extra_info.acceptterms == False:
                return redirect(url_for('home._preStart'))
            elif current_user.extra_info.company_id is None:
                return redirect(url_for('digitalcenter.__form_perfil_emp'))
            else:
                #
                return render_template('home_dashboard.html')
        else:
            today = dt.today()
    
            appointments = Appointments.query.filter(Appointments.date_scheduled > today).all()
            appointments = Appointments.query.join(UserXEmployeeAssigned).filter(
        Appointments.date_scheduled > today,
        UserXEmployeeAssigned.user_id == Appointments.created_for,
        UserXEmployeeAssigned.employee_id == current_user.id,
        Appointments.cancelled == False
        ).order_by(Appointments.date_scheduled.asc()).all()
            context = {'appointments':appointments}
            return render_template('home_dashboard_admin.html',**context)
    else:
        return redirect(url_for('home._login'))



@home.route('/pre/')
#@login_required
def _preStart():
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    return render_template('prelogin.html')

@home.route('/login/')
def _login():
    app.logger.debug('** SWING_CMS ** - Login')
    try:
        # Validate if the user has a Valid Session and Redirects
        response = isUserLoggedInRedirect('login', 'redirect')
        if response is not None:
            return response
        else:
            return render_template('login.html')
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Login Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


@home.route('/loginuser/', methods=['POST'])
def _loginuser():
    app.logger.debug('** SWING_CMS ** - Login')
    try:
        # Validate if the user has a Valid Session and Redirects
        response = isUserLoggedInRedirect('loginuser', 'jsonResponse')
        if response is not None: return response
        
        # Login Process
        # Retrieve the uid from the JWT idToken
        app.logger.info('** SWING_CMS ** - LoginUser added: {}'.format('siii'))
        idToken = request.json['idToken']
        decoded_token = auth.verify_id_token(idToken)
        app.logger.info('** SWING_CMS ** - LoginUser added: {}'.format('siii2'))
        usremail = decoded_token['email'] if 'email' in decoded_token else None
        uid = decoded_token['uid'] if usremail != 'admusr@innova.com' else 'INNO-Administrator'
        app.logger.info('** SWING_CMS ** - LoginUser added: {}'.format('siii3'))
        # Search for the user in the DB.
        user = User.query.filter_by(uid = uid).first()
        if user is None:
            # Retrieve Firebase User info
            fibaUser = auth.get_user(uid)
            # Validate Firebase Sign In Provider Data
            fibaData = decoded_token['firebase']
            # Update User Display Name and Email if Sign In Provider is Phone
            if fibaData['sign_in_provider'] == 'phone':
                fibaUserDisplayName = 'Usuari@ ' + fibaUser.phone_number
                fibaUserEmail = uid + '@no-email.org'

                fibaUser = auth.update_user(
                    uid,
                    email = fibaUserEmail,
                    display_name =  fibaUserDisplayName
                )

            # User is not registered on DB. Insert user in DB.
            user = User()
            user.uid = uid
            user.email = fibaUser.email
            user.name = fibaUser.display_name
            user.phonenumber = fibaUser.phone_number
            user.datecreated = dt.now(tz.utc)
            user.cmuserid = 'INNO-' + user.name.strip().upper()[0:1] + user.datecreated.strftime('-%y%m%d-%H%M%S')
            db.session.add(user)
            
            db.session.commit()
            db.session.refresh(user)

            # Add User Role
            user_role = CatalogUserRoles.query.filter_by(name_short='usr').first()
            user_userxrole = UserXRole()
            user_userxrole.user_id = user.id
            user_userxrole.user_role_id = user_role.id
            db.session.add(user_userxrole)

            db.session.commit()

            app.logger.info('** SWING_CMS ** - LoginUser added: {}'.format(user.id))
        
        # Create User Session
        createLoginSession(user)
        
        # Return Session Cookie
        # Set URL depending on role
        url = getUserRedirectURL(user, 'loginuser')
        
        response = createCookieSession(idToken, 'redirectURL', url)
        return response

    except Exception as e:
        app.logger.error('** SWING_CMS ** - LoginUser Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


@home.route('/logoutuser/')
@login_required
def _logoutuser():
    app.logger.debug('** SWING_CMS ** - Logout')
    try:
        # First, user is logged out from Flask Login Session
        logout_user()

        response = make_response(redirect(url_for('home._welcome')))

        # Second, user is logged out from Firebase Cookie Session
        # The Firebase Cookie is cleared
        response.set_cookie(app.config['FIREBASE_COOKIE_NAME'], expires=0)

        return response
    except Exception as e:
        app.logger.error('** SWING_CMS ** - LogoutUser Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


@home.route('/conexioninnova/')
def _conexioninnova():
    app.logger.debug('** SWING_CMS ** - Marketplace')
    return render_template('conexioninnova.html')


@home.route('/offline/')
def _offline():
    app.logger.debug('** SWING_CMS ** - Offline')
    return render_template('offline.html')


@home.route('/politicaprivacidad/')
def _politicaprivacidad():
    app.logger.debug('** SWING_CMS ** - PoliticaPrivacidad')
    return render_template('politicaprivacidad.html')


@home.route('/statistics/')
@login_required
def _statistics():
    app.logger.debug('** SWING_CMS ** - Statistics')
    return render_template('stats.html')


@home.route('/terminosdelservicio/')
def _terminosdelservicio():
    app.logger.debug('** SWING_CMS ** - TerminosDelServicio')
    return render_template('terminosdelservicio.html')


@home.route('/welcome/')
def _welcome():
    app.logger.debug('** SWING_CMS ** - Welcome')
    return render_template('welcome.html')

@home.route('/welcome/2')
def _welcome2():
    app.logger.debug('** SWING_CMS ** - Welcome')
    return render_template('welcome2.html')

@home.route('/base/')
def _base():
    app.logger.debug('** SWING_CMS ** - Welcome')
    return render_template('components.html')


@home.route('/empresaria/')
def _perfil_empresaria():
    app.logger.debug('** SWING_CMS ** - TerminosDelServicio')
    return render_template('empresaria.html')

@home.route('/resumen/')
def _resumen():
    app.logger.debug('** SWING_CMS ** - TerminosDelServicio')
    return render_template('resumen.html')

@home.route('/empresarias/')
def _empresarias():
    app.logger.debug('** SWING_CMS ** - TerminosDelServicio')
    user = User.query.filter_by(id=current_user.id)
    company = Company.query.filter_by(id=current_user.extra_info.company_id).first()
    diagnos = DiagnosisCompany.query.filter_by(company_id=company.id).all()
    actions = ActionPlan.query.filter_by(company_id=company.id).all()
    print(diagnos)
    print(actions)
    direccion_estrategica =  DiagnosisCompany.query.filter(DiagnosisCompany.status == True, DiagnosisCompany.categoria == "Dirección Estratégica", DiagnosisCompany.company_id == company.id).first()
    mercadeo_ventas =  DiagnosisCompany.query.filter(DiagnosisCompany.status == True,DiagnosisCompany.categoria == "Mercadeo y ventas", DiagnosisCompany.company_id == company.id).first()
    madurez_digital =  DiagnosisCompany.query.filter(DiagnosisCompany.status == True,DiagnosisCompany.categoria == "Madurez Digital", DiagnosisCompany.company_id == company.id).first()
    gestion_financiera =  DiagnosisCompany.query.filter(DiagnosisCompany.status == True,DiagnosisCompany.categoria == "Gestión Financiera", DiagnosisCompany.company_id == company.id).first()
    gestion_produccion =  DiagnosisCompany.query.filter(DiagnosisCompany.status == True,DiagnosisCompany.categoria == "Gestión de la producción", DiagnosisCompany.company_id == company.id).first()
    organizacion_gestion =  DiagnosisCompany.query.filter(DiagnosisCompany.status == True,DiagnosisCompany.categoria == "Organización y Gestión del talento humano", DiagnosisCompany.company_id == company.id).first()
    resultado_direccion_estrategica  = direccion_estrategica.result_total 
    total_direccion_estrategica = direccion_estrategica.result_area
    resultado_mercadeo_ventas =  mercadeo_ventas.result_total
    total_mercadeo_ventas =mercadeo_ventas.result_area
    total_madurez_digital = madurez_digital.result_area
    resultado_madurez_digital = madurez_digital.result_total
    total_gestion_financiera = gestion_financiera.result_area
    resultado_gestion_financiera = gestion_financiera.result_total
    total_gestion_produccion = gestion_produccion.result_area
    resultado_gestion_produccion = gestion_produccion.result_total
    total_organizacion_gestion = organizacion_gestion.result_area
    resultado_organizacion_gestion = organizacion_gestion.result_total
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
        'api': company,
        'actions':actions,
        "total_direccion_estrategica":total_direccion_estrategica,
        "total_mercadeo_ventas":total_mercadeo_ventas,
        "total_madurez_digital":total_madurez_digital,
        "total_gestion_financiera":total_gestion_financiera,
        "total_gestion_produccion":total_gestion_produccion,
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
 
    return render_template('home_empresarias.html',**context)
