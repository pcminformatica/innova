
class JsonPhone():
    phone = ''
    cellphone = ''
    def jsonFormat(self):
        return [{"phone": self.phone, "cellphone": self.cellphone}]

class JsonSocial():
    facebook = ''
    email = ''
    instagram = ''    
    def jsonFormat(self):
        return [{"facebook": self.facebook, "email": self.email,"instagram": self.instagram}]