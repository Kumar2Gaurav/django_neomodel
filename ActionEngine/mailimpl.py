import smtplib
from ActionEngine.models import *

# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.login("youremailusername", "password")
#smtpserver='smtp.gmail.com:587'



class MailSend:


    def sendemail(self,data):
        # import ipdb;
        # ipdb.set_trace()
        try:
            message = data["message"]
            subject = data["subject"]
            to_addr_list = data["to_addr_list"]
            objmail = OutputConfig.objects.get(name="Email")#need to change
            smtpserver = objmail.host + ":" + str(objmail.port)
            login = objmail.username
            password = objmail.password
            smessage = 'Subject: {}\n\n{}'.format(subject, message)

            server = smtplib.SMTP(smtpserver)
            server.starttls()
            server.login(login, password)
            problems = server.sendmail(login, to_addr_list, smessage)
            server.quit()
            return {"Status":True,"msg":"Mail Send"}
        except Exception as e:
            return {"status":False,"msg":e}



