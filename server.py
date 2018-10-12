''' server.py
usage: python server.py PORT
Interprets command, makes error checking, sends response to client
Based on code by Dale R. Thompson
'''

import sys

# Import socket library
from socket import *

def deposit(args, balance):
    if (len(args) != 2):
        return (-1, 'deposit [amount]: deposit the selected amount')
    
    try:
        amount = float(args[1])
    except ValueError:
        return (-3, 'Invalid command argument(s)')
    
    if (amount <= 0):
        return (-2, '[amount] parameter must be positive')
    else:
        return (0, amount, 'Deposit successful. New balance: ' + str(balance + amount))
    
def withdraw(args, balance):
    if (len(args) != 2):
        return (-1, 'withdraw [amount]: withdraw the selected amount')
    
    try:
        amount = float(args[1])
    except ValueError:
        return (-3, 'Invalid command argument(s)')
    
    if (amount <= 0):
        return (-2, '[amount] parameter must be positive')
    elif (balance < float(args[1])):
        return (-3, 'Insufficient funds')
    else:
        return (0, -1*amount, 'Withdrawal successful. New balance: ' + str(balance - amount))


def check(args, balance):
    return (0, 0, 'Current balance is: ' + str(balance))

def ATMHelp(args, balance):
    return (0, 0, format('Available commands:\n' + 'deposit\n' + 'withdraw\n' + 'check\n' + 'logout\n' + 'help\n'))

# Set port number by converting argument string to integer
# If no arguments set a default port number
# Defaults
if sys.argv.__len__() != 2:
    serverPort = 5555
# Get port number from command line
else:
    serverPort = int(sys.argv[1])

# Choose SOCK_STREAM, which is TCP
# This is a welcome socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# The SO_REUSEADDR flag tells the kernel to reuse a local socket
# in TIME_WAIT state, without waiting for its natural timeout to expire.
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Start listening on specified port
serverSocket.bind(('', serverPort))

# Listener begins listening
serverSocket.listen(1)
print('Server online')

balance = 10000.0;

closeFlag = 0
comDict = {
        'deposit': deposit,
        'withdraw': withdraw,
        'check': check,
        'help': ATMHelp
        }

# Forever, read in sentence, convert to uppercase, and send
while (closeFlag == 0):
    # Wait for connection and create a new socket
    # It blocks here waiting for connection
    connectionSocket, addr = serverSocket.accept()

    # Read bytes from socket
    inCommand = connectionSocket.recv(1024)
  
    command = inCommand.decode('utf-8')
    args = command.split()
    if (args[0] == 'logout'):
        reply = 'logout'
    elif (args[0] == 'close'):
        closeFlag = 1
        reply = 'closing'
    elif (args[0] in comDict):
        result = comDict[args[0]](args, balance)
        if (result[0] != 0):
            reply = result[1]
        else:
            balance += result[1]
            reply = result[2]
    else:
        reply = 'Unknown command'
        
    reply = reply.encode('utf-8')
    # Send it into established connection
    connectionSocket.send(reply)
    # Close connection to client but do not close welcome socket
    connectionSocket.close()
    
print('Closing server')
serverSocket.close()
