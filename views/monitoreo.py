from . import credentials,auth,changePassword, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app

from flask_login import logout_user, current_user, login_required
from models.models import DocumentCompany,Company, DiagnosisCompany,ActionPlan, Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
monitoreo = Blueprint('monitoreo', __name__, template_folder='templates/', static_folder='static')
from models.models import ActionPlanReferences,DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Company,Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import catalogCategory,CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from models.diagnostico import Diagnosticos

@monitoreo.route('/indicadores/productividad/',methods = ['GET', 'POST'])
def _indicadores_productividad():
    list_user = [3,5,6,15,16,17,18,20,21,25,24,30]
    users = User.query.filter(User.id.in_(list_user)).order_by(User.name.desc()).all()
    context = {'users':users}
    return render_template('monitoreo/indicadores_productividad.html',**context)

@monitoreo.route('/indicadores/servicios/',methods = ['GET', 'POST'])
def _indicadores_servicios():
    return render_template('monitoreo/indicadores_servicios.html')

from collections import Counter
@monitoreo.route('/indicadores/inscritas/',methods = ['GET', 'POST'])
def _indicadores_inscritas():
    query = Inscripciones.query.filter(Inscripciones.cohorte==5).order_by(Inscripciones.id.desc())
    repite = []
    repiteobj =[]
    for obj in query:
        if not obj.dni in repite:
            repite.append(obj.dni)
            repiteobj.append(obj)
    context = {
        'inscripciones': repiteobj
    }
 
    return render_template('monitoreo/indicadores_inscritas.html',**context)
