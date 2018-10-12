''' client.py
usage: python3 client.py HOSTNAMEorIP PORT
Client interface for ATM server application
Based on code by Dale R. Thompson
'''

import sys

# Import socket library
from socket import *

# Set hostname or IP address from command line or default to localhost
# Set port number by converting argument string to integer or use default
# Use defaults
if sys.argv.__len__() != 3:
    serverName = 'localhost'
    serverPort = 5555
# Get from command line
else:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
    
    
closeFlag = 0
print(format('\n' + 'ATM software\n' + 'Type \'help\' for a list of available commands\n'))

while (closeFlag == 0):
    # Choose SOCK_STREAM, which is TCP
    clientSocket = socket(AF_INET, SOCK_STREAM)
    
    # Connect to server using hostname/IP and port
    clientSocket.connect((serverName, serverPort))
    
    # Get sentence from user
    sentence = input('Input command: ')
    
    # Send it into socket to server
    sentenceBytes = sentence.encode('utf-8')
    clientSocket.send(sentenceBytes)
    
    # Receive response from server via socket
    answer = clientSocket.recv(1024)
    answer = answer.decode('utf-8')
    
    if (answer == 'closing' or answer == 'logout'):
        closeFlag = 1
    else:
        print(format(answer))
    
    clientSocket.close()
print('ATM session terminated correctly')