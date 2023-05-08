from socket import *
import logging
import os
import hashlib

BUFF_SIZE = 2048
FORMAT = "utf-8"
TCP_PORT = 56777
UDP_PORT = 8888
SERVER_NAME = "172.16.100.115"
MSG_SIZE = 6

ACK = "   ACK"
SYN = "   SYN"
SYNACK = "SYNACK"
REQ = "   REQ"
OK = "    OK"
NO = "    NO"
MORE = "  DATA"
CORRUPT = "CORRUP"
EOF = "   EOF"
TIMEOUT = "TIMOUT"

#Setting up logger
logging.basicConfig(level=logging.DEBUG)

tcp_welcome_sock = socket(AF_INET, SOCK_STREAM)
udp_welcome_sock = socket(AF_INET, SOCK_DGRAM)

tcp_welcome_sock.bind(("",TCP_PORT))
udp_welcome_sock.bind(("",UDP_PORT))

tcp_welcome_sock.listen(1)
logging.info("TCP SERVER IS UP AND LISTENING AT PORT " + str(TCP_PORT))

while True:
        
    tcp_connection, tcp_addr = tcp_welcome_sock.accept()
    logging.info("TCP CONNECTION WITH CLIENT AT " + str(tcp_addr) + " ESTABLISHED")
    tcp_msg = tcp_connection.recv(BUFF_SIZE).decode(FORMAT)
    logging.info("SERVER TCP SOCKET RECEIVED SEGMENT FROM CLIENT")
    tcp_msg_head = tcp_msg[:MSG_SIZE]
    tcp_msg_data = tcp_msg[MSG_SIZE:]

    print(tcp_msg_head)

    if tcp_msg_head == REQ:
        file_name_query = tcp_msg_data
        logging.info("Client is requesting a file: " + file_name_query)

        try:
            path = '/Users/mollerup/Desktop/github repos/networks_FTP_project/TCP/server/'
            with open(path + file_name_query,'r') as file:
                file_size = os.stat(path + file_name_query).st_size
                file_as_string = file.read()

            response = OK + str(file_size)
            tcp_connection.send(bytes(response, FORMAT))
            logging.info("SENDING " + file_name_query + " TO CLIENT " + "(" + str(file_size) + ")")

            ## Getting client address from UDP test packet

            udp_msg, clientAddress = udp_welcome_sock.recvfrom(BUFF_SIZE)

            file_bytes = bytes(file_as_string,"utf-8")
            file_hash = hashlib.md5(file_bytes).digest()

            while file_bytes:

                status = MORE

                status_bytes = bytes(status,"utf-8")

                #message = bytearray(status_bytes)
                #message = message.append(file_hash)

                message = status_bytes + file_hash

                tcp_connection.sendall(message)
                udp_welcome_sock.sendto(file_bytes, clientAddress)

                response = tcp_connection.recv(BUFF_SIZE)
                response_head = response[:MSG_SIZE].decode("utf-8")

                if response_head == ACK:
                    pass

                elif response_head == CORRUPT:
                    udp_welcome_sock.sendto(file_bytes, clientAddress)

                elif response_head == TIMEOUT:
                    tcp_connection.close()
                    break

            
            status = EOF
            tcp_connection.send((status,"utf-8"))


        except FileNotFoundError:
            response = NO
            tcp_connection.sendall(bytes(response, FORMAT))
            logging.info("FILE NOT FOUND, CLIENT NOTIFIED")

        logging.info("SERVER IS UP AND LISTENING AT PORT " + str(TCP_PORT) + " ...")     
            
        