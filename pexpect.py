import pexpect

PROMPT = '#'
IPs = ['172.31.101.4', '172.31.101.5', '172.31.101.6']
USERNAME = 'admin'   
PASSWORD = 'cisco'

for i in range(1, 4):
    child = pexpect.spawn('telnet ' + IPs[i - 1])
    child.expect('Username')
    child.sendline(USERNAME)
    child.expect('Password')
    child.sendline(PASSWORD)
    child.expect(PROMPT)
    child.sendline('configure terminal')
    child.expect(PROMPT)
    child.sendline('interface loopback 0')
    child.expect(PROMPT)
    child.sendline(f'ip address {i}.{i}.{i}.{i} 255.255.255.255')
    child.expect(PROMPT)
    child.sendline('exit')
    print(f'configure loopback 0 on R{i} completed.')
print("All done!!!")