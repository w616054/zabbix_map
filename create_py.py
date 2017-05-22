#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wangliang
# zabbix server: 3.2
#

from pyzabbix import ZabbixAPI, ZabbixAPIException
import json,sys


def get_hostgroup(zapi):
  try:
    re=zapi.hostgroup.get(
        output="extend",
    )

    no_hg = ('Discovered hosts', \
             'Hypervisors',\
             'Linux servers',\
             'Templates', \
             'Virtual machines', \
             'Zabbix servers'
            )
    hg_dict = {} # name:groupid
    for hg in re:
      if hg['name'] not in no_hg:
        hg_dict[hg['name']] = hg['groupid']

    return hg_dict
  except ZabbixAPIException as e:
    print(e)
    sys.exit()


def get_host_by_groupid(zapi, groupid):
  try:
    re = zapi.host.get(
        output="extend",
        groupids=groupid,
    )

    return re  # list
  except ZabbixAPIException as e:
    print(e)
    sys.exit()


def get_map(zapi):
  try:
    re=zapi.map.get(
          output="extend",
#          selectSelements="extend",
#          selectLinks="extend",
#          selectUsers="extend",
#          selectUserGroups="extend",
    )

    return re
  except ZabbixAPIException as e:
    print(e)
    sys.exit()


def host_map_json(zapi, hostid_list):
  try:
    re_list = [
      {
        "elementid": "0",
        "selementid": "200",
        "elementtype": "4",
        "iconid_off": "156",
        "use_iconmap": "0",
        "x": "200",
        "y": "250",
        "width": "200",
        "height": "200",
        "label": "Switch",
        "viewtype": "0",
        "iconid_disabled": "0",
        "sysmapid": "3",
        "application": "",
        "iconid_maintenance": "0",
        "iconid_on": "0"
      }
    ]

    x = 0
    y = 50
    s_id = 0
    for hostid in hostid_list:
      x = x + 150
      s_id = s_id + 1
      one_json = {
        "elementid": hostid, # host/group id
        "selementid": s_id, # 1,2,3,4,5
        "elementtype": "0",
        "iconid_off": "150", # icon image
        "use_iconmap": "0", # Whether icon mapping must be used for host elements. 
        "x": x,
        "y": y
      }
      re_list.append(one_json)

    return re_list
  except ZabbixAPIException as e:
    print(e)
    sys.exit()


def create_host_map_a_group(zapi, groupname, groupid):
  hostid_list = []
  h_list = get_host_by_groupid(zapi, groupid)
  for one in h_list:
    hostid_list.append(one['hostid'])

  tmp_dict={"selementid1": 1, "selementid2": 200, "color": "00CC00"}
  links_list=[]
  for num in range(len(hostid_list)):
    tmp_dict["selementid1"] = num + 1
    links_list.append(json.dumps(tmp_dict))

  for n in range(len(links_list)):
    links_list[n] = json.loads(links_list[n])
 
  try:
    zapi.map.create(
        name=groupname,
        width=1500,
        height=600,
        selements=host_map_json(zapi, hostid_list),
        links=links_list
    )
  except ZabbixAPIException as e:
    print(e)
    sys.exit()



def get_map_id(zapi):
  maps = get_map(zapi)
  map_dict={}
  for one in maps:
    map_dict[one['name']] = one['sysmapid']

  return map_dict


def global_map_json(zapi):
  map_dict = get_map_id(zapi)

  s_id = 0
  x = 20
  y = 100
  re_list = [
      {
        "elementid": "0",
        "selementid": "200",
        "elementtype": "4",
        "iconid_off": "156",
        "use_iconmap": "0",
        "x": "400",
        "y": "300",
        "width": "200",
        "height": "200",
        "label": "Switch",
        "viewtype": "0",
        "iconid_disabled": "0",
        "sysmapid": "3",
        "application": "",
        "iconid_maintenance": "0",
        "iconid_on": "0"
      }
  ]
  for one in map_dict.items():
    s_id = s_id + 1
    x = x + 100
    tmp_json = {
          "elementid": one[1], # host/group id
          "selementid": s_id, # 1,2,3,45
          "elementtype": "1",
          "iconid_off": "150", # icon image
          "use_iconmap": "0", # Whether icon mapping must be used for host elements. 
          "x": x,
          "y": y
    }
    re_list.append(tmp_json)

  return re_list


def create_global_map(zapi, name):
  map_dict = get_map_id(zapi)


  tmp_dict={"selementid1": 1, "selementid2": 200, "color": "00CC00"}
  links_list=[]
  for num in range(len(map_dict.items())):
    tmp_dict["selementid1"] = num + 1
    links_list.append(json.dumps(tmp_dict))

  for n in range(len(links_list)):
    links_list[n] = json.loads(links_list[n])

  try:
     zapi.map.create(
        name=name,
        width=1500,
        height=600,
        selements=global_map_json(zapi),
        links=links_list
     )
  except ZabbixAPIException as e:
    print(e)
    sys.exit()


def main():
  zapi = ZabbixAPI("http://127.0.0.1/zabbix")
  zapi.login("admin", "zabbix")

  hg_dict =  get_hostgroup(zapi)
  for one in hg_dict.items():
    create_host_map_a_group(zapi, one[0], one[1])

  create_global_map(zapi, 'Overview')


if __name__ == "__main__": 
  main()
