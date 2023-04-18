from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response,send_from_directory
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import catalogCategory,Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import Company,CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from werkzeug.utils import secure_filename
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
        
    return render_template('/admindash/listuser.html',**cxt)

@admindash.route('/admin/list/user/<int:user_id>/custom', methods = ['GET'])
@login_required
def _admin_form_user(user_id):
    app.logger.debug('** SWING_CMS ** - listuser')
    user = User.query.filter_by(id = user_id).first()
    roles = CatalogUserRoles.query.all()
    cxt = {'user':user,'roles':roles}
    return render_template('/admindash/formuser.html',**cxt)

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
    return render_template('/admindash/formuser_company.html',**cxt)


from sqlalchemy import desc
@admindash.route('/servi/',methods=['GET', 'POST'])
def _servi():
    services = CatalogServices.query.filter_by(enabled = 1).order_by(desc(CatalogServices.name_short)).all()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    context = {'services':services}  
    return render_template('admindash/servi.html',**context)

@admindash.route('/servi/<int:user_uid>',methods=['GET', 'POST'])
def _servi_detalle(user_uid):
    services = catalogCategory.query.all()
    service = CatalogServices.query.filter_by(id = user_uid).first()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    context = {'services':services,'service':service}  
    return render_template('admindash/formservicios.html',**context)

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
    return render_template('/admindash/admin_list_company.html',**cxt)

@admindash.route('/admin/company/<int:company_id>/edit',methods=['GET', 'POST'])
@login_required
def _admin_list_company_edit(company_id):
    company = Company.query.filter_by(id = company_id).first()
    if request.method == 'POST':
        txt_name = request.form.get('txt_name') 
        txt_identidad= request.form.get('txt_identidad')
        cxb_status = False
        if 'cxb_status' in request.form: 
            cxb_status = True
        company.name = txt_name
        company.dni = txt_identidad
        company.enabled =  cxb_status
        db.session.add(company)
        db.session.commit()
    app.logger.debug('** SWING_CMS ** - Home Dashboard')
    cxt = {'company':company}
    return render_template('/admindash/form_company.html',**cxt)
    return redirect(url_for('admindash._servi'))