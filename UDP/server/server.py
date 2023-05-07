from socket import *
import logging

BUFF_SIZE = 2048
FORMAT = "utf-8"
TCP_PORT = 9090
UDP_PORT = 7690
SERVER_NAME = "172.16.99.131"
MSG_SIZE = 6

ACK = "   ACK"
SYN = "   SYN"
SYNACK = "SYNACK"

#Setting up logger
logging.basicConfig(level=logging.DEBUG)

tcp_welcome_sock = socket(AF_INET, SOCK_STREAM)
udp_welcome_sock = socket(AF_INET, SOCK_DGRAM)

tcp_welcome_sock.bind(("",TCP_PORT))
udp_welcome_sock.bind(("",UDP_PORT))

tcp_welcome_sock.listen(1)

while True:

        tcp_connection, tcp_addr = tcp_welcome_sock.accept()
        tcp_msg = tcp_connection.recv(BUFF_SIZE).decode(FORMAT)
        tcp_msg_head = tcp_msg[:MSG_SIZE]
        
        if tcp_msg_head == SYN:
            tcp_connection.sendall(bytes(SYNACK,FORMAT))
        
        elif tcp_msg_head == ACK:
            
            message, clientAddress = udp_welcome_sock.recvfrom(BUFF_SIZE)
            
        