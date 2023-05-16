from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response,send_from_directory
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import Inscripciones,catalogCategory,Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import DocumentCompany,ActionPlan,DiagnosisCompany,Company,CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from werkzeug.utils import secure_filename
from models.formatjson import JsonPhone, JsonSocial,JsonConfigProfile
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
import os

admindash = Blueprint('admindash', __name__, template_folder='templates', static_folder='static')


@admindash.route('/admin/list/user/', methods = ['GET'])
@login_required
def _admin_list_user():

    app.logger.debug('** SWING_CMS ** - listuser')
    users = User.query.all()
    #users = User.query.join(UserXRole, User.id==UserXRole.user_id).filter(UserXRole.user_role_id == 3).all()
    app.logger.debug(users)
    cxt = {'users':users}
        
    return render_template('/admindash/user_list.html',**cxt)

@admindash.route('/admin/list/user/<int:user_id>/custom', methods = ['GET'])
@login_required
def _admin_form_user(user_id):
    app.logger.debug('** SWING_CMS ** - listuser')
    user = User.query.filter_by(id = user_id).first()
    roles = CatalogUserRoles.query.all()
    cxt = {'user':user,'roles':roles}
    return render_template('/admindash/user_form.html',**cxt)

@admindash.route('/super/innova', methods = ['GET'])
@login_required
def _home_admin():
    app.logger.debug('** SWING_CMS ** - listuser')
    return render_template('/admindash/home.html')

@admindash.route('/admin/list/user/company/<int:user_id>/custom', methods = ['GET'])
@login_required
def _admin_form_company(user_id):
    app.logger.debug('** SWING_CMS ** - listuser')
    user = User.query.filter_by(id = user_id).first()
    company = Company.query.all()
    cxt = {'user':user,'company':company}
    return render_template('/admindash/user_company_form.html',**cxt)


from sqlalchemy import desc
@admindash.route('/servi/',methods=['GET', 'POST'])
def _servi():
    services = CatalogServices.query.filter_by(enabled = 1).order_by(desc(CatalogServices.name_short)).all()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    context = {'services':services}  
    return render_template('admindash/service_list.html',**context)

@admindash.route('/servi/<int:user_uid>',methods=['GET', 'POST'])
def _servi_detalle(user_uid):
    services = catalogCategory.query.all()
    service = CatalogServices.query.filter_by(id = user_uid).first()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    context = {'services':services,'service':service}  
    return render_template('admindash/service_form.html',**context)

@admindash.route('/servi/delete/<int:service_id>',methods=['GET', 'POST'])
def _servi_detalle_delete(service_id):
    service = CatalogServices.query.filter_by(id = service_id).delete()
    db.session.commit()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    return redirect(url_for('admindash._servi'))

@admindash.route('/admin/list/company', methods = ['GET'])
@login_required
def _admin_list_company():
    companys = Company.query.all()
    cxt = {'companys':companys}
    return render_template('/admindash/company_list.html',**cxt)

@admindash.route('/admin/company/<int:company_id>/view/all', methods = ['GET'])
@login_required
def _admin_company_view(company_id):
    company = Company.query.filter_by(id = company_id).first()
    diagnosis=  DiagnosisCompany.query.filter_by(company_id=company.id).all()
    actionplan = ActionPlan.query.filter_by(company_id=company.id).all()
    documents = DocumentCompany.query.filter_by(company_id=company.id).all()
    cxt = {'company':company,'documents':documents,'diagnosis':diagnosis,'actionplan':actionplan}
    return render_template('/admindash/company_view.html',**cxt)

@admindash.route('/admin/company/<int:company_id>/edit',methods=['GET', 'POST'])
@login_required
def _admin_list_company_edit(company_id):
    company = Company.query.filter_by(id = company_id).first()
    if request.method == 'POST':
        txt_name = request.form.get('txt_name') 
        txt_identidad= request.form.get('txt_identidad')
        txt_rtn= request.form.get('txt_rtn')
        txt_email= request.form.get('txt_email')
        txt_facebook= request.form.get('txt_facebook')
        txt_instagram= request.form.get('txt_instagram')
        txt_description= request.form.get('txt_description')
        txt_created_by= request.form.get('txt_created_by')
        company.description = txt_description
        jsonSocial= JsonSocial()
        jsonSocial.email = txt_email
        jsonSocial.facebook = txt_facebook
        jsonSocial.instagram =txt_instagram
        company.social_networks = jsonSocial.jsonFormat()
        cxb_status = False
        if 'cxb_status' in request.form: 
            cxb_status = True
        company.name = txt_name
        company.dni = txt_identidad
        company.enabled =  cxb_status
        company.rtn = txt_rtn
        company.created_by = txt_created_by
        db.session.add(company)
        db.session.commit()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    cxt = {'company':company}
    return render_template('/admindash/company_form.html',**cxt)

@admindash.route('/admin/company/inscripcion/<int:company_id>/edit',methods=['GET', 'POST'])
@login_required
def _admin_company_inscription_edit(company_id):
    company = Company.query.filter_by(id = company_id).first()
    inscripciones = Inscripciones.query.filter_by(elegible=True).all()
    if request.method == 'POST':
        txt_inscripcion = request.form.get('txt_inscripcion') 
        inscripcion = Inscripciones.query.filter_by(id = txt_inscripcion).first()
        company.inscripcion_id = inscripcion.id
        db.session.add(company)
        db.session.commit()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    cxt = {'company':company,'inscripciones':inscripciones}
    return render_template('/admindash/company_inscription.html',**cxt)

@admindash.route('/admin/list/inscripciones', methods = ['GET'])
@login_required
def _admin_list_inscription():
    inscripciones = Inscripciones.query.all()
    cxt = {'inscripciones':inscripciones}
    return render_template('/admindash/incripcione_list.html',**cxt)
import json
@admindash.route('/admin/inscripcion/<int:inscription_id>/edit',methods=['GET', 'POST'])
@login_required
def _admin_inscription_edit(inscription_id):
    inscripcion = Inscripciones.query.filter_by(id = inscription_id).first()
    inscripciones = Inscripciones.query.filter_by(elegible=True).all()
    if request.method == 'POST':
        txt_respuestas = request.form.get('txt_respuestas') 
        txt_name = request.form.get('txt_name') 
        txt_company_name = request.form.get('txt_company_name') 
        txt_correo = request.form.get('txt_correo') 
        txt_dni = request.form.get('txt_dni')
        
        cxb_status = False
        if 'cxb_status' in request.form: 
            cxb_status = True
        inscripcion.elegible = cxb_status
        inscripcion.respuestas = json.loads( txt_respuestas.replace("\'", "\""))
        inscripcion.dni = txt_dni
        inscripcion.name = txt_name
        inscripcion.company_name = txt_company_name
        inscripcion.correo = txt_correo
        db.session.add(inscripcion)
        db.session.commit()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    cxt = {'inscripcion':inscripcion}
    return render_template('/admindash/incripcione_edit.html',**cxt)

    diagnosis=  DiagnosisCompany.query.filter_by(company_id=company.id).all()
    actionplan = ActionPlan.query.filter_by(company_id=company.id).all()
    documents = DocumentCompany.query.filter_by(company_id=company.id).all()

@admindash.route('/document/delete/<int:document_id>/<int:company_id>',methods=['GET', 'POST'])
def _document_delete(document_id,company_id):
    document = DocumentCompany.query.filter_by(id = document_id).delete()
    db.session.commit()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    return redirect(url_for('admindash._admin_company_view',company_id=company_id))

@admindash.route('/plan/delete/<int:actionplan_id>/<int:company_id>',methods=['GET', 'POST'])
def _actionplan_delete(actionplan_id,company_id):
    actionplan = ActionPlan.query.filter_by(id = actionplan_id).delete()
    db.session.commit()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    return redirect(url_for('admindash._admin_company_view',company_id=company_id))

@admindash.route('/diagnosis/delete/<int:diagnosis_id>/<int:company_id>',methods=['GET', 'POST'])
def _diagnosis_delete(diagnosis_id,company_id):
    diagnosis = DiagnosisCompany.query.filter_by(id = diagnosis_id).delete()
    db.session.commit()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    return redirect(url_for('admindash._admin_company_view',company_id=company_id))