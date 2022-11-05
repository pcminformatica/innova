from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned

digitalcenter = Blueprint('digitalcenter', __name__, template_folder='templates', static_folder='static')

@digitalcenter.route('/digitalcenter/')
def _home_view():
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