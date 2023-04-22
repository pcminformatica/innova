from . import auth,crypto_key, db, removeItemFromList, updateItemFromList

from datetime import datetime as dt
from datetime import timezone as tz
from flask import Blueprint, request, url_for, jsonify, make_response
from flask import current_app as app
from flask_login import current_user, login_required
from models.models import DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Appointments, CatalogIDDocumentTypes, CatalogUserRoles, CatalogServices
from models.models import ActionPlanReferences,User, UserExtraInfo, UserXEmployeeAssigned, UserXRole,Company
from models.formatjson import JsonPhone, JsonSocial,JsonConfigProfile
from models.diagnostico import Diagnosticos
from sqlalchemy import or_,desc,asc

import json
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
            xrol = UserXRole.query.filter_by(user_id = user.id).first()
            xrol.user_role_id = txt_rol
            db.session.add(user)
            db.session.add(xrol)
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
            txt_diagnostic_questions = request.json['txt_diagnostic_questions']

            user.name = txt_name
            user.catalog_category = int(txt_rol)
            user.advisory_time = int(txt_tiempo_asesoria)
            user.execution_time = int(txt_tiempo_ejecucion)
            user.cost =float(txt_costo)
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
            inscripcion.name = list(e for e in preguntas if e['id']  == '1_1')[0]['respuesta']
            inscripcion.company_name = list(e for e in preguntas if e['id']  == '3_1')[0]['respuesta']
            inscripcion.correo = list(e for e in preguntas if e['id']  == '1_8')[0]['respuesta']
            inscripcion.phone = list(e for e in preguntas if e['id']  == '1_3')[0]['respuesta']
            inscripcion.cohorte = 5
            inscripcion.dni = list(e for e in preguntas if e['id']  == '1_2')[0]['respuesta']
            inscripcion.departamento = list(e for e in preguntas if e['id']  == '1_4')[0]['respuesta']
            inscripcion.municipio = list(e for e in preguntas if e['id']  == '1_5')[0]['respuesta']
            inscripcion.rtn = list(e for e in preguntas if e['id']  == '1_2')[0]['respuesta']
            inscripcion.respuestas = preguntas
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
            company =  Company.query.filter(or_(Company.dni == txt_identidad, Company.id == txt_company_id)).first()
            if not company:
                txt_company_name = request.json['txt_company_name']
                txt_company_rtn = request.json['txt_company_rtn']
                company = Company()
                company.name = txt_company_name
                company.rtn = txt_company_rtn
                company.dni = txt_identidad
                company.description = 'description'
                company.created_by = current_user.id
                db.session.add(company)
                db.session.commit()
            services = json.loads(services)
            for service in services:
                actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service['service'],fase=service['fase']).first()
                if not actionplan:
                    actionplan = ActionPlan()
                    actionplan.company_id = actionplan.id
                    actionplan.company = company
                    actionplan.date_scheduled_start = service['fecha_inicio']
                    actionplan.date_scheduled_end = service['fecha_final']
                    actionplan.services_id = int(service['service'])
                    actionplan.created_by = current_user.id
                    actionplan.fase = service['fase']
                    actionplan.descripcion = service['comentario']
                    db.session.add(actionplan)
                    db.session.commit()
                    

                    
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
            url = "https://kf.kobotoolbox.org/api/v2/assets/aTaYkJZNSLYUpSqoRd9snr/data/{}/?format=json".format(txt_code)
            headers={'Authorization':'token 5690e59a570b717402ac2bcdba1fe02afc8abd85'}
            resp = requests.get(url,headers=headers)
            api = json.loads(resp.content)
            company =  Company.query.filter(Company.dni == api['IDENTIDAD']).first()
            if not company:
                company = Company()
                company.name = api['NOMBRE_EMPRESA']
                company.rtn = api['RTN']
                company.dni = api['IDENTIDAD']
                company.address = api['DIRECCION']
                jsonPhone = JsonPhone()
                jsonPhone.phone = api['TELEFONO']
                jsonSocial= JsonSocial()
                jsonSocial.email = api['EMAIL']
                company.phones = jsonPhone.jsonFormat()
                company.social_networks = jsonSocial.jsonFormat()
                company.created_by = current_user.id
                db.session.add(company)
                db.session.commit()
            diagnosis =  DiagnosisCompany.query.filter(DiagnosisCompany.company_id == company.id).first()
            if not diagnosis:
                diagnostico = Diagnosticos()
                resultados  = diagnostico.calcular_area(api)
                diagnosis =  DiagnosisCompany()
                diagnosis.company_id = company.id
                diagnosis.respuestas = api
                diagnosis.resultados =  json.loads( str(resultados))
                diagnosis.created_by = current_user.id
                db.session.add(diagnosis)
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
            history =  ActionPlanHistory()
            history.created_by = current_user.id 
            history.description = txt_comentario
            history.progress = txt_porcentaje
            history.action_plan_id = txt_servicios
            history.endservices = txt_finalizo
            db.session.add(history)
            db.session.commit()
            plan = ActionPlan.query.filter_by(id = txt_servicios).first()
            plan.progress =txt_porcentaje
            db.session.add(plan)
            db.session.commit()
            if txt_finalizo == True and txt_porcentaje == "100":
                company = Company.query.filter_by(id = plan.company_id).first()
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


@api.route('/create/company/user',methods=['GET', 'POST'])
def _diagnosis_monitoring_lisst():
    app.logger.debug('** SWING_CMS ** - ------------------')
    try:
        if request.method == 'POST':
            txt_email = request.json['txt_email']
            txt_name = request.json['txt_name']
            txt_company_id = request.json['txt_company_id'] 
            fibaUser = auth.create_user(
                email=txt_email,
                email_verified=False,
                display_name=txt_name,
                disabled=False)
            print('Sucessfully created new user: {0}'.format(fibaUser.uid))
            print('Sucessfully created new user: {0}'.format(fibaUser.email))
            user = User.query.filter_by(uid = fibaUser.uid).first()
            if user is None:
                user = User()
                user.uid = fibaUser.uid
                user.email = fibaUser.email
                user.name = fibaUser.display_name
                user.phonenumber = fibaUser.phone_number
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
                    db.session.commit()
                    db.session.refresh(user)


                # Add User Role
                user_role = CatalogUserRoles.query.filter_by(name_short='usr').first()
                user_userxrole = UserXRole()
                user_userxrole.user_id = user.id
                user_userxrole.user_role_id = user_role.id
                db.session.add(user_userxrole)
                db.session.refresh(user)
                db.session.commit()
            f = open(app.config.get('GOOGLE_APPLICATION_KEY'))
            js = json.load(f)
        
            url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={0}".format(js['firebaseConfig']['apiKey'])
            headers={'Content-Type':'application/json'}
            myobj = {'requestType': 'PASSWORD_RESET','email':fibaUser.email}
            x = requests.post(url,headers=headers, json = myobj)
            print(x)
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })



@api.route('/initial/attention/companies',methods=['GET', 'POST'])
def _initial_attention_companies():
    try:
        if request.method == 'POST':
            txt_inscripcion_id = request.json['txt_id']
            inscripcion =  Inscripciones.query.filter(Inscripciones.id == txt_inscripcion_id).first()
            Inscripciones
            company =  Company.query.filter(Company.dni == inscripcion.dni).first()
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
                db.session.add(company)
                db.session.commit()
            else:
                company
                company.inscripcion_id = inscripcion.id
                db.session.add(company)
                db.session.commit()
                db.session.refresh(company)
            #insertamos el servicio de atencion inicial al plan de mejora como primer servicio de empresa
            service = CatalogServices.query.filter_by(name_short = 'a1').first()
            actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service.id,fase=0).first()
            if not actionplan:
                actionplan = ActionPlan()
                actionplan.company_id = actionplan.id
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
                db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

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
            totalEmpleadosPermanentes = list(e for e in preguntas if e['id']  == '3_17')[0]['respuesta']['u_total_mujer'] + list(e for e in preguntas if e['id']  == '3_17')[0]['respuesta']['u_total_hombre']
            totalEmpleadosTemporales =  list(e for e in preguntas if e['id']  == '3_18')[0]['respuesta']['temp_total_mujer'] + list(e for e in preguntas if e['id']  == '3_18')[0]['respuesta']['temp_total_hombre']
            idDN = list(e for e in preguntas if e['id']  == '1_2')[0]['respuesta']
            data = {
                "nombre_asesora" :'',
                "fecha":"fecha",
                "sabeusteddeinnova":'',
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
                "numero_empleados":totalEmpleadosPermanentes +totalEmpleadosTemporales ,
                "empleados_permanentes":totalEmpleadosPermanentes,
                "empleados_temporales":totalEmpleadosTemporales,
                "status":list(e for e in preguntas if e['id']  == '4_1')[0]['respuesta'],
                "tipo_formalizacion":list(e for e in preguntas if e['id']  == '4_2')[0]['respuesta'],
                "tipo_organizacion":"",
                "registros_pendientes":list(e for e in preguntas if e['id']  == '4_3')[0]['respuesta'],
                "volumen_venta_mensual":list(e for e in preguntas if e['id']  == '3_22')[0]['respuesta'],
                "gasto_operativo_mensual":"",
                "utilidades_mensuales":list(e for e in preguntas if e['id']  == '3_23')[0]['respuesta'],
                "tiene_deudas_la_empresa":list(e for e in preguntas if e['id']  == '3_24')[0]['respuesta'],
                "monto":list(e for e in preguntas if e['id']  == '3_26')[0]['respuesta'],
                "institucion_financiera":list(e for e in preguntas if e['id']  == '3_27')[0]['respuesta']
            }
            
            url = app.config.get('GOOGLE_SCRIPT_FICHA_STEP_1')

            id_asesor = user.extra_info.national_id
            id_empresa = company.dni
            response = requests.post(url, data = data)
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
                db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
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

            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

