from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response,send_from_directory
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import AttentionLog,WalletTransaction,ActionPlanReferences,DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Company,Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import CompanyMonitoring,ServiceChannel,CompanyStage,EnrollmentRecord,CompanyStatus,TrainingType,ModalityType,CourseManagers,Courses,catalogCategory,CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from models.diagnostico import Diagnosticos
from werkzeug.utils import secure_filename
from sqlalchemy import or_,not_
import pytz
from views.wallet import _update_wallet

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
import os

mae = Blueprint('mae', __name__, template_folder='templates', static_folder='static')

#entry


@mae.route('/mae/create')
def _create_company():
    return render_template('/mae/create_company.html')

#process
@mae.route('/mae/home')
def _mae_home():
    return render_template('/mae/home.html')

@mae.route('/mae/list')
def _mae_list():
    return render_template('/mae/mae_list.html')
#    return render_template('/digitalcenter/form_profile_sde.html')

#output
@mae.route('/mae/perfil')
def _mae_perfil():
    return render_template('/mae/perfil.html')