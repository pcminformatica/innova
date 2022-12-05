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

admindash = Blueprint('admindash', __name__, template_folder='templates', static_folder='static')


@admindash.route('/admin/list/user/', methods = ['GET'])
@login_required
def _admin_list_user():

    app.logger.debug('** SWING_CMS ** - listuser')
    users = User.query.all()
    app.logger.debug(users)
    cxt = {'users':users}
        
    return render_template('/admindash/listuser.html',**cxt)

@admindash.route('/admin/list/user/<int:user_id>/custom', methods = ['GET'])
@login_required
def _admin_form_user(user_id):

    app.logger.debug('** SWING_CMS ** - listuser')
    user = User.query.filter_by(id = user_id).first()
    roles = CatalogUserRoles.query.all()
    cxt = {'user':user,'roles':roles}
        
    return render_template('/admindash/formuser.html',**cxt)
