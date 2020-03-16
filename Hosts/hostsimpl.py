from Hosts.models import Hosts,HostsGraph,ServicesGraph
from EventEngine.models import InputSource,InputSourceType
import openpyxl


class CI():

    data=None

    def __init__(self,data=None):
        self.data=data


    def create_hosts(self):
        try:
            typeObj=InputSource.objects.get(pk=self.data['inputSource_id'])
            if Hosts.objects.filter(name=self.data['name']).filter(inputType=typeObj):
                return {"status": True, "msg":  self.data['name'] + " host already exists"}
            else:
                hostobj=Hosts(name=self.data['name'],ipAddress=self.data['ipAddress'],hostType=self.data['hostType'],inputType=typeObj)
                hostobj.save()
                return {"status": True, "msg":  self.data['name'] + " host record is created"}
        except InputSource.DoesNotExist:
            return {"Status": False, "msg": "InputSource doesnot exist"}
        except Exception as ae:
            return {"Status": False, "msg": str(ae)}


    def update_hosts(self):
        try:
            # import ipdb;ipdb.set_trace()
            typeObj = InputSource.objects.get(pk=self.data['inputSource_id'])
            hostobj = Hosts.objects.get(pk=self.data['host_id'])
            if "name" in self.data:
                # if Hosts.objects.filter(name=self.data['name']).filter(inputType=typeObj):
                #     return {"status": False, "msg": self.data['name'] + " name already exists"}
                # else:
                hostobj.name=self.data['name']
            if "ipAddress" in self.data:
                hostobj.ipAddress=self.data['ipAddress']
            if 'hostType' in self.data:
                hostobj.hostType = self.data['hostType']
            if 'inputType_id' in self.data:
                hostobj.inputType = typeObj
            hostobj.save()
            return {"status": True, "msg":" host record is updated"}
        except InputSource.DoesNotExist:
            return {"Status": False, "msg": "InputSource doesnot exist"}
        except Hosts.DoesNotExist:
            return {"Status": False, "msg": "host doesnot exist"}
        except Exception as ae:
            return {"Status": False, "msg": str(ae)}


    def delete_hosts(self):
        try:
            hostobj = Hosts.objects.get(pk=self.data['host_id'])
            hostobj.delete()
            return {"status": True, "msg": " host record is deleted"}
        except Hosts.DoesNotExist:
            return {"Status": False, "msg": "host doesnot exist"}
        except Exception as ae:
            return {"Status": False, "msg": str(ae)}


    def get_hosts(self):
        try:
            host = Hosts.objects.get(pk=self.data['host_id'])
            dic = {}
            dic['id'] = host.id
            dic['name']=host.name
            dic['ipAddress'] = host.ipAddress
            # dic['hostType'] = host.hostType
            dic['hostType'] = host.hostType
            dic['inputSource'] = host.inputType.name
            return {"Status":True,"host_details":dic}
        except Hosts.DoesNotExist:
            return {"Status": True, "msg": "no host exist"}
        except Exception as ae:
            return {"Status":False,"msg": str(ae)}


    def get_all_hosts(self):
        try:
            host_list = Hosts.objects.all()
            host_list_res =[]
            for ci in host_list:
                dic = {}
                dic['id'] = ci.id
                dic['name']=ci.name
                dic['ipAddress'] = ci.ipAddress
                dic['hostType'] = ci.hostType
                dic['inputSource'] = ci.inputType.name
                host_list_res.append(dic)
            return {"Status":True,"host_list":host_list_res}
        except Hosts.DoesNotExist:
            return {"Status": True, "msg": "no host exist"}
        except Exception as ae:
            return {"Status":False,"msg": str(ae)}

    def host_search(self):
        host = self.data['name']
        try:
            all_host = Hosts.objects.filter(name__icontains=host)
            list = []
            for host in all_host:
                result = {}
                result['host'] = host.name
                result['id'] =host.id
                list.append(result)
            return {"Status": True, "msg": list}
        except Hosts.DoesNotExist:
            return {"Status": False, "msg": "no host exist"}
        except Exception as ae:
            return {'status': False, "msg": "can find get the host"+str(ae)}


    def get_type_id(self, name):
        temp=InputSource.objects.get(name=name)
        return temp

    def all_ci_entries(self, file):

        try:
            wb = openpyxl.load_workbook(file)
            worksheet = wb["Sheet1"]
            excel_data = {}
            # import ipdb;ipdb.set_trace()
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data['name'] = row_data[0]
                excel_data['ipAddress'] = row_data[1]
                excel_data['hostType'] = row_data[2]
                ciType_code = row_data[3]
                try:
                    if Hosts.objects.filter(name=excel_data['name']).filter(inputType=self.get_type_id(ciType_code)):
                        continue
                    else:
                        hostobj = Hosts(name=excel_data['name'], ipAddress=excel_data['ipAddress'],
                                        hostType=excel_data['hostType'], inputType=self.get_type_id(ciType_code))
                        hostobj.save()
                except InputSource.DoesNotExist:
                    print("continue---------------------------")
                    pass
            return {'status': True, "msg": excel_data}

        except InputSourceType.DoesNotExist:
            return {'Status': False,'Notification':"Input Source Type Does not exists"}
        except Exception as ae:
            return {'status': False, "msg": ae}


        #--------------NEO MODEL ---------------------#


    def create_hnode(self):
        try:
            host=HostsGraph.nodes.first_or_none(name=self.data['host_name'])
            if host:
                return {"Status": False, "Notification": "Host already exists"}
            else:
                host = HostsGraph(name=str(self.data['host_name']), ip=str(self.data['host_ip']), alias=str(self.data['host_alias']),
                        type=str(self.data['type']))
                host.save()
                return {"Status": True, "Notification": "Host Node {} created successfully".format(self.data['host_name'])}
        except Exception as ae:
            return {"Status": False, "Notification": "Host Node not created " + str(ae)}

    def update_hnode(self):
        host_name = self.data['host_name']
        try:
            import ipdb;ipdb.set_trace()
            get_host = HostsGraph.nodes.first_or_none(name=host_name)
            if 'newhost_name' in self.data:
                temp=HostsGraph.nodes.first_or_none(name=self.data['newhost_name'])
                if temp:
                    return {'status': False, 'notification': 'host {} already exists'.format(self.data['newhost_name'])}
                else:
                    get_host.name = self.data['newhost_name']
            if 'host_ip' in self.data:
                get_host.ip = self.data['host_ip']
            if 'host_alias' in self.data:
                get_host.alias = self.data['host_alias']
            if 'type' in self.data:
                get_host.type = self.data['type']
            get_host.save()
            return {'status': True, 'notification': 'host {} updated successfully'.format(get_host.name)}
        except HostsGraph.DoesNotExist:
            return {'status': True, 'notification': 'host {} doesnot exist'.format(get_host.name)}
        except Exception as ae:
            return {"Status": False, "notification": str(ae)}

    def delete_hnode(self):
        host_name = self.data['host_name']
        try:
            host = HostsGraph.nodes.first_or_none(name=host_name)
            temp=host.service.all()
            for serv in temp:
                serv.delete()
            host.delete()
            return {'Status': True, 'Notification': 'host {} deleted successfully'.format(self.data['host_name'])}
        except HostsGraph.DoesNotExist:
            return {'Status': True, 'Notification': 'host doesnot exist'}
        except Exception as ae:
            return {"Status": False, "Notification": "failed" + str(ae)}

    def get_hnode(self):
        try:
            get_host = HostsGraph.nodes.get(name=self.data['host_name'])
            host_details = {}
            host_details['host_name'] = get_host.name
            host_details['host_ip'] = get_host.ip
            host_details['host_alias'] = get_host.alias
            host_details['type'] = get_host.type
            return {'status': True, 'notification': 'host details-' + host_details}
        except HostsGraph.DoesNotExist:
            return {'status': True, 'notification': 'host -' + get_host.name + 'doesnot exist'}
        except Exception as ae:
            return {"Status": False, "notification": str(ae)}

    def create_snode(self):
        try:
            serv = ServicesGraph.nodes.first_or_none(name=self.data['service_name'])
            if serv:
                return {"Status": False, "Notification": "Service already exists"}
            else:
                serv = ServicesGraph(name=self.data['service_name'], host_name=self.data['host_name'], type=self.data['type'])
                serv.save()
                get_host = HostsGraph.nodes.first(name=self.data['host_name'])
                get_serv = ServicesGraph.nodes.first(name=self.data['service_name'])
                get_serv.host.connect(get_host)
                return {"Status": True, "Notification": "service Node created successfully"}
        except HostsGraph.DoesNotExist:
            temp = ServicesGraph.nodes.first_or_none(name=self.data['service_name'])
            temp.delete()
            return {'status': True, 'notification': 'host {} doesnot exist'.format(self.data['host_name'])}
        except Exception as ae:
            return {"Status": False, "Notification": ae}

    def update_snode(self):
        try:
            get_serv = ServicesGraph.nodes.first_or_none(name=self.data['service_name'])
            if 'newservice_name' in self.data:
                temp=ServicesGraph.nodes.first_or_none(name=self.data['newservice_name'])
                if temp:
                    return {"Status": False, "Notification": "Service already exists"}
                else:
                    get_serv.name = self.data['newservice_name']
            if 'newhost_name' in self.data:
                old_host=get_serv.host_name
                get_host=HostsGraph.nodes.first_or_none(name=old_host)
                get_serv.host.disconnect(get_host)
                new_host_obj=HostsGraph.nodes.first_or_none(name=self.data['newhost_name'])
                get_serv.host.connect(new_host_obj)
                get_serv.host_name = self.data['newhost_name']
            if 'type' in self.data:
                get_serv.type = self.data['type']
            get_serv.save()
            return {'Status': True, 'Notification': 'service updated successfully'}
        except HostsGraph.DoesNotExist:
            return {'Status': True, 'Notification': 'Host doesnot exist'}
        except ServicesGraph.DoesNotExist:
            return {'Status': True, 'Notification': 'Service doesnot exist'}
        except Exception as ae:
            return {"Status": False, "Notification": str(ae)}

    def delete_snode(self):
        try:
            serv = ServicesGraph.nodes.first_or_none(name=self.data['service_name'])
            serv.delete()
            return {'status': True, 'notification': 'deleted successfully'}
        except ServicesGraph.DoesNotExist:
            return {'status': True, 'notification': 'doesnot exist'}
        except Exception as ae:
            return {"Status": False, "notification": str(ae)}

    def get_snode(self):
        try:
            get_serv = ServicesGraph.nodes.first(name=self.data['service_name'])
            serv_details = {}
            serv_details['service_name'] = get_serv.name
            serv_details['host_name'] = get_serv.host_name
            serv_details['type'] = get_serv.type
            return {'status': True, 'notification': serv_details}
        except ServicesGraph.DoesNotExist:
            return {'status': True, 'notification': 'service doesnot exist'}
        except Exception as ae:
            return {"Status": False, "notification": str(ae)}

    def get_hnode(self):
        try:
            get_host = HostsGraph.nodes.first(name=self.data['host_name'])
            host_details = {}
            host_details['host_name'] = get_host.name
            host_details['host_ip'] = get_host.ip
            host_details['host_alias'] = get_host.alias
            host_details['type'] = get_host.type
            return {'status': True, 'notification': host_details}
        except ServicesGraph.DoesNotExist:
            return {'status': True, 'notification': 'host doesnot exist'}
        except Exception as ae:
            return {"Status": False, "notification": str(ae)}

    def all_hnode(self):
        try:
            get_host = HostsGraph.nodes.all()
            all_details = []
            for h in get_host:
                host_details = {}
                host_details['host_name'] = h.name
                host_details['host_ip'] = h.ip
                host_details['host_alias'] = h.alias
                host_details['type'] = h.type
                host_details['id']=h.id
                all_details.append(host_details)
            return {'status': True, 'notification': all_details}
        except HostsGraph.DoesNotExist:
            return {'status': True, 'notification': 'host doesnot exist'}
        except Exception as ae:
            return {"Status": False, "notification": str(ae)}

    def all_snode(self):
        try:
            get_service = ServicesGraph.nodes.all()
            all_details = []
            for x in get_service:
                service_details = {}
                service_details['name'] = x.name
                service_details['host_name'] = x.host_name
                service_details['type'] = x.host_name
                all_details.append(service_details)
            return {'status': True, 'notification': all_details}
        except ServicesGraph.DoesNotExist:
            return {'status': True, 'notification': 'host doesnot exist'}
        except Exception as ae:
            return {"Status": False, "notification": str(ae)}

    def connect_node(self):
        try:
            get_host = HostsGraph.nodes.first(name=self.data['host_name'])
            get_serv = ServicesGraph.nodes.first(name=self.data['service_name'])
            get_serv.host.connect(get_host)
            return {'status': True, 'notification': 'connection created'}
        except HostsGraph.DoesNotExist:
            return {'status': True, 'notification': 'host not found'}
        except ServicesGraph.DoesNotExist:
            return {'status': True, 'notification': 'Service not found'}
        except Exception as ae:
            return {"status": False, "notification": str(ae)}

    def disconnect_node(self):
        con_host = self.data['host_name']
        con_service = self.data['service_name']
        try:
            get_host = HostsGraph.nodes.first(name=con_host)
            get_serv = ServicesGraph.nodes.first(name=con_service)
            if (get_host.service.search(name=con_service)):
                get_serv.host.disconnect(get_host)
                return {'status': True, "notification": "disconnected"}
            else:
                return {'status': True, "notification": "node doesnot exists"}
        except Exception as ae:
            return {"status": False, "notification": str(ae)}

    def connecting_hosts(self):
        first_host = self.data['host1']
        second_host = self.data['host2']
        try:

            get_host_1 = HostsGraph.nodes.first_or_none(name=first_host)
            get_host_2 = HostsGraph.nodes.first_or_none(name=second_host)
            get_host_1.link.connect(get_host_2)
            return {'status': True, "notification": "connected"}
        except Exception as ae:
            return {"status": False, "notification": str(ae)}

    def disconnecting_hosts(self):
        first_host = self.data['host1']
        second_host = self.data['host2']
        try:
            get_host_1 = HostsGraph.nodes.first(name=first_host)
            get_host_2 = HostsGraph.nodes.first(name=second_host)
            if (get_host_1.link.search(name=get_host_2)):
                get_host_1.link.disconnect(get_host_2)
            return {'status': True, "notification": "disconnected"}
        except Exception as ae:
            return {"status": False, "notification": str(ae)}


    def get_all_hnodes_Connections(self):
        try:
            get_host = HostsGraph.nodes.all()
            final_dic = {}
            nodes = []
            links = []
            for host in get_host:
                dic = {}
                dic['id'] = host.id
                dic['name'] = host.name
                dic['ip'] = host.ip
                dic['alias'] = host.alias
                dic['type'] = host.type
                nodes.append(dic)
                for x in host.service.all(): nodes.append(
                    {'id': x.id, 'name': x.name, 'host_name': x.host_name, 'type': x.type}) \
                    , links.append({'source': host.id, 'target': x.id})
            final_dic['nodes'] = nodes
            final_dic['links'] = links
            return final_dic
        except Exception as ae:
            return {"status": False, "notification": str(ae)}




