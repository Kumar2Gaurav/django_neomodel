from twilio.rest import Client
from ActionEngine.models import *
account_sid = "ACd9e2c478a6cbe5bd28d68e7f1e592f32" #d5afbc9a73fd0cb180781eda1a390846
# auth_token = "16836908492c5837f472a1e68b8f2496" #AC52d78d2feb707f9ec6696a3964665ebd

class SMS:

  def sendsms(self,data):
    message=data['message']

    objmail= OutputConfig.objects.get(name="SMS")
    auth_token=objmail.techKey
    client = Client(account_sid, auth_token)
    client.messages.create(to="+919818873256",
                          from_='+16148929947',
                          body=message)
    return {"Status":True,"data":"message send"}