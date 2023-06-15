
from . import auth, createCookieSession, createLoginSession, createJsonResponse, db, getUserRedirectURL, isUserLoggedInRedirect,isUserLoggedInRedirectDC

from babel.dates import format_date, format_datetime, format_time
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response,send_from_directory
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import WalletTransaction,ActionPlanReferences,DocumentCompany,ActionPlanHistory,DiagnosisCompany,Inscripciones,ActionPlan,Company,Professions,Appointments, CatalogIDDocumentTypes, CatalogServices, CatalogUserRoles, User, UserXRole, UserXEmployeeAssigned
from models.models import catalogCategory,CatalogOperations, CatalogUserRoles, LogUserConnections, RTCOnlineUsers, User,UserExtraInfo
from models.diagnostico import Diagnosticos
from werkzeug.utils import secure_filename
from sqlalchemy import or_
import pytz


def _update_wallet(company_id):
    company = Company.query.filter_by(id=company_id).first()

    #type – (0) deposit
    deposits = WalletTransaction.query.filter(WalletTransaction.company_id == company.id, WalletTransaction.type ==0,WalletTransaction.status!=0).all()
    inputs = 0
    for deposit in deposits:
        inputs = inputs + deposit.amount

    #type – (1) withdrawal
    withdrawals = WalletTransaction.query.filter(WalletTransaction.company_id == company.id, WalletTransaction.type ==1,WalletTransaction.status!=0).all()
    outputs = 0
    for withdrawal in withdrawals:
        outputs = outputs + withdrawal.amount
    company.available_credit = inputs - outputs
    db.session.add(company)
    db.session.commit() 
    return True