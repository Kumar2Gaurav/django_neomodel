from rest_framework.response import Response
from rest_framework import status
from EventEngine.eventImpl import (
    InputSourceTypeInfo,
    InputSourceInfo,
    EventInfo)
from EventEngine.nagiosImpl import NagionsProcessEvent
from EventEngine.huwaie_u2000impl import HuwaieU2000Event
from EventEngine.huwaie_m2000Impl import HuwaieM2000Event

from rest_framework.decorators import api_view
from ActionEngine.logsprint import entryExit
from EventEngine import CONFIG as MIB


# ============================= NMS Plugins =========================== #
def _parse_U2000_nms(myDict):
    if len(myDict.keys()) > 10:
        res_dic = {"data":{
                        "time_obj" : myDict["SNMPv2-SMI::enterprises.2011.2.15.2.4.3.3.3.0"],
                        "alert_type" : "ALERT",
                        "CI_hostname" : myDict["SNMPv2-SMI::enterprises.2011.2.15.2.4.3.3.4.0"],
                        "CI_ack" : MIB.mib_2[myDict["SNMPv2-SMI::enterprises.2011.2.15.2.4.3.3.2.0"]].upper(),
                        "CI_state" : MIB.mib_11[myDict["SNMPv2-SMI::enterprises.2011.2.15.2.4.3.3.11.0"]].upper(),
                        "CI_alert_name" : myDict["SNMPv2-SMI::enterprises.2011.2.15.2.4.3.3.28.0"],
                        "CI_message" : myDict["SNMPv2-SMI::enterprises.2011.2.15.2.4.3.3.27.0"],
                        "CI_alarm_type" : MIB.mib_10[myDict["SNMPv2-SMI::enterprises.2011.2.15.2.4.3.3.10.0"]],
                        "CI_service":"",
                        "CI_ip":""},
                    "host":myDict["host"],
                    "type":myDict["type"]
        				}
        return res_dic

    return None

def _parse_M2000_nms(myDict):

    if len(myDict.keys()) > 10:
        service = myDict["SNMPv2-SMI::enterprises.2011.2.15.1.7.1.3.0"]
        alarm =myDict["SNMPv2-SMI::enterprises.2011.2.15.1.7.1.24.0"].split(",",2)[-1]
        alarm_type =myDict["SNMPv2-SMI::enterprises.2011.2.15.1.7.1.8.0"].split(",",2)[-1]
        res_dic = {"data":{
                        "time_obj" : myDict["SNMPv2-SMI::enterprises.2011.2.15.1.7.1.5.0"],
                        "alert_type" : "HOST ALERT",
                        "CI_hostname" : myDict["SNMPv2-SMI::enterprises.2011.2.15.1.7.1.1.0"],
                        "CI_ack" : "",
                        "CI_state" : myDict["SNMPv2-SMI::enterprises.2011.2.15.1.7.1.7.0"].upper(),
                        "CI_alert_name" : alarm,
                        "CI_message" : myDict["SNMPv2-SMI::enterprises.2011.2.15.1.7.1.14.0"]+"\n"+myDict["SNMPv2-SMI::enterprises.2011.2.15.1.7.1.3.0"],
                        "CI_alarm_type" : alarm_type,
                        "CI_service":service.strip(),
                        "CI_ip":myDict["SNMPv2-SMI::enterprises.2011.2.15.1.7.1.12.0"]},
                    "host":myDict["host"],
                    "type":myDict["type"]
        				}
        return res_dic

    return None

@api_view(['POST'])
def nagios_log(request):
    data = request.data
    # event = NagionsProcessEvent(data)
    # res = event.processlogEvent()
    return Response("",status=status.HTTP_200_OK)

@api_view(['POST'])
def snmp_huwaie_u2000(request):
    data = request.data
    res = {"Status":False,"msg":"Not Processable event"}
    if len(data.keys())>10:
        data = _parse_U2000_nms(data)
        if data and data["data"]["CI_state"].strip() != "CLEAR":
            u2000 = HuwaieU2000Event(data)
            res = u2000.processU200Event()
    return Response(res,status=status.HTTP_200_OK)

@api_view(['POST'])
def snmp_huwaie_m2000(request):
    data = request.data
    res = {"Status":False,"msg":"Not Processable event"}
    if len(data.keys())>10:
        data = _parse_M2000_nms(data)
        if data and data["data"]["CI_state"].strip() != "CLEAR":
            m2000 = HuwaieM2000Event(data)
            res = m2000.processM2000Event()
    return Response(res,status=status.HTTP_200_OK)


# ========================= Input source type ========================= #
@api_view(['GET'])
@entryExit
def getAllInputSourceType(request):
    data = request.GET
    result = InputSourceTypeInfo(data).getAllInputSourceType()
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@entryExit
def createInputSourceType(request):
    data = request.data
    result = InputSourceTypeInfo(data).createInputSourceType()
    return Response(result, status=status.HTTP_200_OK)


@api_view(['PUT'])
@entryExit
def updateInputSourceType(request):
    data = request.data
    result = InputSourceTypeInfo(data).updateInputSourceType()
    return Response(result, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@entryExit
def deleteInputSourceType(request):
    data = request.data
    result = InputSourceTypeInfo(data).deleteInputSourceType()
    return Response(result, status=status.HTTP_200_OK)



# =========================== Input Source ============================== #
@api_view(['GET'])
@entryExit
def getAllInputSource(request):
    data = request.GET
    result = InputSourceInfo(data).getAllInputSource()
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@entryExit
def createInputSource(request):
    data = request.data
    result = InputSourceInfo(data).createInputSource()
    return Response(result, status=status.HTTP_200_OK)


@api_view(['PUT'])
@entryExit
def updateInputSource(request):
    data = request.data
    result = InputSourceInfo(data).updateInputSource()
    return Response(result, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@entryExit
def deleteInputSource(request):
    data = request.data
    result = InputSourceInfo(data).deleteInputSource()
    return Response(result, status=status.HTTP_200_OK)


# =========================== Events api's ========================= #


@api_view(['GET'])
@entryExit
def getAllEvents(request):
    data = request.GET
    result = EventInfo(data).getAllEvents()
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
@entryExit
def getEventChild(request):
    data = request.GET
    result = EventInfo(data).getChildEvent()
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@entryExit
def getEventsWithCITypeCount(request):
    data = request.GET
    result = EventInfo(data).getEventsWithCITypeCount()
    return Response(result, status=status.HTTP_200_OK)



@api_view(['GET'])
@entryExit
def getDailyEventsAndIncidentCount(request):
    data = request.GET
    result = EventInfo(data).getDailyEventsAndIncidentCountChart()
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
# @entryExit
def getEventData(request):
    data = request.GET
    result = EventInfo(data).getEventData()
    return Response(result, status=status.HTTP_200_OK)


