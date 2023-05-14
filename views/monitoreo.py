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
from sqlalchemy import desc
import requests
import json 
@monitoreo.route('/indicadores/productividad/',methods = ['GET', 'POST'])
def _indicadores_productividad():
    #lista de usuarios a evaluar
    list_user = [3,4,5,6,15,16,17,18,20,21,25,24,30]
    users = User.query.filter(User.id.in_(list_user)).order_by(User.name.desc()).all()
    #consultamos en KOBO la cantidad de diagnosticos
    url = app.config.get('KOBOTOOLBOX_ALL')
    headers=app.config.get('KOBOTOOLBOX_TOKEN')
    resp = requests.get(url,headers=headers)
    api = json.loads(resp.content)
    datos =  []
    for user in users:
        #contamos los diagnosticos
        diagnosticos = 0
        if user.extra_info.kobotoolbox:
            diagnosticos = list(e for e in api['results'] if e['_submitted_by']  in user.extra_info.kobotoolbox['kobotoolbox_access'] )
            if diagnosticos:
                diagnosticos = len(diagnosticos)
        companys = Company.query.join(User, User.id==Company.created_by).filter(Company.enabled==True, Company.created_by == user.id).all()
        planes = 0
        for company in companys:
            plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0).first()
            if plan:
                planes = planes + 1
        references = ActionPlanReferences.query.filter_by(employe_assigned=user.id).order_by(desc(ActionPlanReferences.id)).all()
        lista = []
        for reference in references:
            lista.append(reference.action_plan.company.id)
        company_references = Company.query.filter(Company.id.in_(lista)).all()
        profesion = ''
        if user.extra_info.profession:
            profesion = user.extra_info.profession.name
        names = ''
        if user.extra_info.names:
            names = user.extra_info.names
        last_names = ''
        if  user.extra_info.last_names:
            last_names = user.extra_info.last_names
        full_name = names + ' ' + last_names

        diccionario = {
            'nombre':full_name,
            'profesion':profesion,
            'diagnosticos':diagnosticos,
            'company':len(companys),
            'company_references':len(company_references),
            'planes':planes
        }
        datos.append(diccionario)
    context = {'datos':datos}
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
