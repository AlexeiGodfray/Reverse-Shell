import socket 
import sys

# create socket (allows two computers to conncect)
def socket_create():
    try:
        global host 
        global port 
        global s 
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Sockt creation error: " + str(msg))

#Bind socket to port and wait for onnection from client 
def socket_bind():
    try:
        global host 
        global port 
        global s 
        print("Binding socket to port: " + str(port))
        s.bind((host,port))
        #allows server to accecpt coonection (5 tries before refeusing)
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying")
        socket_bind()


#Establish a connection with client (socket must be listening for them)
def socket_accept():
    conn, address = s.accept()
    print("Connection has been established | " + " IP " + address[0] + " | Port " + str(address[1]))
    send_commands(conn)
    conn.close()
