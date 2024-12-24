from flask import Flask,request,jsonify
from flask_mail import Mail,Message

app=Flask(__name__)


#mail configurations

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='pradeepmajji42@gmail.com'
app.config['MAIL_PASSWORD']='rapkekywqeuwybej'
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USE_TLS']=False


mail=Mail(app)

@app.route('/send-email',methods=['POST'])
def send_mail():
    data=request.get_json()
    rec=data["to"]
    sub=data["subject"]
    body=data["text"]

    msg=Message(sub,sender='Pradeep Majji <pradeepmajji42@gmail.com>',recipients=[rec])
    msg.body=body

    try:
        mail.send(msg)
        return jsonify({'message':'email sent success'}),200
    except Exception as e:
        return jsonify({'error':'error in email sending'}),500
    
if __name__=='__main__':
    app.run(debug=True)


