选择**EVE-NG**作为实验环境

### 确保网络互通
新增**NE40E**设备，并将其桥接到物理机的网络上（见[《EVE-NG环境搭建》](../../00-Getting-Started/EVE-NG环境搭建.md)）。

执行设备接口状态查询命令，确认物理及协议层面的接口状态：
```bash
<NE40E>display ip int br
...
Interface                         IP Address/Mask      Physical   Protocol VPN 
Ethernet1/0/0                     192.168.1.511/24     up         up       --  
...
```
通过 ping 命令验证设备与物理机（IP：`192.168.1.5`）的网络连通性，结果显示数据包无丢失，网络互通正常：
```bash
<NE40E>ping 192.168.1.5
  PING 192.168.1.5: 56  data bytes, press CTRL_C to break
    Reply from 192.168.1.5: bytes=56 Sequence=1 ttl=64 time=19 ms
    ...
    Reply from 192.168.1.5: bytes=56 Sequence=5 ttl=64 time=1 ms

  --- 192.168.1.5 ping statistics ---
    5 packet(s) transmitted
    5 packet(s) received
    0.00% packet loss
    round-trip min/avg/max = 1/5/19 ms
```

### 配置设备
首先查看设备上支持的传感器路径及相关参数（采样类型、周期等）：
```bash
[NE40E]display telemetry sensor-path
Sample(S) : Serial sample.
Sample(P) : Parallel sample.
------------------------------------------------------------------------------------------------------------------
Type        MinPeriod(ms)  MaxEachPeriod  Path      
------------------------------------------------------------------------------------------------------------------
...
Sample(S)   10000          --             huawei-devm:devm/cpuInfos/cpuInfo
Sample(S)   10000          --             huawei-devm:devm/memoryInfos/memoryInfo
Sample(S)   10000          --             huawei-ifm:ifm/interfaces/interface
...
------------------------------------------------------------------------------------------------------------------
note:           
1. Recommended configuration: Sampling period = (Total number of sampling instances) / (Number of sampling instances in each minimum sampling period) * (Minimum sampling period)
2. Sampling tasks are performed one by one. The actual sampling period is the sum of the time consumed by all sampling tasks.
```
接下来配置静态订阅方式：
```bash
[NE40E]telemetry 
# 配置数据推送目标组（指定接收端 IP：192.168.1.5，端口：20000，采用无 TLS 的 gRPC 协议）
[NE40E-telemetry]destination-group Dest1
[NE40E-telemetry-destination-group-Dest1]ipv4-address 192.168.1.5 port 20000 protocol grpc no-tls 
[NE40E-telemetry-destination-group-Dest1]quit
# 配置传感器组并指定采样路径，可根据上一步查询到的路径填写，本例中选择采集 CPU 信息
[NE40E-telemetry]sensor-group Sensor1
[NE40E-telemetry-sensor-group-Sensor1]sensor-path huawei-devm:devm/cpuInfos/cpuInfo
[NE40E-telemetry-sensor-group-Sensor1]quit
# 创建静态订阅，关联目标组与传感器组并设置采样间隔
[NE40E-telemetry]subscription Sub1
[NE40E-telemetry-subscription-Sub1]destination-group Dest1 
[NE40E-telemetry-subscription-Sub1]sensor-group Sensor1 sample-interval 1000
```
执行命令查看订阅详情，确认传感器组、目标组状态均为 `RESOLVED`，订阅状态正常：
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
配置完成后，设备将按设定周期向目标地址持续推送 CPU 信息数据。

### 编译proto文件
通过 **pip** 安装 **gRPC核心库** 和工具库：
```bash
pip install grpcio grpcio-tools
```

新建`huawei-dialout`文件夹作为我们的实验文件夹，按照如下结构组织文件（proto文件需从华为官方获取）：
```bash
huawei-dialout/
    ├── protos/
    │   ├── huawei-telemetry.proto    # 遥测基础协议定义
    │   ├── huawei-devm.proto         # 设备信息模型定义
    │   └── huawei-grpc-dialout.proto # gRPC-Dialout模式协议定义
    └── run_codegen.py # 编译脚本
```
创建`run_codegen.py`脚本，通过`grpc_tools.protoc`工具编译 proto 文件，生成 Python 语言的 gRPC 和 Protobuf 绑定代码：
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
运行脚本后，会在当前文件夹生成如下文件：
```
├── huawei_devm_pb2.py
├── huawei_devm_pb2_grpc.py
├── huawei_grpc_dialout_pb2.py
├── huawei_grpc_dialout_pb2_grpc.py
├── huawei_telemetry_pb2.py
├── huawei_telemetry_pb2_grpc.py
```

也可以用如下命令进行编译：
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./protos/huawei-grpc-dialout.proto ./protos/huawei-telemetry.proto ./protos/huawei-devm.proto 
```

### 编写Python服务端
编写 Python 脚本作为 gRPC 服务端，用于接收并解析设备推送的 Telemetry 数据：
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
启动服务端后，可观察到设备推送的 CPU 信息数据，输出内容包含：
- 遥测数据包基本信息（设备标识、订阅 ID、传感器路径、时间戳等）
- 解码后的 CPU 详细数据（如位置、系统 CPU 使用率、阈值等）

示例输出片段展示了两个 CPU 核心的监控数据，验证了数据采集与解析流程的正确性：
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