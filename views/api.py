from . import crypto_key, db, removeItemFromList, updateItemFromList

from datetime import datetime as dt
from datetime import timezone as tz
from flask import Blueprint, request, url_for, jsonify, make_response
from flask import current_app as app
from flask_login import current_user, login_required
from models.models import ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Appointments, CatalogIDDocumentTypes, CatalogUserRoles, CatalogServices
from models.models import User, UserExtraInfo, UserXEmployeeAssigned, UserXRole,Company
from sqlalchemy import or_
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
    app.logger.debug('** SWING_CMS ** - API List Users')
    app.logger.debug('** SWING_CMS ** - API List Users')
    app.logger.debug('** SWING_CMS ** - API List Users')
    app.logger.debug('** SWING_CMS ** - API List Users')
    app.logger.debug('** SWING_CMS ** - API List Users')
    try:
        if request.method == 'GET':
            query = request.args.get('qry')
            filters = request.args.get('flt')
            filters_type = request.args.get('ft')
            app.logger.debug(query)
            app.logger.debug(filters)
            app.logger.debug(filters_type)

            if query is not None:
                ulist, total = User.search(query, 1, 9)

                # Check if there is a User Role Filter parameter and Filter by it
                if filters is not None and filters != '':
                    userRolesFilters = filters.split('-')
                    
                    # Check if the Filters are of type Servie User Role
                    filters_type = 'sur'
                    if filters_type is not None and filters_type == 'sur':
                        app.logger.debug('** 12 ** - sur List Users')
                        app.logger.debug('** 123 ** - sur List Users')
                        newUserRolesFilters = []
                        
                        services = CatalogServices.query.filter(CatalogServices.name_short.in_(userRolesFilters))
                        for service in services:
                            user_role = CatalogUserRoles.query.filter(CatalogUserRoles.id == service.service_user_role).first()
                            if user_role is not None:
                                newUserRolesFilters.append(user_role.name_short)
                        
                        userRolesFilters = newUserRolesFilters
                    else:
                        app.logger.debug('** 123 ** - API List Users')
                        app.logger.debug('** 123 ** - API List Users')

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
                app.logger.debug('** SWING_CMS ** - API List Users')
                app.logger.debug('** SWING_CMS ** - API List Users')
                app.logger.debug('** SWING_CMS ** - API List Users')
                app.logger.debug('** SWING_CMS ** - API List Users')
                app.logger.debug('** SWING_CMS ** - API List Users')
                app.logger.debug(query)
                app.logger.debug(filters)
                app.logger.debug(filters)
                app.logger.debug(userRolesFilters)    
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
                app.logger.debug('** SWING_CMS ** - API acceptterms')
            # Update User information

            return jsonify({ 'status': 200, 'msg': 'Cita creada' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API acceptterms Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/perfil/', methods = ['POST'])
@login_required
def _d_():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
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
                app.logger.debug('** nooooo ** - API Appointment Detail')
                app.logger.debug('** SWING_CMS ** - API Appointment Detail')
 
 
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
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
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
                app.logger.debug('** nooooo ** - API Appointment Detail')
                app.logger.debug('** SWING_CMS ** - API Appointment Detail')
 
 

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
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            txt_id = request.json['txt_id']
            user = User.query.filter_by(id = txt_id).first()
            txt_name = request.json['txt_name']
            txt_email = request.json['txt_email']
            txt_rol = request.json['txt_rol']
            user.email = txt_email
            user.name = txt_name
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
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        app.logger.debug('** SWING_CMS ** - API Appointment Detail')
        # POST: Save Appointment
        if request.method == 'POST':
            servicio = CatalogServices.query.filter_by(id = 1).first()
            scheduled_dt = request.json['scheduled_dt']
            emp_id = request.json['emp_id']
            app.logger.debug(scheduled_dt)
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
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API /api/save/appointment/admin Detail')
    try:
        app.logger.debug('** SWING_CMS ** - API Appointment Detail')
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
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        app.logger.debug('** SWING_CMS ** - API Appointment Detail')
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
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    dt_today = '2023-01-20 10:00:00'
    try:
        app.logger.debug('** SWING_CMS ** - API Appointment Detail')
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
                    app.logger.debug('sii')
                    app.logger.debug(detail.date_scheduled)
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
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
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

            user.name = txt_name
            user.catalog_category = int(txt_rol)
            user.advisory_time = int(txt_tiempo_asesoria)
            user.execution_time = int(txt_tiempo_ejecucion)
            user.cost =float(txt_costo)
            db.session.add(user)
            db.session.commit()
            print('111')
            print('111')
            print('111')
            print('111')
            print('111')
            return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        print('111')
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        app.logger.error('** SWING_CMS1 ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

import requests

@api.route('/api/inscripciones/', methods = ['POST'])
# @login_required
def _d_inscripciones():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            preguntas = request.json['preguntas']
            
           
            elegible = True
            #evaluar elegible
            print(preguntas)
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
            temp_mujeres = temp_tiempo_completo["temp_total_mujer"]
            temp_hombres = temp_tiempo_completo["temp_total_hombre"]
            temp_total = (int(temp_mujeres) + int(temp_hombres))/2
            totales = total + temp_total
            if totales <= 4:
                elegible = False
            print(list(e for e in preguntas if e['id']  == '1_4')[0]['respuesta'])

            inscripcion = Inscripciones()
            inscripcion.name = list(e for e in preguntas if e['id']  == '1_1')[0]['respuesta']
            inscripcion.company_name = list(e for e in preguntas if e['id']  == '1_2')[0]['respuesta']
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
                    print(x.text)
                else:
                    url = 'http://inscripciones.ciudadmujer.gob.hn/inscribite/web/no/web'
                    myobj = {'txt_Correo': list(e for e in preguntas if e['id']  == '1_8')[0]['respuesta']}
                    x = requests.post(url, data = myobj)
                    print(x.text)
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
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':

            txt_company_name = request.json['txt_company_name']
            txt_company_rtn = request.json['txt_company_rtn']
            services = request.json['services']
            app.logger.error(txt_company_name)
            app.logger.error(txt_company_rtn)
            app.logger.error(services)
            company =  Company.query.filter(or_(Company.name == txt_company_name, Company.rtn == txt_company_rtn)).first()
            if not company:
                company = Company()
                company.name = txt_company_name
                company.rtn = txt_company_rtn
                company.description = 'description'
                db.session.add(company)
                db.session.commit()
            else:
                app.logger.error('** siiiiiiiiiii * - API Appointment Detail Error: {}'.format('e'))
            services = json.loads(services)
            for service in services:
                actionplan = ActionPlan.query.filter_by(company_id = company.id,services_id=service['service'],version=service['fase']).first()
                if not actionplan:
                    actionplan = ActionPlan()
                    actionplan.company_id = actionplan.id
                    actionplan.company = company
                    actionplan.date_scheduled_start = service['fecha_inicio']
                    actionplan.date_scheduled_end = service['fecha_final']
                    actionplan.services_id = int(service['service'])
                    actionplan.created_by = current_user.id
                    actionplan.fase = service['fase']
                    db.session.add(actionplan)
                    db.session.commit()
                    

                    
        return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/diagnosis/company/', methods = ['POST'])
# @login_required
def _d_save_DiagnosisCompany():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':

            txt_company_name = request.json['txt_company_name']
            txt_company_rtn = request.json['txt_company_rtn']
            app.logger.error(txt_company_name)
            app.logger.error(txt_company_rtn)

            company =  Company.query.filter(or_(Company.name == txt_company_name, Company.rtn == txt_company_rtn)).first()
            if not company:
                company = Company()
                company.name = txt_company_name
                company.rtn = txt_company_rtn
                company.description = 'description'
                db.session.add(company)
                db.session.commit()
            #11
            existe =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Dirección Estratégica", DiagnosisCompany.company_id == company.id).first()
            if existe:
                existe.status = False
                db.session.add(existe)
                db.session.commit()
            diagnosis = DiagnosisCompany()
            diagnosis.categoria = "Dirección Estratégica"
            diagnosis.result_area = request.json["total_direccion_estrategica"]
            diagnosis.result_total = request.json["resultado_direccion_estrategica"]
            diagnosis.status = True
            diagnosis.created_by = current_user.id
            diagnosis.company_id = company.id
            diagnosis.respuestas = request.json["respuestas_direccion_estrategica"]
            db.session.add(diagnosis)
            db.session.commit()

            existe =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Mercadeo y ventas", DiagnosisCompany.company_id == company.id).first()
            if existe:
                existe.status = False
                db.session.add(existe)
                db.session.commit()

            diagnosis = DiagnosisCompany()
            diagnosis.categoria = "Mercadeo y ventas"
            diagnosis.result_area = request.json["total_mercadeo_ventas"]
            diagnosis.result_total = request.json["resultado_mercadeo_ventas"]
            diagnosis.status = True
            diagnosis.created_by = current_user.id
            diagnosis.company_id = company.id
            diagnosis.respuestas = request.json["respuestas_mercadeo_ventas"]
            db.session.add(diagnosis)
            db.session.commit()

            existe =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Madurez Digital", DiagnosisCompany.company_id == company.id).first()
            if existe:
                existe.status = False
                db.session.add(existe)
                db.session.commit()
            diagnosis = DiagnosisCompany()
            diagnosis.categoria = "Madurez Digital"
            diagnosis.result_area = request.json["total_madurez_digital"]
            diagnosis.result_total = request.json["resultado_madurez_digital"]
            diagnosis.status = True
            diagnosis.created_by = current_user.id
            diagnosis.company_id = company.id
            diagnosis.respuestas = request.json["respuestas_madurez_digital"]
            db.session.add(diagnosis)
            db.session.commit()

            existe =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Gestión Financiera", DiagnosisCompany.company_id == company.id).first()
            if existe:
                existe.status = False
                db.session.add(existe)
                db.session.commit()
            diagnosis = DiagnosisCompany()
            diagnosis.categoria = "Gestión Financiera"
            diagnosis.result_area = request.json["total_gestion_financiera"]
            diagnosis.result_total = request.json["resultado_gestion_financiera"]
            diagnosis.status = True
            diagnosis.created_by = current_user.id
            diagnosis.company_id = company.id
            diagnosis.respuestas = request.json["respuestas_gestion_financiera"]
            db.session.add(diagnosis)
            db.session.commit()

            existe =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Gestión de la producción", DiagnosisCompany.company_id == company.id).first()
            if existe:
                existe.status = False
                db.session.add(existe)
                db.session.commit()
            diagnosis = DiagnosisCompany()
            diagnosis.categoria = "Gestión de la producción"
            diagnosis.result_area = request.json["total_gestion_produccion"]
            diagnosis.result_total = request.json["resultado_gestion_produccion"]
            diagnosis.status = True
            diagnosis.created_by = current_user.id
            diagnosis.company_id = company.id
            diagnosis.respuestas = request.json["respuestas_gestion_produccion"]
            db.session.add(diagnosis)
            db.session.commit()

            existe =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Organización y Gestión del talento humano", DiagnosisCompany.company_id == company.id).first()
            if existe:
                existe.status = False
                db.session.add(existe)
                db.session.commit()
            diagnosis = DiagnosisCompany()
            diagnosis.categoria = "Organización y Gestión del talento humano"
            diagnosis.result_area = request.json["total_organizacion_gestion"]
            diagnosis.result_total = request.json["resultado_organizacion_gestion"]
            diagnosis.status = True
            diagnosis.created_by = current_user.id
            diagnosis.company_id = company.id
            diagnosis.respuestas = request.json["respuestas_organizacion_gestion"]
            db.session.add(diagnosis)
            db.session.commit()

                    
        return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

@api.route('/api/save/action/plan/history/', methods = ['POST'])
# @login_required
def _d_save_ActionPlanHistory():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
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
                servicios_mejorados = plan.services.diagnostic_questions

                for servicio_mejorado in servicios_mejorados:
                    #1

                    encontro = False
                    clave = servicio_mejorado['id']
                    direccion_estrategicax =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Dirección Estratégica", DiagnosisCompany.company_id == company.id).first()
                    orj =  json.loads(direccion_estrategicax.respuestas)
                    for resp in orj:
                        if clave in resp:  
                            resp[clave] = 3
                            encontro = True
                    if encontro:
                        direccion_estrategica = ["_1_1","_1_2","_1_3","_1_4","_1_5","_1_6","_1_7","_1_8","_1_9","_1_10","_1_11"]
                        total_direccion_estrategica = 0
                        for clave in direccion_estrategica:
                            for resp in orj:
                                if clave in resp:
                                    total_direccion_estrategica = total_direccion_estrategica + int(resp[clave])
                                    print("Pregunta: {} respuesta: {}".format(clave,resp[clave]))
                        resultado_direccion_estrategica = total_direccion_estrategica/(len(direccion_estrategica)*3) * 0.10 * 100
                        resultado_direccion_estrategica = round(resultado_direccion_estrategica, 2)
                        #desactivar
                        direccion_estrategicax.status = 0
                        db.session.add(direccion_estrategicax)
                        db.session.commit()
                        #crear
                        diagnosis = DiagnosisCompany()
                        diagnosis.categoria = "Dirección Estratégica"
                        diagnosis.result_total = resultado_direccion_estrategica 
                        diagnosis.result_area = total_direccion_estrategica
                        diagnosis.status = True
                        diagnosis.created_by = current_user.id
                        diagnosis.company_id = company.id
                        diagnosis.respuestas = orj
                        db.session.add(diagnosis)
                        db.session.commit()   

                    #2
                    encontro = False
                    clave = servicio_mejorado['id']
                    mercadeo_ventasx =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Mercadeo y ventas", DiagnosisCompany.company_id == company.id).first()
                    orj =  json.loads(mercadeo_ventasx.respuestas)
                    for resp in orj:
                        if clave in resp:  
                            resp[clave] = 3
                            encontro = True
                    if encontro:
                        mercadeo_ventas = ["_2_1","_2_2","_2_3","_2_4","_2_5","_2_6","_2_7","_2_8", "_2_9", "_2_10", "_2_11", "_2_12","_2_13","_2_14","_2_15","_2_16","_2_17","_2_18","_2_19","_2_20","_2_21","_2_22","_2_23","_2_24","_2_25","_2_26"]
                        total_mercadeo_ventas = 0
                        for clave in mercadeo_ventas:
                            for resp in orj:
                                if clave in resp:
                                    total_mercadeo_ventas = total_mercadeo_ventas + int(resp[clave])
                                    print("Pregunta: {} respuesta: {}".format(clave,resp[clave]))
                        resultado_mercadeo_ventas = total_mercadeo_ventas/(len(mercadeo_ventas)*3) * 0.25 * 100
                        resultado_mercadeo_ventas = round(resultado_mercadeo_ventas, 2)
                        #desactivar
                        mercadeo_ventasx.status = 0
                        db.session.add(mercadeo_ventasx)
                        db.session.commit()
                        #crear
                        diagnosis = DiagnosisCompany()
                        diagnosis.categoria = "Mercadeo y ventas"
                        diagnosis.result_total = resultado_mercadeo_ventas 
                        diagnosis.result_area = total_mercadeo_ventas
                        diagnosis.status = True
                        diagnosis.created_by = current_user.id
                        diagnosis.company_id = company.id
                        diagnosis.respuestas = orj
                        db.session.add(diagnosis)
                        db.session.commit()   

                    #3
                    encontro = False
                    clave = servicio_mejorado['id']
                    madurez_digitalx =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Madurez Digital", DiagnosisCompany.company_id == company.id).first()
                    orj =  json.loads(madurez_digitalx.respuestas)
                    for resp in orj:
                        if clave in resp:  
                            resp[clave] = 3
                            encontro = True
                    if encontro:
                        madurez_digital = ["_3_1","_3_2","_3_3","_3_4","_3_5","_3_6","_3_7","_3_8","_3_9","_3_10","_3_11"]
                        total_madurez_digital = 0
                        for clave in madurez_digital:
                            for resp in orj:
                                if clave in resp:
                                    total_madurez_digital = total_madurez_digital + int(resp[clave])
                                    print("Pregunta: {} respuesta: {}".format(clave,resp[clave]))
                        resultado_madurez_digital = total_madurez_digital/(len(madurez_digital)*3) * 0.10 * 100
                        resultado_madurez_digital = round(resultado_madurez_digital, 2)
                        #desactivar
                        madurez_digitalx.status = 0
                        db.session.add(madurez_digitalx)
                        db.session.commit()
                        #crear
                        diagnosis = DiagnosisCompany()
                        diagnosis.categoria = "Mercadeo y ventas"
                        diagnosis.result_total = resultado_madurez_digital 
                        diagnosis.result_area = total_madurez_digital
                        diagnosis.status = True
                        diagnosis.created_by = current_user.id
                        diagnosis.company_id = company.id
                        diagnosis.respuestas = orj
                        db.session.add(diagnosis)
                        db.session.commit()   

                    #4
                    encontro = False
                    clave = servicio_mejorado['id']
                    gestion_financierax =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Gestión Financiera", DiagnosisCompany.company_id == company.id).first()
                    orj =  json.loads(gestion_financierax.respuestas)
                    for resp in orj:
                        if clave in resp:  
                            resp[clave] = 3
                            encontro = True
                    if encontro:
                        gestion_financiera = ["_4_1","_4_2","_4_3","_4_4","_4_5","_4_6","_4_7","_4_8","_4_9","_4_10","_4_11","_4_12","_4_13","_4_14","_4_15","_4_16","_4_17","_4_18","_4_19","_4_20","_4_21" ]
    
                        total_gestion_financiera = 0
                        for clave in gestion_financiera:
                            for resp in orj:
                                if clave in resp:
                                    total_gestion_financiera = total_gestion_financiera + int(resp[clave])
                                    print("Pregunta: {} respuesta: {}".format(clave,resp[clave]))
                        resultado_gestion_financiera = total_gestion_financiera/(len(gestion_financiera)*3)  * 0.25 * 100
                        resultado_gestion_financiera = round(resultado_gestion_financiera, 2)
                        #desactivar
                        gestion_financierax.status = 0
                        db.session.add(gestion_financierax)
                        db.session.commit()
                        #crear
                        diagnosis = DiagnosisCompany()
                        diagnosis.categoria = "Gestión Financiera"
                        diagnosis.result_total = resultado_gestion_financiera 
                        diagnosis.result_area = total_gestion_financiera
                        diagnosis.status = True
                        diagnosis.created_by = current_user.id
                        diagnosis.company_id = company.id
                        diagnosis.respuestas = orj
                        db.session.add(diagnosis)
                        db.session.commit()   
                    #5
                    encontro = False
                    clave = servicio_mejorado['id']
                    gestion_produccionx =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Gestión de la producción", DiagnosisCompany.company_id == company.id).first()
                    orj =  json.loads(gestion_produccionx.respuestas)
                    for resp in orj:
                        if clave in resp:  
                            resp[clave] = 3
                            encontro = True
                    if encontro:
                        gestion_produccion = ["_5_1","_5_2","_5_3","_5_4","_5_5","_5_6","_5_7","_5_8","_5_9","_5_10","_5_11","_5_12","_5_13","_5_14","_5_15","_5_16","_5_17","_5_18","_5_19","_5_20","_5_21","_5_22","_5_23","_5_24",]
                        total_gestion_produccion = 0
                        for clave in gestion_produccion:
                            for resp in orj:
                                if clave in resp:
                                    total_gestion_produccion = total_gestion_produccion + int(resp[clave])
                                    print("Pregunta: {} respuesta: {}".format(clave,resp[clave]))
                        resultado_gestion_produccion = total_gestion_produccion/(len(gestion_produccion)*3)  * 0.20 * 100
                        resultado_gestion_produccion = round(resultado_gestion_produccion, 2)
                        #desactivar
                        gestion_produccionx.status = 0
                        db.session.add(gestion_produccionx)
                        db.session.commit()
                        #crear
                        diagnosis = DiagnosisCompany()
                        diagnosis.categoria = "Gestión de la producción"
                        diagnosis.result_total = resultado_gestion_produccion 
                        diagnosis.result_area = total_gestion_produccion
                        diagnosis.status = True
                        diagnosis.created_by = current_user.id
                        diagnosis.company_id = company.id
                        diagnosis.respuestas = orj
                        db.session.add(diagnosis)
                        db.session.commit()   

                    #6
                    encontro = False
                    clave = servicio_mejorado['id']
                    organizacion_gestionx =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Organización y Gestión del talento humano", DiagnosisCompany.company_id == company.id).first()
                    orj =  json.loads(organizacion_gestionx.respuestas)
                    for resp in orj:
                        if clave in resp:  
                            resp[clave] = 3
                            encontro = True
                    if encontro:
                        organizacion_gestion = ["_6_1","_6_2","_6_3","_6_4","_6_5","_6_6","_6_7","_6_8","_6_9","_6_10","_6_11","_6_12","_6_13","_6_14","_6_15","_6_16" ,"_6_17"]
        
                        total_organizacion_gestion = 0
                        for clave in organizacion_gestion:
                            for resp in orj:
                                if clave in resp:
                                    total_organizacion_gestion = total_organizacion_gestion + int(resp[clave])
                                    print("Pregunta: {} respuesta: {}".format(clave,resp[clave]))
                        resultado_organizacion_gestion = total_organizacion_gestion/(len(organizacion_gestion)*3)  * 0.10 * 100
                        resultado_organizacion_gestion = round(resultado_organizacion_gestion, 2)
                        #desactivar
                        organizacion_gestionx.status = 0
                        db.session.add(organizacion_gestionx)
                        db.session.commit()
                        #crear
                        diagnosis = DiagnosisCompany()
                        diagnosis.categoria = "Organización y Gestión del talento humano"
                        diagnosis.result_total = resultado_organizacion_gestion 
                        diagnosis.result_area = total_organizacion_gestion
                        diagnosis.status = True
                        diagnosis.created_by = current_user.id
                        diagnosis.company_id = company.id
                        diagnosis.respuestas = orj
                        db.session.add(diagnosis)
                        db.session.commit()   
                return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
                    
                    
                mercadeo_ventas =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Mercadeo y ventas", DiagnosisCompany.company_id == company.id).first()
                print(mercadeo_ventas.respuestas)
                madurez_digital =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Madurez Digital", DiagnosisCompany.company_id == company.id).first()
                print(madurez_digital.respuestas)
                gestion_financiera =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Gestión Financiera", DiagnosisCompany.company_id == company.id).first()
                print(json.loads(gestion_financiera.respuestas))
                r = json.dumps(gestion_financiera.respuestas)

                gestion_produccion =  DiagnosisCompany.query.filter(DiagnosisCompany.categoria == "Gestión de la producción", DiagnosisCompany.company_id == company.id).first()
                print(json.loads(gestion_produccion.respuestas))

                organizacion_gestionx =  DiagnosisCompany.query.filter( DiagnosisCompany.categoria == "Organización y Gestión del talento humano", DiagnosisCompany.company_id == company.id).first()
                print(json.loads(organizacion_gestionx.respuestas))
                orj =  json.loads(organizacion_gestionx.respuestas)
                clave = '_6_5'
                for resp in orj:
                    if clave in resp:
                        resp[clave] = 3
                     
                        print('siiiiiiiii')
                        print('siiiiiiiii')
                        print('siiiiiiiii')
                        print('siiiiiiiii')
                        print('siiiiiiiii')
                organizacion_gestion = ["_6_1","_6_2","_6_3","_6_4","_6_5","_6_6","_6_7","_6_8","_6_9","_6_10","_6_11","_6_12","_6_13","_6_14","_6_15","_6_16" ,"_6_17"]
 
                respuestas_organizacion_gestion = [clave]
                total_organizacion_gestion = 0
                for clave in organizacion_gestion:
                    for resp in orj:
                        if clave in resp:
                            respuestas_organizacion_gestion.append({clave:resp[clave]})
                            total_organizacion_gestion = total_organizacion_gestion + int(resp[clave])
                            print("Pregunta: {} respuesta: {}".format(clave,resp[clave]))

                resultado_organizacion_gestion = total_organizacion_gestion/(len(organizacion_gestion)*3) * 0.10 * 100
                resultado_organizacion_gestion = round(resultado_organizacion_gestion, 2)

                #desactivar
                organizacion_gestionx.status = 0
                db.session.add(organizacion_gestionx)
                db.session.commit()
                #crear
                diagnosis = DiagnosisCompany()
                diagnosis.categoria = "Organización y Gestión del talento humano"
                diagnosis.result_total = resultado_organizacion_gestion 
                diagnosis.result_area = total_organizacion_gestion
                diagnosis.status = True
                diagnosis.created_by = current_user.id
                diagnosis.company_id = company.id
                diagnosis.respuestas = orj
                db.session.add(diagnosis)
                db.session.commit()                                

        return jsonify({ 'status': 200, 'msg': 'Perfil actulizado con' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': e })

