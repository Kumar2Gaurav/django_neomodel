import requests
import json

from EventEngine.models import *
from ActionEngine.models import *
from RuleEngine.models import Action
from datetime import datetime, timedelta

class OutputOperation:

    def createOutputType(self,data):
        try:
            createtype= OutputType(name=data['name'],code=data['code'])
            createtype.save()
            return {"Status": True, "msg": "outputsource created successfully","data":createtype.id}

        except Exception as e:
            return {"Status": False, "msg": str(e)}


    def getOutputtype(self,data):
        try:
            alloutputType= OutputType.objects.all()
            alloutputTypelist=[]
            for i in alloutputType:
                dic={}
                dic['name']=i.name
                dic['code']=i.code
                dic["id"]=i.id
                alloutputTypelist.append(dic)
            return {"Status": True, "msg": "all output type","data":alloutputTypelist}
        except Exception as e:
            return {"Status": False, "msg": str(e)}


    def allaction(self,data):
        try:
            #import ipdb;ipdb.set_trace()
            allactionOut= Action.objects.all()
            Actionlist=[]
            for i in allactionOut:
                dic={}
                dic["id"]=i.id
                dic["name"]= i.name
                dic["code"]=i.code
                dic["output_ass"]=i.output_ass.name
                Actionlist.append(dic)
            return {"Status": True, "msg": "all output type", "data": Actionlist}
        except Exception as e:
            return {"Status": False, "msg": str(e)}

    def createOutputSource(self,data):
        try:
            #import ipdb;ipdb.set_trace()
            type=OutputType.objects.get(code= data['type'])
            result = OutputConfig(name=data["name"],
            outType = type,
            host = data['host'],
            port = data['port'],
            username = data['username'],
            password = data['password'],
            techKey = data['techkey'])
            result.save()

            return {"Status": True, "msg": "outputsource created successfully","data":result.id}
        except Exception as e:
            return {"Status": False, "msg": str(e)}


    def getAllOutputSource(self):
        try:
            #import ipdb;ipdb.set_trace()
            outputsource = OutputConfig.objects.all()
            outputList = []
            for output in outputsource:
                dic = {
                    'id': output.id,
                    'name': output.name,
                    'host' :output.host,
                    'port': output.port,
                    'username':output.username,
                    'password':output.password,
                    'techkey':output.techKey,
                    'code' : output.outType.name
                }
                outputList.append(dic)
            return {"Status": True, "data": outputList}

        except OutputConfig.DoesNotExist:
            return {"Status": False, "msg": "outputconfig does not exsist"}
        except Exception as e:
            return {"Status": False, "msg": str(e)}


    def updateOutputSource(self,data):
        try:
            id= data["source_id"]
            type = OutputType.objects.get(code=data['code'])
            updateoutput_source=OutputConfig.objects.filter(id=id).update(name=data["name"],
            outType = type,
            host = data['host'],
            port = data['port'],
            username = data['username'],
            password = data['password'],
            techkey = data['techkey'])
            return {"Status": True, "msg": "Output source is successfully updated for" ,"data":updateoutput_source}

        except OutputConfig.DoesNotExist:
            return {"Status": False, "msg": "outputconfig does not exsist"}

        except Exception as e:
            return {"Status": False, "msg": str(e)}



    def deleteOutputSource(self,data):
        try:
            id= OutputConfig.objects.filter(id=int(id)).delete()
            return {"Status": "Success", "data": data['name'],"msg": "successfully deleted"}

        except OutputConfig.DoesNotExist:
            return {{"Status": False, "msg": "outputconfig does not exsist"}}
        except Exception as e:
            return {"Status": False, "msg": str(e)}