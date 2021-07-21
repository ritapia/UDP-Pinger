# UDP_PingC.py

from socket import *
import sys
import time

argv = sys.argv

#take commandline ip
serverIPaddress = argv[1]
serverPort = 12000

#list to hold all rtt calculated
rtTimes = []

#count the amount of packets sent and received
packSent = 0
packLost = 0

#create socket and set timeout to 1 sec
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

#loop 50 times
for sequence_number in range(1, 51):

    #get local date and time
    dateTime = time.asctime(time.localtime(time.time()))

    #compose message with sequence number and local date time
    message = "ping " + str(sequence_number) + " " + dateTime

    #get send time for rtt calculation
    beginTime = time.time()

    #send message to server and increment amount of packets sent
    clientSocket.sendto(message.encode(), (serverIPaddress, serverPort))
    packSent += 1

    try:
        #retrieve message and addressfrom server
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)

        #get receive time for rtt calculation
        endTime = time.time()

        #calculate rtt and add to list
        rtt = endTime - beginTime
        rtTimes.append(rtt)

        print("Reply from " + serverIPaddress + ": " + modifiedMessage)
        print("RTT: " + str(rtt))

    except timeout:
        print("Request timed out.")

        #increment num of packets lost
        packLost += 1

#calculate packets received and loss rate
packRecv = packSent - packLost
packLossRate = (packLost / 50.0) * 100

print(str(packSent) + " packets sent, " + str(packRecv) + " packets recieved, " + str(packLost) + " packets lost, " + "packet loss rate: " + str(packLossRate) + " %")

if not rtTimes:
    pass
else:
    #calculate the min, avg, and max round trip times of all sent packages
    minRTT = min(rtTimes)
    avgRTT = sum(rtTimes) / len(rtTimes)
    maxRTT = max(rtTimes)
    print("min RTT = " + str(minRTT) + " , avgRTT = " + str(avgRTT) + " , maxRTT = " + str(maxRTT))

clientSocket.close()
