from netmiko import ConnectHandler

for no in range(4, 6):
    device = {
        "device_type": "hp_comware_telnet",
        "host": "127.0.0.1",
        "username": "",
        "password": "",
        "port": str(30000 + no), # HCL里面的设备的telnet地址都是127.0.0.1，端口就是30001往后排
    }
    print(f"连接{device["host"]}:{device["port"]}")
    conn = ConnectHandler(**device)
    config_set = [
        "sysname R" + str(no),
        "int loopback 0",
        f"ip addr 10.0.{no}.{no} 24",
        f"ospf 1 router-id 10.0.{no}.{no}",
        "save force"
    ]
    conn.send_config_set(config_set)
    # conn.save_config()
    # conn.send_config_set("save f")

    print(f"{device["host"]}:{device["port"]}操作完成")
    conn.disconnect()

