# UDP_HbS.py
# By Ricardo Tapia
# Date: 04/07/2018
# CS 4390
# Section 003
# Net-ID rit160030

from socket import *
import sys

argv = sys.argv

#take commandline ip
serverIPaddress = argv[1]

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
#set socket timeout to 1 sec
serverSocket.settimeout(1)
# Assign IP address and port number to socket, use port 12000
serverSocket.bind((serverIPaddress, 12000))

#value to keep track of last seq num received
previousSeqNum = 0
#value to keep track of num of consecutive timeouts
numTimeOuts = 0
#max consecutive timeouts before server closes
maxTimeOuts = 50

while numTimeOuts < maxTimeOuts:
    try:
        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)

        sequence_number = message.split(" ")[1]
        print("Server received msg " + sequence_number)

        #check if sequence number incremented by more than 1
        if (int(sequence_number) - 1) > previousSeqNum:
            #calculate the number of lost packets
            numLost = int(sequence_number) - previousSeqNum - 1
            print("Lost " + str(numLost) + " messages")

        #Capitalize the message from the client
        message = message.upper()

        #set prev seq num to remember the last seq num seen
        previousSeqNum = int(sequence_number)

        #reset num of consecutve timeouts
        numTimeOuts = 0

        #send message to client
        serverSocket.sendto(message, address)

    except timeout:
        print("Server timed out")

        #increment number of consecutive timeouts
        numTimeOuts += 1

serverSocket.close()
