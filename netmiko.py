from netmiko import ConnectHandler

def get_data_from_device(device_params):
    with ConnectHandler(**device_params) as ssh:
        result_shipinbt = ssh.send_command('sh ip int br')
        result_shintdes = ssh.send_command('sh int descr')
        result_shiproutemanage = ssh.send_command('sh ip route vrf management | include ^C')
        result_shiproutecontrol = ssh.send_command('sh ip route vrf control-data | include ^C')
        result_shcdpnei = ssh.send_command('sh cdp nei')
        allinfo = result_shipinbt, result_shintdes, result_shiproutemanage, result_shiproutecontrol,result_shcdpnei
        return allinfo

def get_ip(device_params, intf):
    data = get_data_from_device(device_params)
    result = data[0].strip().split('\n')
    for line in result[1:]:
        words = line.strip().split()
        if words[0][0] == intf[0] and words[0][-3:] == intf[-3:]:
            return words[1]
        
def get_subnet(device_params, intf):
    data = get_data_from_device(device_params)
    result = data[2].strip().split('\n')
    result1 = data[3].strip().split('\n')

    for line in result[1:]:
        words = line.strip()
        if intf[0] in words and words[-3:] == intf[-3:]:
            return words[(words.find('/')):(words.find('is'))].strip()
    for line in result1[1:]:
        words = line.strip()
        if intf[0] in words and words[-3:] == intf[-3:]:
            return words[(words.find('/')):(words.find('is'))].strip()
        
def get_des(device_params, intf):
    data = get_data_from_device(device_params)
    result = data[1].strip().split('\n')

    for line in result[1:]:
        line = line.replace('admin down', "admindown")
        words = line.split()
        if intf[0] in words[0] and intf[-3:] in words[0]:
            return ' '.join([str(elem) for i,elem in enumerate(words[3:])])
        
def get_status(device_params, intf):
    data = get_data_from_device(device_params)
    result = data[1].strip().split('\n')
    for line in result[1:]:
        words = line.split()
        if words[0][0] == intf[0] and words[0][-3:] == intf[-3:]:
            if intf[0] in words[0] and words[1] == 'admin':
                return 'admin down'
            if intf[0] in words[0] and words[1] == 'down':
                return 'down'
            if intf[0] in words[0] and words[1] == 'up':
                return 'up'
        
def set_des(device_params):
    data = get_data_from_device(device_params)
    result = data[1].strip().split('\n')
    command = []
    for i in result[1:]:
        i = i.replace('admin down', 'admindown')
        command.append(i.split())
    for k in data[4].split('\n')[5:-2]:
        k = k.split()
        count = 0
        for info in command:
            if k[1][:2] in info[0] and k[2] in info[0]:
                command[count].append(k[1][:2]+k[2])
                command[count].append(k[0][:k[0].find(".")])
            count += 1

    use_command = []
    for i in command:

        inf = "int " +  i[0]
        des = "descript "
        if device_params["ip"] == "?????" ????? and i[0] == "Gi0/2":
            des += "Connect to WAN"
            use_command.append(inf)
            use_command.append(des)
            continue
        if "/" in i[-2]:
            des += "Connect to " + i[-2] + " of " + i[-1]
        elif i[1] == 'down':
            des += "Not use down"
        elif i[1] == 'admindown':
            des += "Not use admin down"
        elif "Lo" in i[0]:
            des += "This is loopback"

        use_command.append(inf)
        use_command.append(des)
        use_command.append("do wr")
    with ConnectHandler(**device_params) as ssh:
        config = ssh.send_config_set(use_command)
        print(config)

        
if __name__ == '__main__':
    device_ip = '??????' ?????
    username = 'admin'
    password = 'cisco'

    device_params = {
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'username': username,
        'password': password
    }
    set_des(device_params)
    print(get_des(device_params, 'G0/0'))
    print(get_des(device_params, 'G0/1'))
    print(get_des(device_params, 'G0/2'))
    print(get_des(device_params, 'G0/3'))
#no do wr
#upload to git first