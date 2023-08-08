import json

import utils.read_x_ui as util

def start():
    ports = dict()
    
    # 读配置文件
    configs = util.read_server_config()
    
    # 根据配置文件内容读取port
    for i in configs:
        i["ip"] = util.get_ip_from_url(i["url"])
        ports[i["url"]]=util.read_xui_config(i["ip"],i["user_name"],i["private_key_path"],i["remote_file_path"])
    
    # 根据ports写回clash的配置文件
    if(ports):
        with open("config/yaml_path.json") as path_file:
            path_obj = json.load(path_file)
        final_path = path_obj["path"]
        data = util.read_yaml(final_path)
        for i in data["proxies"]:
            server = i["server"]
            if ports.get(server) is not None:
                i["port"] = ports[server]
        util.write_yaml(final_path,data=data)

if __name__ == "__main__":
    start()