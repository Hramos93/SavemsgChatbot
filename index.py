from flask import Flask, request, jsonify, render_template
import os
import re
import dialogflow
from google.protobuf.json_format import MessageToJson
from decouple import config
# import firebase as fb


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    "Retail-679ab540deb3.json"

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


usuarioMsg = []
chatMsg = []
name, sucess = '', ''


def getMsg(Msg):
    Id = Msg.response_id
    responseId = Id[-8:]
    userMsg = Msg.query_result.query_text
    botMsg = Msg.query_result.fulfillment_text
    parameters = Msg.query_result.parameters.fields
    pckg = {
        'Id': Id,
        'resultId': responseId,
        'userMsg': userMsg,
        'botMsg': botMsg,
        'parameters': parameters
    }
    return pckg


def detect_intent_texts(project_id, session_id, text, language_code):
    global usuarioMsg, chatMsg, name, sucess
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        Msg = getMsg(response)
        for i in Msg['parameters']:
            if i == 'given-name':
                name = "".join(re.findall("[a-zA-Z]+", MessageToJson(Msg['parameters'][i]))) # noqa
            print(name)
            if i == 'Cierre':
                sucess = "".join(re.findall("[a-zA-Z]+", MessageToJson(Msg['parameters'][i]))) # noqa
        if Msg['responseId'] == Msg['responseId']:
            usuarioMsg.append(Msg['userMsg'])
            chatMsg.append(Msg['botMsg'])
        else:
            usuarioMsg = Msg['userMsg']
            chatMsg = Msg['botMsg']
        # fb.message(usuarioMsg, chatMsg, responseId, name, sucess)
        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = config('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message":  fulfillment_text}

    return jsonify(response_text)
# run Flask app


if __name__ == "__main__":
    app.run()
