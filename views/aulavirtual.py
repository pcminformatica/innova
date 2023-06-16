from . import credentials,auth,changePassword, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app

from flask_login import logout_user, current_user, login_required
from models.models import WalletTransaction,catalogCategory,DocumentCompany,Company, DiagnosisCompany,ActionPlan, Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
aulavirtual = Blueprint('aulavirtual', __name__, template_folder='templates', static_folder='static')

# Creates Timestamps without UTC for JavaScript handling:
# utcDate.replace(tzinfo=tz.utc).timestamp()
#
# Creates Dates witout UTC for Python handling:
# utcDate.replace(tzinfo=tz.utc).astimezone(tz=None)
import json


@aulavirtual.route('/formulario/')
def _curso_created():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    return render_template('aulavirtual/curso_created.html')

@aulavirtual.route('/enroll/')
def _curso_enroll():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    return render_template('aulavirtual/curso_enroll.html')

@aulavirtual.route('/cursos/list/')
def _curso_list():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    return render_template('aulavirtual/curso_list.html')