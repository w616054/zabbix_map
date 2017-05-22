# zabbix_map

利用Python的pyzabbix模块，根据hostgroup自动生成maps.（zabbix3.2）
忽略的组： 

```
    no_hg = ('Discovered hosts', \
             'Hypervisors',\
             'Linux servers',\
             'Templates', \
             'Virtual machines', \
             'Zabbix servers'
            )
```

