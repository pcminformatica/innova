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
#@login_required
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
    app.logger.debug('** varela')   
    app.logger.debug(x)
    app.logger.debug('** iiiiiiiiiiii varela')   
    new_userlist = new_oul.userlist
    app.logger.debug(new_userlist)    
    app.logger.debug('** xxxxxxxxxxxxx varela')    
    app.logger.debug('** SWING_CMS ** - Welcome2')
    context = {'userRu':userRu,'userRi':userRi,'userLCB':userLCB,'userSPS':userSPS,'userCholo':userCholo,'userCholu':userCholu}
    return render_template('digitalcenter/home_view.html',**context)

@digitalcenter.route('/digitalcenter/chat/')
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
    return render_template('/digitalcenter/dc_chat_admin.html')

@digitalcenter.route('/digitalcenter/chat/home/')
def _dc_chat_home():
    app.logger.debug('** SWING_CMS ** - Welcome2')
    return render_template('/digitalcenter/dc_chat_home.html')


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
    return render_template('digitalcenter/appointments_create_admin.html')


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
    