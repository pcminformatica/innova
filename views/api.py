from . import auth,crypto_key, db, removeItemFromList, updateItemFromList

from datetime import datetime as dt
from datetime import timezone as tz
from flask import Blueprint, request, url_for, jsonify, make_response
from flask import current_app as app
from flask_login import current_user, login_required
from models.models import CourseManagers,TrainingType,ActionPlanReferences,WalletTransaction,DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Appointments, CatalogIDDocumentTypes, CatalogUserRoles, CatalogServices
from models.models import CompanyMonitoring,ServiceChannel,surveys_sde,catalog_surveys_sde,Evaluations,ModalityType,CompanyStage,EnrollmentRecord,Courses,CompanyStatus,User, UserExtraInfo, UserXEmployeeAssigned, UserXRole,Company
from models.formatjson import JsonPhone, JsonSocial,JsonConfigProfile
from models.diagnostico import Diagnosticos
from sqlalchemy import or_,desc,asc
from views.wallet import _update_wallet
from views.digitalcenter import convertir_a_datetime
import json
from views.email_app import send_email  # Importar la función send_email desde email_app.py
from models.models import default_timezone
api = Blueprint('api', __name__, template_folder='templates', static_folder='static')

# Set the Appointment's Details
@api.route('/api/detail/appointment/', methods = ['POST'])
# @login_required
def _d_appointment():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            usr_id = request.json['uid']
            emp_id = request.json['eid']
            srv_id = request.json['sid']
            sch_date = request.json['sch']
            usr_data = request.json['udata']

            # Update User information
            if usr_data is not None:
                _u_userinfo(usr_data)

            # Get scheduled hours in UTC - Javascript Timestamp needs to be divided by 1000 (miliseconds)
            scheduled_dt = dt.fromtimestamp((sch_date / 1000), tz.utc)
            # Get Service ID
            service = CatalogServices.query.filter_by(name_short = srv_id).first()
            # Get Employee Assigned ID
            employee_assigned = UserXEmployeeAssigned.query.filter_by(
                employee_id = emp_id,
                enabled = True,
                service_id = service.id,
                user_id = usr_id
            ).order_by(UserXEmployeeAssigned.datecreated.desc()).first()

            if employee_assigned is None:
                employee_assigned = UserXEmployeeAssigned()
                employee_assigned.employee_id = emp_id
                employee_assigned.user_id = usr_id
                employee_assigned.service_id = service.id
                db.session.add(employee_assigned)
            
            appointment = Appointments()
            appointment.created_by = current_user.id
            appointment.created_for = usr_id
            appointment.date_scheduled = scheduled_dt
            appointment.emp_assigned = employee_assigned.id
            appointment.service_id = service.id
            if not current_user.is_user_role(['usr']):
                appointment.emp_accepted = True
            db.session.add(appointment)

            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Cita creada' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

# Get the Service's Details
@api.route('/api/detail/service/<string:service_id>/', methods = ['GET'])
# @login_required
def _d_service(service_id = None):
    app.logger.debug('** SWING_CMS ** - API Service Detail')
    try:
        if request.method == 'GET':
            if service_id is not None:
                response = {
                    'break_minutes': None,
                    'duration_minutes': None,
                    'enabled': None,
                    'id': None,
                    'name': None,
                    'name_short': None,
                    'service_user_role': None,
                    'sessions_schedule': None,
                    'status': 404
                }

                detail = CatalogServices.query.filter(CatalogServices.name_short == service_id).first()
                if detail is not None:
                    response['status'] = 200
                    response['id'] = detail.id
                    response['name'] = detail.name
                    response['name_short'] = detail.name_short
                    response['break_minutes'] = detail.break_minutes
                    response['duration_minutes'] = detail.duration_minutes
                    response['sessions_schedule'] = detail.sessions_schedule
                    response['enabled'] = detail.enabled
                    if detail.service_user_role is not None:
                        serv_ur = CatalogServices.query.filter_by(id = detail.service_user_role).first()
                        response['service_user_role'] = serv_ur.name_short

                return jsonify(response)
            else:
                return jsonify({ 'status': 400 })
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Service Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


# Get the User's Details
@api.route('/api/detail/user/<int:user_id>/', methods = ['GET'])
# @login_required
def _d_user(user_id = None):
    app.logger.debug('** SWING_CMS ** - API User Detail')
    try:
        if request.method == 'GET':
            if user_id is not None:
                response = {
                    'alias': None,
                    'birthdate': None,
                    'city': None,
                    'country': None,
                    'email': None,
                    'enabled': None,
                    'id': user_id,
                    'last_names': None,
                    'name': None,
                    'names': None,
                    'national_id': None,
                    'national_id_type': None,
                    'phonenumber': None,
                    'roles': None,
                    'state': None,
                    'status': 404
                }

                detail = User.query.filter(User.id == user_id).first()
                if detail is not None:
                    response['status'] = 200
                    response['id'] = user_id
                    response['name'] = detail.name
                    response['email'] = detail.email
                    response['phonenumber'] = detail.phonenumber
                    response['enabled'] = detail.enabled
                    response['roles'] = detail.get_user_roles(True)
                    if detail.birthdate is not None:
                        response['birthdate'] = detail.birthdate.strftime('%Y-%m-%d')
                    if detail.extra_info is not None:
                        if detail.extra_info.national_id_type is not None:
                            natid = CatalogIDDocumentTypes.query.filter_by(id = detail.extra_info.national_id_type).first()
                            response['national_id_type'] = natid.name_short
                        response['national_id'] = detail.extra_info.national_id
                        response['last_names'] = detail.extra_info.last_names
                        response['names'] = detail.extra_info.names
                        response['alias'] = detail.extra_info.alias
                        response['country'] = detail.extra_info.country
                        response['state'] = detail.extra_info.state
                        response['city'] = detail.extra_info.city
                    if detail.extra_info.company is not None:
                        response['company_rtn'] = detail.extra_info.company.rtn
                        response['company_name'] = detail.extra_info.company.name
                        response['company_description'] = detail.extra_info.company.description
                        response['company_address'] = detail.extra_info.company.address
                        response['company_social_networks'] = detail.extra_info.company.social_networks
                        response['company_phones'] = detail.extra_info.company.phones

                return jsonify(response)
            else:
                return jsonify({ 'status': 400 })
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API User Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


# Get a list of Appointments
@api.route('/api/list/appointments/<string:cmds>/<int:user_id>/', methods = ['GET'])
# @login_required
def _l_appointments(cmds = None, user_id = None):
    app.logger.debug('** SWING_CMS ** - API List Appointments')
    try:
        if request.method == 'GET':
            if cmds is not None and user_id is not None:
                cmd_lst = cmds.split('-')
                dt_today = dt.now(tz.utc).replace(hour=0, minute=0, second=0, microsecond=0)
                
                response = {
                    'appointments': [],
                    'datetime': dt_today,
                    'id': user_id,
                    'status': 404
                }

                for cmd in cmd_lst:
                    details = None
                    
                    if cmd == 'assigned':
                        # Appointments - emp_assigned
                        details = Appointments.query.join(UserXEmployeeAssigned).filter(
                            Appointments.date_scheduled > dt_today,
                            UserXEmployeeAssigned.user_id == Appointments.created_for,
                            UserXEmployeeAssigned.employee_id == user_id,
                            Appointments.cancelled == False
                        ).order_by(Appointments.date_scheduled.asc())
                    elif cmd == 'by':
                        # Appointments - created_by
                        details = Appointments.query.filter(
                            Appointments.created_by == user_id,
                            Appointments.cancelled == False,
                            Appointments.date_scheduled > dt_today
                        ).order_by(Appointments.date_scheduled.asc())
                    elif cmd == 'for':
                        # Appointments - created_for
                        details = Appointments.query.filter(
                            Appointments.created_for == user_id,
                            Appointments.cancelled == False,
                            Appointments.date_scheduled > dt_today
                        ).order_by(Appointments.date_scheduled.asc())
                    
                    if details is not None:
                        response['status'] = 200
                        for record in details:
                            usr_for = User.query.filter_by(id = record.created_for).first()
                            emp_crt = User.query.filter_by(id = record.created_by).first()
                            emp_tab = UserXEmployeeAssigned.query.filter_by(id = record.emp_assigned).first()
                            emp_asg = User.query.filter_by(id = emp_tab.employee_id).first()
                            service = CatalogServices.query.filter_by(id = record.service_id).first()
                            
                            response['appointments'].append({
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
                                'date_scheduled': record.date_scheduled,
                                'emp_assigned': {
                                    'accepted': record.emp_accepted,
                                    'attended': record.emp_attendance,
                                    'name': emp_asg.name
                                },
                                'service': {
                                    'duration': service.duration_minutes,
                                    'name': service.name,
                                    'name_short': service.name_short
                                }
                            })

                return jsonify(response)
            else:
                return jsonify({ 'status': 400 })
            
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API List Appointments Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


# Get a list of Users
@api.route('/api/list/users/', methods = ['GET'])
# @login_required
def _l_users():
    app.logger.debug('** SWING_CMS ** - API List Users')
    try:
        if request.method == 'GET':
            query = request.args.get('qry')
            filters = request.args.get('flt')
            filters_type = request.args.get('ft')

            if query is not None:
                ulist, total = User.search(query, 1, 9)

                # Check if there is a User Role Filter parameter and Filter by it
                if filters is not None and filters != '':
                    userRolesFilters = filters.split('-')
                    
                    # Check if the Filters are of type Servie User Role
                    filters_type = 'sur'
                    if filters_type is not None and filters_type == 'sur':
                        newUserRolesFilters = []
                        
                        services = CatalogServices.query.filter(CatalogServices.name_short.in_(userRolesFilters))
                        for service in services:
                            user_role = CatalogUserRoles.query.filter(CatalogUserRoles.id == service.service_user_role).first()
                            if user_role is not None:
                                newUserRolesFilters.append(user_role.name_short)
                        
                        userRolesFilters = newUserRolesFilters

                    ulistFiltered = []
                    for user in ulist:
                        ulistFiltered.append(user)
                
                            
                    ulist = ulistFiltered
                    total = len(ulistFiltered)

                response = {
                    'r_filter': filters,
                    'r_total': total,
                    'records': [],
                    'status': 404
                }

                if total > 0:
                    response['status'] = 200
                    for usr in ulist:
                        response['records'].append({
                            'u_id': usr.id,
                            'u_name': usr.name,
                            'u_email': usr.email
                        })

                return jsonify(response)
            else:
                return jsonify({ 'status': 400 })
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API List Users Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


# Update User Info
def _u_userinfo(js):
    app.logger.debug('** SWING_CMS ** - API Save User Info')
    try:
        user = User.query.filter_by(id = js['id']).first()
        
        if user.extra_info is None:
            user_extra = UserExtraInfo()
            user_extra.id = user.id
            
            db.session.add(user_extra)
            db.session.commit()
            db.session.refresh(user)
        
        user.extra_info.alias = js['alias']
        user.extra_info.names = js['names']
        user.extra_info.last_names = js['last_names']
        user.extra_info.country = js['country']
        user.extra_info.state = js['state']
        user.extra_info.city = js['city']
        if js['national_id_type'] is not None:
            natid = CatalogIDDocumentTypes.query.filter_by(name_short = js['national_id_type']).first()
            user.extra_info.national_id = js['national_id']
            user.extra_info.national_id_type = natid.id

        if js['birthdate'] is not None:
            date_format = '%Y-%m-%d'
            user.birthdate = dt.strptime(js['birthdate'], date_format)
        user.phonenumber = js['phonenumber']
        
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Save User Info Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

# Set the Appointment's Details
@api.route('/api/accept/terminos/', methods = ['POST'])
@login_required
def _d_accept_terms():
    app.logger.debug('** SWING_CMS ** - API acceptterms')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            user = User.query.filter_by(id = current_user.id).first()
        
            if user.extra_info is None:
                user_extra = UserExtraInfo()
                user_extra.id = user.id
                user_extra.acceptterms = True
                db.session.add(user_extra)
                db.session.commit()
                db.session.refresh(user)
            # Update User information

            return jsonify({ 'status': 200, 'msg': 'Cita creada' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API acceptterms Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/perfil/', methods = ['POST'])
@login_required
def _d_():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            user = User.query.filter_by(id = current_user.id).first()
    
            if user.extra_info is None:
                user_extra = UserExtraInfo()
                user_extra.id = user.id
                user_extra.acceptterms = True
                db.session.add(user_extra)
                db.session.commit()
                db.session.refresh(user)

            if user.extra_info.company_id is None:
                company = Company()
            else:
                company = Company.query.filter_by(id = user.extra_info.company_id).first()

            company_phone = request.json['txt_company_phone']
            company_facebook = request.json['txt_company_facebook']
            company_instagram = request.json['txt_company_instagram']
            jsPhones = {
                'phone':company_phone if company_phone else ''
            }
            jsSocial = {
                'facebook':company_facebook if company_facebook else '',
                'instagram':company_instagram if company_instagram else '',
            }
            
            company.name = request.json['txt_company_name']
            company.rtn = request.json['txt_company_rtn']
            company.address = request.json['txt_company_address']
            company.description = request.json['txt_company_description']
            company.phones = jsPhones
            company.social_networks = jsSocial
            company.public = request.json['txt_company_public']
            db.session.add(company)
            db.session.commit()
            user.extra_info.national_id = request.json['txt_dni']
            user.extra_info.names = request.json['txt_name']
            user.extra_info.last_names = request.json['txt_last']
            user.extra_info.company = company
            txt_Departamento = request.json['txt_depto']
            jsDepto = {'title':txt_Departamento}
            txt_Municipio = request.json['txt_municipio']
            jsMunicipio = {'title':txt_Municipio}
            user.extra_info.country = jsDepto
            user.extra_info.state = jsMunicipio
            db.session.add(user)
            db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/sde/perfil/', methods = ['POST'])
# @login_required
def _d_sde():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            user = User.query.filter_by(id = current_user.id).first()
        
            if user.extra_info is None:
                user_extra = UserExtraInfo()
                user_extra.id = user.id
                user_extra.acceptterms = True
                db.session.add(user_extra)
                db.session.commit()
                db.session.refresh(user)

            txt_bio_expertise = request.json['txt_bio_expertise']
    
            txt_occupation = request.json['txt_occupation']
            txt_office_hours = request.json['txt_office_hours']
            txt_LinkedIN = request.json['txt_LinkedIN']
            txt_bio_description = request.json['txt_bio_description']
            jsbio= {
                'occupation':txt_occupation if txt_occupation else '',
                'office_hours':txt_office_hours if txt_office_hours else '',
                'linkedIN':txt_LinkedIN if txt_LinkedIN else '',
                'description':txt_bio_description if txt_bio_description else '',
                'expertise':txt_bio_expertise if txt_bio_expertise else '',
                
            }
            txt_Departamento = request.json['txt_Departamento']
            jsDepto = {'title':txt_Departamento}
            txt_Municipio = request.json['txt_Municipio']
            jsMunicipio = {'title':txt_Municipio}


            user.extra_info.national_id = request.json['txt_dni']
            user.extra_info.names = request.json['txt_name']
            user.extra_info.last_names = request.json['txt_last']
            user.extra_info.biography = jsbio
            user.extra_info.profession_id = request.json['txt_profession']
            user.extra_info.country = jsDepto
            user.extra_info.state = jsMunicipio
            user.phonenumber = request.json['txt_phone']
            db.session.add(user)
            db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/save/user/admin', methods = ['POST'])
# @login_required
def _d_save_admin_user():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_id = request.json['txt_id']
            user = User.query.filter_by(id = txt_id).first()
            txt_name = request.json['txt_name']
            txt_email = request.json['txt_email']
            txt_rol = request.json['txt_rol']
            txt_cobotoolbox = request.json['txt_cobotoolbox']
            user.email = txt_email
            user.name = txt_name
            jsconfig = JsonConfigProfile()
            jsconfig.kobotoolbox_access = txt_cobotoolbox.split(',')
            user.extra_info.kobotoolbox = jsconfig.jsonFormat()
            if UserXRole.query.filter_by(user_id = user.id).first():
                xrol = UserXRole.query.filter_by(user_id = user.id).first()
                xrol.user_role_id = txt_rol
                db.session.add(xrol)
            db.session.add(user)
            db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

from datetime import datetime


@api.route('/api/save/app', methods = ['POST'])
# @login_required
def _d_save_admin():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            servicio = CatalogServices.query.filter_by(id = 1).first()
            scheduled_dt = request.json['scheduled_dt']
            emp_id = request.json['emp_id']
            scheduled_dt = datetime.strptime(scheduled_dt, '%Y-%m-%d %H:%M')

            employee_assigned = UserXEmployeeAssigned()
            employee_assigned.employee_id = emp_id
            employee_assigned.user_id = current_user.id
            db.session.add(employee_assigned)
            db.session.commit()
            
            appointment = Appointments()
            appointment.created_by = current_user.id
            appointment.created_for = current_user.id
            appointment.date_scheduled = scheduled_dt
            appointment.emp_assigned = employee_assigned.id
            appointment.service_id = servicio.id
            db.session.add(appointment)
            db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/save/appointment/admin', methods = ['POST'])
# @login_required
def _save_admin_appointment():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            scheduled_dt = request.json['scheduled_dt']
            emp_id = request.json['emp_id']
            usr_id = request.json['usr_id']
            app_service_id = request.json['app_service_id']
            
            servicio = CatalogServices.query.filter_by(id = app_service_id).first()
            scheduled_dt = datetime.strptime(scheduled_dt, '%Y-%m-%d %H:%M')
            emp = User.query.filter_by(id = emp_id).first()
            usr = User.query.filter_by(id = usr_id).first()

            employee_assigned = UserXEmployeeAssigned()
            employee_assigned.employee_id = emp.id
            employee_assigned.user_id = usr.id
            db.session.add(employee_assigned)
            db.session.commit()
            
            appointment = Appointments()
            appointment.created_by = current_user.id
            appointment.created_for = usr.id
            appointment.date_scheduled = scheduled_dt
            appointment.emp_assigned = employee_assigned.id
            appointment.service_id = servicio.id
            db.session.add(appointment)
            db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/save/config/calendar', methods = ['POST'])
# @login_required
def _d_save_config_calendar():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            user = User.query.filter_by(id = current_user.id).first()
            config_json = request.json['config_json']
            user.extra_info.config =config_json
            db.session.add(user)
            db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
                        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

#consultar el calendario del especialista
@api.route('/api/sde/calendar', methods = ['POST'])
# @login_required
def _d_calendar_sde():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    dt_today = '2023-01-20 10:00:00'
    try:
        # POST:
        if request.method == 'POST':
            date = request.json['date']
            emp_id = request.json['emp_id']
            details = Appointments.query.join(UserXEmployeeAssigned).filter(
        Appointments.date_scheduled > date,
        UserXEmployeeAssigned.user_id == Appointments.created_for,
        UserXEmployeeAssigned.employee_id == emp_id,
        Appointments.cancelled == False
        ).order_by(Appointments.date_scheduled.asc()).all()
            dates = []
            if len(details)!=0:
                for detail in details:
                    #dates.append(detail.date_scheduled.strftime("%Y-%m-%d %H:%M:%S"))
                    dates.append(detail.date_scheduled.strftime("%Y-%m-%d %H:%M:%S"))
            
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con','citas':dates })
                        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })
    

# Get a list of Users or company
@api.route('/api/list/users/company', methods = ['GET','POST'])
# @login_required
def _l_users_company():
    app.logger.debug('** SWING_CMS ** - API List Users')
    try:
        if request.method == 'POST':
            query= request.json['query']
            search = "%{}%".format(query)
            ulist = User.query.filter(User.name.like('%e%')).all()[:2]
            ulist = User.query.join(UserExtraInfo, User.id==UserExtraInfo.id)\
                .join(Company, Company.id==UserExtraInfo.company_id)\
                .join(UserXRole, UserXRole.user_id==User.id)\
                .filter(or_(UserExtraInfo.last_names.like(search),\
                    UserExtraInfo.names.like(search),UserExtraInfo.national_id.like(search),\
                    Company.rtn.like(search),Company.name.like(search),
                    User.name.like(search),User.email.like(search),User.phonenumber.like(search),
                     ))\
                .filter(UserXRole.user_role_id == 1)\
                .all()[:9]
            total = len(ulist)
            response = {
                'r_filter': 'usr',
                'r_total': total,
                'records': [],
                'status': 404
            }

            if total > 0:
                response['status'] = 200
                for usr in ulist:
                    response['records'].append({
                        'u_id': usr.id,
                        'u_name': usr.name,
                        'u_email': usr.email
                    })
            return jsonify(response)
 
        else:
            return jsonify({ 'status': 400 })
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API List Users Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


# Get a list of Users employees
@api.route('/api/list/users/employees', methods = ['GET','POST'])
# @login_required
def _l_users_emp():
    app.logger.debug('** SWING_CMS ** - API List Users')
    try:
        if request.method == 'POST':
            query= request.json['query']
            search = "%{}%".format(query)
            ulist = User.query.filter(User.name.like('%e%')).all()[:2]
            ulist = User.query.join(UserExtraInfo, User.id==UserExtraInfo.id)\
                .join(Company, Company.id==UserExtraInfo.company_id)\
                .join(UserXRole, UserXRole.user_id==User.id)\
                .filter(or_(UserExtraInfo.last_names.like(search),\
                    UserExtraInfo.names.like(search),UserExtraInfo.national_id.like(search),\
                    Company.rtn.like(search),Company.name.like(search),
                    User.name.like(search),User.email.like(search),User.phonenumber.like(search),
                     ))\
                .filter(UserXRole.user_role_id != 1)\
                .all()[:9]
            total = 10
            response = {
                'r_filter': query,
                'r_total': 10,
                'records': [],
                'status': 404
            }

            if total > 0:
                response['status'] = 200
                for usr in ulist:
                    response['records'].append({
                        'u_id': usr.id,
                        'u_name': usr.name,
                        'u_email': usr.email
                    })
            return jsonify(response)
 
        else:
            return jsonify({ 'status': 400 })
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API List Users Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/save/user/service', methods = ['POST'])
# @login_required
def _d_save_admin_servi():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_id = request.json['txt_id']
            user = CatalogServices.query.filter_by(id = txt_id).first()
            txt_name = request.json['txt_name']
            txt_rol = request.json['txt_rol']
            txt_tiempo_asesoria = request.json['txt_tiempo_asesoria']
            txt_tiempo_ejecucion = request.json['txt_tiempo_ejecucion']
            txt_costo = request.json['txt_costo']
            txt_costo_innova = request.json['txt_costo_innova']            
            txt_diagnostic_questions = request.json['txt_diagnostic_questions']
            user.name = txt_name
            user.catalog_category = int(txt_rol)
            user.advisory_time = int(txt_tiempo_asesoria)
            user.execution_time = int(txt_tiempo_ejecucion)
            user.cost =float(txt_costo)
            user.cost_innova = float(txt_costo_innova)
            user.diagnostic_questions =  txt_diagnostic_questions
            db.session.add(user)
            db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

import requests

@api.route('/api/inscripciones/', methods = ['POST'])
# @login_required
def _d_inscripciones():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            preguntas = request.json['preguntas']
            
           
            elegible = True
            #evaluar elegible
             #cargo de relevancia
            cargo = list(e for e in preguntas if e['id']  == '2_6')[0]['respuesta']
            if "Accionista minotaria" in cargo:
                elegible = False
            #cargo de relevancia
            tiempo = list(e for e in preguntas if e['id']  == '3_11')[0]['respuesta']
            if int(tiempo) < 1:
                elegible = False
            #3_17 
            tiempo_completo = list(e for e in preguntas if e['id']  == '3_17')[0]['respuesta']

            #3_18
            temp_tiempo_completo = list(e for e in preguntas if e['id']  == '3_18')[0]['respuesta']
            mujeres = tiempo_completo["u_total_mujer"]
            hombres =tiempo_completo["u_total_hombre"]
            total = int(mujeres) + int(hombres)
            if total < 2:
                elegible = False
            temp_mujeres = temp_tiempo_completo["temp_total_mujer"]
            temp_hombres = temp_tiempo_completo["temp_total_hombre"]
            temp_total = (int(temp_mujeres) + int(temp_hombres))
            totales = total + temp_total
            if totales <= 4:
                elegible = False
            inscripcion = Inscripciones()
            dni = list(e for e in preguntas if e['id']  == '1_2')[0]['respuesta']
            inscripcion.name = list(e for e in preguntas if e['id']  == '1_1')[0]['respuesta']
            inscripcion.company_name = list(e for e in preguntas if e['id']  == '3_1')[0]['respuesta']
            inscripcion.correo = list(e for e in preguntas if e['id']  == '1_8')[0]['respuesta']
            inscripcion.phone = list(e for e in preguntas if e['id']  == '1_3')[0]['respuesta']
            inscripcion.cohorte = 5
            inscripcion.dni = dni.replace("-", "")
            inscripcion.departamento = list(e for e in preguntas if e['id']  == '1_4')[0]['respuesta']
            inscripcion.municipio = list(e for e in preguntas if e['id']  == '1_5')[0]['respuesta']
            inscripcion.rtn = list(e for e in preguntas if e['id']  == '1_2')[0]['respuesta']
            inscripcion.respuestas = preguntas
            inscripcion.status = 1
            inscripcion.elegible = elegible
            db.session.add(inscripcion)
            db.session.commit()
            try:
                #enviar    
                if elegible: 
                    url = 'http://inscripciones.ciudadmujer.gob.hn/inscribite/web/acepta/'
                    myobj = {'txt_Correo': list(e for e in preguntas if e['id']  == '1_8')[0]['respuesta']}
                    x = requests.post(url, data = myobj)
                else:
                    url = 'http://inscripciones.ciudadmujer.gob.hn/inscribite/web/no/web'
                    myobj = {'txt_Correo': list(e for e in preguntas if e['id']  == '1_8')[0]['respuesta']}
                    x = requests.post(url, data = myobj)
            
            except Exception as e:
                #enviar
                app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/action/plan/', methods = ['POST'])
# @login_required
def _d_save_ActionPlan():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':

            txt_company_id = request.json['txt_company_id']
            txt_identidad = request.json['txt_identidad']
            services = request.json['services']
            company =  Company.query.filter(or_(Company.dni == txt_identidad.replace("-", ""), Company.id == txt_company_id)).first()
            if not company:
                return jsonify({ 'status': 'error', 'msg': 'Empresa no encontrada' })
            services = json.loads(services)
            for service in services:
                actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service['service'],fase=service['fase'],cancelled=False).first()
                service_plan = CatalogServices.query.filter_by(id=int(service['service'])).first()
                if not actionplan:
                    actionplan = ActionPlan()
                    actionplan.company_id = company.id
                    actionplan.company = company
                    actionplan.date_scheduled_start = service['fecha_inicio']
                    actionplan.date_scheduled_end = service['fecha_final']
                    actionplan.services_id = service_plan.id
                    actionplan.created_by = current_user.id
                    actionplan.fase = service['fase']
                    actionplan.descripcion = service['comentario']
                    db.session.add(actionplan)
                    wallet = WalletTransaction()
                    wallet.amount = service_plan.cost_innova
                    wallet.company_id =company.id
                    wallet.services_id = service_plan.id
                    wallet.created_by = current_user.id
                    wallet.status = 2
                    wallet.type = 1
                    db.session.add(wallet)
                    db.session.commit()
            # Verificar si la empresa tiene al menos un registro en ActionPlan con fase no igual a 0
            has_non_zero_phase = ActionPlan.query.filter(
                ActionPlan.company_id == company.id,
                ActionPlan.cancelled != True,  # Filtrar registros donde 'cancelled' no sea verdadero
                ActionPlan.fase != 0
            ).first()

            if has_non_zero_phase:
                # Obtener el primer registro de ActionPlan de la empresa que cumple con el requisito
                first_action_plan = ActionPlan.query.filter(
                    ActionPlan.company_id == company.id,
                    ActionPlan.cancelled != True,  # Filtrar registros donde 'cancelled' no sea verdadero
                    ActionPlan.fase != 0
                ).order_by(ActionPlan.date_created.asc()).first()

                # Imprimir las fechas date_created y date_scheduled_start del primer registro
                if not company.have_action_plan:
                    company.have_action_plan = True
                    company.date_action_plan = first_action_plan.date_created
                    company.date_first_service_action_plan = first_action_plan.date_scheduled_start
                    action_plans = ActionPlan.query.filter(
                        ActionPlan.company_id == company.id,
                        ActionPlan.fase == 1,
                        ActionPlan.cancelled != True  # Filtrar registros donde 'cancelled' no sea verdadero
                    ).all()
                    # Calcular la suma de progreso y la cantidad de ActionPlan
                    total_progress = sum(action_plan.progress for action_plan in action_plans)  + 200
                    num_action_plans = len(action_plans) + 2

                    # Calcular el promedio de avance total y redondearlo a dos decimales máximo
                    average_progress = round(total_progress / num_action_plans, 2) if num_action_plans > 0 else 0
                    company.action_plan_progress = average_progress
                    if average_progress == 100.0:
                        stage = CompanyStage.query.filter_by(name_short='E3').first()
                        company.stage_id = stage.id
                    db.session.add(company)
                    db.session.commit()
            actualizar = _update_wallet(company.id)
            if actualizar:
                return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
                
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })



import copy
@api.route('/api/save/diagnosis/company/', methods = ['POST'])
@login_required
def _d_save_DiagnosisCompany():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_code = request.json['txt_code']
            url = app.config.get('KOBOTOOLBOX_VIEW').format(txt_code)
            headers=  app.config.get('KOBOTOOLBOX_TOKEN')
            resp = requests.get(url,headers=headers)
            api = json.loads(resp.content)
            identidad = api['IDENTIDAD'].replace("-", "")
            fecha_string = api['_submission_time']
            company =  Company.query.filter(Company.dni == identidad).first()
            if not company:
                return jsonify({ 'status': 201, 'dni': identidad })

            diagnosis =  DiagnosisCompany.query.filter(DiagnosisCompany.company_id == company.id).first()
            if not diagnosis:
                diagnostico = Diagnosticos()
                resultados  = diagnostico.calcular_area(api)
                diagnosis =  DiagnosisCompany()
                diagnosis.company_id = company.id
                diagnosis.respuestas = api
                diagnosis.resultados =  json.loads( str(resultados))
                diagnosis.created_by = current_user.id
                fecha_datetime = convertir_a_datetime(fecha_string)
                if fecha_datetime:
                    diagnosis.date_created = fecha_datetime
                db.session.add(diagnosis)

                update =  Company.query.filter(Company.id == company.id).first()
                status = CompanyStatus.query.filter_by(name_short='6').first()
                update.status_id = status.id
                db.session.add(update)
            
                db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
        


                    
        return jsonify({ 'status': 243, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/action/plan/history/', methods = ['POST'])
@login_required
def _d_save_ActionPlanHistory():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_comentario = request.json['txt_comentario']
            txt_porcentaje = request.json['txt_porcentaje']
            txt_finalizo = request.json['txt_finalizo']
            txt_servicios = request.json['txt_servicios']
            txt_fecha = request.json['txt_fecha']
            txt_url = request.json['txt_url']
            txt_hora = request.json['txt_hora']
            txt_modality = request.json['txt_modality'] 
            if int(txt_porcentaje) > 100:
                return jsonify({ 'status': 201, 'msg': 'Perfil actulizado con' })
            plan = ActionPlan.query.filter_by(id = txt_servicios).first()
            historys = ActionPlanHistory.query.filter_by(action_plan_id=plan.id)
            #Recorremos el porcentaje actual del servicio
            porcentaje = 0
            for history in historys:
                porcentaje = porcentaje + history.progress
            #sumamos el porcentaje actual + el porcentaje de la nueva asesoria
            porcentaje = porcentaje + int(txt_porcentaje)
            #Si el porcentaje es mayor a 100 lanzamos el error
            if porcentaje > 10000:
                return jsonify({ 'status': 201, 'msg': 'Perfil actulizado con' })
            
            history =  ActionPlanHistory()
            history.created_by = current_user.id 
            history.description = txt_comentario
            history.progress = txt_porcentaje
            history.action_plan_id = txt_servicios
            history.endservices = txt_finalizo
            history.date_created = txt_fecha
            history.url = txt_url
            history.advisory_time = txt_hora
            if txt_modality:
                modality = ModalityType.query.filter_by(name_short=txt_modality).first()
                history.id_modality_type = modality.id
                
            db.session.add(history)
            db.session.commit()
           
            if porcentaje > 100:
                plan.progress =100
            else:
                plan.progress =porcentaje
            db.session.add(plan)
            db.session.commit()

            company = Company.query.filter_by(id = plan.company_id).first()
            action_plans = ActionPlan.query.filter(
                ActionPlan.company_id == company.id,
                ActionPlan.fase == 1,
                ActionPlan.cancelled != True  # Filtrar registros donde 'cancelled' no sea verdadero
            ).all()

            # Calcular la suma de progreso y la cantidad de ActionPlan
            total_progress = sum(action_plan.progress for action_plan in action_plans) + 200
            num_action_plans = len(action_plans) + 2

            # Calcular el promedio de avance total y redondearlo a dos decimales máximo
            average_progress = round(total_progress / num_action_plans, 2) if num_action_plans > 0 else 0
            company.action_plan_progress = average_progress
            if average_progress == 100.0:
                stage = CompanyStage.query.filter_by(name_short='E3').first()
                company.stage_id = stage.id
            db.session.add(company)
            db.session.commit()

            if txt_finalizo == True and porcentaje == 100:
                wallet = WalletTransaction.query.filter_by(company_id = plan.company_id, services_id =plan.services_id).first()
                if not wallet:
                    wallet = WalletTransaction()
                    wallet.amount = plan.services.cost_innova
                    wallet.company_id =plan.company_id
                    wallet.services_id = plan.services.id
                    wallet.created_by = current_user.id
                    wallet.status = 1
                    wallet.type = 1
                    db.session.add(wallet)
                    db.session.commit()
                else:
                    wallet.status = 1
                    db.session.add(wallet)
                    db.session.commit()
                actualizar = _update_wallet(plan.company_id)
                areas_mejoras = plan.services.diagnostic_questions
                diagnos = DiagnosisCompany.query.filter_by(company_id=company.id,status=True).order_by(desc(DiagnosisCompany.date_created)).first()
                api = diagnos.respuestas
                for area_mejora in areas_mejoras:
                    clave = area_mejora['id'] 
                    if clave in api:
                        api[clave] = 3
                # nuevo diagnosticos activado
                diagnostico = Diagnosticos()
                resultados  = diagnostico.calcular_area(api)
                diagnosis =  DiagnosisCompany()
                diagnosis.company_id = company.id
                diagnosis.respuestas = api
                diagnosis.resultados =  json.loads( str(resultados))
                diagnosis.created_by = current_user.id
                db.session.add(diagnosis)
                db.session.commit()
                # anterior diagnosticos desactivado
                diagnos.status = False
                db.session.add(diagnos)
                db.session.commit()
                return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
                                          

        return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/save/action/plan/history/update', methods = ['POST'])
@login_required
def _d_save_ActionPlanHistory_update():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_comentario = request.json['txt_comentario']
            txt_porcentaje = request.json['txt_porcentaje']
            txt_finalizo = request.json['txt_finalizo']
            txt_servicios = request.json['txt_servicios']
            txt_fecha = request.json['txt_fecha']
            txt_url = request.json['txt_url']
            txt_hora = request.json['txt_hora']
            txt_modality = request.json['txt_modality'] 
            #buscamos el historial a actulizar
            historyUpdate =  ActionPlanHistory.query.filter(ActionPlanHistory.id==txt_servicios).first()
            #buscamos el plan de accion que deseamos actulizar
            plan = ActionPlan.query.filter_by(id = historyUpdate.action_plan_id).first()
            #buscamos todos los historias que tengan que ver con el plan de accion
            historys = ActionPlanHistory.query.filter_by(action_plan_id=plan.id)
            #Recorremos el porcentaje actual del servicio
            porcentaje = 0
            for history in historys:
                #si el historial no es el que estamos actulizando lo sumamos para optener el porcentaje de avance actual
                if historyUpdate.id != history.id:
                    porcentaje = porcentaje + history.progress
            #sumamos el porcentaje actual + el porcentaje de la asesoria que estamos editando
            porcentaje = porcentaje + int(txt_porcentaje)
            #Si el porcentaje es mayor a 100 lanzamos el error
            if porcentaje > 10000:
                return jsonify({ 'status': 201, 'msg': 'Perfil actulizado con' })

            historyUpdate.created_by = current_user.id 
            historyUpdate.description = txt_comentario
            historyUpdate.progress = txt_porcentaje
            historyUpdate.endservices = txt_finalizo
            historyUpdate.date_created = txt_fecha
            historyUpdate.url = txt_url
            historyUpdate.advisory_time = txt_hora
            if txt_modality:
                modality = ModalityType.query.filter_by(name_short=txt_modality).first()
                historyUpdate.id_modality_type = modality.id
            db.session.add(historyUpdate)
            db.session.commit()
            if porcentaje > 100:
                plan.progress =100
            else:
                plan.progress =porcentaje
            db.session.add(plan)
            db.session.commit()
            company = Company.query.filter_by(id = plan.company_id).first()
            action_plans = ActionPlan.query.filter(
                ActionPlan.company_id == company.id,
                ActionPlan.fase == 1,
                ActionPlan.cancelled != True  # Filtrar registros donde 'cancelled' no sea verdadero
            ).all()

            # Calcular la suma de progreso y la cantidad de ActionPlan
            total_progress = sum(action_plan.progress for action_plan in action_plans) + 200
            num_action_plans = len(action_plans) + 2

            # Calcular el promedio de avance total y redondearlo a dos decimales máximo
            average_progress = round(total_progress / num_action_plans, 2) if num_action_plans > 0 else 0
            company.action_plan_progress = average_progress
            if average_progress == 100.0:
                stage = CompanyStage.query.filter_by(name_short='E3').first()
                company.stage_id = stage.id

            db.session.add(company)
            db.session.commit()
            if txt_finalizo == True and porcentaje == 100:
                wallet = WalletTransaction.query.filter_by(company_id = plan.company_id, services_id =plan.services_id).first()
                if not wallet:
                    wallet = WalletTransaction()
                    wallet.amount = plan.services.cost_innova
                    wallet.company_id =plan.company_id
                    wallet.services_id = plan.services.id
                    wallet.created_by = current_user.id
                    wallet.status = 1
                    wallet.type = 1
                    db.session.add(wallet)
                    db.session.commit()
                else:
                    wallet.status = 1
                    db.session.add(wallet)
                    db.session.commit()
                actualizar = _update_wallet(plan.company_id)
  

                areas_mejoras = plan.services.diagnostic_questions
                diagnos = DiagnosisCompany.query.filter_by(company_id=company.id,status=True).order_by(desc(DiagnosisCompany.date_created)).first()
                api = diagnos.respuestas
                for area_mejora in areas_mejoras:
                    clave = area_mejora['id'] 
                    if clave in api:
                        api[clave] = 3
                # nuevo diagnosticos activado
                diagnostico = Diagnosticos()
                resultados  = diagnostico.calcular_area(api)
                diagnosis =  DiagnosisCompany()
                diagnosis.company_id = company.id
                diagnosis.respuestas = api
                diagnosis.resultados =  json.loads( str(resultados))
                diagnosis.created_by = current_user.id
                db.session.add(diagnosis)
                db.session.commit()
                # anterior diagnosticos desactivado
                diagnos.status = False
                db.session.add(diagnos)
                db.session.commit()
                return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
                                          

        return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        print(e)
        print(e)
        print(e)
        app.logger.error('** SWING_CMS ** - xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })



@api.route('/api/save/user/company/admin', methods = ['POST'])
@login_required
def _d_save_admin_company():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_id = request.json['txt_id']
            user = User.query.filter_by(id = txt_id).first()
            txt_company = request.json['txt_company']
            company = Company.query.filter_by(id = txt_company).first()
            user.extra_info.company = company
            db.session.add(user)
            db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })
    
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

from flask_mail import Message
from . import mail  # Importar la instancia de Flask-Mail desde __init__.py
@api.route('/create/company/user',methods=['GET', 'POST'])
def _diagnosis_monitoring_lisst():
    app.logger.debug('** SWING_CMS ** - ------------------')
    try:
        if request.method == 'POST':
            txt_email = request.json['txt_email'].strip()
            txt_name = request.json['txt_name'].strip()
            txt_company_id = request.json['txt_company_id'] 
            txt_password = generar_contraseña_temporal()  # Agregar campo de contraseña en el formulario
            # Verificar si el correo ya existe

            try:
                existing_user = auth.get_user_by_email(txt_email)
            except Exception as e:
                existing_user = False
            existing_email = User.query.filter_by(email = txt_email).first()
            # Si el correo existe, retorna un JSON con un mensaje de error
            if existing_user or existing_email:
                return jsonify({'status': 201, 'msg': 'Correo ya existe'})
            # Crea el usuario en Firebase Authentication
            fibaUser = auth.create_user(
                email=txt_email,
                display_name=txt_name,
                password=txt_password,  # Utiliza la contraseña proporcionada por el usuario
                disabled=False)


            # Envía un correo electrónico al usuario con la información de inicio de sesión
            msg = Message('Bienvenida a la plataforma Innova Mujer Honduras', sender='infoinnova@ciudadmujer.gob.hn', recipients=[txt_email])
            # Contenido del correo electrónico con formato HTML
            msg.html = f'''
                <p>Estimada empresaria,</p>
                <p>¡Felicitaciones! Ahora tienes tu propio usuario en nuestra plataforma Innova Mujer Honduras.</p>
                <p>Para acceder a tu cuenta, utiliza la siguiente información:</p>
                <ul>
                    <li><strong>Correo Electrónico:</strong> {txt_email}</li>
                    <li><strong>Contraseña:</strong> <em>{txt_password}</em></li>
                </ul>
                <p>Puedes iniciar sesión en la plataforma Innova Mujer Honduras a través del siguiente enlace:</p>
                <p><a href="https://innova.ciudadmujer.gob.hn/login/">Iniciar Sesión</a></p>
                <p>Si no solicitaste un usuario o restablecimiento de contraseña, no dudes en ignorar este correo electrónico con confianza.</p>
                <p>Gracias por unirte a nosotras y ser parte de Innova Mujer Honduras.</p>
                <p>Atentamente,</p>
                <p>Equipo INNOVA MUJER HONDURAS</p>
            '''
            
            print('Sucessfully created new user: {0}'.format(fibaUser.uid))
            print('Sucessfully created new user: {0}'.format(fibaUser.email))
            user = User.query.filter_by(uid = fibaUser.uid).first()
            if user is None:
                user = User()
                user.uid = fibaUser.uid
                user.email = fibaUser.email
                user.name = fibaUser.display_name
                user.datecreated = dt.now(tz.utc)
                user.cmuserid = 'INNO-' + user.name.strip().upper()[0:1] + user.datecreated.strftime('-%y%m%d-%H%M%S')
                db.session.add(user)
                db.session.commit()
                if user.extra_info is None:
                    user_extra = UserExtraInfo()
                    user_extra.id = user.id
                    user_extra.names = txt_name
                    user_extra.acceptterms = True
                    user_extra.company_id = txt_company_id
                    db.session.add(user_extra)
                    db.session.refresh(user)


                # Add User Role
                #user_role = CatalogUserRoles.query.filter_by(name_short='usr').first()
                user_userxrole = UserXRole()
                user_userxrole.user_id = user.id
                user_userxrole.user_role_id = 1
                db.session.add(user_userxrole)
                db.session.commit()
                mail.send(msg)
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': str(e) })

@api.route('/update/company/user',methods=['GET', 'POST'])
def _update_monitoring_lisst():
    app.logger.debug('** SWING_CMS ** - ------------------')
    try:
        if request.method == 'POST':
            txt_user = request.json['txt_user'].strip()
            txt_password = generar_contraseña_temporal()  # Agregar campo de contraseña en el formulario
            # Verificar si el correo ya existe
            user = User.query.filter_by(id = txt_user).first()
            if user:
                # Crea el usuario en Firebase Authentication
                uid = user.uid
                user = auth.update_user(
                uid,
                password=txt_password,
                )

                # Envía un correo electrónico al usuario con la información de inicio de sesión
                msg = Message('Bienvenida a la plataforma Innova Mujer Honduras', sender='infoinnova@ciudadmujer.gob.hn', recipients=[user.email])
                # Contenido del correo electrónico con formato HTML
                msg.html = f'''
                    <p>Estimada empresaria,</p>
                    <p>¡Felicitaciones! Ahora tienes tu propio usuario en nuestra plataforma Innova Mujer Honduras.</p>
                    <p>Para acceder a tu cuenta, utiliza la siguiente información:</p>
                    <ul>
                        <li><strong>Correo Electrónico:</strong> {user.email}</li>
                        <li><strong>Contraseña:</strong> <em>{txt_password}</em></li>
                    </ul>
                    <p>Puedes iniciar sesión en la plataforma Innova Mujer Honduras a través del siguiente enlace:</p>
                    <p><a href="https://innova.ciudadmujer.gob.hn/login/">Iniciar Sesión</a></p>
                    <p>Si no solicitaste un usuario o restablecimiento de contraseña, no dudes en ignorar este correo electrónico con confianza.</p>
                    <p>Gracias por unirte a nosotras y ser parte de Innova Mujer Honduras.</p>
                    <p>Atentamente,</p>
                    <p>Equipo INNOVA MUJER HONDURAS</p>
                '''
                
                mail.send(msg)
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': str(e) })

import secrets
import string

# Función para generar una contraseña aleatoria y segura
def generar_contraseña_temporal(tamaño=8):
    caracteres = string.ascii_letters + string.digits  # Letras mayúsculas, minúsculas y números
    # También puedes agregar símbolos permitidos, por ejemplo: +*%$#@!&?
    caracteres += '-+*%$#@!<>?'
    contraseña = ''.join(secrets.choice(caracteres) for _ in range(tamaño))
    return contraseña

# Ejemplo de uso

@api.route('/initial/attention/companies',methods=['GET', 'POST'])
def _initial_attention_companies():
    try:
        if request.method == 'POST':
            txt_inscripcion_id = request.json['txt_id']
            inscripcion =  Inscripciones.query.filter(Inscripciones.id == txt_inscripcion_id).first()
            dni= inscripcion.dni.replace("-", "")
            company =  Company.query.filter(Company.dni == dni).first()
            status  =   CompanyStatus.query.filter(CompanyStatus.name_short == 2).first()
            #creamos la empresa
            if not company:
                company = Company()
                company.name = inscripcion.company_name.strip()
                company.rtn = inscripcion.rtn
                company.dni = dni.strip()
                company.address = inscripcion.departamento + ' - ' + inscripcion.municipio
                jsonPhone = JsonPhone()
                jsonPhone.phone = inscripcion.phone
                jsonSocial= JsonSocial()
                jsonSocial.email = inscripcion.correo.strip()
                company.phones = jsonPhone.jsonFormat()
                company.social_networks = jsonSocial.jsonFormat()
                company.created_by = current_user.id
                company.inscripcion_id = inscripcion.id
                company.status_id = status.id
                db.session.add(company)
                db.session.commit()
            else:
                company.status_id = status.id
                company.inscripcion_id = inscripcion.id
                if not company.created_by:
                    company.created_by = current_user.id
                db.session.add(company)
                db.session.commit()
                db.session.refresh(company)
            #insertamos el servicio de atencion inicial al plan de mejora como primer servicio de empresa
            service = CatalogServices.query.filter_by(name_short = 'a1').first()
            actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service.id,fase=0).first()
            if not actionplan:
                actionplan = ActionPlan()
                actionplan.company_id = company.id
                actionplan.company = company
                actionplan.services_id = service.id
                actionplan.created_by = current_user.id
                actionplan.fase = 0
                db.session.add(actionplan)
                db.session.commit()
            #actulizamos la inscripcion a ya atendida 
            inscripcion.attended = True
            inscripcion.attended_user = current_user.id
            inscripcion.attention_date = dt.now(tz.utc)
            db.session.add(inscripcion)
            db.session.commit()
            db.session.refresh(inscripcion)
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

import os
from werkzeug.utils import secure_filename
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
@api.route('/api/create/carta/compromio', methods = ['POST'])
@login_required
def _d_create_carta_compromiso():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_company_id = request.json['txt_company_id']
            txt_documente_id = request.json['txt_documente_id']
            document_type = CatalogIDDocumentTypes.query.filter_by(name_short=txt_documente_id).first()
            user = User.query.filter_by(id = current_user.id).first()
            company = Company.query.filter_by(id = txt_company_id).first()
            url = app.config.get('GOOGLE_SCRIPT_CARTA_STEP_1')

            id_asesor = user.extra_info.national_id
            id_empresa = company.dni
            response = requests.get(url.format(id_asesor,id_empresa))
            print("file generated")
            responsejson = json.loads(response.text)
            print("file downloaded")
            print(responsejson["documentId"])
            response = requests.get(responsejson["pdf"])
            print("file downloaded")
            filename = str(company.dni) + ' ' + str(document_type.name)  + str('0') + '.pdf'
            filename = filename.replace(" ", "_")
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(path, "wb") as file:
                file.write(response.content)
            carta = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=document_type.id,enabled = True).first()
            if not carta:
                # empty file without a filename.
                carta = DocumentCompany()
                carta.company_id = company.id
                carta.documente_type_id = document_type.id
                carta.complete = False
                carta.signed = False
                carta.signed_innova = False
                carta.enabled = True
                carta.document_local = filename
                carta.created_by = current_user.id
                db.session.add(carta)
                if document_type.name_short == 'DOC1':
                    status  =   CompanyStatus.query.filter(CompanyStatus.name_short == 3).first()
                    company.status_id = status.id
                    db.session.add(company)
                db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })
import re
@api.route('/api/create/ficha/inscripcion', methods = ['POST'])
@login_required
def _d_create_ficha_inscripcion():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_company_id = request.json['txt_company_id']
            txt_documente_id = request.json['txt_documente_id']
            document_type = CatalogIDDocumentTypes.query.filter_by(name_short=txt_documente_id).first()
            user = User.query.filter_by(id = current_user.id).first()
            company = Company.query.filter_by(id = txt_company_id).first()
            inscripciones =  Inscripciones.query.filter_by(id=company.inscripcion_id).first()
            preguntas = inscripciones.respuestas
            if inscripciones.cohorte <= 4:
                print('3_17')
                data = list(e for e in preguntas if e['id']  == '3_17')[0]['respuesta']
                # Buscar y extraer los números usando expresiones regulares
                numbers = re.findall(r'\d+', data)

                # Convertir los números a enteros y separarlos en listas para cada sección
                total_mujeres = int(numbers[0])
                total_hombres = int(numbers[1])
                total_general = int(numbers[2])

                remunerados_mujeres = int(numbers[3])
                remunerados_hombres = int(numbers[4])
                total_remunerados = int(numbers[5])

                no_remunerados_mujeres = int(numbers[6])
                no_remunerados_hombres = int(numbers[7])
                total_no_remunerados = int(numbers[8])
                totalEmpleadosPermanentes = total_general + total_remunerados + total_no_remunerados
                data = list(e for e in preguntas if e['id']  == '3_18')[0]['respuesta']
                # Buscar y extraer los números usando expresiones regulares
                numbers = re.findall(r'\d+', data)

                # Convertir los números a enteros y separarlos en listas para cada sección
                total_mujeres = int(numbers[0])
                total_hombres = int(numbers[1])
                total_general = int(numbers[2])

                remunerados_mujeres = int(numbers[3])
                remunerados_hombres = int(numbers[4])
                total_remunerados = int(numbers[5])

                no_remunerados_mujeres = int(numbers[6])
                no_remunerados_hombres = int(numbers[7])
                total_no_remunerados = int(numbers[8])
                # Sumar los totales
                totalEmpleadosTemporales = total_general + total_remunerados + total_no_remunerados
                print(totalEmpleadosPermanentes)
                print(totalEmpleadosTemporales)

            else:
                
                totalEmpleadosPermanentes = int(list(e for e in preguntas if e['id']  == '3_17')[0]['respuesta']['u_total_mujer']) + int(list(e for e in preguntas if e['id']  == '3_17')[0]['respuesta']['u_total_hombre'])
                totalEmpleadosTemporales =  int(list(e for e in preguntas if e['id']  == '3_18')[0]['respuesta']['temp_total_mujer']) + int(list(e for e in preguntas if e['id']  == '3_18')[0]['respuesta']['temp_total_hombre'])
      
            idDN = list(e for e in preguntas if e['id']  == '1_2')[0]['respuesta']
            registrospendientes = list(e for e in preguntas if e['id']  == '4_3')[0]['respuesta']
            if not registrospendientes:
                registrospendientes = ""
            data = {
                "nombre_asesora" :user.extra_info.names + ' ' + user.extra_info.last_names,
                "fecha":dt.now(tz.utc).strftime("%Y-%m-%d"),
                "sabeusteddeinnova":'SI',
                "conoce_servicios":list(e for e in preguntas if e['id']  == 'A')[0]['respuesta'],
                "que_servicios":list(e for e in preguntas if e['id']  == 'B')[0]['respuesta'],
                "porque_considera":list(e for e in preguntas if e['id']  == 'C')[0]['respuesta'],
                "nombre_completo":list(e for e in preguntas if e['id']  == '1_1')[0]['respuesta'],
                "nacionalidad":"",
                "n_identidad":list(e for e in preguntas if e['id']  == '1_2')[0]['respuesta'],
                "correo_electronico":list(e for e in preguntas if e['id']  == '1_8')[0]['respuesta'],
                "telefono":list(e for e in preguntas if e['id']  == '1_3')[0]['respuesta'],
                "estadocivil":"",
                "departamento":list(e for e in preguntas if e['id']  == '1_4')[0]['respuesta'],
                "ciudad":"",
                "direccion":"",
                "celular":list(e for e in preguntas if e['id']  == '1_4')[0]['respuesta'],
                "tiempo_de_operacion":list(e for e in preguntas if e['id']  == '3_11')[0]['respuesta'],
                "cargo_empresa":list(e for e in preguntas if e['id']  == '2_6')[0]['respuesta'],
                "actividad_comercia":list(e for e in preguntas if e['id']  == '3_12')[0]['respuesta'],
                "nombre_empresa":list(e for e in preguntas if e['id']  == '3_1')[0]['respuesta'],
                "descripcion_producto":"",
                "rtn":"",
                "correo_electronico_empresa":list(e for e in preguntas if e['id']  == '3_9')[0]['respuesta'],
                "redes_sociales":list(e for e in preguntas if e['id']  == '3_10')[0]['respuesta'],
                "pagina_web":"pagina_web",
                "celular":list(e for e in preguntas if e['id']  == '3_4')[0]['respuesta'],
                "ciudad":list(e for e in preguntas if e['id']  == '3_7')[0]['respuesta'],
                "departamento":list(e for e in preguntas if e['id']  == '3_5')[0]['respuesta'],
                "direccion_exacta":list(e for e in preguntas if e['id']  == '3_8')[0]['respuesta'],
                "numero_empleados":int(totalEmpleadosPermanentes) +int(totalEmpleadosTemporales) ,
                "empleados_permanentes":totalEmpleadosPermanentes,
                "empleados_temporales":totalEmpleadosTemporales,
                "status":list(e for e in preguntas if e['id']  == '4_1')[0]['respuesta'],
                "tipo_formalizacion":list(e for e in preguntas if e['id']  == '4_2')[0]['respuesta'],
                "tipo_organizacion":"",
                "registros_pendientes":registrospendientes,
                "volumen_venta_mensual":list(e for e in preguntas if e['id']  == '3_22')[0]['respuesta'],
                "gasto_operativo_mensual":"",
                "utilidades_mensuales":list(e for e in preguntas if e['id']  == '3_23')[0]['respuesta'],
                "tiene_deudas_la_empresa":list(e for e in preguntas if e['id']  == '3_24')[0]['respuesta'],
                "monto":"",
                "institucion_financiera":""
            }
        
            print(list(e for e in preguntas if e['id']  == '4_3')[0]['respuesta'])
            print(list(e for e in preguntas if e['id']  == '4_3')[0]['respuesta'])
            print(list(e for e in preguntas if e['id']  == '4_3')[0]['respuesta'])
                #"monto":list(e for e in preguntas if e['id']  == '3_26')[0]['respuesta'],
                #"institucion_financiera":list(e for e in preguntas if e['id']  == '3_27')[0]['respuesta']
            url = app.config.get('GOOGLE_SCRIPT_FICHA_STEP_1')

            id_asesor = user.extra_info.national_id
            id_empresa = company.dni
            response = requests.post(url, data = data)
            print("file generated")
            print("file generated")
            print("file generated")
            print("file generated-s")
            print(response.text)
            print(response.text)
            print(response.text)
            responsejson = json.loads(response.text)
            print("file downloaded")
            print(responsejson["documentId"])
            response = requests.get(responsejson["pdf"])
            print("file downloaded")
            filename = str(company.dni) + ' ' + str(document_type.name)  + str('0') + '.pdf'
            filename = filename.replace(" ", "_")
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(path, "wb") as file:
                file.write(response.content)
            carta = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=document_type.id,enabled = True).first()
            if not carta:
                # empty file without a filename.
                carta = DocumentCompany()
                carta.company_id = company.id
                carta.documente_type_id = document_type.id
                carta.complete = False
                carta.signed = False
                carta.signed_innova = False
                carta.enabled = True
                carta.document_local = filename
                carta.created_by = current_user.id
                db.session.add(carta)
                db.session.commit()


            if document_type.name_short == 'DOC1':
                update =  Company.query.filter(Company.id == company.id).first()
                status = CompanyStatus.query.filter_by(name_short='3').first()
                update.status_id = status.id
                db.session.add(update)
                db.session.commit()
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        print(e)
        print(e)
        print(e)
        print(e)
        print(e)
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })
    
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


@api.route('/api/aprobar/documento/', methods = ['POST'])
@login_required
def _d_aprobar_documento():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_documente_id = request.json['txt_documente_id']
 
            carta = DocumentCompany.query.filter_by(id=txt_documente_id).first()
            if carta:
                carta.complete = True
                carta.enabled = True
                db.session.add(carta)
                db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/created/reference/', methods = ['POST'])
@login_required
def _d_created_reference():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_action_id = request.json['txt_action_id']
            txt_user_x = request.json['txt_user_x']
            plan = ActionPlan.query.filter_by(id = txt_action_id).first()

            user = User.query.filter(User.id == txt_user_x).first()
            if plan:
                plan.employe_assigned =user.id
                db.session.add(plan)
                db.session.commit()
                reference = ActionPlanReferences.query.filter_by(action_plan_id = plan.id,employe_assigned=user.id).first()
                if not reference:
                    reference = ActionPlanReferences()
                    reference.action_plan_id = plan.id
                    reference.employe_assigned = user.id
                    db.session.add(reference)
                    db.session.commit()
                usr_name = current_user.name
                companyName = plan.company.name
                servicesName = plan.services.name
                now_time=dt.now(default_timezone)
                # Formatear now_time como un string con el formato deseado
                formatted_time = now_time.strftime('%Y-%m-%d a las %I:%M %p')
                html_content = f'''
                <html>
                <body>
                    <p><strong>{usr_name}</strong> ha asignado la empresa  <strong>{companyName}</strong> que requiere el servicio <strong>{servicesName}</strong>, referencia creada el <strong>{formatted_time}</strong>.</p>
                </body>
                </html>
                '''
                recipient =  [current_user.email, user.email] 
                subject = 'Referencia creada - INNOVA MUJER HONDURAS'

                try:
                    if send_email(recipient, subject, html_content):
                        print('Correo enviado con éxito.')
                    else:
                        print('Error al enviar el correo.' )
                except Exception as e:
                    print('Ocurrió un error: ' + str(e))


            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/reference/response', methods = ['POST'])
@login_required
def _d_response_reference():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            cod_refence = request.json['cod_refence']
            txt_tipo = request.json['txt_tipo']
            txt_observacion = request.json['txt_observacion']
            reference = ActionPlanReferences.query.filter_by(id = cod_refence).first()
            if reference:
                actionplan = ActionPlan.query.filter_by(id = reference.action_plan_id).first()
                #si la refenrecia fue aceptada
                if txt_tipo == '1':
                    reference.employe_accepted = True
                    actionplan.employe_accepted = True
                else:
                    reference.employe_accepted = False
                    actionplan.employe_accepted = False
                    reference.cancelled = True
                    reference.cancelled_by = current_user.id
                    actionplan.employe_assigned = None
                reference.descripcion = txt_observacion
                db.session.add(reference)
                db.session.add(actionplan)
                db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/innova/cohortes/', methods = ['POST'])
@login_required
def _api_innova_cohortes():
    try:
        if request.method == 'POST':
            txt_busqueda = request.json['txt_busqueda']
            url = app.config.get('INNOVA_API_1')
            data={'txt_busqueda':txt_busqueda}
            resp = requests.post(url,data=data)
            responsejson = json.loads(resp.content)
            for responsejs in responsejson:
                print('responsejs:')
                print(responsejs)
            return jsonify({ 'status': 200, 'resultado': responsejson })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/initial/attention/api/companies/',methods=['GET', 'POST'])
def _initial_attention_companies_api():
    try:
        print('company_name')
        print('company_name')
        if request.method == 'POST':
            id = request.json['id']
            dni = request.json['dni']
            name = request.json['name']
            company_name = request.json['company_name']
            departamento = request.json['departamento']
            municipio = request.json['municipio']
            correo = request.json['correo']
            phone = request.json['phone']
            cohorte = request.json['cohorte']
            #creamos la inscripcion
            inscripcion = Inscripciones()
            inscripcion.name = name
            inscripcion.company_name = company_name
            inscripcion.correo = correo
            inscripcion.phone = phone
            inscripcion.cohorte = cohorte
            inscripcion.dni = dni.replace("-", "")
            inscripcion.departamento = departamento
            inscripcion.municipio = municipio
            inscripcion.rtn = ''
            inscripcion.respuestas = ''
            inscripcion.elegible = True
            inscripcion.externa = int(id)
            db.session.add(inscripcion)
            db.session.commit()
            company =  Company.query.filter(Company.dni == inscripcion.dni).first()
            status  =   CompanyStatus.query.filter(CompanyStatus.name_short == 2).first()
            #creamos la empresa
            if not company:
                company = Company()
                company.name = inscripcion.company_name
                company.rtn = inscripcion.rtn
                company.dni = inscripcion.dni
                company.address = inscripcion.departamento + ' - ' + inscripcion.municipio
                jsonPhone = JsonPhone()
                jsonPhone.phone = inscripcion.phone
                jsonSocial= JsonSocial()
                jsonSocial.email = inscripcion.correo
                company.phones = jsonPhone.jsonFormat()
                company.social_networks = jsonSocial.jsonFormat()
                company.created_by = current_user.id
                company.inscripcion_id = inscripcion.id
                company.status_id = status.id
                db.session.add(company)
                db.session.commit()
            else:
                if not company.created_by:
                    company.created_by = current_user.id
                company.inscripcion_id = inscripcion.id
                company.status_id = status.id
                db.session.add(company)
                db.session.commit()
                db.session.refresh(company)
            #creamos los servicios iniciales
            #insertamos el servicio de atencion inicial al plan de mejora como primer servicio de empresa
            service = CatalogServices.query.filter_by(name_short = 'a1').first()
            actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service.id,fase=0).first()
            if not actionplan:
                actionplan = ActionPlan()
                actionplan.company_id = company.id
                actionplan.company = company
                actionplan.services_id = service.id
                actionplan.created_by = current_user.id
                actionplan.fase = 0
                db.session.add(actionplan)
                db.session.commit()
            #actulizamos la inscripcion a ya atendida 
            inscripcion.attended = True
            inscripcion.attended_user = current_user.id
            inscripcion.attention_date = dt.now(tz.utc)
            db.session.add(inscripcion)
            db.session.commit()
            db.session.refresh(inscripcion)
            
            return jsonify({ 'status': 200, 'resultado': 'responsejson' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/action/delete/', methods = ['POST'])
# @login_required
def _d_delete_ActionPlan():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            actionPlan = request.json['actionPlan']
            cancelledReason = request.json['cancelledReason']  
            actionplan = ActionPlan.query.filter_by(id = actionPlan).first()
            actionplan.cancelled = True
            actionplan.cancelled_by = current_user.id
            actionplan.cancelled_reasons = cancelledReason
            db.session.add(actionplan)
            wallet = WalletTransaction.query.filter_by(company_id = actionplan.company_id, services_id =actionplan.services_id).first()
            if wallet:
                wallet.status = 0
                wallet.cancelled_reasons = cancelledReason
                db.session.add(wallet)     
                
            db.session.commit()
            actualizar = _update_wallet(actionplan.company_id)
            if actualizar:
                return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/save/courses/', methods = ['POST'])
# @login_required
def _d_save_curso():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_name = request.json['txt_name']
            txt_formacion = request.json['txt_formacion']  
            txt_modalidad = request.json['txt_modalidad']
            txt_responsable = request.json['txt_responsable']  
            txt_horas = request.json['txt_horas']
            txt_fecha_inicial = request.json['txt_fecha_inicial']  
            txt_fecha_final = request.json['txt_fecha_final']
            txt_hora_curso = request.json['txt_hora_curso']  
            courses = Courses()
            courses.name = txt_name
            courses.id_training_type = txt_formacion
            courses.id_modality_type = txt_modalidad
            courses.id_course_managers = txt_responsable
            courses.date_scheduled_start = txt_fecha_inicial
            courses.date_scheduled_end = txt_fecha_final
            courses.time_scheduled_start = txt_horas
            courses.created_by = current_user.id
            db.session.add(courses)         
            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/save/enroll/', methods = ['POST'])
# @login_required
def _d_save_enroll():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_curso = request.json['txt_curso']
            txt_company = request.json['txt_company']  
            txt_lugar = request.json['txt_lugar']  
            inscripcion =  Inscripciones.query.filter(Inscripciones.id == txt_company).first()
            company =  Company.query.filter(Company.dni == inscripcion.dni).first()
            status  =   CompanyStatus.query.filter(CompanyStatus.name_short == 1).first()
            #creamos la empresa
            if not company:
                company = Company()
                company.name = inscripcion.company_name
                company.rtn = inscripcion.rtn
                company.dni = inscripcion.dni
                company.address = inscripcion.departamento + ' - ' + inscripcion.municipio
                jsonPhone = JsonPhone()
                jsonPhone.phone = inscripcion.phone
                jsonSocial= JsonSocial()
                jsonSocial.email = inscripcion.correo
                company.phones = jsonPhone.jsonFormat()
                company.social_networks = jsonSocial.jsonFormat()
                company.inscripcion_id = inscripcion.id
                company.status_id = status.id
                db.session.add(company)
                db.session.commit()
                
            enroll = EnrollmentRecord.query.filter_by(id_course = txt_curso,company_id=company.id).first()
            if not enroll:
                courses = EnrollmentRecord()
                courses.id_course = txt_curso
                courses.company_id = company.id
                courses.created_by = current_user.id
                courses.lugar = txt_lugar
                db.session.add(courses)         
                db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/delete/enroll/', methods = ['POST'])
# @login_required
def _d_delete_enroll():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_curso = request.json['txt_curso']
            txt_company = request.json['txt_company']  
            document = EnrollmentRecord.query.filter_by(id = txt_company).delete()
            db.session.commit()
            
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/company/search/', methods = ['GET','POST'])
# @login_required
def _d_company_search():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        query = request.json['txt_busqueda']
        search = "%{}%".format(query)
        clist = Inscripciones.query\
            .filter(or_(Inscripciones.name.like(search),\
                Inscripciones.dni.like(search),Inscripciones.municipio.like(search),\
                Inscripciones.departamento.like(search),\
                Inscripciones.correo.like(search),
                Inscripciones.company_name.like(search),
                ))\
            .filter(Company.enabled == True)\
            .all()[:20]
        total = len(clist)
        response = {
            'r_filter': 'clist',
            'r_total': total,
            'records': [],
            'status': 404
        }

        if total > 0:
            response['status'] = 200
            for company in clist:
                response['records'].append({
                    'company_id': company.id,
                    'company_name': company.name,
                    'company_dni': company.dni,
                    'empresarea_name':company.company_name,
                    'company_departamento': company.departamento,
                    'company_municipio': company.municipio,
                    'company_cohorte': company.cohorte,
                    'company_mail': company.correo,
                    'company_phone': company.phone,
                })
        return jsonify(response)
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })
    


@api.route('/api/action/search/', methods = ['GET','POST'])
# @login_required
def _d_action_search():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:

        clist = ActionPlan.query.filter(ActionPlan.date_created.between('2023-04-01', '2023-05-05')).all()[:100]
        total = len(clist)
        response = {
            'r_filter': 'clist',
            'r_total': total,
            'records': [],
            'status': 404
        }

        if total > 0:
            response['status'] = 200
            for company in clist:
                response['records'].append({
                    'company_id': company.id,

                })
            return jsonify(response)
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': 'e' })
    
@api.route('/api/save/asesoria/puntual', methods = ['POST'])
# @login_required
def _d_save_asesoria_puntual():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_company = request.json['txt_company']
            txt_servicio = request.json['txt_servicio']
            txt_nombre = request.json['txt_nombre']  
            txt_fecha = request.json['txt_fecha']
            txt_hora = request.json['txt_hora']  
            txt_comentario = request.json['txt_comentario']
            company = Company.query.filter_by(id = txt_company).first()
            service = CatalogServices.query.filter_by(id = txt_servicio).first()
            actionplan = ActionPlan()
            actionplan.company_id = company.id
            actionplan.services_id = service.id
            actionplan.created_by = current_user.id
            actionplan.fase = 0
            actionplan.progress = 100
            actionplan.date_scheduled_end = txt_fecha
            actionplan.date_scheduled_start = txt_fecha
            actionplan.espuntal = True
            actionplan.descripcion = txt_nombre
            db.session.add(actionplan)
            db.session.commit()
            db.session.refresh(actionplan)
            history =  ActionPlanHistory()
            history.created_by = current_user.id 
            history.description = txt_comentario
            history.progress = 100
            history.action_plan_id = actionplan.id
            history.endservices = True
            history.date_created = txt_fecha
            history.advisory_time = txt_hora
            db.session.add(history)
            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })



@api.route('/api/save/stage/', methods = ['POST'])
# @login_required
def _d_save_stage_company():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_status = request.json['txt_status']
            txt_company = request.json['txt_company']

            stage = CompanyStage.query.filter_by(name_short=txt_status).first()

            company = Company.query.filter_by(id = txt_company).first()
            company.stage_id = stage.id
            db.session.add(company)
            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/channel/', methods = ['POST'])
# @login_required
def _d_save_service_channel():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_channel = request.json['txt_channel']
            txt_company = request.json['txt_company']
            txt_description = request.json['txt_description']
            

            service_channel = ServiceChannel.query.filter_by(name_short=txt_channel).first()
            company = Company.query.filter_by(id = txt_company).first()
            history = CompanyMonitoring()
            history.company_id = company.id
            history.created_by = current_user.id 
            history.id_service_channel = service_channel.id
            history.description = txt_description
            db.session.add(history)
            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/depto/', methods = ['POST'])
# @login_required
def _d_save_depto_company():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':

            txt_company = request.json['txt_company']
            txt_departamentousuaria = request.json['txt_departamentousuaria']
            txt_municipiousuaria = request.json['txt_municipiousuaria']
            txt_aldeusuaria = request.json['txt_aldeusuaria']
            txt_direccion = request.json['txt_direccion']


            company = Company.query.filter_by(id = txt_company).first()
            company.inscripcion.departamento = txt_departamentousuaria
            company.inscripcion.municipio = txt_municipiousuaria
            company.inscripcion.aldea = txt_aldeusuaria
            company.address = txt_direccion
          
            db.session.add(company)
            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })
    
 # Set the Appointment's Details
@api.route('/api/save/test/madurez/123/', methods = ['POST'])
def _save_test_madurez():
    app.logger.debug('** SWING_CMS ** - API acceptterms')
    try:
        # POST: Save Appointment
        print('siiiiiiiiiiii')
        if request.method == 'POST':
            txt_name = request.json['txt_name']
            txt_identidad = request.json['txt_identidad']  
            txt_preguntas = request.json['txt_preguntas']
            total = request.json['total']
            print('siiiiiiiiiiii')
            evaluation = Evaluations()
            evaluation.name = txt_name
            evaluation.dni = txt_identidad
            evaluation.respuestas =txt_preguntas
            evaluation.result = total
            db.session.add(evaluation)
            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Cita creada' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API acceptterms Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/company/dash/', methods = ['POST','GET'])
def _d_company_dash_search():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        lista = []

        if current_user.id == 3 or current_user.id == 24 or current_user.id == 144:
            companies = Company.query.join(User, User.id==Company.created_by)\
                .filter(Company.enabled==True).all()
        else:
            companies = Company.query.join(User, User.id==Company.created_by).filter(Company.enabled==True, or_(Company.created_by == current_user.id,Company.id.in_(lista))).all()

            # Obtiene una lista de ids de las compañías
        company_ids = [company.id for company in companies]

        # Consulta los diagnósticos para las compañías en la lista de ids
        diagnoses = DiagnosisCompany.query.filter(DiagnosisCompany.company_id.in_(company_ids)).order_by(DiagnosisCompany.date_created.asc()).all()
        actions = ActionPlan.query.filter(ActionPlan.company_id.in_(company_ids)).order_by(ActionPlan.date_created.asc()).all()
        total = len(companies)
        response = {
            'r_filter': 'company',
            'r_total': total,
            'records': [],
            'status': 404
        }

        if total > 0:
            response['status'] = 200
            for company in companies:
                # Después de obtener la variable 'diagnoses' con la consulta original
                filtered_diagnoses = [diagnosis for diagnosis in diagnoses if diagnosis.company_id == company.id]
                dni = company.dni
                company_name = company.name
                action_plan_progress = '0.0 %' 
                if company.have_action_plan:
                    if company.stage:
                        if company.stage.name_short == 'E1':
                            action_plan_progress = 'Empresa en etapa 1' 
                        else:
                            action_plan_progress = company.action_plan_progress
                                                   
                if company.status:
                    company_status = company.status.name
                else:
                    company_status = ''
                totalempleados = ''
                edad = ''
                if company.inscripcion:
                    name = company.inscripcion.name
                    departamento = company.inscripcion.departamento
                    municipio = company.inscripcion.municipio
                    respuestas = company.inscripcion.respuestas
                    etenia = ''
                    
                    if isinstance(respuestas, list):
                        for item in respuestas:
                            if item['id'] == '2_5':
                                etenia = str(item['respuesta'])
                                break
                    if isinstance(respuestas, list):
                        for item in respuestas:
                            if item['id'] == '1_6':
                                edad = str(item['respuesta']).strip()
                                break

                    preguntas = company.inscripcion.respuestas
                    if '""' not in preguntas:
                        if preguntas:
                            if company.inscripcion.cohorte <= 4:

                                print('3_17-1')
                                print(company.id)
                                print(company.id)
                                data = list(e for e in preguntas if e['id']  == '3_17')[0]['respuesta']
                                # Buscar y extraer los números usando expresiones regulares
                                numbers = re.findall(r'\d+', data)

                                total_general = int(numbers[2])
                                total_no_remunerados = int(numbers[8])
                                totalEmpleadosPermanentes = total_general 
                                data = list(e for e in preguntas if e['id']  == '3_18')[0]['respuesta']
                                # Buscar y extraer los números usando expresiones regulares
                                numbers = re.findall(r'\d+', data)

                                # Sumar los totales
                                totalEmpleadosTemporales = total_general 
                                totalempleados = totalEmpleadosPermanentes + totalEmpleadosTemporales
                            else:
                                if company.inscripcion.externa == 0 or not company.inscripcion.externa:
                                    totalEmpleadosPermanentes = int(list(e for e in preguntas if e['id']  == '3_17')[0]['respuesta']['u_total_mujer']) + int(list(e for e in preguntas if e['id']  == '3_17')[0]['respuesta']['u_total_hombre'])
                                    totalEmpleadosTemporales =  int(list(e for e in preguntas if e['id']  == '3_18')[0]['respuesta']['temp_total_mujer']) + int(list(e for e in preguntas if e['id']  == '3_18')[0]['respuesta']['temp_total_hombre'])
                                    totalempleados = totalEmpleadosPermanentes + totalEmpleadosTemporales
                                else:
                                    print('3_17-1')
                                    print(company.id)
                                    print(company.id)
                                    data = list(e for e in preguntas if e['id']  == '3_17')[0]['respuesta']
                                    # Buscar y extraer los números usando expresiones regulares
                                    numbers = re.findall(r'\d+', data)

                                    total_general = int(numbers[2])
                                    total_no_remunerados = int(numbers[8])
                                    totalEmpleadosPermanentes = total_general 
                                    data = list(e for e in preguntas if e['id']  == '3_18')[0]['respuesta']
                                    # Buscar y extraer los números usando expresiones regulares
                                    numbers = re.findall(r'\d+', data)

                                    # Sumar los totales
                                    totalEmpleadosTemporales = total_general 
                                    totalempleados = totalEmpleadosPermanentes + totalEmpleadosTemporales
                else:
                    departamento = ''
                    municipio = ''
                    name = ''
                    respuestas = ''
                    etenia = ''
                    diagnosis_date = ''
                ids = ''
                status = ''
                respuestas = ''
                resultados = ''
                diagnoses_submission_time = ''
                constituida = ''
                if filtered_diagnoses:
                    ids = filtered_diagnoses[0].id
                    status = filtered_diagnoses[0].status
                    respuestas = filtered_diagnoses[0].respuestas
                    if '_submission_time' in respuestas:
                        # Convertir el valor de cadena a un objeto datetime
                        submission_time = datetime.strptime(respuestas['_submission_time'], '%Y-%m-%dT%H:%M:%S')
                        
                    if '_7_2' in respuestas:
                        constituida = respuestas['_7_2']

                        # Obtener la fecha (año, mes, día) en formato "YYYY-MM-DD"

                        # Obtener la fecha (año, mes, día)
                        diagnoses_submission_time = submission_time.strftime('%Y-%m-%d')
                        print(submission_time)
                    resultados = filtered_diagnoses[0].resultados
                #filtered_diagnoses = [diagnosis.titulo for diagnosis in diagnoses if diagnosis.id == 10]
                actions_diagnoses = [action.services_id  for action in actions if action.company_id == company.id]
                date_action_plan = ''
                if company.date_action_plan:
                    date_action_plan = company.date_action_plan.strftime('%Y-%m-%d')
                response['records'].append({
                    'company_id': company.id,
                    "dni":dni,
                    "name":name,
                    "company_name":company_name,
                    "company_status":company_status,
                    "action_plan_progress":action_plan_progress,
                    "have_action_plan":company.have_action_plan,
                    "date_action_plan":date_action_plan,
                    "diagnoses_submission_time":diagnoses_submission_time,
                    "departamento":departamento,
                    "municipio":municipio,
                    "etenia":etenia,
                    'id':ids,
                    "ids":ids,
                    "status":status,
                    "respuestas":respuestas,
                    "resultados":resultados,
                    'services':actions_diagnoses,
                    'totalempleados':totalempleados,
                    'constituida':constituida,
                    'edad':edad,

                })
            return jsonify(response)
    except Exception as e:
        print(e)
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error','s':company.id, 'msg': str(e) })



@api.route('/api/update/enroll/', methods = ['POST'])
# @login_required
def _d_update_enroll():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            lugar = request.json['lugar']
            enroll_id = request.json['id']  
                        
            enroll = EnrollmentRecord.query.filter_by(id = enroll_id).first()
            enroll.lugar = lugar
            db.session.add(enroll)    

            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/catalog/surveys', methods = ['POST'])
# @login_required
def save_catalog_surveys_SDE():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_preguntas = request.json['txt_preguntas']
            txt_company = request.json['txt_company']  
            company = Company.query.filter_by(id = txt_company).first()

            surveys = surveys_sde()
            surveys.company_id = company.id
            surveys.catalog_surveys_id = 1
            surveys.respuestas = txt_preguntas
            db.session.add(surveys)    

            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


#Chepe save  ENCUESTA DE IMPACTO
@api.route('/api/save/surveys/impacto', methods = ['POST'])
# @login_required
def save_surveys_impacto():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_preguntas = request.json['txt_preguntas']
            txt_company = request.json['txt_company']  
            company = Company.query.filter_by(id = txt_company).first()

            surveys = surveys_sde()
            surveys.company_id = company.id
            surveys.catalog_surveys_id = 2
            surveys.respuestas = txt_preguntas
            db.session.add(surveys)    
            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/save/info/', methods = ['POST'])
# @login_required
def _d_save_info_company():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':

            txt_company = request.json['txt_company']
            companyName = request.json['companyName']
            dni = request.json['dni']
            email = request.json['email']
            phone = request.json['phone']
            company = Company.query.filter_by(id = txt_company).first()
            company.dni = dni
            company.name = companyName
            jsonPhone = JsonPhone()
            jsonPhone.phone = phone
            jsonSocial= JsonSocial()
            jsonSocial.email = email
            if company.inscripcion:
                company.inscripcion.phone = phone
                company.inscripcion.correo = email
            company.phones = jsonPhone.jsonFormat()
            db.session.add(company)
            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


# @login_required
@api.route('/api/save/rating/', methods = ['POST'])
def _d_save_rating_actions():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':

            txt_comentario = request.json['txt_comentario']
            selectedValue = request.json['selectedValue']
            txt_id = request.json['txt_id']

            actions = ActionPlan.query.filter_by(id=txt_id).first()
            actions.puntuacion = selectedValue
            actions.nota = txt_comentario
            db.session.add(actions)
            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })


@api.route('/api/etapa/1', methods = ['GET','POST'])
def InscripcionesResource():
    # Consulta la base de datos para obtener Inscripciones con elegible igual a True y dni distinto
    inscripciones = Inscripciones.query.filter_by(elegible=True).distinct(Inscripciones.dni).all()

    # Crea una lista de diccionarios con los campos requeridos
    result = [
        {
            'id': inscripcion.id,
            'dni': inscripcion.dni,
            'name': inscripcion.name,
            'company_name': inscripcion.company_name,
            'departamento': inscripcion.departamento,
            'municipio': inscripcion.municipio,
            'atendida': inscripcion.user.name if inscripcion.user else 'no atendida'
        }
        for inscripcion in inscripciones
    ]

    return jsonify(result)


@app.route('/api/companies', methods=['GET'])
def get_companies():
    try:
       # Consulta la base de datos para obtener las Company registradas en EnrollmentRecord con Courses en TrainingType TT1
        enrollment_records = (
            EnrollmentRecord.query
            .join(Courses, EnrollmentRecord.id_course == Courses.id)
            .join(TrainingType, Courses.id_training_type == TrainingType.id)
            .join(Company, EnrollmentRecord.company_id == Company.id)
            .join(CourseManagers, Courses.id_course_managers == CourseManagers.id)
            .filter(TrainingType.name_short == 'TT1')
            .all()
        )

        # Procesar los resultados para obtener la información deseada
        result = [
            {
                'company_dni': record.company.dni,
                'company_name': record.company.name,
                'course_name': record.course.name,
                'course_manager_name': record.course.course_managers.name
            }
            for record in enrollment_records
        ]

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/combined_data', methods=['GET'])
def get_combined_data():
    try:
        # Consulta la base de datos para obtener Inscripciones con elegible igual a True y dni distinto
        #inscripciones = Inscripciones.query.filter_by(elegible=True).filter(or_(Inscripciones.status != 0, Inscripciones.status == None)).distinct(Inscripciones.dni).all()
        inscripciones = Inscripciones.query.filter(Inscripciones.cohorte==5).filter(or_(Inscripciones.status != 0, Inscripciones.status == None)).order_by(Inscripciones.id.desc())
        # Crea una lista de diccionarios con los campos requeridos
        result = []
        for inscripcion in inscripciones:
            data = {
                'id': inscripcion.id,
                'dni': inscripcion.dni,
                'name': inscripcion.name,
                'company_name': inscripcion.company_name,
                'departamento': inscripcion.departamento,
                'municipio': inscripcion.municipio,
                'cohorte':inscripcion.cohorte,
                'atendida': inscripcion.user.name if inscripcion.user else 'no atendida'
            }

            # Si hay una Company asociada a la inscripción, incluir datos de enrollment_records
            # Verificar si la inscripción pertenece a una empresa y obtener datos de la empresa si es así
            company = Company.query.filter_by(inscripcion_id=inscripcion.id).first()
            if company:
                
                enrollment_record_data = get_enrollment_record_data(company)
                data.update(enrollment_record_data)
            else:
                data['estado'] = 'Elegible'
                data['company_dni'] ='',
                data['company_name']= '',
                data['course_name']='',
                data['course_manager_name']= ''

            result.append(data)


            result.append(data)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

def get_enrollment_record_data(company):
    try:
        # Consulta la base de datos para obtener datos de enrollment_records
        enrollment_record = (
            EnrollmentRecord.query
            .join(Courses, EnrollmentRecord.id_course == Courses.id)
            .join(TrainingType, Courses.id_training_type == TrainingType.id)
            .join(Company, EnrollmentRecord.company_id == Company.id)
            .join(CourseManagers, Courses.id_course_managers == CourseManagers.id)
            .filter(Company.id == company.id, TrainingType.name_short == 'TT1')
            .first()
        )

        if enrollment_record:
            return {
                'estado': 'Capacitada',
                'company_dni': company.dni,
                'company_dni': company.dni,
                'company_name': company.name,
                'course_name': enrollment_record.course.name,
                'course_manager_name': enrollment_record.course.course_managers.name
            }
        else:
            # Si no hay enrollment_record asociado, retornar diccionario vacío
            return {
                'estado': 'Elegible',
                'company_dni': '',
                'company_name': '',
                'course_name': '',
                'course_manager_name': ''
            }
    except Exception as e:
        return {'error': str(e)}