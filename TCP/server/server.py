
"""TCP_FTP_SERVER.py
NAME Philip mOLLERUS
DATE May 7 2023
This module will act a
FTP server
"""


from socket import *
import logging

SERVER_PORT = 9090
BUFF_SIZE = 1024
MSG_SIZE = 3
FORMAT = "utf-8"

## MAGIC NUMBERS
REQUEST_CODE = "200"
FILE_FOUND_CODE = "506"
FILE_NOT_FOUND_CODE = "404"

logging.basicConfig(level=logging.DEBUG)

welcome_sock = socket(AF_INET, SOCK_STREAM)
welcome_sock.bind(("",SERVER_PORT))

welcome_sock.listen(1)
logging.info("SERVER IS UP AND LISTENING AT PORT " + str(SERVER_PORT) + " ...")

while True:
   
    connection, addr = welcome_sock.accept()
    msg = connection.recv(BUFF_SIZE).decode(FORMAT)
    logging.info("CONNECTION WITH CLIENT " + str(addr) + " ESTABLISHED")

    if msg[:MSG_SIZE] == REQUEST_CODE:
        file_name_query = msg[MSG_SIZE:]
        print("Client is requesting a file: " + file_name_query)

    
    try:
        path = '/Users/mollerup/Desktop/server/networks_FTP_project/TCP/server/'
        with open(path + file_name_query,'r') as file:
            file_as_string = file.read()

            response = FILE_FOUND_CODE + file_as_string
            connection.sendall(bytes(response, FORMAT))
            logging.info("SENDING " + file_name_query + " TO CLIENT")

    except:
        connection.sendall(bytes(FILE_NOT_FOUND_CODE, FORMAT))
        logging.info("FILE NOT FOUND, CLIENT NOTIFIED")

    logging.info("SERVER IS UP AND LISTENING AT PORT " + str(SERVER_PORT) + " ...")