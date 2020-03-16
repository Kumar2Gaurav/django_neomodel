"""CatsMagroo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Hosts import views as host_views
from EventEngine import views as event_views
from ActionEngine import views as action_views
from RuleEngine import views as rule_views


urlpatterns = [
    path('admin/', admin.site.urls),
# ========================================= Eventengine urls ===================================== #
    path('eventengine/nagios', event_views.nagios_log),
    path('eventengine/huwaei_u2000', event_views.snmp_huwaie_u2000),
    path('eventengine/huwaei_m2000', event_views.snmp_huwaie_m2000),
    # path('eventengine/huawei', event_views.huawei_event),

# ========================================= Input Source Type ==================================== #
    path('eventengine/inputsourcetype/getall', event_views.getAllInputSourceType),
    path('eventengine/inputsourcetype/create', event_views.createInputSourceType),
    path('eventengine/inputsourcetype/update', event_views.updateInputSourceType),
    path('eventengine/inputsourcetype/delete', event_views.deleteInputSourceType),

# ========================================= Input Source ========================================= #
    path('eventengine/inputsource/getall', event_views.getAllInputSource),
    path('eventengine/inputsource/create', event_views.createInputSource),
    path('eventengine/inputsource/update', event_views.updateInputSource),
    path('eventengine/inputsource/delete', event_views.deleteInputSource),

# ============================================= Events =========================================== #
    path('eventengine/events/getall', event_views.getAllEvents),
    path('eventengine/events/geteventchild', event_views.getEventChild),
    path('eventengine/events/getcounts', event_views.getEventsWithCITypeCount),
    path('eventengine/events/geteventdata', event_views.getEventData),

# ========================================= Progress Charts ====================================== #
    path('eventengine/events/chart', event_views.getDailyEventsAndIncidentCount),

# ============================================= Hosts ============================================ #
    path('hosts/host/create', host_views.create_host),
    path('hosts/host/update', host_views.update_host),
    path('hosts/host/delete', host_views.delete_host),
    path('hosts/host/get', host_views.get_host),
    path('hosts/host/get_all', host_views.get_all_host),
    path('hosts/host/search_host',host_views.search_host),
    path('hosts/enter_all_entries',host_views.all_ci_entries),

# ======================================== Neo Model  ============================================ #
    path('neomodel/create/host_node', host_views.create_host_node),
    path('neomodel/update/host_node', host_views.update_host_node),
    path('neomodel/delete/host_node', host_views.delete_host_node),
    path('neomodel/get/host_node', host_views.get_host_node),
    path('neomodel/get_all/host_node', host_views.getall_hosts),
    path('neomodel/create/service_node', host_views.create_service_node),
    path('neomodel/update/service_node', host_views.update_service_node),
    path('neomodel/delete/service_node', host_views.delete_service_node),
    path('neomodel/get/service_node', host_views.get_service_node),
    path('neomodel/get_all/service_node', host_views.getall_services),
    path('neomodel/connect', host_views.node_connection),
    path('neomodel/disconnect', host_views.node_disconnection),
    path('neomodel/host/connect', host_views.host_connection),
    path('neomodel/host/disconnect', host_views.host_disconnection),
    path('neomodel/all_nodes/host', host_views.all_host_nodes),

# ========================================= Rule Engine ========================================== #
    path('ruleengine/rule/create',rule_views.create_rule),
    path('ruleengine/rule/update', rule_views.update_rule),
    path('ruleengine/rule/delete', rule_views.delete_rule),
    path('ruleengine/rule/get_rule', rule_views.get_rule_details),
    path('ruleengine/rule/get_all', rule_views.getall_rules),
    path('ruleengine/rule/get_status', rule_views.get_status),
    path('ruleengine/rule/associate_action', rule_views.assosiate_action),
    path('ruleengine/rule/delete_action',rule_views.delete_action),
    path('ruleengine/rule/create_action',rule_views.create_action),
# ======================================== Rule Association ===================================== #

    path('ruleengine/rule/associate_host', rule_views.associate_host_rule),
    path('ruleengine/rule/get_associate_host', rule_views.get_host_rule),
    path('ruleengine/rule/delete_associate_host', rule_views.delete_association),
    #===========================Action engine ==============================#
                 #===========Output source url================
    path('actionengine/outputtype/create',action_views.createOutputtype),
    path('actionengine/source/create',action_views.createOutputSource),
    path('actionengine/source/get',action_views.getAllOutputSource),
    path('actionengine/source/getoutputype',action_views.getOutputtype),
    path('actionengine/source/update',action_views.updateOutputSource),
    path('actionengine/source/delete',action_views.deleteOutputSource),
    path('actionengine/source/allaction',action_views.getAllAction),
      #======================Action Incident url=================
    path('actionengine/getincidentinfo',action_views.getIncidentInfo),
   path('actionengine/getallincident',action_views.getallIncident),
    path('actionengine/executeAction',action_views.executeAction),
    path('actionengine/updateAction',action_views.updateAction),
   path('actionengine/worklogincident',action_views.worklogIncident),
   path('actionengine/allworklog',action_views.getallWorklog),
   path('actionengine/addresolution',action_views.AddToResolution),
    path('actionengine/sendmail',action_views.mailaction),
]
