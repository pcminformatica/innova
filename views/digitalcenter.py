from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User
digitalcenter = Blueprint('digitalcenter', __name__, template_folder='templates', static_folder='static')


@digitalcenter.route('/form/perfil/')
@login_required
def __form_perfil_emp():
        
    app.logger.debug('** SWING_CMS ** - Welcome2')

    user = User.query.filter_by(id = current_user.id).first()
    app.logger.debug('** SWING_CMS ** - Welcome2')

    ctx = {'user':user}
    return render_template('/digitalcenter/form_perfil_emp.html',ctx=ctx)
  


@digitalcenter.route('/digitalcenter/')
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
    app.logger.debug('** zzzzzzzzzzz varela')   
    app.logger.debug(x)
    app.logger.debug('** iiiiiiiiiiii varela')   
    new_userlist = new_oul.userlist
    app.logger.debug(new_userlist)    
    app.logger.debug('** xxxxxxxxxxxxx varela')    
    app.logger.debug('** SWING_CMS ** - Welcome2')
    return render_template('digitalcenter/home_view.html')

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
