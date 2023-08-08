import json
import pickle
import socket
import paramiko
import yaml

def read_server_config():
    with open("config/config.json") as json_file:
        obj = json.load(json_file)
        return obj

def read_xui_config(ip,user_name,private_key_path,remote_file_path):
    port = None
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    mykey = paramiko.RSAKey(filename=private_key_path)
    ssh.connect(ip, username=user_name, pkey=mykey)
    
    sftp = ssh.open_sftp()
    
    remote_file = sftp.file(remote_file_path, 'rb')
    
    obj = json.load(remote_file)
    inbounds = obj["inbounds"]
    for i in inbounds:
        if i["protocol"] == "trojan":
            port = i["port"]
    
    remote_file.close()
    sftp.close()

    ssh.close()
    return port

def get_ip_from_url(url):
    return socket.gethostbyname(url)

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    return data

def write_yaml(file_path,data):
    with open(file_path, 'w' ,encoding="utf-8") as file:
        yaml.dump(data, file,allow_unicode=True)