from flask_mail import Message
from flask import current_app
from . import mail  # Importar la instancia de Flask-Mail desde __init__.py

def send_email(recipients, subject, html_content):
    try:
        # Crear un objeto de mensaje
        mensaje = Message(subject, sender='infoinnova@ciudadmujer.gob.hn', recipients=recipients)
        
        # Contenido HTML del correo
        mensaje.html = html_content
        
        # Enviar el correo
        mail.send(mensaje)
        
        return True
    except Exception as e:
        print(str(e))
        return False
