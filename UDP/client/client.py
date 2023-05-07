from socket import *
import logging

BUFF_SIZE = 2048
FORMAT = "utf-8"
TCP_PORT = 9090
UDP_PORT = 7690
SERVER_NAME = "172.16.99.131"
MSG_SIZE = 6

REQUEST = "   REQ"
ACK = "   ACK"
SYN = "   SYN"
SYNACK = "SYNACK"
FILE_NOT_FOUND = "   FNF"
FILE_FOUND = "    FF"
#Setting up logger
logging.basicConfig(level=logging.DEBUG)

tcp_client_socket = socket(AF_INET, SOCK_STREAM)
udp_client_socket = socket(AF_INET, SOCK_DGRAM)




tcp_client_socket.connect((SERVER_NAME,TCP_PORT))
logging.info("CLIENT CONNECTED WITH SERVER AT " + SERVER_NAME + " AT PORT " + str(SERVER_NAME))

file_name_query = input("Enter the name of the file ... ")
tcp_client_socket.send(bytes(REQUEST + file_name_query,FORMAT))
logging.info("REQUEST FOR FILE " + file_name_query + " SENT TO SERVER")

resp_str = tcp_client_socket.recv(BUFF_SIZE).decode(FORMAT)

if resp_str[:MSG_SIZE] == FILE_FOUND:
    logging.info("FILE RECIEVED FROM SERVER ... ")
    
    ## Initializing UDP data transfer
    tcp_client_socket.send(bytes(SYN,FORMAT))
    udp_client_socket.sendto(bytes(SYN,FORMAT), (SERVER_NAME, UDP_PORT))

    try:
        udp_client_socket.settimeout(3)
        udp_client_socket.recvfrom(BUFF_SIZE)
    except: timeout("TIMED OUT")
  







elif resp_str[:MSG_SIZE] == FILE_NOT_FOUND:
    logging.info("FILE NOT FOUND")





modifiedMessage, serverAddress = udp_welcome_sock.recvfrom(BUFF_SIZE)
modifiedMessage = modifiedMessage.decode("utf-8")

