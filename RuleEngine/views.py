from django.shortcuts import render
from RuleEngine import models
from RuleEngine.ruleengineimpl import Rules
from ActionEngine.logsprint import entryExit
from rest_framework.response import Response
from rest_framework.decorators import api_view
import rest_framework.status as status


@api_view(['POST'])
@entryExit
def create_rule(request):
    data = request.data
    rule=Rules(data)
    result = rule.create_rule()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['PUT'])
@entryExit
def update_rule(request):
    data = request.data
    rule = Rules(data)
    result = rule.update_rule()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['DELETE'])
@entryExit
def delete_rule(request):
    data = request.data
    rule = Rules(data)
    result = rule.delete_rule()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['GET'])
@entryExit
def getall_rules(request):
    data=request.GET
    rule = Rules(data)
    result = rule.getall_rules()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['GET'])
@entryExit
def get_rule_details(request):
    data = int(request.GET['rule_id'])
    rule = Rules(data)
    result = rule.get_rule_details()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['POST'])
@entryExit
def associate_host_rule(request):
    data = request.data
    rule = Rules(data)
    result = rule.associate_host_rule()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['GET'])
@entryExit
def get_host_rule(request):
    data=request.GET
    rule = Rules(data)
    result=rule.get_host_rule()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['DELETE'])
@entryExit
def delete_association(request):
    data=request.data
    rule = Rules(data)
    result=rule.delete_association()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['GET'])
@entryExit
def get_status(request):
    data=request.GET
    rule = Rules(data)
    result=rule.get_status()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['GET'])
@entryExit
def assosiate_action(request):
    data=request.GET
    rule = Rules(data)
    result=rule.associate_action()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['DELETE'])
@entryExit
def delete_action(request):
    data = request.data
    rule = Rules(data)
    result = rule.delete_action()
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
@entryExit
def create_action(request):
    data = request.data
    rule = Rules(data)
    result = rule.create_action()
    return Response(result, status=status.HTTP_200_OK)
