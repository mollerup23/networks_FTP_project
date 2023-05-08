from socket import *
import logging
import hashlib

BUFF_SIZE = 2048
FORMAT = "utf-8"
TCP_PORT = 56777
UDP_PORT = 8888
SERVER_NAME = "172.16.100.115"
MSG_SIZE = 6

REQUEST = "   REQ"
ACK = "   ACK"
SYN = "   SYN"
SYNACK = "SYNACK"
OK = "    OK"
NO = "    NO"
MORE = "  DATA"
CORRUPT = "CORRUP"
TIMEOUT = "TIMOUT"

def recvall(sock):
    data = ""
    while True:
        part = sock.recv(BUFF_SIZE).decode(FORMAT)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data

#Setting up logger
logging.basicConfig(level=logging.DEBUG)

tcp_client_socket = socket(AF_INET, SOCK_STREAM)
udp_client_socket = socket(AF_INET, SOCK_DGRAM)

tcp_client_socket.connect((SERVER_NAME,TCP_PORT))
logging.info("CLIENT CONNECTED WITH SERVER AT " + SERVER_NAME + " AT PORT " + str(SERVER_NAME))

file_name_query = input("Enter the name of the file ... ")
logging.info("REQUEST FOR FILE " + file_name_query + " SENT TO SERVER")
tcp_client_socket.send(bytes(REQUEST + file_name_query,FORMAT))

response = tcp_client_socket.recv(BUFF_SIZE).decode(FORMAT)
logging.info("RECEIVED RESPONSE FROM SERVER")
tcp_msg_head = response[:MSG_SIZE]
tcp_msg_data = response[MSG_SIZE:]

print(tcp_msg_head)
print(tcp_msg_data)

if tcp_msg_head == OK:
    logging.info("SERVER HAS " + file_name_query + " (" + tcp_msg_data + ")")
    
    ## Initializing UDP data transfer
    #tcp_client_socket.send(bytes(SYN,FORMAT))

    input_string = ""

    udp_client_socket.sendto(bytes(SYN,FORMAT), (SERVER_NAME, UDP_PORT))
    status = MORE

    timeouts = 0
    while status == MORE:

        tcp_response = tcp_client_socket.recv(BUFF_SIZE)
        status = tcp_response[:MSG_SIZE].decode("utf-8")
        server_hash = tcp_response[MSG_SIZE:]

        try:
            input_bytes, serverAddr = udp_client_socket.recvfrom(BUFF_SIZE)
            logging.info("RECEIVING UDP DATAGRAMS FROM SERVER")
            udp_client_socket.settimeout(3)
            logging.info("TIME OUT COUNTER STARTED")
            timeouts = 0
            input_hash = hashlib.md5(input_bytes).digest()
        except: 
            timeout("TIME OUT")
            timeouts = timeouts + 1
            if timeouts >= 3:
                msg = TIMEOUT
                noise = recvall(tcp_client_socket)
                tcp_client_socket.send(bytes(msg,"utf-8"))
                response = tcp_client_socket.recv(BUFF_SIZE).decode("utf-8")
                response_head = response[:MSG_SIZE]

                if response_head == OK:
                    tcp_client_socket.close()
                    break       

        if input_hash == server_hash:
            logging.info("HASHES MATCH")
            input_string = input_string + input_bytes.decode("utf-8")
            response = ACK
            tcp_client_socket.send(bytes(response,"utf-8"))
        
        else:
            logging.info("HASHES DON'T MATCH")
            status = CORRUPT
            tcp_client_socket.send(bytes(status,"utf-8"))
            logging.info("SENDING SERVER PACKET CORRUPTED MSG")

            
            

elif tcp_msg_head == NO:
    logging.info("SERVER DOES NOT HAVE " + file_name_query)

