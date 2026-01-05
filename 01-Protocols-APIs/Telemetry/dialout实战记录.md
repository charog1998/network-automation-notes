选择**EVE-NG**作为实验环境

### 确保网络互通
新建一个**NE40E**设备，并令其桥接到真机的网络上（步骤见《EVE-NG环境搭建》）。

```bash
<NE40E>display ip int br
*down: administratively down
!down: FIB overload down
^down: standby
(l): loopback
(s): spoofing
(d): Dampening Suppressed
(E): E-Trunk down
The number of interface that is UP in Physical is 23
The number of interface that is DOWN in Physical is 0
The number of interface that is UP in Protocol is 13
The number of interface that is DOWN in Protocol is 10

Interface                         IP Address/Mask      Physical   Protocol VPN 
Ethernet1/0/0                     192.168.1.511/24     up         up       --  
...
<NE40E>ping 192.168.1.5
  PING 192.168.1.5: 56  data bytes, press CTRL_C to break
    Reply from 192.168.1.5: bytes=56 Sequence=1 ttl=64 time=19 ms
    Reply from 192.168.1.5: bytes=56 Sequence=2 ttl=64 time=2 ms
    Reply from 192.168.1.5: bytes=56 Sequence=3 ttl=64 time=2 ms
    Reply from 192.168.1.5: bytes=56 Sequence=4 ttl=64 time=1 ms
    Reply from 192.168.1.5: bytes=56 Sequence=5 ttl=64 time=1 ms

  --- 192.168.1.5 ping statistics ---
    5 packet(s) transmitted
    5 packet(s) received
    0.00% packet loss
    round-trip min/avg/max = 1/5/19 ms
```
可以看到设备与真机网络互通。

### 配置设备
首先查看设备上支持的传感器路径：
```bash
[NE40E-telemetry-subscription-Sub1]display telemetry sensor-path
Sample(S) : Serial sample.
Sample(P) : Parallel sample.
------------------------------------------------------------------------------------------------------------------
Type        MinPeriod(ms)  MaxEachPeriod  Path      
------------------------------------------------------------------------------------------------------------------
Event       --             --             huawei-bfd:hwBfdSessDown
Event       --             --             huawei-bfd:hwBfdSessUp
Alarm       --             --             huawei-bgp:BACKWARD
Alarm       --             --             huawei-bgp:ESTABLISHED
Sample(P)   100            20             huawei-debug:debug/debugInfos/debugInfo
Sample(S)   10000          --             huawei-devm:devm/cpuInfos/cpuInfo
Sample(S)   10000          --             huawei-devm:devm/memoryInfos/memoryInfo
Sample(S)   10000          --             huawei-ifm:ifm/interfaces/interface
Sample(P)   100            20             huawei-ifm:ifm/interfaces/interface/ifClearedStat
Sample(S)   10000          --             huawei-ifm:ifm/interfaces/interface/ifDynamicInfo
Sample(P)   100            20             huawei-ifm:ifm/interfaces/interface/ifStatistics
Sample(P)   1000           20             huawei-ifm:ifm/interfaces/interface/ifStatistics/ethPortErrSts
Sample(S)   100            20             huawei-ifm:interfaces/interface
Alarm       --             --             huawei-isiscomm:isisAdjacencyChange
OnChange    --             --             huawei-kpi:kpi/kpiDatas/kpiData
Sample(S)   10000          200            huawei-mac:mac/bdMacTotalNumbers/bdMacTotalNumber
Alarm       --             --             huawei-mpls:Session-Down-MIB
Alarm       --             --             huawei-mpls:Session-Up-MIB
Event       --             --             huawei-mpls:TNLREROUTED
Sample(S)   10000          --             huawei-mpls:mpls/mplsTe/rsvpTeTunnels/rsvpTeTunnel/tunnelPaths/tunnelPath
Alarm       --             --             huawei-ospfv2:ospfNbrStateChange
Alarm       --             --             huawei-ospfv2:ospfVirtNbrStateChange
Alarm       --             --             huawei-ospfv3:ospfv3NbrStateChange
Alarm       --             --             huawei-sem:hwCPUUtilizationResume
Alarm       --             --             huawei-sem:hwCPUUtilizationRisingAlarm
Alarm       --             --             huawei-sem:hwStorageUtilizationResume
Alarm       --             --             huawei-sem:hwStorageUtilizationRisingAlarm
Sample(S)   30000          1050           other paths 
------------------------------------------------------------------------------------------------------------------
note:           
1. Recommended configuration: Sampling period = (Total number of sampling instances) / (Number of sampling instances in each minimum sampling period) * (Minimum sampling period)
2. Sampling tasks are performed one by one. The actual sampling period is the sum of the time consumed by all sampling tasks.
```
接下来配置静态订阅方式：
```bash
[NE40E]telemetry 
# 配置推送目标组
[NE40E-telemetry]destination-group Dest1
[NE40E-telemetry-destination-group-Dest1]ipv4-address 192.168.1.5 port 20000 protocol grpc no-tls 
[NE40E-telemetry-destination-group-Dest1]quit
# 配置传感器组并指定采样路径，我们选择采集CPU信息
[NE40E-telemetry]sensor-group Sensor1
[NE40E-telemetry-sensor-group-Sensor1]sensor-path huawei-devm:devm/cpuInfos/cpuInfo
[NE40E-telemetry-sensor-group-Sensor1]quit
# 创建静态订阅
[NE40E-telemetry]subscription Sub1
[NE40E-telemetry-subscription-Sub1]destination-group Dest1 
[NE40E-telemetry-subscription-Sub1]sensor-group Sensor1 sample-interval 1000
```
查看详细的订阅信息：
```bash
[NE40E]disp telemetry subscription 
---------------------------------------------------------------------------
Sub-name           : Sub1
Sensor group:
----------------------------------------------------
Sensor-name     Sample-interval(ms)  State          
----------------------------------------------------
Sensor1         1000                 RESOLVED       
----------------------------------------------------
Destination group:
----------------------------------------------------------------------
Dest-name   Dest-IP          Dest-port   State        Vpn-name     Protocol   
----------------------------------------------------------------------
Dest1       192.168.1.5      20000       RESOLVED     -            GRPC       
----------------------------------------------------------------------
Sub-state          : PASSIVE 
---------------------------------------------------------------------------

Total subscription number is :  1
```
至此，设备将持续向目标设备推送数据。

### 编译proto文件
新建文件夹`huawei-dialout`，按照如下结构组织文件：
```bash
huawei-dialout/
    ├── protos/
    │   ├── huawei-telemetry.proto    # 从华为官方获取
    │   ├── huawei-devm.proto         # 从华为官方获取 (设备信息模型)
    │   └── huawei-grpc-dialout.proto # 从华为官方获取
    └── run_codegen.py # 下一步创建
```
在文件夹下创建`run_codegen.py`并写入如下内容后运行：
```python
from grpc_tools import protoc

protoc.main(
    (
        '',
        '-I./protos',
        '--python_out=.',
        '--grpc_python_out=.',
        './protos/huawei-grpc-dialout.proto'
    )
)
protoc.main(
    (
        '',
        '-I./protos',
        '--python_out=.',
        '--grpc_python_out=.',
        './protos/huawei-telemetry.proto'
    )
)
protoc.main(
    (
        '',
        '-I./protos',
        '--python_out=.',
        '--grpc_python_out=.',
        './protos/huawei-devm.proto'
    )
)
```
运行后会在当前文件夹生成如下Python文件：
```
├── huawei_devm_pb2.py
├── huawei_devm_pb2_grpc.py
├── huawei_grpc_dialout_pb2.py
├── huawei_grpc_dialout_pb2_grpc.py
├── huawei_telemetry_pb2.py
├── huawei_telemetry_pb2_grpc.py
```

### 编写Python服务端
接下来我们编写一个Python脚本用来接收设备发送来的数据：
```python
from concurrent import futures
import time
import importlib
import grpc
import huawei_grpc_dialout_pb2_grpc
import huawei_telemetry_pb2

_ONE_DAY_IN_SECONDS = 60*60*24

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    huawei_grpc_dialout_pb2_grpc.add_gRPCDataserviceServicer_to_server(TelemetryDataService(),server)
    server.add_insecure_port('192.168.1.5:20000')
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

class TelemetryDataService(huawei_grpc_dialout_pb2_grpc.gRPCDataserviceServicer):
    """
    一个通用的Telemetry数据处理服务。
    通过解析 'proto_path' 动态加载对应的 Protobuf 模块来解码数据。
    """
    def __init__(self):
        return
    
    def dataPublish(self, request_iterator, context):
        """
        处理来自 gRPC 客户端的流式数据。
        """
        for i in request_iterator:
            print('############ New Telemetry Packet ############\n')
            telemetry_data = huawei_telemetry_pb2.Telemetry.FromString(i.data)
            print(telemetry_data)

            for row_data in telemetry_data.data_gpb.row:
                print("------------------ Proto is ------------------")
                print(telemetry_data.proto_path)
                print("----------------------------------------------")
                module_name = telemetry_data.proto_path.split(".")[0]
                root_class = telemetry_data.proto_path.split(".")[1]

                decode_module = importlib.import_module( module_name+"_pb2" )
                print(decode_module)

                decode_func = getattr(decode_module,root_class).FromString

                print("----------------- Content is -----------------\n")
                print(decode_func(row_data.content))
                print("----------- Packet Processing Done -----------")

if __name__ == "__main__":
    serve()
```

### 运行结果
运行服务端，观察输出结果：
```bash
############ New Telemetry Packet ############

node_id_str: "NE40E"
subscription_id_str: "Sub1"
sensor_path: "huawei-devm:devm/cpuInfos/cpuInfo"
collection_id: 1
collection_start_time: 1767600803731
msg_timestamp: 1767600803736
data_gpb {
  row {
    timestamp: 1767600803731
    content: "*\022\n\020\"\0011\010\201\200\204\010(\003\030Z0K\020\010"
  }
  row {
    timestamp: 1767600803731
    content: "*\023\n\021\"\00217\010\201\200\304\010(\003\030Z0K\020\010"
  }
}
collection_end_time: 1767600803731
current_period: 10000
except_desc: "OK"
product_name: "NE40E"
proto_path: "huawei_devm.Devm"

------------------ Proto is ------------------
huawei_devm.Devm
----------------------------------------------
<module 'huawei_devm_pb2' from 'G:\\network-automation-labs\\gRPC-Telemetry\\huawei-dialout\\huawei_devm_pb2.py'>
----------------- Content is -----------------

cpuInfos {
  cpuInfo {
    entIndex: 16842753
    interval: 8
    ovloadThreshold: 90
    position: "1"
    systemCpuUsage: 3
    unovloadThreshold: 75
  }
}

----------- Packet Processing Done -----------
------------------ Proto is ------------------
huawei_devm.Devm
----------------------------------------------
<module 'huawei_devm_pb2' from 'G:\\network-automation-labs\\gRPC-Telemetry\\huawei-dialout\\huawei_devm_pb2.py'>
----------------- Content is -----------------

cpuInfos {
  cpuInfo {
    entIndex: 17891329
    interval: 8
    ovloadThreshold: 90
    position: "17"
    systemCpuUsage: 3
    unovloadThreshold: 75
  }
}

----------- Packet Processing Done -----------
```