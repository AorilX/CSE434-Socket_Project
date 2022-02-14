import socket
localIP = "127.0.0.1"
#9000~9499
localPort = 9001
bufferSize = 1024
user_list = []
ip_list = []
port_list = []
player = []
games = []
user = ""
ip = ""
port = ""
msg = ""
def register(user, ip, port):

    #messagefromclient = UDPServerSocket.recvfrom(bufferSize)
   # user = messagefromclient[0]
    if not user.isalpha():
        msg = "you must enter user in alphabet"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)
        return
    elif user in user_list:
        msg = "user exist"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)
        return
    elif len(user) < 0 or len(user) > 15:
        msg = "the length of string is 1 to 15"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)
        return
    elif port in port_list:
        msg = "port exist"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)

    else:
        player.append((user, ip, port))
        user_list.append(user)
        ip_list.append(ip)
        port_list.append(port)
        msg = "User registered"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)

def queryplayers():
    if not player:
        msg = "There is no player"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)
        return
    else:
        #for i in player:
        #    print(i)
       # print(player)
        values = ','.join(str(v) for v in player) #convert tulpe to string and send to client
        UDPServerSocket.sendto(values.encode(), clientAddress)
        msg = "queryplayer printed"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)

def querygames():
    if not games:
        games.clear()
        msg = "There is no game ongoing"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)
        return
    else:
        for i in games:
            print(i)
        msg = "querygames printed"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)

def deregister(user):

    if user in user_list:
        i = user_list.index(user)
        user_list.remove(user)
        player.remove(player[i])
        msg = "User deregistered"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)
    else:
        msg = "User does not exist"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)

msgFromServer = "Hello UDP Client"

bytesToSend = str.encode(msgFromServer)

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while True:
    message, clientAddress = UDPServerSocket.recvfrom(bufferSize)
    #print(clientAddress[0])
    #print("split")
    #print(clientAddress[1])
    receive_message = message.decode()
    m = receive_message.split()

    a = clientAddress[0] #ip address
    b = clientAddress[1] #port number

   # message = bytesAddressPair[0]
   # address = bytesAddressPair[1] #ip, port
   # print(m[0])
    lens = len(m)
    if m[0] == 'register' and lens == 2:

        register(m[1], a, b)


    elif m[0] == 'queryplayers' and lens == 1:
        queryplayers()

    elif m[0] == 'querygames' and lens == 1:
        querygames()
       # msg = "querygames printed"
       # UDPServerSocket.sendto(msg.encode(), clientAddress)
    elif m[0] == 'deregister' and lens == 2:
        deregister(m[1])

    else:
        msg = "please enter the correct command"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
    #clientIP = "Client IP Address:{}".format(address)


    #print(clientMsg)
    #print(clientIP)

    # Sending a reply to client

    #UDPServerSocket.sendto(bytesToSend, address)


print("end")








