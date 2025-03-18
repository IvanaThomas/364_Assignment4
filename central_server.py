import socket
import threading

peers = {}

def recv_message(connection, addr):
    
    received_packet = connection.recv(5120)
    print("Received message")
    decoded_packet = received_packet.decode().strip()
    decoded_packet = decoded_packet.replace("[", "")
    decoded_packet = decoded_packet.replace("]", "")
    decoded_packet = decoded_packet.replace("\"", "")
    decoded_packet = decoded_packet.replace("'","")

    packet = decoded_packet.split(",")
    command = packet[0]
    print(packet)
    print(command)
    match command: 
        case 'j':
            peers[packet[1]] = packet[2]
            print(f"Connected: Peer id {packet[1]}, address: {packet[2]}{packet[3]}")
        
        case 'l':
            connection.sendall(str(peers).encode())


def start_server():
    central_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    central_soc.bind(('127.0.0.1', 8010))
    central_soc.listen()

    while True:
        conn, addr = central_soc.accept()
        threading.Thread(target=recv_message, args=(conn, addr)).start()


#main----------------------------------------
start_server()