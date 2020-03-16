from rest_framework.response import Response
from rest_framework.decorators import api_view
import rest_framework.status as status
from ActionEngine.sdimpl import ServiceDeskimpl
from ActionEngine.outputsrcilmpl import OutputOperation
from ActionEngine.mailimpl import MailSend
from ActionEngine.smsimpl import SMS
from .models import *
from ActionEngine.logsprint import entryExit
import rest_framework.status as status
from rest_framework.response import Response
#from ldapAuth.my_decorators import auth_user


@api_view(["POST"])
def mailaction(request):
    try:
        data=request.data
        mail_send=MailSend()
        result= mail_send.sendemail(data)
        return Response(result, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def smsaction(request):
    try:
        data=request.data
        sms=SMS()
        result= sms.sendemail(data)
        return Response(result, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@entryExit
def getAllAction(request):
    try:
        #import ipdb;ipdb.set_trace()
        data= request.data
        outputsrcilmpl = OutputOperation()
        result=outputsrcilmpl.allaction(data)
        return Response(result,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@entryExit
def createOutputtype(request):
    try:
        data= request.data
        outputsrcilmpl = OutputOperation()
        result=outputsrcilmpl.createOutputType(data)
        return Response(result,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@entryExit
def getOutputtype(request):
    try:
        data= request.GET
        outputsrcilmpl = OutputOperation()
        result=outputsrcilmpl.getOutputtype(data)
        return Response(result,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@entryExit
def createOutputSource(request):
    try:
        data=request.data
        print(data)
        outputsrcilmpl = OutputOperation()
        result=outputsrcilmpl.createOutputSource(data)
        return Response(result,status=status.HTTP_200_OK)
    except :
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@entryExit
def getAllOutputSource(request):
    try:
        data= request.GET
        outputsrcilmpl = OutputOperation()
        result= outputsrcilmpl.getAllOutputSource()
        return Response(result,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@entryExit
def updateOutputSource(request):
    try:
        data=request.data
        outputsrcilmpl = OutputOperation()
        result=outputsrcilmpl.updateOutputSource(data)
        print(result)
        return Response(result,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@entryExit
def deleteOutputSource(request):
    try:
        data= request.data
        outputsrcilmpl = OutputOperation()
        result= outputsrcilmpl.deleteOutputSource(data)
        return Response(result, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@entryExit
def getIncidentInfo(request):
    try:
        data = request.GET
        type = data["type_id"]
        output_type= OutputType.objects.get(id=type).code
        # checking of output type
        if output_type=="MNG" :
            sdimpl = ServiceDeskimpl()
            result = sdimpl.GetIncident(data)
            return Response(result, status=status.HTTP_200_OK)

        elif output_type=="SNOW":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        elif output_type=="MAIL":
            result =None
            return Response(result, status=status.HTTP_200_OK)

        else:
            return None

    except:
        return None

@api_view(['GET'])
@entryExit
def getallIncident(request):
    try:
        data = request.GET
        type = data["type_id"]
        output_type= OutputType.objects.get(id=type).code
        #import ipdb;ipdb.set_trace()
        # checking of output type
        if output_type=="MNG" :
            sdimpl = ServiceDeskimpl()
            result = sdimpl.getallIncident(data)
            return Response(result, status=status.HTTP_200_OK)
        elif output_type=="SNOW":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        elif output_type=="MAIL":
            result =None
            return Response(result, status=status.HTTP_200_OK)

        else:
            return None

    except:
        return None


@api_view(['POST'])
@entryExit
def executeAction(request):
    try:
        data = request.data
        type = data["type"]
        # output_type = OutputType.objects.get(id=type).code
        if type == "MNG":
            sdimpl = ServiceDeskimpl()
            result = sdimpl.CreateIncident(data)
            return Response(result, status=status.HTTP_200_OK)
        elif type=="SNOW":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        elif type == "MAIL":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        else:
            return None

    except:
        return None


@api_view(['PUT'])
@entryExit
def updateAction(request):
    try:
        data = request.data
        type = data["type_id"]
        output_type = OutputType.objects.get(id=type).code
        if output_type == "MNG":
            sdimpl = ServiceDeskimpl()
            result = sdimpl.UpdateIncident(data)
            return Response(result, status=status.HTTP_200_OK)
        elif output_type=="SNOW":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        elif output_type == "MAIL":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        else:
            return None

    except:
        return None



@api_view(['PUT'])
@entryExit
def worklogIncident(request):
    try:
        data = request.data
        type = data["type_id"]
        output_type = OutputType.objects.get(id=type).code
        if output_type == "MNG":
            sdimpl = ServiceDeskimpl()
            result = sdimpl.AddWorklog(data)
            return Response(result, status=status.HTTP_200_OK)
        elif output_type=="SNOW":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        elif output_type == "MAIL":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        else:
            return None

    except:
        return None

@api_view(['GET'])
@entryExit
def getallWorklog(request):
    try:
        data = request.data
        type = data["type_id"]
        output_type = OutputType.objects.get(id=type).code
        if output_type == "MNG":
            sdimpl = ServiceDeskimpl()
            result = sdimpl.AllWorklogs(data)
            return Response(result, status=status.HTTP_200_OK)
        elif output_type=="SNOW":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        elif output_type == "MAIL":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        else:
            return None

    except:
        return None


@api_view(['POST'])
@entryExit
def AddToResolution(request):
    try:
        data = request.data
        type = data["type_id"]
        output_type = OutputType.objects.get(id=type).code
        if output_type == "MNG":
            sdimpl = ServiceDeskimpl()
            result = sdimpl.AddToResolution(data)
            return Response(result, status=status.HTTP_200_OK)
        elif output_type=="SNOW":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        elif output_type == "MAIL":
            result = None
            return Response(result, status=status.HTTP_200_OK)

        else:
            return None

    except:
        return None

