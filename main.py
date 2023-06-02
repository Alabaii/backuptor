import paramiko
import time
from pprint import pprint
import re
from config import settings


import threading

strdata=''
fulldata=''

class ssh:
    shell = None
    client = None
    transport = None

    def __init__(self, address, username, password):
        print("Connecting to server on ip", str(address) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((address, 22))
        self.transport.connect(username=username, password=password)

        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()

    def close_connection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()

    def open_shell(self):
        self.shell = self.client.invoke_shell()

    def send_shell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")

    def process(self):
        global strdata, fulldata
        while True:
            # Print data when available
            if self.shell is not None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = strdata + str(alldata)
                fulldata = fulldata + str(alldata)
                strdata = self.print_lines(strdata) # print all received data except last line

    def print_lines(self, data):
        last_line = data
        if '\n' in data:
            lines = data.splitlines()
            for i in range(0, len(lines)-1):
                print(lines[i])
            last_line = lines[len(lines) - 1]
            if data.endswith('\n'):
                print(last_line)
                last_line = ''
        return last_line


sshUsername = settings.SSH_USER
sshPassword = settings.SSH_PASS
sshServer = settings.SSH_HOST


connection = ssh(sshServer, sshUsername, sshPassword)
connection.open_shell()
connection.send_shell('cd /var/www')
connection.send_shell('ls -l')
#connection.send_shell('cmd3')
time.sleep(10)
print(strdata)    # print the last line of received data
print('==========================')
print(fulldata)   # This contains the complete data received.
print('==========================')
connection.close_connection()
#print(settings.SSH_HOST,settings.SSH_USER,settings.SSH_PASS,settings.SSH_PORT)