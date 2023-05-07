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

clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.sendto(bytes(message,"utf-8"), (SERVER_NAME, UDP_PORT))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
modifiedMessage = modifiedMessage.decode("utf-8")

