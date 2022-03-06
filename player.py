import socket

serverAddressPort = ("127.0.0.1", 48000)

bufferSize = 2048

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
while True:
    msgFromClient = input(": ")

    bytesToSend = str.encode(msgFromClient)

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg = "Message from Manager {}".format(msgFromServer[0].decode())

    print(msg)

print("finished")