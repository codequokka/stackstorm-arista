# An example integration pack for StackStrom

## Install
```
$ git clone <this_repo_url> /opt/stackstorm/packs/arista
$ st2 pack install file:///opt/stackstorm/packs/arista
```

## Actions
```
$ st2 action list -p arista
+-------------------------+--------+--------------------------------------+
| ref                     | pack   | description                          |
+-------------------------+--------+--------------------------------------+
| arista.check_login      | arista | Check login by using telnet          |
| arista.execute_commands | arista | Execute commands vie eAPI            |
| arista.search_logs      | arista | Search logs from show logging result |
+-------------------------+--------+--------------------------------------+
```

- arista.check_login
```
$ st2 run arista.check_login hostname=192.168.1.238 port=10123 user=admin password=arista
.
id: 63b368fc018a290992abcee9
action.ref: arista.check_login
context.user: st2admin
parameters:
  hostname: 192.168.1.238
  password: '********'
  port: 10123
  user: admin
status: succeeded
start_timestamp: Mon, 02 Jan 2023 23:30:04 UTC
end_timestamp: Mon, 02 Jan 2023 23:30:05 UTC
result:
  exit_code: 0
  result: Login succeeded
  stderr: ''
  stdout: ''
```

- arista.execute_commands
```
$ st2 run arista.execute_commands hostname=192.168.1.238 port=10443 user=admin password=arista commands="show version, show clock"
.
id: 63b38187018a290992abcf0d
action.ref: arista.execute_commands
context.user: st2admin
parameters:
  commands:
  - show version
  - show clock
  hostname: 192.168.1.238
  password: '********'
  port: 10443
  user: admin
status: succeeded
start_timestamp: Tue, 03 Jan 2023 01:14:47 UTC
end_timestamp: Tue, 03 Jan 2023 01:14:47 UTC
result:
  exit_code: 0
  result:
  - architecture: x86_64
    bootupTimestamp: 1672700253.236861
    cEosToolsVersion: '1.1'
    configMacAddress: 00:00:00:00:00:00
    hardwareRevision: ''
    hwMacAddress: 00:00:00:00:00:00
    imageFormatVersion: '1.0'
    imageOptimization: None
    internalBuildId: b32bd8f9-3baf-4332-8f58-45e1afe2f695
    internalVersion: 4.29.0.2F-29226602.42902F
    isIntlVersion: false
    kernelVersion: 4.18.0-425.3.1.el8.x86_64
    memFree: 9810584
    memTotal: 16207132
    mfgName: Arista
    modelName: cEOSLab
    serialNumber: 8D8FBE0646992FAABD041F22509E6852
    systemMacAddress: 02:42:ac:11:3e:b8
    uptime: 8234.66374373436
    version: 4.29.0.2F-29226602.42902F (engineering build)
  - clockSource:
      local: true
    localTime:
      dayOfMonth: 3
      dayOfWeek: 1
      dayOfYear: 3
      daylightSavingsAdjust: 0
      hour: 10
      min: 14
      month: 1
      sec: 47
      year: 2023
    timezone: Asia/Tokyo
    utcTime: 1672708487.9017143
  stderr: ''
  stdout: ''
```

- arista.search_logs
```
$ st2 run arista.search_logs hostname=192.168.1.238 port=10443 user=admin password=arista filter_string="%LINEPROTO-5-UPDOWN"
.
id: 63b389d7018a290992abcf25
action.ref: arista.search_logs
context.user: st2admin
parameters:
  filter_string: '%LINEPROTO-5-UPDOWN'
  hostname: 192.168.1.238
  password: '********'
  port: 10443
  user: admin
status: succeeded
start_timestamp: Tue, 03 Jan 2023 01:50:15 UTC
end_timestamp: Tue, 03 Jan 2023 01:50:15 UTC
result:
  exit_code: 0
  result:
  - datetime: '2023-01-03T10:48:03+09:00'
    fqdn: cEOS-1
    message: 'Ebra: %LINEPROTO-5-UPDOWN: Line protocol on Interface Ethernet1, changed state to down'
  stderr: ''
  stdout: ''
```
