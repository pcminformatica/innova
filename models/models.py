from datetime import datetime as dt
from datetime import timezone as tz
from elasticsearch import Elasticsearch
from flask import jsonify
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy, orm
from operator import attrgetter
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types import JSONType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
import pytz
default_timezone=pytz.timezone('America/Tegucigalpa')

# **************************************************************************
# SQLAlchemy Utilities
# **************************************************************************

class AESCryptoKey():
    def __init__(self):
        self._crypKey = None
    
    @property
    def key(self):
        return self._crypKey

    @key.setter
    def key(self, val):
        self._crypKey = val

def get_crypto_key():
    return crypto_key.key


# **************************************************************************
# SQLAlchemy init instances
# **************************************************************************

db = SQLAlchemy()
crypto_key = AESCryptoKey()


# **************************************************************************
# ElasticSearch Utilities
# **************************************************************************

class ElasticSearchInit():
    def __init__(self):
        self._es = None
        self._esOn = False
    
    def init_app(self, app):
        # Validate that Elastic Search URL Exists
        if 'ELASTICSEARCH_URL' in app.config:
            self._es = Elasticsearch(app.config['ELASTICSEARCH_URL'])
        
    @property
    def instance(self):
        return self._es

    @instance.setter
    def instance(self, val):
        self._es = val
    
    @property
    def instanceOn(self):
        try:
            self._esOn = self._es.ping()
        except Exception as e:
            pass
        return self._esOn
    
    @instanceOn.setter
    def instanceOn(self, val):
        self._esOn = val


# **************************************************************************
# ElasticSearch init instances
# **************************************************************************

es = ElasticSearchInit()


# **************************************************************************
# ElasticSearch/SQLAlchemy implementation
# **************************************************************************

def es_refactor_index(index):
    # This is an acronym for the app, making an index app exclusive
    # Must be lowercase 
    app_acr = 'inno-'
    ref_index = app_acr + str(index)
    return ref_index

def add_to_index(index, model):
    if not es.instanceOn:
        return
    index = es_refactor_index(index)
    if not es.instance.indices.exists(index=index):
        settings = {
            "mappings": {
                "dynamic_templates": [{
                    "case_accent_insensitive": {
                        "match_mapping_type": "string",
                        "mapping": {
                            "analyzer": "asciif_ngram_lowcase",
                            "search_analyzer": "asciif_lowcase"
                        }
                    }
                }]
            },
            "settings": {
                "analysis": {
                    "analyzer": {
                        "asciif_lowcase": {
                            "tokenizer": "standard",
                            "filter": [
                                "asciifolding",
                                "lowercase"
                            ]
                        },
                        "asciif_ngram_lowcase": {
                            "tokenizer": "standard",
                            "filter": [
                                "asciifolding",
                                "ngram_filter",
                                "lowercase"
                            ]
                        }
                    },
                    "filter": {
                        "ngram_filter": {
                            "type": "ngram",
                            "max_gram": 10,
                            "min_gram": 2
                        }
                    }
                },
                "index.max_ngram_diff" : 10
            }
        }
        es.instance.indices.create(index=index, body=settings)
    indexData = {}
    for field in model.__searchable__:
        ag = attrgetter(field)
        try:
            indexData[field] = ag(model)
        except Exception as e:
            pass
    es.instance.index(index=index, id=model.id, body=indexData)

def query_index(index, query, page, per_page):
    if not es.instanceOn:
        return [], 0
    index = es_refactor_index(index)
    search = es.instance.search(
        index = index,
        body = {
            "from": (page - 1) * per_page,
            "query": {
                "multi_match": {
                    "fields": ["*"],
                    "query": query
                }
            },
            "size": per_page
        }
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']

def remove_from_index(index, model = None):
    if not es.instanceOn:
        return
    index = es_refactor_index(index)
    if not model:
        es.instance.indices.delete(index=index, ignore=[404])
    else:
        es.instance.delete(index=index, id=model.id)

class ElasticMixin(object):
    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, ElasticMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, ElasticMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, ElasticMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }
    
    @classmethod
    def delete_index(cls):
        remove_from_index(cls.__tablename__)

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)
    
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total

db.event.listen(db.session, 'after_commit', ElasticMixin.after_commit)
db.event.listen(db.session, 'before_commit', ElasticMixin.before_commit)


# **************************************************************************
# Database Models
# **************************************************************************

# Appointments Class
class Appointments(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.now(default_timezone))
    date_scheduled = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_for = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('catalog_services.id'), nullable=True)
    service_supp_id = db.Column(db.Integer, db.ForeignKey('services_supplement.id'), nullable=True)
    emp_assigned = db.Column(db.Integer, db.ForeignKey('user_x_employees_assigned.id'), nullable=False)
    emp_accepted = db.Column(db.Boolean, nullable=True, default=False)
    conversation_id = db.Column(db.JSON, nullable=True)
    usr_attendance = db.Column(db.DateTime, nullable=True)
    emp_attendance = db.Column(db.DateTime, nullable=True)
    ended_with_survey = db.Column(db.DateTime, nullable=True)
    cancelled = db.Column(db.Boolean, nullable=True, default=False)
    cancelled_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    cancelled_reason = db.Column(EncryptedType(db.Text, get_crypto_key, AesEngine, 'pkcs5'), nullable=True)
    created_by_user = db.relationship("User", foreign_keys=[created_by])
    created_for_user = db.relationship("User", foreign_keys=[created_for])
    cancelled_by_cancelled_by = db.relationship("User", foreign_keys=[cancelled_by])
    def __repr__(self):
        return jsonify(
            id = self.id,
            service_id = self.service_id,
            created_for = self.created_for,
            emp_assigned = self.emp_assigned,
            date_scheduled = self.date_scheduled
        )

class DocumentCompany(db.Model):
    _tablename__ = 'documentcompany'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_local = db.Column(db.String(250), unique=False, nullable=True)
    document_external = db.Column(db.String(250), unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    complete = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    signed = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    signed_innova = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    documente_type_id = db.Column(db.Integer, db.ForeignKey("catalog_id_document_types.id"),nullable=True)
    documente_type = db.relationship("CatalogIDDocumentTypes")
    date_created = db.Column(db.DateTime, nullable=True, default=dt.now(default_timezone))
    def __repr__(self):
        return jsonify(
            id = self.id,
            company_id = self.company_id,
            description = self.description,
            documente_type_id = self.documente_type_id
        )

# Catalog - ID Document Type Class
class CatalogIDDocumentTypes(db.Model):
    __tablename__ = 'catalog_id_document_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    name_short = db.Column(db.String(6), unique=True, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    length = db.Column(db.Integer, unique=False, nullable=True)
    date_created = db.Column(db.DateTime, nullable=True, default=dt.now(default_timezone))
    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
            name_short = self.name_short,
            length = self.length
        )


# Catalog - Operations Class
class CatalogOperations(db.Model):
    __tablename__ = 'catalog_operations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    name_short = db.Column(db.String(6), unique=True, nullable=True)

    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
            name_short = self.name_short
        )

class catalogCategory(db.Model):
    __tablename__ = 'catalog_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
        )


# Catalog - Services Class
class CatalogServices(db.Model):
    __tablename__ = 'catalog_services'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(350), unique=True, nullable=False)
    name_short = db.Column(db.String(6), unique=True, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    execution_time = db.Column(db.Integer, unique=False, nullable=True, default=0)
    advisory_time = db.Column(db.Integer, unique=False, nullable=True, default=0)
    cost  = db.Column(db.FLOAT, unique=False, nullable=True, default=0.00)
    cost_innova  = db.Column(db.FLOAT, unique=False, nullable=True, default=0.00)
    service_user_role = db.Column(db.Integer, db.ForeignKey('catalog_user_roles.id'), nullable=True)
    sessions_schedule = db.Column(db.JSON, nullable=True)
    diagnostic_questions = db.Column(db.JSON, nullable=True)
    fase = db.Column(db.Integer, unique=False, nullable=True, default=0)
    catalog_category = db.Column(db.Integer, db.ForeignKey('catalog_category.id'), nullable=True)
    catalog_catego = db.relationship("catalogCategory")
    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
            name_short = self.name_short,
            break_minutes = self.break_minutes,
            duration_minutes = self.duration_minutes
        )


# Catalog - Survey Answers Types Class
class CatalogSurveysAnswerTypes(db.Model):
    __tablename__ = 'catalog_surveys_answer_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(35), unique=True, nullable=False)
    name_short = db.Column(db.String(6), unique=True, nullable=True)

    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
            name_short = self.name_short
        )


# Catalog - User Roles Class
class CatalogUserRoles(db.Model):
    __tablename__ = 'catalog_user_roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    name_short = db.Column(db.String(6), unique=True, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    users = db.relationship('UserXRole', lazy='subquery', back_populates='user_role')

    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
            name_short = self.name_short,
            enabled = self.enabled,
            users = self.users
        )


# Chat Conversation Class
class Chat():
    date = db.Column(db.DateTime, primary_key=True, default=dt.now(default_timezone))
    users = db.Column(EncryptedType(JSONType, get_crypto_key, AesEngine, 'pkcs5'), nullable=False)
    messages = db.Column(EncryptedType(JSONType, get_crypto_key, AesEngine, 'pkcs5'), nullable=False)
    # date_usr_msg = db.Column(db.DateTime, nullable=False)
    # date_emp_msg = db.Column(db.DateTime, nullable=False)
    # date_usr_reply = db.Column(db.DateTime, nullable=False)
    # date_emp_reply = db.Column(db.DateTime, nullable=False)
    # json = {
    #   usr_con: date,
    #   emp_con: date, 
    #   usr_1st_msg: date,
    #   emp_1st_msg: date,
    #   usr_1st_reply: date,
    #   emp_1st_reply: date
    # }

    def __init__(self):
        self.users = []
        self.messages = []


# Chat Conversations Class - Anonymous
class ChatsAnonymous(Chat, db.Model):
    __tablename__ = 'chats_anonymous'
    sid = db.Column(db.String(35), primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False)
    transferred = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    ended_with_survey = db.Column(db.DateTime, unique=False, nullable=True)

    def __repr__(self):
        return jsonify(
            date = self.date,
            users = self.users,
            messages = self.messages,
            ip_address = self.ip_address
        )


# Chat Conversations Class - Chatbot
class ChatsChatbot(Chat, db.Model):
    __tablename__ = 'chats_chatbot'
    sid = db.Column(db.String(35), primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return jsonify(
            date = self.date,
            users = self.users,
            messages = self.messages,
            ip_address = self.ip_address
        )


# Chat Conversations Class - Employees
class ChatsEmployees(Chat, db.Model):
    __tablename__ = 'chats_employees'
    user_id_01 = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user_id_02 = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return jsonify(
            date = self.date,
            users = self.users,
            messages = self.messages,
            user01 = self.user_id_01,
            user02 = self.user_id_02
        )


# Chat Conversations Class - Registered
class ChatsRegistered(Chat, db.Model):
    __tablename__ = 'chats_registered'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    sid = db.Column(db.String(35), nullable=True)
    ip_address = db.Column(db.String(15), nullable=False)
    transferred = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    ended_with_survey = db.Column(db.DateTime, unique=False, nullable=True)

    def __repr__(self):
        return jsonify(
            date = self.date,
            users = self.users,
            messages = self.messages,
            user_id = self.user_id
        )


# Log User Connections Class
class LogUserConnections(db.Model):
    __tablename__ = 'log_user_connections'
    id = db.Column(db.DateTime, primary_key=True, default=dt.now(default_timezone))
    sid = db.Column(db.String(35), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    operation_id = db.Column(db.Integer, db.ForeignKey('catalog_operations.id'), nullable=False)

    def __repr__(self):
        return jsonify(
            id = self.id,
            user_id = self.user_id,
            ip_address = self.ip_address,
            operation_id = self.operation_id
        )


# Real Time Communication Online Users List Class
class RTCOnlineUsers(db.Model):
    __tablename__ = 'rtc_online_users'
    id = db.Column(db.DateTime, primary_key=True, default=dt.now(default_timezone))
    userlist = db.Column(db.JSON, nullable=False)
    operation_id = db.Column(db.Integer, db.ForeignKey('catalog_operations.id'), nullable=False)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)

    def __repr__(self):
        return jsonify(
            id = self.id,
            userlist = self.userlist,
            operation_id = self.operation_id,
            enabled = self.enabled
        )


# Services Supplement Class
class ServicesSupplement(db.Model):
    __tablename__ = 'services_supplement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('catalog_services.id'), nullable=False)
    name = db.Column(db.String(280), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(EncryptedType(db.String(2000), get_crypto_key, AesEngine, 'pkcs5'), nullable=True)

    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
            service_id = self.service_id,
            description = self.description,
            url = self.url
        )


# Surveys Class
class Surveys(db.Model):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    name_short = db.Column(db.String(6), unique=True, nullable=True)
    description = db.Column(db.Text, nullable=True)
    questions = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
            name_short = self.name_short,
            description = self.description,
            questions = self.questions
        )


# Surveys Answered Class
class SurveysAnswered(db.Model):
    __tablename__ = 'surveys_answered'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    answers = db.Column(db.JSON, unique=False, nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    conversation_id = db.Column(db.JSON, nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)

    def __repr__(self):
        return jsonify(
            id = self.id,
            answers = self.answers,
            survey_id = self.survey_id,
            conversation_id = self.conversation_id,
            appointment_id = self.appointment_id
        )


# Surveys Questions Class
class SurveysQuestions(db.Model):
    __tablename__ = 'surveys_questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text, unique=False, nullable=False)
    question_answers = db.Column(db.JSON, unique=False, nullable=False)
    answers_type = db.Column(db.Integer, db.ForeignKey('catalog_surveys_answer_types.id'), nullable=False)

    def __repr__(self):
        return jsonify(
            id = self.id,
            question = self.question,
            answers_type = self.answers_type,
            question_answers = self.question_answers
        )


# User Class
class User(ElasticMixin, UserMixin, db.Model):
    __tablename__ = 'user'
    __searchable__ = ['email', 'name', 'extra_info.names', 'extra_info.last_names']
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=False, nullable=False)
    name = db.Column(db.String(300), unique=False, nullable=False)
    cmuserid = db.Column(db.String(20), unique=False, nullable=False)
    birthdate = db.Column(db.DateTime, unique=False, nullable=True)
    phonenumber = db.Column(db.String(20), unique=False, nullable=True)
    notifications = db.Column(db.Boolean, unique=False, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    datecreated = db.Column(db.DateTime, unique=False, nullable=False, index=True, default=dt.now(default_timezone))
    roles = db.relationship('UserXRole', lazy='subquery', back_populates='user')
    extra_info = db.relationship('UserExtraInfo', lazy='subquery', back_populates='user', uselist=False)

    # UserClass properties and methods
    @orm.reconstructor
    def __init__(self):
        # Properties required by Flask-Login
        self._is_active = True
        self._is_authenticated = True

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, val):
        self._is_active = val

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, val):
        self._is_authenticated = val

    def __repr__(self):
        return jsonify(
            id = self.id,
            uid = self.uid,
            email = self.email,
            name = self.name,
            cmuserid = self.cmuserid,
            birthdate = self.birthdate,
            phonenumber = self.phonenumber,
            notifications = self.notifications,
            enabled = self.enabled,
            roles = self.roles
        )
    
    # Method required by Flask-Login
    def get_id(self):
        return self.uid
    
    # Method to return user roles
    def get_user_roles(self, name_short = False):
        u_roles = []

        # Iterate through all roles
        for role in self.roles:
            u_roles.append(role.user_role.name if not name_short else role.user_role.name_short)
        
        return u_roles
    
    # Method to validate user role
    def is_user_role(self, uroles):
        hasRole = False

        # Iterate through all roles
        for role in self.roles:
            # Check the specified user role
            if role.user_role.name_short in uroles:
                hasRole = True
        
        return hasRole
    

# User Additional Information
class UserExtraInfo(db.Model):
    __tablename__ = 'UserExtraInfo'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    national_id_type = db.Column(db.Integer, db.ForeignKey('catalog_id_document_types.id'), nullable=True)
    national_id = db.Column(db.String(30), unique=False, nullable=True)
    last_names = db.Column(db.String(300), unique=False, nullable=True)
    names = db.Column(db.String(300), unique=False, nullable=True)
    alias = db.Column(db.String(300), unique=False, nullable=True)
    avatar = db.Column(db.String(50), unique=False, nullable=True)
    country = db.Column(db.JSON, unique=False, nullable=True)
    state = db.Column(db.JSON, unique=False, nullable=True)
    city = db.Column(db.JSON, unique=False, nullable=True)
    user = db.relationship('User', lazy='subquery', back_populates='extra_info')
    biography = db.Column(db.JSON, unique=False, nullable=True)
    config = db.Column(db.JSON, unique=False, nullable=True)
    kobotoolbox = db.Column(db.JSON, unique=False, nullable=True)
    acceptterms = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    profession_id = db.Column(db.Integer, db.ForeignKey("professions.id"),nullable=True)
    profession = db.relationship("Professions")
    def __repr__(self):
        return jsonify(
            id = self.id,
            alias = self.alias,
            names = self.names,
            last_names = self.last_names,
            avatar = self.avatar,
            country = self.country,
            state = self.state,
            city = self.city,
            acceptterms = self.acceptterms
        )

# Professions
class Professions(db.Model):
    _tablename__ = 'professions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), unique=False, nullable=True)
    name_short = db.Column(db.String(40), unique=True, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    users = db.relationship("UserExtraInfo", back_populates="profession")
    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
            enabled = self.enabled,
            name_short = self.name_short
        )


# WalletTransaction
class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transaction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.now(default_timezone))
    #status (2) in progress, (1) completed, (0) canceled
    status = db.Column(db.Integer, unique=False, nullable=True, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    amount = db.Column(db.Numeric(precision=10, scale=2), unique=False, nullable=True, default=0)
    #type – (0)deposit, (1)withdrawal
    type = db.Column(db.Integer, unique=False, nullable=True, default=0)
    descripcion = db.Column(db.Text, nullable=True)
    cancelled_reasons = db.Column(db.Text, unique=False, nullable=True)
    services_id = db.Column(db.Integer, db.ForeignKey('catalog_services.id'), nullable=True)
    services = db.relationship("CatalogServices")

# Catalog - Services Class
class CompanyStatus(db.Model):
    __tablename__ = 'company_status'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    name_short = db.Column(db.String(10), unique=True, nullable=True)


class CompanyStage(db.Model):
    __tablename__ = 'company_stage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    name_short = db.Column(db.String(10), unique=True, nullable=True)

# Attention Log
class AttentionLog(db.Model):
    _tablename__ = 'attentionlog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 0 none , 1 create , 2 update, 3 delete, 4 diagnosis, 5 action plan, 6 bitacora, 7 asignada
    codigo = db.Column(db.Integer, unique=False, nullable=True, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    description = db.Column(db.Text, unique=False, nullable=True)
    date_attention = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, nullable=True, default=dt.now(default_timezone))

# Attention Log
class ContactCenter(db.Model):
    _tablename__ = 'contactcenter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    name = db.Column(db.String(300), unique=False, nullable=True)
    phone = db.Column(db.String(300), unique=False, nullable=True)
    message = db.Column(db.Text, unique=False, nullable=True)
    date_created = db.Column(db.DateTime, nullable=True, default=dt.now(default_timezone))

# Company
class Company(db.Model):
    _tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rtn = db.Column(db.String(50), unique=False, nullable=True)
    dni = db.Column(db.String(50), unique=True, nullable=True)
    name = db.Column(db.String(300), unique=False, nullable=True)
    avatar = db.Column(db.String(50), unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    address = db.Column(db.String(400), unique=False, nullable=True)
    social_networks = db.Column(db.JSON, unique=False, nullable=True)
    phones = db.Column(db.JSON, unique=False, nullable=True)
    public = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    users = db.relationship("UserExtraInfo", back_populates="company")
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by_data = db.relationship("User", backref='created_by_data')
    inscripcion_id = db.Column(db.Integer, db.ForeignKey("inscripciones.id"),nullable=True)
    inscripcion = db.relationship("Inscripciones")
    available_credit = db.Column(db.FLOAT, unique=False, nullable=True, default=0)
    status_id = db.Column(db.Integer, db.ForeignKey('company_status.id'), nullable=True)
    status = db.relationship("CompanyStatus")
    stage_id = db.Column(db.Integer, db.ForeignKey('company_stage.id'), nullable=True)
    stage = db.relationship("CompanyStage")
    date_created = db.Column(db.DateTime, nullable=True, default=dt.now(default_timezone))
    istransferred = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    have_action_plan = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    date_action_plan = db.Column(db.DateTime, nullable=True)
    date_first_service_action_plan = db.Column(db.DateTime, nullable=True)
    action_plan_progress = db.Column(db.FLOAT, unique=False, nullable=True, default=0)

# Company
class Inscripciones(db.Model):
    _tablename__ = 'inscripciones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni = db.Column(db.String(50), unique=False, nullable=True)
    rtn = db.Column(db.String(50), unique=False, nullable=True)
    name = db.Column(db.String(300), unique=False, nullable=True)
    company_name = db.Column(db.String(300), unique=False, nullable=True)
    departamento = db.Column(db.Text, unique=False, nullable=True)
    municipio = db.Column(db.String(400), unique=False, nullable=True)
    aldea = db.Column(db.String(400), unique=False, nullable=True)
    correo = db.Column(db.String(50), unique=False, nullable=True)
    phone = db.Column(db.String(50), unique=False, nullable=True)
    elegible = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    cohorte = db.Column(db.Integer, unique=False, nullable=True, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.now(default_timezone))
    respuestas = db.Column(db.JSON, unique=False, nullable=True)
    attended = db.Column(db.Boolean, unique=False, nullable=True, default=False)
    attended_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship("User")
    attention_date = db.Column(db.DateTime, nullable=True)
    externa = db.Column(db.Integer, unique=False, nullable=True, default=0)
    #status (1) completed, (0) canceled
    status = db.Column(db.Integer, unique=False, nullable=True, default=1)
    def __repr__(self):
        return jsonify(
            id = self.id,
            dni = self.dni,
            name = self.name,
            rtn = self.rtn,
        )
    
class DiagnosisCompany(db.Model):
    __tablename__ = 'diagnosis_company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.now(default_timezone))
    status = db.Column(db.Boolean, nullable=False, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    # (1) KOBOTOOLBOX, (2) INOOVA
    origin = db.Column(db.Integer, unique=False, nullable=True, default=1)
    respuestas = db.Column(db.JSON, unique=False, nullable=True)
    resultados = db.Column(db.JSON, unique=False, nullable=True)
    first = db.Column(db.Boolean, nullable=True, default=False)

# Appointments Class
class ActionPlan(db.Model):
    __tablename__ = 'action_plan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.now(default_timezone))
    date_scheduled_start = db.Column(db.DateTime, nullable=True)
    date_scheduled_end = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Define la relación con la clase User para employe_assigned
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    services_id = db.Column(db.Integer, db.ForeignKey('catalog_services.id'), nullable=True)
    services = db.relationship("CatalogServices")
    employe_assigned = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    date_created = db.Column(db.DateTime, nullable=True, default=dt.now(default_timezone))
    # Define la relación con la clase User para employe_assigned
    employe_assigned_user = db.relationship('User', foreign_keys=[employe_assigned])
    employe_accepted = db.Column(db.Boolean, nullable=True, default=False)
    usr_accepted = db.Column(db.DateTime, nullable=True)
    emp_attendance_start = db.Column(db.DateTime, nullable=True)
    emp_attendance_ending = db.Column(db.DateTime, nullable=True)
    cancelled = db.Column(db.Boolean, nullable=True, default=False)
    cancelled_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    cancelled_reasons = db.Column(db.Text, unique=False, nullable=True)
    progress = db.Column(db.FLOAT, unique=False, nullable=True, default=0)
    fase = db.Column(db.Integer, unique=False, nullable=True, default=0)
    version = db.Column(db.Integer, unique=False, nullable=True, default=0)
    descripcion = db.Column(db.Text, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    comment_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    comment_by_user = db.relationship('User', foreign_keys=[comment_by])
    # Define si es una asesoria es puntual
    espuntal = db.Column(db.Boolean, nullable=True, default=False)
    puntuacion = db.Column(db.FLOAT, unique=False, nullable=True, default=0)
    nota = db.Column(db.Text, nullable=True)
    rating_date_created = db.Column(db.DateTime, nullable=True)
    rating_given_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    rating_given_by_user = db.relationship('User', foreign_keys=[rating_given_by])
    rating_value = db.Column(db.Float, nullable=True, default=0)
    rating_comment = db.Column(db.Text, nullable=True)

class ActionPlanReferences(db.Model):
    __tablename__ = 'action_plan_references'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_plan_id = db.Column(db.Integer, db.ForeignKey("action_plan.id"),nullable=True)
    action_plan = db.relationship("ActionPlan")
    employe_assigned = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    employe_accepted = db.Column(db.Boolean, nullable=True, default=False)
    cancelled = db.Column(db.Boolean, nullable=True, default=False)
    cancelled_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    descripcion = db.Column(db.Text, unique=False, nullable=True)
    date_created = db.Column(db.DateTime, nullable=True, default=dt.now(default_timezone))
    # Define la relación con la clase User para employe_assigned
    employe_assigned_user = db.relationship('User', foreign_keys=[employe_assigned])
    # Define la relación con la clase User para cancelled_by
    cancelled_by_user = db.relationship('User', foreign_keys=[cancelled_by])

# Services Supplement Class
class ActionPlanHistory(db.Model):
    __tablename__ = 'action_plan_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    documento = db.Column(db.String(50), unique=False, nullable=True)
    action_plan_id = db.Column(db.Integer, db.ForeignKey('action_plan.id'), nullable=False)
    action_plan = db.relationship("ActionPlan")
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=True)
    endservices = db.Column(db.Boolean, nullable=True, default=False)
    cancelled = db.Column(db.Boolean, nullable=True, default=False)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.now(default_timezone))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    progress = db.Column(db.Integer, unique=False, nullable=True, default=0)
    advisory_time = db.Column(db.Time, nullable=True)
    id_modality_type =db.Column(db.Integer, db.ForeignKey('modality_type.id'),nullable=True)
    modality_type = db.relationship("ModalityType")


# Services Supplement Class
class CompanyMonitoring(db.Model):
    __tablename__ = 'company_monitoring'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=True)
    cancelled = db.Column(db.Boolean, nullable=True, default=False)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.now(default_timezone))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_service_channel =db.Column(db.Integer, db.ForeignKey('service_channel.id'),nullable=True)
    service_channel = db.relationship("ServiceChannel")
    document_local = db.Column(db.String(250), unique=False, nullable=True)
    date = db.Column(db.Date, nullable=True)
    hour = db.Column(db.Time, nullable=True)


# User's Employees Assigned Class
class UserXEmployeeAssigned(db.Model):
    __tablename__ = 'user_x_employees_assigned'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('catalog_services.id'), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datecreated = db.Column(db.DateTime, unique=False, nullable=False, index=True, default=dt.now(default_timezone))
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)

    def __repr__(self):
        return jsonify(
            id = self.id,
            user_id = self.user_id,
            service_id = self.service_id,
            employee_id = self.employee_id,
            enabled = self.enabled,
            name = self.user_id.name,
        )


# User Roles Class
class UserXRole(db.Model):
    __tablename__ = 'user_x_role'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user_role_id = db.Column(db.Integer, db.ForeignKey('catalog_user_roles.id'), primary_key=True)
    datecreated = db.Column(db.DateTime, unique=False, nullable=False, index=True, default=dt.now(default_timezone))
    user = db.relationship('User', back_populates='roles')
    user_role = db.relationship('CatalogUserRoles', back_populates='users')
    
    def __repr__(self):
        cxt = {'id':str(self.user_role.name)}
        return str(self.user_role.name) + ' , ' + str(self.user_role.id)



# Catalog - ID Document Type Class
class TrainingType(db.Model):
    __tablename__ = 'training_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    name_short = db.Column(db.String(10), unique=True, nullable=True,)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
        )

# Catalog - ID Document Type Class
class ModalityType(db.Model):
    __tablename__ = 'modality_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    name_short = db.Column(db.String(10), unique=True, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
        )

class ServiceChannel(db.Model):
    __tablename__ = 'service_channel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    name_short = db.Column(db.String(10), unique=True, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
        )
    
# Catalog - ID Document Type Class
class CourseManagers(db.Model):
    __tablename__ = 'course_managers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    name_short = db.Column(db.String(10), unique=True, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)

    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
        )

class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(200), unique=False, nullable=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    id_training_type =db.Column(db.Integer, db.ForeignKey('training_type.id'), nullable=False)
    training_type = db.relationship("TrainingType")
    id_modality_type =db.Column(db.Integer, db.ForeignKey('modality_type.id'), nullable=False)
    modality_type = db.relationship("ModalityType")
    id_course_managers = db.Column(db.Integer, db.ForeignKey('course_managers.id'), nullable=False)
    course_managers = db.relationship("CourseManagers")
    date_scheduled_start = db.Column(db.DateTime, nullable=True)
    date_scheduled_end = db.Column(db.DateTime, nullable=True)
    time_scheduled_start = db.Column(db.Time, nullable=True)
    time_scheduled_end = db.Column(db.Time, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    isworkshop  = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)
    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
        )
class Workshops(db.Model):
    __tablename__ = 'workshops'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_course =db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    course = db.relationship("Courses")
    date_start = db.Column(db.DateTime, nullable=True)
    date_end = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lugar = db.Column(db.String(300), unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.description
        )

class EnrollmenWorkshops(db.Model):
    __tablename__ = 'enrollmenworkshops'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_workshop =db.Column(db.Integer, db.ForeignKey('workshops.id'), nullable=False)
    workshop = db.relationship("Workshops")
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    date_start = db.Column(db.DateTime, nullable=True)
    date_end = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lugar = db.Column(db.String(300), unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    complete = db.Column(db.Boolean, nullable=True, default=False)
    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.description
        )
    
class EnrollmentRecord(db.Model):
    __tablename__ = 'enrollment_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_course =db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    course = db.relationship("Courses")
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    date_start = db.Column(db.DateTime, nullable=True)
    date_end = db.Column(db.DateTime, nullable=True)
    complete = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lugar = db.Column(db.String(300), unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.description,
        )

# Catalog - ID Evaluations
class Evaluations(db.Model):
    _tablename__ = 'evaluations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni = db.Column(db.String(50), unique=False, nullable=True)
    name = db.Column(db.String(300), unique=False, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.now(default_timezone))
    respuestas = db.Column(db.JSON, unique=False, nullable=True)
    result = db.Column(db.FLOAT, unique=False, nullable=True, default=0.00)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)


class surveys_sde(db.Model):
    _tablename__ = 'surveys_sde'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=True)
    company = db.relationship("Company")
    date_created = db.Column(db.DateTime, nullable=False, default=dt.now(default_timezone))
    respuestas = db.Column(db.JSON, unique=False, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    catalog_surveys_id = db.Column(db.Integer, db.ForeignKey("catalog_surveys_sde.id"),nullable=True)
    catalog_surveys = db.relationship("catalog_surveys_sde")
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship("User")
    document_local = db.Column(db.String(250), unique=False, nullable=True)
    
class catalog_surveys_sde(db.Model):
    _tablename__ = 'catalog_surveys_sde'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    name = db.Column(db.String(60), unique=True, nullable=False)
    name_short = db.Column(db.String(6), unique=True, nullable=True)