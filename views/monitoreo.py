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
from models.models import Courses,CompanyStage,WalletTransaction,CompanyStatus,ActionPlanReferences,DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Company,Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import EnrollmentRecord,TrainingType, ModalityType,catalogCategory,CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from models.diagnostico import Diagnosticos
from sqlalchemy import desc
import requests
import json 
@monitoreo.route('/indicadores/productividad/',methods = ['GET', 'POST'])
@login_required
def _indicadores_productividad():
    #lista de usuarios a evaluar
    list_user = [3,5,6,15,16,17,18,20,21,25,24,30,66]
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
            plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.created_by == user.id,ActionPlan.company_id==company.id,ActionPlan.fase!=0).first()
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

@monitoreo.route('/indicadores/sde/productividad/',methods = ['GET', 'POST'])
@login_required
def _indicadores_productividad_sde():
    #lista de usuarios a evaluar
    list_user = [173,176,215,216,217]
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
            plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.created_by == user.id,ActionPlan.company_id==company.id,ActionPlan.fase!=0).first()
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



from sqlalchemy import or_
@monitoreo.route('/indicadores/servicios/',methods = ['GET', 'POST'])
@login_required
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
    query = Inscripciones.query.filter(Inscripciones.cohorte==5).filter(or_(Inscripciones.status != 0, Inscripciones.status == None)).order_by(Inscripciones.id.desc())
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
    capacitadasx = EnrollmentRecord.query.join(
        Courses, Courses.id==EnrollmentRecord.id_course).join(
        TrainingType, Courses.id_training_type==TrainingType.id).join(
        Company,Company.id == EnrollmentRecord.company_id).join(
        Inscripciones,Inscripciones.id == Company.inscripcion_id
        ).filter(
                TrainingType.name_short == 'TT1'
        ).all()
    
    inscripciones_ids_distintas = [company.company.inscripcion.id for company in capacitadasx]
    inscripciones = Inscripciones.query.filter_by(elegible = True).filter(Inscripciones.id.in_(inscripciones_ids_distintas)).filter(or_(Inscripciones.status != 0, Inscripciones.status == None)).all()
    capacitadas = len(inscripciones)  
    context = {
        'total_inscritas': total_inscritas,
        'total_elegibles':total_elegibles,
        'diagnosticos':len(diagnosticos),
        'planes':planes,
        'serviciosTotal':serviciosTotal,
        'serviciosNoinciados':serviciosNoinciados,
        'serviciosEnProceso':serviciosEnProceso,
        'serviciosFinalizados':serviciosFinalizados,
        'capacitadas':capacitadas
    }

    return render_template('monitoreo/indicadores_servicios.html',**context)

from collections import Counter
@monitoreo.route('/indicadores/inscritas/1',methods = ['GET', 'POST'])
@login_required
def _indicadores_inscritas_1():
    query = Inscripciones.query.filter(Inscripciones.cohorte==5).order_by(Inscripciones.id.desc())[0:150]
    repite = []
    repiteobj =[]
    for obj in query:
        if not obj.dni in repite:
            repite.append(obj.dni)
            repiteobj.append(obj)
    respuesta = []
    empresas = []
    preguntas = [
                "A",    
                "B",
                "C",
                "1_1",
                "1_2",
                "1_3",
                "1_4",
                "1_5",
                "1_6",
                "1_7",
                "1_8",
                "1_9",
                "1_10",
                "1_11",
                "2_1",
                "2_2",
                "2_3",
                "2_4",
                "2_5",
                "2_6",
                "2_7",
                "2_8",
                "3_1",
                "3_2",
                "3_3",
                "3_4",
                "3_5",
                "3_6",
                "3_7",
                "3_8",
                "3_9",
                "3_10",
                "3_11",
                "3_12",
                "3_13",
                "3_14",
                "3_15",
                "3_16",
                "3_17",
                "3_18",
                "3_19",
                "3_20",
                "3_21",
                "3_22",
                "3_23",
                "3_24",
                "3_25",
                "3_26",
                "3_27",
                "3_28",
                "3_29",
                "4_1",
                "4_2",
                "4_3",
                "4_4",
                "4_5",
                 ]
    
    for repite in repiteobj:
        if repite.respuestas:
            lista_dic =[]
            if repite.elegible: 
                elegible = 'ELEGIBLE'
            else:
                elegible = "NO ELEGIBLE"
            lista_dic.append({
                                        "id":'PVA',
                                        "pregunta":"ELEGIBLE",
                                        "respuesta":elegible,
                                    })
            for pregunta in preguntas:
                if len(list(e for e in repite.respuestas if e['id']  == pregunta)) != 0:
                    repites =list(e for e in repite.respuestas if e['id']  == pregunta)
        
                    titulo = repites[0]['pregunta']
                    respuesta= repites[0]['respuesta']
            
                    lista_dic.append({
                                        "id":pregunta,
                                        "pregunta":titulo,
                                        "respuesta":respuesta,
                                    })

                else:
                    lista_dic.append({
                                        "id":pregunta,
                                        "pregunta":"",
                                        "respuesta":"",
                                    })
            #for repites in repite.respuestas:

            empresas.append(lista_dic)    
    context = {
        'inscripciones': repiteobj,
        'respuesta':empresas
    }
 
    return render_template('monitoreo/indicadores_inscritas.html',**context)


@monitoreo.route('/indicadores/inscritas/2',methods = ['GET', 'POST'])
@login_required
def _indicadores_inscritas_2():
    query = Inscripciones.query.filter(Inscripciones.cohorte==5).order_by(Inscripciones.id.desc())[151:300]
    repite = []
    repiteobj =[]
  
   
    for obj in query:
        try:
            if not obj.dni in repite:
                repite.append(obj.dni)
                repiteobj.append(obj)
        except Exception as e:
            pass
    respuesta = []
    empresas = []
    preguntas = [
                "A",    
                "B",
                "C",
                "1_1",
                "1_2",
                "1_3",
                "1_4",
                "1_5",
                "1_6",
                "1_7",
                "1_8",
                "1_9",
                "1_10",
                "1_11",
                "2_1",
                "2_2",
                "2_3",
                "2_4",
                "2_5",
                "2_6",
                "2_7",
                "2_8",
                "3_1",
                "3_2",
                "3_3",
                "3_4",
                "3_5",
                "3_6",
                "3_7",
                "3_8",
                "3_9",
                "3_10",
                "3_11",
                "3_12",
                "3_13",
                "3_14",
                "3_15",
                "3_16",
                "3_17",
                "3_18",
                "3_19",
                "3_20",
                "3_21",
                "3_22",
                "3_23",
                "3_24",
                "3_25",
                "3_26",
                "3_27",
                "3_28",
                "3_29",
                "4_1",
                "4_2",
                "4_3",
                "4_4",
                "4_5",
                 ]
    
    for repite in repiteobj:
        try:
            if repite.respuestas:
                lista_dic =[]
                if repite.elegible: 
                    elegible = 'ELEGIBLE'
                else:
                    elegible = "NO ELEGIBLE"
                lista_dic.append({
                                            "id":'PVA',
                                            "pregunta":"ELEGIBLE",
                                            "respuesta":elegible,
                                        })
            for pregunta in preguntas:
                if len(list(e for e in repite.respuestas if e['id']  == pregunta)) != 0:
                    repites =list(e for e in repite.respuestas if e['id']  == pregunta)
        
                    titulo = repites[0]['pregunta']
                    respuesta= repites[0]['respuesta']
            
                    lista_dic.append({
                                        "id":pregunta,
                                        "pregunta":titulo,
                                        "respuesta":respuesta,
                                    })

                else:
                    lista_dic.append({
                                        "id":pregunta,
                                        "pregunta":"",
                                        "respuesta":"",
                                    })
            #for repites in repite.respuestas:
            empresas.append(lista_dic)    
        except Exception as e:
            pass
    context = {
        'inscripciones': repiteobj,
        'respuesta':empresas
    }
 
    return render_template('monitoreo/indicadores_inscritas.html',**context)


@monitoreo.route('/indicadores/inscritas/3',methods = ['GET', 'POST'])
@login_required
def _indicadores_inscritas_3():
    query = Inscripciones.query.filter(Inscripciones.cohorte==5).order_by(Inscripciones.id.desc())[301:450]
    repite = []
    repiteobj =[]
    for obj in query:
        if not obj.dni in repite:
            repite.append(obj.dni)
            repiteobj.append(obj)
    respuesta = []
    empresas = []
    preguntas = [
                "A",    
                "B",
                "C",
                "1_1",
                "1_2",
                "1_3",
                "1_4",
                "1_5",
                "1_6",
                "1_7",
                "1_8",
                "1_9",
                "1_10",
                "1_11",
                "2_1",
                "2_2",
                "2_3",
                "2_4",
                "2_5",
                "2_6",
                "2_7",
                "2_8",
                "3_1",
                "3_2",
                "3_3",
                "3_4",
                "3_5",
                "3_6",
                "3_7",
                "3_8",
                "3_9",
                "3_10",
                "3_11",
                "3_12",
                "3_13",
                "3_14",
                "3_15",
                "3_16",
                "3_17",
                "3_18",
                "3_19",
                "3_20",
                "3_21",
                "3_22",
                "3_23",
                "3_24",
                "3_25",
                "3_26",
                "3_27",
                "3_28",
                "3_29",
                "4_1",
                "4_2",
                "4_3",
                "4_4",
                "4_5",
                 ]
    
    for repite in repiteobj:
        if repite.respuestas:
            lista_dic =[]
            if repite.elegible: 
                elegible = 'ELEGIBLE'
            else:
                elegible = "NO ELEGIBLE"
            lista_dic.append({
                                        "id":'PVA',
                                        "pregunta":"ELEGIBLE",
                                        "respuesta":elegible,
                                    })
            for pregunta in preguntas:
                if len(list(e for e in repite.respuestas if e['id']  == pregunta)) != 0:
                    repites =list(e for e in repite.respuestas if e['id']  == pregunta)
        
                    titulo = repites[0]['pregunta']
                    respuesta= repites[0]['respuesta']
            
                    lista_dic.append({
                                        "id":pregunta,
                                        "pregunta":titulo,
                                        "respuesta":respuesta,
                                    })

                else:
                    lista_dic.append({
                                        "id":pregunta,
                                        "pregunta":"",
                                        "respuesta":"",
                                    })
            #for repites in repite.respuestas:

            empresas.append(lista_dic)    
    context = {
        'inscripciones': repiteobj,
        'respuesta':empresas
    }
 
    return render_template('monitoreo/indicadores_inscritas.html',**context)



@monitoreo.route('/indicadores/inscritas/4',methods = ['GET', 'POST'])
@login_required
def _indicadores_inscritas_4():
    query = Inscripciones.query.filter(Inscripciones.cohorte==5).order_by(Inscripciones.id.desc())[451:600]
    repite = []
    repiteobj =[]
    for obj in query:
        if not obj.dni in repite:
            repite.append(obj.dni)
            repiteobj.append(obj)
    respuesta = []
    empresas = []
    preguntas = [
                "A",    
                "B",
                "C",
                "1_1",
                "1_2",
                "1_3",
                "1_4",
                "1_5",
                "1_6",
                "1_7",
                "1_8",
                "1_9",
                "1_10",
                "1_11",
                "2_1",
                "2_2",
                "2_3",
                "2_4",
                "2_5",
                "2_6",
                "2_7",
                "2_8",
                "3_1",
                "3_2",
                "3_3",
                "3_4",
                "3_5",
                "3_6",
                "3_7",
                "3_8",
                "3_9",
                "3_10",
                "3_11",
                "3_12",
                "3_13",
                "3_14",
                "3_15",
                "3_16",
                "3_17",
                "3_18",
                "3_19",
                "3_20",
                "3_21",
                "3_22",
                "3_23",
                "3_24",
                "3_25",
                "3_26",
                "3_27",
                "3_28",
                "3_29",
                "4_1",
                "4_2",
                "4_3",
                "4_4",
                "4_5",
                 ]
    
    for repite in repiteobj:
        if repite.respuestas:
            lista_dic =[]
            if repite.elegible: 
                elegible = 'ELEGIBLE'
            else:
                elegible = "NO ELEGIBLE"
            lista_dic.append({
                                        "id":'PVA',
                                        "pregunta":"ELEGIBLE",
                                        "respuesta":elegible,
                                    })
            for pregunta in preguntas:
                if len(list(e for e in repite.respuestas if e['id']  == pregunta)) != 0:
                    repites =list(e for e in repite.respuestas if e['id']  == pregunta)
        
                    titulo = repites[0]['pregunta']
                    respuesta= repites[0]['respuesta']
            
                    lista_dic.append({
                                        "id":pregunta,
                                        "pregunta":titulo,
                                        "respuesta":respuesta,
                                    })

                else:
                    lista_dic.append({
                                        "id":pregunta,
                                        "pregunta":"",
                                        "respuesta":"",
                                    })
            #for repites in repite.respuestas:

            empresas.append(lista_dic)    
    context = {
        'inscripciones': repiteobj,
        'respuesta':empresas
    }
 
    return render_template('monitoreo/indicadores_inscritas.html',**context)


from views.digitalcenter import convertir_a_datetime
@monitoreo.route('/indicador/perfil/<int:user_uid>/view',methods=['GET', 'POST'])
@login_required
def _indicadores_perfil_asesor(user_uid):
    if current_user.id in [3,24,25]:
        user = User.query.filter(User.id==user_uid).first()
    else:
        user = User.query.filter(User.id==current_user.id).first()
    url = app.config.get('KOBOTOOLBOX_ALL')
    headers=app.config.get('KOBOTOOLBOX_TOKEN')
    resp = requests.get(url,headers=headers)
    api = json.loads(resp.content)
    datos =  []
    range1 = ""
    range2 = ""
    cod_usuario = user.id
    if request.method == 'POST':
        txt_start_date = request.form.get('txt_start_date') 
        txt_end_date = request.form.get('txt_end_date') 
        clist = ActionPlan.query.filter(ActionPlan.date_created.between('2023-04-01', '2023-05-05')).all()[:100]
        range1 = dt.strptime(txt_start_date, '%Y-%m-%d')
        range2 = dt.strptime(txt_end_date, '%Y-%m-%d')
        #contamos los diagnosticos
        diagnosticos = 0
        diagnosticos_innova = []
        if user.extra_info.kobotoolbox:
            api['results'] = list(e for e in api['results'] if e['_submitted_by']  in user.extra_info.kobotoolbox['kobotoolbox_access'] )
            diagnosticos = list(e for e in api['results'] if e['_submitted_by']  in user.extra_info.kobotoolbox['kobotoolbox_access'] and range1 <= convertir_a_datetime(e['_submission_time']) <= range2  )


        # Filtrar registros en el rango de fechas y con las condiciones de origen, creado por y company_id especificadas
        diagnosticos_innova = DiagnosisCompany.query.filter(
            DiagnosisCompany.date_created.between(range1, range2),
            DiagnosisCompany.origin == 2,
            DiagnosisCompany.created_by == user.id,
        ).distinct(DiagnosisCompany.company_id).all()
        companys = Company.query.join(User, User.id==Company.created_by).join(CompanyStatus, Company.status_id==CompanyStatus.id).filter(Company.date_created.between(txt_start_date, txt_end_date), Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ).all()
        companys1 = Company.query.join(User, User.id == Company.created_by).join(CompanyStatus, Company.status_id == CompanyStatus.id).filter(
            or_(
                Company.date_created.between(txt_start_date, txt_end_date),
                Company.date_action_plan.between(txt_start_date, txt_end_date)
            ),
            Company.enabled == True,
            Company.created_by == user.id,
            CompanyStatus.name_short != 1
        ).all()
        companys_etapa1 = Company.query.join(User, User.id==Company.created_by
                                            ).join(CompanyStatus, Company.status_id==CompanyStatus.id
                                            ).join(CompanyStage, Company.stage_id==CompanyStage.id
                                            ).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ,
                                            CompanyStage.name_short == 'E1',
                                            Company.date_created.between(txt_start_date, txt_end_date)
                                            ).all()
        companys_etapa2 = Company.query.join(User, User.id==Company.created_by
                                            ).join(CompanyStatus, Company.status_id==CompanyStatus.id
                                            ).join(CompanyStage, Company.stage_id==CompanyStage.id
                                            ).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ,
                                            CompanyStage.name_short == 'E2',Company.date_created.between(txt_start_date, txt_end_date)
                                            ).all()
        inactivas = ['4','5']
        companys_etapa1 = Company.query.join(User, User.id==Company.created_by
                                            ).join(CompanyStatus, Company.status_id==CompanyStatus.id
                                            ).join(CompanyStage, Company.stage_id==CompanyStage.id
                                            ).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ,
                                            CompanyStage.name_short == 'E1',Company.date_created.between(txt_start_date, txt_end_date)
                                            ).count()
        companys_etapa1_inactivas = Company.query.join(User, User.id==Company.created_by
                                            ).join(CompanyStatus, Company.status_id==CompanyStatus.id
                                            ).join(CompanyStage, Company.stage_id==CompanyStage.id
                                            ).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ,
                                            CompanyStage.name_short == 'E1',CompanyStatus.name_short.in_(inactivas),
                                            Company.date_created.between(txt_start_date, txt_end_date)
                                            ).count()
        companys_etapa1_activas = companys_etapa1 - companys_etapa1_inactivas
        companys_etapa2 = Company.query.join(User, User.id==Company.created_by
                                            ).join(CompanyStatus, Company.status_id==CompanyStatus.id
                                            ).join(CompanyStage, Company.stage_id==CompanyStage.id
                                            ).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ,
                                            CompanyStage.name_short == 'E2',
                                            Company.date_created.between(txt_start_date, txt_end_date)
                                            ).count()
        companys_etapa2_inactivas = Company.query.join(User, User.id==Company.created_by
                                            ).join(CompanyStatus, Company.status_id==CompanyStatus.id
                                            ).join(CompanyStage, Company.stage_id==CompanyStage.id
                                            ).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ,
                                            CompanyStage.name_short == 'E1',CompanyStatus.name_short.in_(inactivas),
                                            Company.date_created.between(txt_start_date, txt_end_date)
                                            ).count()   
        companys_etapa2_activas = companys_etapa2 - companys_etapa2_inactivas   
        planes = 0
        lista = []
        for company in companys1:
            #plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.created_by == user.id,ActionPlan.company_id==company.id,ActionPlan.fase!=0).first()
            plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0).first()
            if plan:
                lista.append(company.id)
                planes = planes + 1
        planes = Company.query.filter(Company.id.in_(lista)).all()
        plan_services_total = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id,).filter(ActionPlan.cancelled == False,ActionPlan.company_id.in_(lista),ActionPlan.fase!=0).all()
        referidos_servicios =   []
        referidos_serviciosfin =  []
        for bitacora in plan_services_total:
            if bitacora.id not in referidos_servicios:
                if bitacora.progress == 100:
                    referidos_serviciosfin.append(bitacora.id)
                referidos_servicios.append(bitacora.id)        
        references = ActionPlanReferences.query.filter(ActionPlanReferences.date_created.between(txt_start_date, txt_end_date),ActionPlanReferences.employe_assigned==user.id).order_by(desc(ActionPlanReferences.id)).all()
        lista = []
        for reference in references:
            lista.append(reference.action_plan.company.id)
        company_references = Company.query.filter(Company.id.in_(lista)).all()
        
        references_accepted = ActionPlanReferences.query.filter(ActionPlanReferences.date_created.between(txt_start_date, txt_end_date),ActionPlanReferences.employe_assigned==user.id,ActionPlanReferences.employe_accepted==True).order_by(desc(ActionPlanReferences.id)).all()
        lista = []
        for reference in references_accepted:
            lista.append(reference.action_plan.company.id)
        company_references_accepted = Company.query.filter(Company.id.in_(lista)).all()
        
        bitacoras = ActionPlanHistory.query.distinct(ActionPlanHistory.action_plan_id).filter(ActionPlanHistory.date_created.between(txt_start_date, txt_end_date),ActionPlanHistory.created_by==user.id,ActionPlanHistory.cancelled==False)
        servicios =   []
        serviciosfin =  []
        for bitacora in bitacoras:
            if bitacora.action_plan_id not in servicios:
                if bitacora.action_plan.progress == 100:
                    serviciosfin.append(bitacora.action_plan_id)
                servicios.append(bitacora.action_plan_id)
        asesorias = ActionPlanHistory.query.filter(ActionPlanHistory.date_created.between(txt_start_date, txt_end_date), ActionPlanHistory.created_by==user.id,ActionPlanHistory.cancelled==False).all()
        asesorias_virtual = ActionPlanHistory.query.join(ModalityType, ModalityType.id==ActionPlanHistory.id_modality_type).filter(ActionPlanHistory.date_created.between(txt_start_date, txt_end_date),ModalityType.name_short == 'MT2', ActionPlanHistory.created_by==user.id,ActionPlanHistory.cancelled==False).count()
        asesorias_presencial = len(asesorias) - asesorias_virtual

    else:

        #contamos los diagnosticos
        diagnosticos = 0
        diagnosticos_innova = []
        if user.extra_info.kobotoolbox:
            api['results'] = list(e for e in api['results'] if e['_submitted_by']  in user.extra_info.kobotoolbox['kobotoolbox_access'] )
            diagnosticos = list(e for e in api['results'] if e['_submitted_by']  in user.extra_info.kobotoolbox['kobotoolbox_access']  )

        # Filtrar registros en el rango de fechas y con las condiciones de origen, creado por y company_id especificadas
        diagnosticos_innova = DiagnosisCompany.query.filter(
            DiagnosisCompany.origin == 2,
            DiagnosisCompany.created_by == user.id,
            DiagnosisCompany.status == True
        ).distinct(DiagnosisCompany.company_id).all()
        #companys = Company.query.join(User, User.id==Company.created_by).filter(Company.enabled==True, Company.created_by == user.id).all()
        companys = Company.query.join(User, User.id==Company.created_by).join(CompanyStatus, Company.status_id==CompanyStatus.id).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ).all()
        inactivas = ['4','5']
        companys_etapa1 = Company.query.join(User, User.id==Company.created_by
                                            ).join(CompanyStatus, Company.status_id==CompanyStatus.id
                                            ).join(CompanyStage, Company.stage_id==CompanyStage.id
                                            ).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ,
                                            CompanyStage.name_short == 'E1'
                                            ).count()
        companys_etapa1_inactivas = Company.query.join(User, User.id==Company.created_by
                                            ).join(CompanyStatus, Company.status_id==CompanyStatus.id
                                            ).join(CompanyStage, Company.stage_id==CompanyStage.id
                                            ).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ,
                                            CompanyStage.name_short == 'E1',CompanyStatus.name_short.in_(inactivas)
                                            ).count()
        companys_etapa1_activas = companys_etapa1 - companys_etapa1_inactivas
        companys_etapa2 = Company.query.join(User, User.id==Company.created_by
                                            ).join(CompanyStatus, Company.status_id==CompanyStatus.id
                                            ).join(CompanyStage, Company.stage_id==CompanyStage.id
                                            ).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ,
                                            CompanyStage.name_short == 'E2'
                                            ).count()
        companys_etapa2_inactivas = Company.query.join(User, User.id==Company.created_by
                                            ).join(CompanyStatus, Company.status_id==CompanyStatus.id
                                            ).join(CompanyStage, Company.stage_id==CompanyStage.id
                                            ).filter(Company.enabled==True, Company.created_by == user.id,CompanyStatus.name_short !=1 ,
                                            CompanyStage.name_short == 'E1',CompanyStatus.name_short.in_(inactivas)
                                            ).count()   
        companys_etapa2_activas = companys_etapa2 - companys_etapa2_inactivas     

        planes = 0
        lista = []

        for company in companys:
            category = "No tiene plan de acción"
            if company.action_plan_progress is not None:
            # Calcula la categoría según el valor de action_plan_progress
            
                if company.action_plan_progress:
                    category_start = int(company.action_plan_progress // 20) * 20
                    category = f"{category_start} de {category_start + 20}" if category_start < 100 else "80 de 100"
                else:
                    category = "0 de 20"
            company.avancepa = category
                

            #plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id,).filter(ActionPlan.company_id==company.id,ActionPlan.created_by == user.id,ActionPlan.fase!=0).first()
            plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id,).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0).first()
            if plan:
                lista.append(company.id)
                planes = planes + 1
            
        plan_services_total = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id,).filter(ActionPlan.cancelled == False,ActionPlan.company_id.in_(lista),ActionPlan.fase!=0).all()
        referidos_servicios =   []
        referidos_serviciosfin =  []
        for bitacora in plan_services_total:
            if bitacora.id not in referidos_servicios:
                if bitacora.progress == 100:
                    referidos_serviciosfin.append(bitacora.id)
                referidos_servicios.append(bitacora.id)

        planes = Company.query.filter(Company.id.in_(lista)).all()
        #planes = Company.query.filter(Company.id.in_(planes)).all()
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
        asesorias = ActionPlanHistory.query.filter(ActionPlanHistory.created_by==user.id,ActionPlanHistory.cancelled==False).all()
        asesorias_virtual = ActionPlanHistory.query.join(ModalityType, ModalityType.id==ActionPlanHistory.id_modality_type).filter(ModalityType.name_short == 'MT2', ActionPlanHistory.created_by==user.id,ActionPlanHistory.cancelled==False).count()
        asesorias_presencial = len(asesorias) - asesorias_virtual
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
        'diagnosticos_innova':diagnosticos_innova,
        'company':companys,
        'company_references':company_references,
        'company_references_accepted':len(company_references_accepted),
        'planes':planes,
        'servicios':len(servicios),
        'serviciosproceso':len(servicios) -len(serviciosfin),
        'serviciosfin':len(serviciosfin),
        'users': user,
        'bitacoras':bitacoras,
        'asesorias':asesorias,
        'companys_etapa1':companys_etapa1,
        'companys_etapa2':companys_etapa2,
        "companys_etapa1_inactivas":companys_etapa1_inactivas,
        "companys_etapa1_activas":companys_etapa1_activas,
        "companys_etapa2_inactivas":companys_etapa2_inactivas,
        "companys_etapa2_activas":companys_etapa2_activas,
        "asesorias_presencial":asesorias_presencial,
        "asesorias_virtual":asesorias_virtual,
        "plan_services_total":plan_services_total,
        'referidos_servicios':len(referidos_servicios),
        'referidos_serviciosproceso':len(referidos_servicios) -len(referidos_serviciosfin),
        'referidos_serviciosfin':len(referidos_serviciosfin),
        'txt_start_date':range1,
        'txt_end_date':range2
        }
    return render_template('monitoreo/indicadores_perfil_asesor.html',**context)


from sqlalchemy import desc,asc,func
@monitoreo.route('/diagnostico/publico/<int:user_uid>/',methods=['GET', 'POST'])
@login_required
def _diagnosis_dashboard(user_uid):
    app.logger.debug('** SWING_CMSx ** - ------------------')
    company =  Company.query.filter(Company.id == user_uid).first()
    diagnos = DiagnosisCompany.query.filter_by(company_id=company.id,status=True).order_by(asc(DiagnosisCompany.date_created)).first()
    #actions = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).order_by(asc(ActionPlan.date_scheduled_start)).all()
    actions = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.company_id==company.id,ActionPlan.fase!=0,ActionPlan.cancelled ==False).order_by(asc(ActionPlan.date_scheduled_start)).all()
    catalog = catalogCategory.query.all()
    deposits_total =WalletTransaction.query.with_entities(func.sum(WalletTransaction.amount).label('total')).filter(WalletTransaction.company_id == company.id, WalletTransaction.type ==0,WalletTransaction.status!=0).first()
    deposits = WalletTransaction.query.filter(WalletTransaction.company_id == company.id, WalletTransaction.type ==0,WalletTransaction.status!=0).all()

    plan_action = []
    for catalog in catalog:
        plan = ActionPlan.query.join(CatalogServices, ActionPlan.services_id==CatalogServices.id).filter(ActionPlan.cancelled ==False,CatalogServices.catalog_category == catalog.id,ActionPlan.company_id==company.id,ActionPlan.fase!=0).all()
        if plan:
            miplan = {'catalog_id':catalog.id,'catalog_name':catalog.name,'plan_action':plan}
            plan_action.append(miplan)
    if diagnos:
        diagnostico = diagnos.resultados
    else:
        diagnostico = False
    #buscamos la carta de compromiso DOC2
    carta = CatalogIDDocumentTypes.query.filter_by(name_short='DOC2').first()
    carta = DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=carta.id,enabled=True).order_by(desc(DocumentCompany.date_created)).first()
    #buscamos la ficha de inscripcion DOC1
    ficha = CatalogIDDocumentTypes.query.filter_by(name_short='DOC1').first()
    ficha =  DocumentCompany.query.filter_by(company_id=company.id,documente_type_id=ficha.id,enabled=True).order_by(desc(DocumentCompany.date_created)).first()
    context = {
        
        "deposits":deposits,
        "deposits_total":deposits_total,

        "carta":carta,
        "ficha":ficha,
        "company":company,
        "diagnostico":diagnostico,
        "actions":actions,
        "diagnosis":diagnos,
        "plan_action":plan_action
    }
    return render_template('monitoreo/indicadores_diagnostivo.html',**context)




@monitoreo.route('/doc/',methods=['GET', 'POST'])
@login_required
def _doc_dashboard():
    return render_template('doc.html')


@monitoreo.route('/guia/',methods=['GET', 'POST'])
@login_required
def _guia_dashboard():
    return render_template('guia.html')


@monitoreo.route('/monitoring/dashboard',methods=['GET', 'POST'])
@login_required
def _monitoring_dashboard():
    departamentos_honduras = [
        {"titulo": "Atlántida", "codigo": "01"},
        {"titulo": "Choluteca", "codigo": "02"},
        {"titulo": "Colón", "codigo": "03"},
        {"titulo": "Comayagua", "codigo": "04"},
        {"titulo": "Copán", "codigo": "05"},
        {"titulo": "Cortés", "codigo": "06"},
        {"titulo": "El Paraíso", "codigo": "07"},
        {"titulo": "Francisco Morazán", "codigo": "08"},
        {"titulo": "Gracias a Dios", "codigo": "09"},
        {"titulo": "Intibucá", "codigo": "10"},
        {"titulo": "Islas de la Bahía", "codigo": "11"},
        {"titulo": "La Paz", "codigo": "12"},
        {"titulo": "Lempira", "codigo": "13"},
        {"titulo": "Ocotepeque", "codigo": "14"},
        {"titulo": "Olancho", "codigo": "15"},
        {"titulo": "Santa Bárbara", "codigo": "16"},
        {"titulo": "Valle", "codigo": "17"},
        {"titulo": "Yoro", "codigo": "18"}
    ]
    services = CatalogServices.query.filter_by().all()
    categorys = catalogCategory.query.filter_by().all()
    status = CompanyStatus.query.filter(~CompanyStatus.name_short.in_(['1', ])).all()

    
    context = {"departamentos_honduras":departamentos_honduras,'services':services,'categorys':categorys,'status':status}
    return render_template('monitoreo/monitoring_dashboard.html',**context)



@monitoreo.route('/monitoreo/empresas/',methods=['GET', 'POST'])
@login_required
def _admin_company_monitoring_list():
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
    list_user = [3,5,6,15,16,17,18,20,21,25,24,30,66,173,176,215,216,217]
    users = User.query.filter(User.id.in_(list_user)).order_by(User.name.asc()).all()
    context = {
        'users':users,
        'diagnosticos':len(diagnosticos),
        'planes':planes,
        'serviciosTotal':serviciosTotal,
        'serviciosNoinciados':serviciosNoinciados,
        'serviciosEnProceso':serviciosEnProceso,
        'serviciosFinalizados':serviciosFinalizados,
    }

    return render_template('monitoreo/company_monitoring_list.html',**context)

@monitoreo.route('/monitoreo/empresas/gee',methods=['GET', 'POST'])
@login_required
def _admin_company_monitoring_gee_list():

    list_user = [3,5,6,15,16,17,18,20,21,25,24,30,66,173,176]
    users = User.query.filter(User.id.in_(list_user)).order_by(User.name.asc()).all()
    context = {
        'users':users,

  
    }

    return render_template('monitoreo/company_monitoring_gee_list.html',**context)



@monitoreo.route('/directorio/empresas/',methods=['GET', 'POST'])
def _directorio_company():
    return render_template('monitoreo/directorio_company.html')

