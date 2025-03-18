import socket
import sys
from threading import Thread
import time

#create the socket
def create_socket(host, port):
    # 1. Create a socket.
    # 2. Try connecting the socket to the host and port.
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP
        #soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse port
        soc.connect((host, port))
    except Exception as e:
        print(e)
        print("Connection Error to", port)
        sys.exit()
    # 3. Return the connected socket.
    return soc

#register to the central server
def register_peer():
    soc1 = create_socket('127.0.0.1', 8010)
    packet = ['j', 1004, ('127.0.0.1', 8004)]
    soc1.sendall(str(packet).encode())

#send an offer messages and receive -------- every 30s --------------
def send_offer(connection, files):
    peer_id = 1000
    packet = ['o', peer_id]
    for item in files:
        packet.append(item)
    
    connection.sendall(packet)

def send_file(connection, addr, file_rq):
    with open(file_rq, "rb") as file:
            while chunk := file.read(5120):
                connection.sendall(chunk)
        
    connection.sendall(b"EOF") 

def send_ack(connection, addr):
    packet = ['a']
    connection.sendall(packet)


def receive_message(connection, addr):
    received_packet = connection.recv(5120)
    decoded_packet = received_packet.decode().strip()
    decoded_packet = decoded_packet.replace("[", "")
    decoded_packet = decoded_packet.replace("]", "")

    print(decoded_packet)
    packet = decoded_packet.split(",")
    command = packet[0]
    match command:
        case 'o':
            peer_id = packet[1]
            for item in packet[2:]:
                if item not in peer_files:
                    files_to_request[item] = addr
        
        case 'r':
            print("request")
            file_requested = packet[1]
            send_file(connection, addr, file_requested)
        
        case 't':
            print("transfer")
            while True:
                data = connection.recv(5120)  
                send_ack(connection, addr)
                if not data:
                    break  
                print(data.decode())

        case 'a':
            print('ack')


#start threading -> to be able to listen to multiple peers at once
def processing_thread(connection, addr):

    # 2. Continuously process incoming packets
    while True:
        recv_packet = connection.receive_message(connection, addr)  

    soc1.close()
    soc2.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print('server started')


    while True:
        conn, addr = server_socket.accept()
        print(f"New connection from {addr}")
        Thread(target=receive_message, args=(conn,addr)).start()
        time.sleep(10)
        conn.send_offer(conn, peer_files)


#first things first -> register with the central register. 

#main ->
register_peer()
peer_files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']
peer_id = 1004
#gonna store this as file: address
files_to_request = {}

start_server('127.0.0.1', 8004)
