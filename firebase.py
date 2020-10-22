import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime as dt


cred = credentials.Certificate("Retail-679ab540deb3.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
fecha = dt.datetime.now().strftime("%d/%m/%Y")


def message(usuariomsg, chatmsg, Id, name, sas):
    data = {
        u'name': u'%s'%name,
        u'message': usuariomsg,
        u'respuesta': chatmsg,
        u'sastifaccion': sas,
        }

    db.collection(u'chatbot').document(u'%s'%Id).set(data)
    return
