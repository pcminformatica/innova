from datetime import datetime as dt
from datetime import timezone as tz
from flask import current_app as app
from flask import jsonify
from models import db, CatalogIDDocumentTypes, CatalogServices, CatalogOperations, CatalogUserRoles, RTCOnlineUsers, User, UserXRole
from models import CatalogSurveysAnswerTypes, Surveys, SurveysQuestions

# -----------------------------------------------------------------------------------------------------
# DATABASE MINIMUM REQUIRED DATA
# POPULATION FUNCTIONS
# -----------------------------------------------------------------------------------------------------

# Initialize Database Populate Function
def initPopulateDB():
    # Add Surveys Answer Types Catalog
    populateSurveysAnswerTypesCatalog()

    # Add Survey - User Satisfaction
    populateSurveyUserSatisfaction()

    # Add Operations Catalog
    populateCatalogOperations()

    # Add User Roles Catalog
    populateCatalogUserRoles()

    # Add Services Catalog
    populateServicesCatalog()

    # Add ID Document Type Catalog
    populateCatalogIDDocType()

    # Add Default Users
    populateDefaultUsers()

    # Add Default RTC_OUL
    populateDefaultRTC_OUL()

    app.logger.info('** SWING_CMS ** - Populate Database FINISHED.')


# Initialize Elastic Search Populate Function
def initPopulateES():
    try:
        # Delete current indexes
        User.delete_index()

        # Index available records
        User.reindex()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Initialize Populate Elastic Search Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Default RTC Online User List
def populateDefaultRTC_OUL():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Default RTC Online User List')

        #Add Default RTC_OUL JSON
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
                'reg_users': []
            }
        }
        rtc_oul.enabled = True
        db.session.add(rtc_oul)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Default RTC Online User List Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Default Users
def populateDefaultUsers():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Default Users')

        # Add Admin User
        admin_user = User()
        admin_user.uid = 'INNO-Administrator'
        admin_user.email = 'admusr@innova.com'
        admin_user.name = 'Innova Administrador'
        admin_user.cmuserid = 'INNO-ADM-200000-0001'
        db.session.add(admin_user)
        db.session.flush()
        # Add Admin Role
        admin_role = CatalogUserRoles.query.filter_by(name_short='adm').first()
        admin_userxrole = UserXRole()
        admin_userxrole.user_id = admin_user.id
        admin_userxrole.user_role_id = admin_role.id
        db.session.add(admin_userxrole)

        db.session.commit()

        # Add Anon User
        anon_user = User()
        anon_user.uid = 'INNO-Anonim@'
        anon_user.email = 'anon@innova.com'
        anon_user.name = 'Anonim@'
        anon_user.cmuserid = 'INNO-ANN-200000-0001'
        db.session.add(anon_user)
        db.session.flush()
        # Add User Role
        user_role = CatalogUserRoles.query.filter_by(name_short='usr').first()
        anon_userxrole = UserXRole()
        anon_userxrole.user_id = anon_user.id
        anon_userxrole.user_role_id = user_role.id
        db.session.add(anon_userxrole)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Default Users Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Catalog Services Data
def populateServicesCatalog(column=None):
    try:
        app.logger.debug('** SWING_CMS ** - Populate Catalog Services')

        if column is None:
            # Add Services
            staff_it_role = CatalogUserRoles.query.filter_by(name_short='itc').first()
            websites = CatalogServices(name='Páginas web', name_short='web', service_user_role=staff_it_role.id)
            db.session.add(websites)

            ecommerce = CatalogServices(name='Pagos online', name_short='pay', service_user_role=staff_it_role.id)
            db.session.add(ecommerce)

            seo = CatalogServices(name='Aparece en Google', name_short='seo', service_user_role=staff_it_role.id)
            db.session.add(seo)

            support = CatalogServices(name='Soporte técnico', name_short='sup', service_user_role=staff_it_role.id)
            db.session.add(support)
            
            db.session.commit()
        
        elif column == 'sur':
            # Add Service's User Role
            services = CatalogServices.query.all()
            hasUpd = False
            
            for service in services:
                usr_role = CatalogUserRoles.query.filter_by(name_short=service.name_short).first()
                
                if usr_role is not None:
                    service.service_user_role = usr_role.id
                    db.session.add(service)
                    hasUpd = True
            
            if hasUpd:
                db.session.commit()
        
        elif column == 'sch':
            # Add Service's Sessions Schedule
            websrv = CatalogServices.query.filter_by(name_short='web').first()
            websrv.sessions_schedule = [{
                'weeks': 'all',
                'wdays': ['tue', 'wed', 'thu'],
                'hours': [
                    {'start_time': '8:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '9:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '10:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '11:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '13:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '14:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '15:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'evening'}
                ]
            },{
                'weeks': 'even',
                'wdays': ['mon', 'fri'],
                'hours': [
                    {'start_time': '9:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '10:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '12:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '14:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '15:00', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'evening'}
                ]
            },{
                'weeks': 'odd',
                'wdays': ['mon', 'fri'],
                'hours': [
                    {'start_time': '10:30', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '14:30', 'duration': websrv.duration_minutes, 'break_time': websrv.break_minutes, 'tod': 'evening'}
                ]
            }]
            db.session.add(websrv)

            paysrv = CatalogServices.query.filter_by(name_short='pay').first()
            paysrv.sessions_schedule = [{
                'weeks': 'all',
                'wdays': ['mon', 'tue', 'wed', 'thu', 'fri'],
                'hours': [
                    {'start_time': '05:00', 'duration': paysrv.duration_minutes, 'break_time': paysrv.break_minutes, 'tod': 'dawn'},
                    {'start_time': '10:00', 'duration': paysrv.duration_minutes, 'break_time': paysrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '11:00', 'duration': paysrv.duration_minutes, 'break_time': paysrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '13:00', 'duration': paysrv.duration_minutes, 'break_time': paysrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '14:00', 'duration': paysrv.duration_minutes, 'break_time': paysrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '15:00', 'duration': paysrv.duration_minutes, 'break_time': paysrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '17:00', 'duration': paysrv.duration_minutes, 'break_time': paysrv.break_minutes, 'tod': 'night'},
                    {'start_time': '19:00', 'duration': paysrv.duration_minutes, 'break_time': paysrv.break_minutes, 'tod': 'night'},
                    {'start_time': '21:00', 'duration': paysrv.duration_minutes, 'break_time': paysrv.break_minutes, 'tod': 'night'}
                ]
            }]
            db.session.add(paysrv)

            seosrv = CatalogServices.query.filter_by(name_short='seo').first()
            seosrv.sessions_schedule = [{
                'weeks': 'all',
                'wdays': ['mon', 'tue', 'wed', 'thu'],
                'hours': [
                    {'start_time': '8:00', 'duration': seosrv.duration_minutes, 'break_time': seosrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '9:00', 'duration': seosrv.duration_minutes, 'break_time': seosrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '10:00', 'duration': seosrv.duration_minutes, 'break_time': seosrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '11:00', 'duration': seosrv.duration_minutes, 'break_time': seosrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '13:00', 'duration': seosrv.duration_minutes, 'break_time': seosrv.break_minutes, 'tod': 'evening'}
                ]
            },{
                'weeks': 'all',
                'wdays': ['fri'],
                'hours': [
                    {'start_time': '10:00', 'duration': seosrv.duration_minutes, 'break_time': seosrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '14:00', 'duration': seosrv.duration_minutes, 'break_time': seosrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '18:00', 'duration': seosrv.duration_minutes, 'break_time': seosrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '22:00', 'duration': seosrv.duration_minutes, 'break_time': seosrv.break_minutes, 'tod': 'night'}
                ]
            }]
            db.session.add(seosrv)

            supsrv = CatalogServices.query.filter_by(name_short='sup').first()
            supsrv.sessions_schedule = [{
                'weeks': 'all',
                'wdays': ['mon', 'tue', 'wed', 'thu'],
                'hours': [
                    {'start_time': '8:00', 'duration': supsrv.duration_minutes, 'break_time': supsrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '9:00', 'duration': supsrv.duration_minutes, 'break_time': supsrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '10:00', 'duration': supsrv.duration_minutes, 'break_time': supsrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '11:00', 'duration': supsrv.duration_minutes, 'break_time': supsrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '13:00', 'duration': supsrv.duration_minutes, 'break_time': supsrv.break_minutes, 'tod': 'evening'}
                ]
            },{
                'weeks': 'all',
                'wdays': ['fri'],
                'hours': [
                    {'start_time': '10:00', 'duration': supsrv.duration_minutes, 'break_time': supsrv.break_minutes, 'tod': 'morning'},
                    {'start_time': '14:00', 'duration': supsrv.duration_minutes, 'break_time': supsrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '18:00', 'duration': supsrv.duration_minutes, 'break_time': supsrv.break_minutes, 'tod': 'evening'},
                    {'start_time': '22:00', 'duration': supsrv.duration_minutes, 'break_time': supsrv.break_minutes, 'tod': 'night'}
                ]
            }]
            db.session.add(supsrv)

            db.session.commit()

        else: 
            app.logger.debug('** SWING_CMS ** - Populate Catalog Services - Argument Invalid')

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Catalog Services Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Surveys Answer Types
def populateSurveysAnswerTypesCatalog():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Catalog Surveys Answer Types')

        # Add Answer Types
        checkboxes = CatalogSurveysAnswerTypes(name='Selección Múltiple', name_short='chk')
        db.session.add(checkboxes)

        radios = CatalogSurveysAnswerTypes(name='Selección Única', name_short='rad')
        db.session.add(radios)
        
        satisfaction = CatalogSurveysAnswerTypes(name='Rango de Satisfacción (3 Niveles)', name_short='sat_3')
        db.session.add(satisfaction)

        satisfactionFaces = CatalogSurveysAnswerTypes(name='Rango de Satisfacción (3 Caritas)', name_short='sat_3f')
        db.session.add(satisfactionFaces)

        textbox = CatalogSurveysAnswerTypes(name='Respuesta de Usuario', name_short='txt')
        db.session.add(textbox)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Catalog Surveys Answer Types Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Survey - User Satisfaction
def populateSurveyUserSatisfaction():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Survey User Satisfaction')

        # Add Questions
        ans_type = CatalogSurveysAnswerTypes.query.filter_by(name_short='sat_3f').first()

        question01 = SurveysQuestions(
            question = '¿Cómo calificas tu experiencia con el servicio recibido?',
            question_answers = {
                'a_1': 'sentiment_very_dissatisfied',
                'a_2': 'sentiment_satisfied',
                'a_3': 'sentiment_very_satisfied'
            },
            answers_type = ans_type.id
        )
        db.session.add(question01)

        question02 = SurveysQuestions(
            question = '¿Cómo calificas tu experiencia con la plataforma?',
            question_answers = {
                'a_1': 'sentiment_very_dissatisfied',
                'a_2': 'sentiment_satisfied',
                'a_3': 'sentiment_very_satisfied'
            },
            answers_type = ans_type.id
        )
        db.session.add(question02)

        db.session.commit()

        # Add Survey and it's Questions
        userSatisfactionSurvey = Surveys(
            name = 'Encuesta de satisfacción de atención.',
            name_short = 'uss',
            description = 'Encuesta de satisfacción de usuario sobre la atención recibida y el uso de la plataforma.',
            questions = {
                'q_1': question01.id,
                'q_2': question02.id
            }
        )
        db.session.add(userSatisfactionSurvey)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Survey User Satisfaction Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Catalog Operations Data
def populateCatalogOperations():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Catalog Operations')

        # Add Operation
        insert = CatalogOperations(name='Inserción', name_short='ins')
        db.session.add(insert)

        delete = CatalogOperations(name='Eliminación', name_short='del')
        db.session.add(delete)

        update = CatalogOperations(name='Actualización', name_short='upd')
        db.session.add(update)

        read = CatalogOperations(name='Lectura', name_short='read')
        db.session.add(read)

        connect = CatalogOperations(name='Conexión', name_short='con')
        db.session.add(connect)

        disconnect = CatalogOperations(name='Desconexión', name_short='dcon')
        db.session.add(disconnect)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Catalog Operations Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Catalog ID Document Type Data
def populateCatalogIDDocType():
    try:
        app.logger.debug('** SWING_CMS ** - Populate ID Document Type')

        # Add ID Document Type
        nat_id = CatalogIDDocumentTypes(name='Identificación Nacional', name_short='nid')
        db.session.add(nat_id)

        passport = CatalogIDDocumentTypes(name='Pasaporte', name_short='pas')
        db.session.add(passport)

        driver_lic = CatalogIDDocumentTypes(name='Licencia de conducir', name_short='lic')
        db.session.add(driver_lic)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate ID Document Type Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Catalog User Roles Data
def populateCatalogUserRoles():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Catalog User Roles')

        # Add User Roles
        user_role = CatalogUserRoles(name='Usuario', name_short='usr')
        db.session.add(user_role)

        admin_role = CatalogUserRoles(name='Administrador', name_short='adm')
        db.session.add(admin_role)
        
        entrepreneur_role = CatalogUserRoles(name='Empresaria', name_short='emp')
        db.session.add(entrepreneur_role)

        provider_role = CatalogUserRoles(name='Oferente', name_short='ofe')
        db.session.add(provider_role)

        staff_it_role = CatalogUserRoles(name='Colaborador IT', name_short='itc')
        db.session.add(staff_it_role)

        staff_design_role = CatalogUserRoles(name='Colaborador Diseño', name_short='dis')
        db.session.add(staff_design_role)

        staff_marketing_role = CatalogUserRoles(name='Colaborador Marketing', name_short='mkt')
        db.session.add(staff_marketing_role)

        staff_coordinator_role = CatalogUserRoles(name='Coordinador', name_short='coo')
        db.session.add(staff_coordinator_role)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Catalog User Roles Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Specified Table
def populateTable(dp_name, dp_options=None):
    try:
        app.logger.debug('** SWING_CMS ** - Populate Specified Table')

        data_procedures = {
            "catalog_id_types": populateCatalogIDDocType,
            "catalog_operations": populateCatalogOperations,
            "catalog_services": populateServicesCatalog,
            "catalog_user_roles": populateCatalogUserRoles,
            "default_rtc_oul": populateDefaultRTC_OUL,
            "default_users": populateDefaultUsers,
            "survey_answer_types": populateSurveysAnswerTypesCatalog,
            "survey_uss": populateSurveyUserSatisfaction
        }

        if callable(data_procedures[dp_name]):
            if dp_options is not None:
                data_procedures[dp_name](dp_options)
            else:
                data_procedures[dp_name]()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Specified Table Error: {}'.format(e))
        return jsonify({ 'status': 'error' })

