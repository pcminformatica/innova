
from flask import jsonify
import json

class JsonPhone():
    phone = ''
    cellphone = ''
    def jsonFormat(self):
        return {"phone": self.phone, "cellphone": self.cellphone}

class JsonSocial():
    facebook = ''
    email = ''
    instagram = ''    
    def jsonFormat(self):
        return {"facebook": self.facebook, "email": self.email,"instagram": self.instagram}

class JsonConfigProfile():
    kobotoolbox_access = []

    def jsonFormat(self):
        return {"kobotoolbox_access": self.kobotoolbox_access}
        return list(dict(self), ensure_ascii=False)