import time
import paramiko

username = 'admin'
password = 'cisco'

device_ip = [""]
for ip in device_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username='admin', password='cisco', key_filename='')

    print("Connecting to {}...".format(ip))
    commands = ["sh ip int bri"]
    with client.invoke_shell() as ssh:
        print("Connecting to {}...".format(ip))
        # ssh.send("terminal lenghth 0\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("sh ip int br\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)