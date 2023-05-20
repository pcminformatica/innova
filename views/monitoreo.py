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
    list_user = [3,5,6,15,16,17,18,20,21,25,24,30]
    users = User.query.filter(User.id.in_(list_user)).order_by(User.name.asc()).all()
    #consultamos en KOBO la cantidad de diagnosticos
    url = app.config.get('KOBOTOOLBOX_ALL')
    headers=app.config.get('KOBOTOOLBOX_TOKEN')
    resp = requests.get(url,headers=headers)
    api = json.loads(resp.content)
    datos =  []
    for user in users:
        cod_usuario = user.id
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
        
        references_accepted = ActionPlanReferences.query.filter_by(employe_assigned=user.id,employe_accepted=True).order_by(desc(ActionPlanReferences.id)).all()
        lista = []
        for reference in references_accepted:
            lista.append(reference.action_plan.company.id)
        company_references_accepted = Company.query.filter(Company.id.in_(lista)).all()

        bitacoras = ActionPlanHistory.query.distinct(ActionPlanHistory.action_plan_id).filter(ActionPlanHistory.created_by==user.id,ActionPlanHistory.cancelled==False)
        servicios =   []
        serviciosfin =  []
        for bitacora in bitacoras:
            if bitacora.action_plan_id not in servicios:
                if bitacora.action_plan.progress == 100:
                    serviciosfin.append(bitacora.action_plan_id)
                servicios.append(bitacora.action_plan_id)

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
            'cod_usuario':cod_usuario,
            'nombre':full_name,
            'profesion':profesion,
            'diagnosticos':diagnosticos,
            'company':len(companys),
            'company_references':len(company_references),
            'company_references_accepted':len(company_references_accepted),
            'planes':planes,
            'servicios':len(servicios),
            'serviciosproceso':len(servicios) -len(serviciosfin),
            'serviciosfin':len(serviciosfin)
        }
        datos.append(diccionario)
    context = {'datos':datos}
    return render_template('monitoreo/indicadores_productividad.html',**context)

@monitoreo.route('/indicadores/servicios/',methods = ['GET', 'POST'])
def _indicadores_servicios():
    #inscritas
    inscritas_cohorte1 = 585
    inscritas_cohorte2 = 613
    inscritas_cohorte3 = 83
    inscritas_cohorte4 = 285 + 33
    #elegibles
    elegibles_cohorte1 = 238
    elegibles_cohorte2 = 170
    elegibles_cohorte3 = 28 
    elegibles_cohorte4 = 243 + 15
    #Quinta cohorte
    query = Inscripciones.query.filter(Inscripciones.cohorte==5).order_by(Inscripciones.id.desc())
    repite = []
    repiteobj =[]
    repiteobjelegibles =[]
    for obj in query:
        if not obj.dni in repite:
            repite.append(obj.dni)
            repiteobj.append(obj)
            if(obj.elegible):
                repiteobjelegibles.append(obj)
    inscritas_cohorte5 = len(repiteobj)
    elegibles_cohorte5 =len(repiteobjelegibles)
    total_inscritas = inscritas_cohorte1 +inscritas_cohorte2 +inscritas_cohorte3 +inscritas_cohorte4 +inscritas_cohorte5
    total_elegibles = elegibles_cohorte1 +elegibles_cohorte2 +elegibles_cohorte3 + elegibles_cohorte4 + elegibles_cohorte5
    url = app.config.get('KOBOTOOLBOX_ALL')
    headers=app.config.get('KOBOTOOLBOX_TOKEN')
    resp = requests.get(url,headers=headers)
    api = json.loads(resp.content)
    diagnosticos = []
    for e in api['results']:
        if 'estado' in e:
            if e['estado'] !=0:
                diagnosticos.append(e)
        else:
            diagnosticos.append(e)
    companys = Company.query.join(User, User.id==Company.created_by).filter(Company.enabled==True).all()
    planes = 0
    serviciosTotal = 0
    serviciosNoinciados = 0
    serviciosEnProceso = 0
    serviciosFinalizados = 0
    for company in companys:
        plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0).first()
        if plan:
            planes = planes + 1
            actionPlan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0).all()
            for plane in actionPlan:
                serviciosTotal = serviciosTotal + 1
                if plane.progress == 0:
                    serviciosNoinciados = serviciosNoinciados + 1
                elif plane.progress == 100:
                    serviciosFinalizados= serviciosFinalizados + 1
                else:
                    serviciosEnProceso =serviciosEnProceso+1
            
    context = {
        'total_inscritas': total_inscritas,
        'total_elegibles':total_elegibles,
        'diagnosticos':len(diagnosticos),
        'planes':planes,
        'serviciosTotal':serviciosTotal,
        'serviciosNoinciados':serviciosNoinciados,
        'serviciosEnProceso':serviciosEnProceso,
        'serviciosFinalizados':serviciosFinalizados,
    }

    return render_template('monitoreo/indicadores_servicios.html',**context)

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



@monitoreo.route('/indicador/perfil/<int:user_uid>/view',methods=['GET', 'POST'])
def _indicadores_perfil_asesor(user_uid):
    user = User.query.filter(User.id==user_uid).first()
    url = app.config.get('KOBOTOOLBOX_ALL')
    headers=app.config.get('KOBOTOOLBOX_TOKEN')
    resp = requests.get(url,headers=headers)
    api = json.loads(resp.content)
    datos =  []
    
    cod_usuario = user.id
    #contamos los diagnosticos
    diagnosticos = 0
    if user.extra_info.kobotoolbox:
        
        diagnosticos = list(e for e in api['results'] if e['_submitted_by']  in user.extra_info.kobotoolbox['kobotoolbox_access'] )
 
    companys = Company.query.join(User, User.id==Company.created_by).filter(Company.enabled==True, Company.created_by == user.id).all()
    planes = 0
    for company in companys:
        plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0).first()
        planes  =  []
        if plan:
            planes.append(company.id) 
    planes = Company.query.filter(Company.id.in_(planes)).all()
    references = ActionPlanReferences.query.filter_by(employe_assigned=user.id).order_by(desc(ActionPlanReferences.id)).all()
    lista = []
    for reference in references:
        lista.append(reference.action_plan.company.id)
    company_references = Company.query.filter(Company.id.in_(lista)).all()
    
    references_accepted = ActionPlanReferences.query.filter_by(employe_assigned=user.id,employe_accepted=True).order_by(desc(ActionPlanReferences.id)).all()
    lista = []
    for reference in references_accepted:
        lista.append(reference.action_plan.company.id)
    company_references_accepted = Company.query.filter(Company.id.in_(lista)).all()

    bitacoras = ActionPlanHistory.query.distinct(ActionPlanHistory.action_plan_id).filter(ActionPlanHistory.created_by==user.id,ActionPlanHistory.cancelled==False)
    servicios =   []
    serviciosfin =  []
    for bitacora in bitacoras:
        if bitacora.action_plan_id not in servicios:
            if bitacora.action_plan.progress == 100:
                serviciosfin.append(bitacora.action_plan_id)
            servicios.append(bitacora.action_plan_id)

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

    context = {
        'cod_usuario':cod_usuario,
        'nombre':full_name,
        'profesion':profesion,
        'diagnosticos':diagnosticos,
        'company':companys,
        'company_references':company_references,
        'company_references_accepted':len(company_references_accepted),
        'planes':planes,
        'servicios':len(servicios),
        'serviciosproceso':len(servicios) -len(serviciosfin),
        'serviciosfin':len(serviciosfin),
        'users': user
        }
    return render_template('monitoreo/indicadores_perfil_asesor.html',**context)