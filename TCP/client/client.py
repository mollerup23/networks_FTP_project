""" TCP_FPT_client.py                                  
NAME Philip Mollerus
DATE May 7 2023                                    
This module will send
requests for files
from the TCP_FPT_SERVER          
"""

#Setting up imports
from socket import *
import logging

BUFF_SIZE = 1024
FORMAT = "utf-8"
SERVER_PORT = 9090
SERVER_NAME = "172.16.99.131"
MSG_SIZE = 3

## MAGIC NUMBERS

FILE_FOUND_CODE = "506"
FILE_NOT_FOUND_CODE = "404"
REQUEST_CODE = "200"


#Setting up logger
logging.basicConfig(level=logging.DEBUG)

def recvall(sock):
    data = ""
    while True:
        part = sock.recv(BUFF_SIZE).decode(FORMAT)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data

clientSocket = socket(AF_INET, SOCK_STREAM)
logging.info("CLIENT TCP SOCKET ESTABLISHED AT PORT: " + str(clientSocket))

clientSocket.connect((SERVER_NAME, SERVER_PORT))
logging.info("CLIENT CONNECTED WITH SERVER AT " + SERVER_NAME + " AT PORT " + str(SERVER_PORT))

file_name = input("Enter the name of the file ... ")
clientSocket.send(bytes(REQUEST_CODE + file_name, FORMAT))
logging.info("REQUEST FOR FILE " + file_name + " SENT TO SERVER")

resp_string = recvall(clientSocket)

if resp_string[:MSG_SIZE] == FILE_FOUND_CODE:
    logging.info("FILE RECIEVED FROM SERVER ... ")
    print("\n\n\n" + resp_string[MSG_SIZE:])

elif resp_string[:MSG_SIZE] == FILE_NOT_FOUND_CODE:
    logging.info("FILE NOT FOUND")

clientSocket.close()
logging.info("CLOSING CONNECTION WITH " + SERVER_NAME)
