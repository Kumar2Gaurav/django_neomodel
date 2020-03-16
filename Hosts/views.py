from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
import rest_framework.status as status
from Hosts import hostsimpl as impl
from ActionEngine.logsprint import entryExit


@api_view(['POST'])
@entryExit
def create_host(request):
    data=request.data
    ci=impl.CI(data)
    result=ci.create_hosts()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['PUT'])
@entryExit
def update_host(request):
    data=request.data
    ci = impl.CI(data)
    result=ci.update_hosts()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['DELETE'])
@entryExit
def delete_host(request):
    data=request.data
    ci = impl.CI(data)
    result=ci.delete_hosts()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['GET'])
@entryExit
def get_host(request):
    data=request.GET
    ci = impl.CI(data)
    result=ci.get_hosts()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['GET'])
@entryExit
def get_all_host(request):
    ci = impl.CI()
    result=ci.get_all_hosts()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['GET'])
@entryExit
def search_host(request):
    data = request.GET
    ci = impl.CI(data)
    result = ci.host_search()
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@entryExit
def all_ci_entries(request):
    file=request.FILES['file']
    ci = impl.CI(file)
    result=ci.all_ci_entries(file)
    return Response(result, status=status.HTTP_200_OK)

#------------NEO MODEL ---------------------------#


@api_view(['POST'])
@entryExit
def create_host_node(request):
    data = request.data
    ci = impl.CI(data)
    result = ci.create_hnode()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['PUT'])
@entryExit
def update_host_node(request):
    data = request.data
    ci = impl.CI(data)
    result = ci.update_hnode()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['DELETE'])
@entryExit
def delete_host_node(request):
    data = request.data
    ci = impl.CI(data)
    result =ci.delete_hnode()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['GET'])
@entryExit
def get_host_node(request):
    data = request.GET
    ci = impl.CI(data)
    result =ci.get_hnode()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['GET'])
@entryExit
def getall_hosts(request):
    ci = impl.CI()
    result =ci.all_hnode()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['POST'])
@entryExit
def create_service_node(request):
    data = request.data
    ci = impl.CI(data)
    result = ci.create_snode()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['PUT'])
@entryExit
def update_service_node(request):
    data = request.data
    ci = impl.CI(data)
    result = ci.update_snode()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['DELETE'])
@entryExit
def delete_service_node(request):
    data = request.data
    ci = impl.CI(data)
    result =ci.delete_snode()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['GET'])
@entryExit
def getall_services(request):
    ci = impl.CI()
    result =ci.all_snode()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['GET'])
@entryExit
def get_service_node(request):
    data = request.GET
    ci = impl.CI(data)
    result =ci.get_snode()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['POST'])
@entryExit
def node_connection(request):
    data = request.data
    ci = impl.CI(data)
    result=ci.connect_node()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['POST'])
@entryExit
def node_disconnection(request):
    data = request.data
    ci = impl.CI(data)
    result=ci.disconnect_node()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['POST'])
@entryExit
def host_connection(request):
    data = request.data
    ci = impl.CI(data)
    result=ci.connecting_hosts()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['POST'])
@entryExit
def host_disconnection(request):
    data = request.data
    ci = impl.CI(data)
    result=ci.disconnecting_hosts()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['GET'])
@entryExit
def all_host_nodes(request):
    # data = request.GET
    ci = impl.CI()
    result=ci.get_all_hnodes_Connections()
    return Response(result, status=status.HTTP_200_OK)