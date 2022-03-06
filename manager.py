import socket
import itertools
import random

from pyrsistent import discard

localIP = "127.0.0.1"
#48000~48499
localPort = 48000
bufferSize = 2048
user_list = []
waiting_list = []
game_list = []
identifier_list =[]

ip_list = []
port_list = []
player = []
games = []
user = ""
ip = ""
port = ""
msg = ""
k = 0

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
        waiting_list.append(user)
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
        print(player)
        #for i in player:
        #    print(i)
       # print(player)
        #values = ','.join(str(v) for v in player) #convert tulpe to string and send to client
        result_string = '\nplayer: '
        for i in player:
            for x in i:
                result_string += str(x) + '\n'

        UDPServerSocket.sendto(result_string.encode(), clientAddress)
        #msg = "queryplayer printed"
        #UDPServerSocket.sendto(msg.encode(), clientAddress)
        #print(msg)

def querygames():
    #print(game_list)

    if not game_list:
        games.clear()
        msg = "There is no game ongoing"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)
        return
    else:
        result_string = '\n'
        for game in game_list:
            result_string += 'game identifier: ' + game[0]
            result_string += '\ndealer: ' + game[1][0]

            result_string += '\nplayers: '
            for user2 in game[1]:
                result_string += user2 + ' '
            result_string += '\n' + '\n'
        #msg = "querygames printed"
        UDPServerSocket.sendto(result_string.encode(), clientAddress)
        print(result_string)

def deregister(user):

    if user in user_list:
        i = user_list.index(user)
        user_list.remove(user)
        player.remove(player[i])
        msg = "SUCCESS"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)
    else:
        msg = "User does not exist"
        UDPServerSocket.sendto(msg.encode(), clientAddress)
        print(msg)

def startGame(user, k):
    #get k users from the list
    thePlayer = []
    theGame = []
    if user in waiting_list:
        i = waiting_list.index(user)
        thePlayer.append(waiting_list.pop(i))

    if (k > 1 and k < 5):
        for i in range(k-1):
            thePlayer.append(waiting_list.pop(0))

        game_identifier = ''
        game_identifier = 'game_' + user
        print(game_identifier)
        print(thePlayer)

        vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['S', 'C', 'H', 'D']

        deck = list(itertools.product(vals, suits))
        random.shuffle(deck)

        player_cards =[]
        user_view = []
        back_count = []

        for i in range(k*6):
            player_cards.append('***')

        for i in range(k):
            back_count.append(0)

        for i in range(k*6):
            user_view.append('***')

        count = 0

        for i in range(k*6):
            card = deck.pop(0)
            player_cards[i] = card[0] + card[1]


        discard_card = deck.pop(0)
        discard = discard_card[0] + discard_card[1]

        """"
        alist = [["user1"], ['1  ', '2  ', '3  '], ['**', '**', '**'], ['4  ', '5  ', '6  '], ['**', '**', '**'], ['']]
        string = "user1\n" + "1  2  3  \n" + "** ** **\n"

        for x in alist:
            for i in x:
                print(i, end = " ")
            print()
        
        alist = [["Discard: ", discard], ['Top: ', '**']]

        for x in alist:
            for i in x:
                print(i, end = " ")
            print()
        """


        identifier_list.append(game_identifier)

        card_list = []
        card_list.append(player_cards)
        card_list.append(discard)
        card_list.append(deck)
        card_list.append(user_view)
        card_list.append(back_count)

        theGame.append(thePlayer)
        theGame.append(card_list)
        theGame.insert(0, game_identifier)

        game_list.append(theGame)
        print(player_cards)

        result_string = "\n"
        for user1 in thePlayer:
                user_index = theGame[1].index(user1)
                result_string = result_string + user1 + "\n1   2   3   \n" + user_view[user_index*6] + " " + user_view[user_index*6 + 1] + " " + user_view[user_index*6+2]
                result_string = result_string + "\n4   5   6   \n" + user_view[user_index*6 +3] + " " + user_view[user_index*6 + 4] + " " + user_view[user_index*6 + 5] + "\n"
        result_string += "Discard: " + discard + " Top: ***\n"
        print(result_string)
        UDPServerSocket.sendto(result_string.encode(), clientAddress)


        #print(game_list)


        #instruction = input('hello world: ')
        #print(instruction)

        #9 rounds


def playGame(user, game_identifier, num, choice):
    if game_identifier in identifier_list:
        i = identifier_list.index(game_identifier)
        theGame = game_list[i]
        if user in theGame[1]:
            users = theGame[1]
            user_index = theGame[1].index(user)
            card_list = theGame[2]

            player_cards = card_list[0]
            discard = card_list[1]
            deck = card_list[2]
            user_view = card_list[3]
            back_count = card_list[4]

            if choice == "D":
                temp_card_str = player_cards[user_index*6 + int(num)-1]
                player_cards[user_index*6 + int(num)-1] = discard

                the_str = user_view[user_index*6 + int(num)-1]


                user_view[user_index*6 + int(num)-1] = discard
                discard = temp_card_str

                if the_str == "***":
                    back_count[user_index] = back_count[user_index] +1
                    #game ends and calculate scores
                
                card_list[0] = player_cards
                card_list[1] = discard
                card_list[3] = user_view
                card_list[4] = back_count
                card_list[0] = player_cards
                card_list[1] = discard


            elif choice == "T":
                temp_card = deck.pop(0)
                temp_card_str = player_cards[user_index*6 + int(num)-1]

                the_str = user_view[user_index*6 + int(num)-1]


                user_view[user_index*6 + int(num)-1] = temp_card[0] + temp_card[1]
                player_cards[user_index*6 + int(num)-1] = temp_card[0] + temp_card[1]
                discard = temp_card_str


                if the_str == "***":
                    back_count[user_index] = back_count[user_index] +1
                    #game ends and calculate scores

                card_list[0] = player_cards
                card_list[1] = discard
                card_list[2] = deck
                card_list[3] = user_view
                card_list[4] = back_count

            else:
                user_view[user_index*6 + int(num)-1] = player_cards[user_index*6 + int(num)-1]
                user_view[user_index*6 + int(choice)-1] = player_cards[user_index*6 + int(choice)-1]
                back_count[user_index] = back_count[user_index] + 2

                card_list[0] = player_cards
                card_list[1] = discard
                #card_list[2] = deck
                card_list[3] = user_view
                card_list[4] = back_count

            
            result_string = "\n"
            for user1 in users:
                user_index = theGame[1].index(user1)
                result_string += user1 + "\n1   2   3   \n" + user_view[user_index*6] + " " + user_view[user_index*6 + 1] + " " + user_view[user_index*6+2] 
                result_string = result_string + "\n4   5   6   \n" + user_view[user_index*6 +3] + " " + user_view[user_index*6 + 4] + " " + user_view[user_index*6 + 5] + "\n"
            result_string += "Discard: " + discard + " Top: **\n"
            print(result_string)
            UDPServerSocket.sendto(result_string.encode(), clientAddress)
            game_list[i][2] = card_list

            user_index = theGame[1].index(user)
            print(back_count[user_index])

            if back_count[user_index] == 6:
                calculate(game_identifier)
                

            
        
    else:
        print("No game")
    return

def calculate(game_identifier):
    scores = []
    if game_identifier in identifier_list:
        i = identifier_list.index(game_identifier)

        theGame = game_list[i]
        users = theGame[1]
        #user_index = theGame[1].index(user)
        card_list = theGame[2]

        player_cards = card_list[0]
        discard = card_list[1]
        deck = card_list[2]
        user_view = card_list[3]
        back_count = card_list[4]

        for user1 in users:
            i = users.index(user1)
            cards = []
            cards.append(player_cards[i*6])
            cards.append(player_cards[i*6 + 1])
            cards.append(player_cards[i*6 + 2])
            cards.append(player_cards[i*6 + 3])
            cards.append(player_cards[i*6 + 4])
            cards.append(player_cards[i*6 + 5])
            card_name = 0
            cards_list = []

            for card in cards:
                if card[0] == "1":
                    card_name = 10
                elif card[0] == "J":
                    card_name == 11 
                elif card[0] == "Q":
                    card_name == 12
                elif card[0] == "K":
                    card_name == 13
                elif card[0] == "A":
                    card_name == 1
                else:
                    card_name == int(card[0])
                cards_list.append(card_name)
            
            if (cards_list[0] == cards_list[3]):
                cards_list[0] = 0 
                cards_list[3] = 0 

            if (cards_list[1] == cards_list[4]):
                cards_list[1] = 0 
                cards_list[4] = 0
            
            if (cards_list[2] == cards_list[5]):
                cards_list[2] = 0 
                cards_list[5] = 0
            
            for i in range(6):
                if (cards_list[i] == 13):
                    cards_list[i] = 0
                elif cards_list[i] == 2:
                    cards_list[i] = -2
                elif (cards_list[i] == 11 or cards_list[i] == 12):
                    cards_list[i] = 10
            
            theScore = 0
            for i in cards_list:
                theScore += i
            scores.append(theScore)
        result_string = '\n'
        for user1 in users:
            user_index = theGame[1].index(user1)
            result_string = result_string + user1 + ": " + str(scores[user_index]) + "\n"

        min_score = min(scores)
        min_index = scores.index(min_score)
        result_string += users[min_index] + " wins!"
        print(result_string)

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
    elif m[0] == 'startgame':

        startGame(m[1], int(m[2]))
    elif m[0] == 'playgame':
        playGame(m[1], m[2], m[3], m[4])

    else:
        msg = "please enter the correct command"
        print(m[0])
        print(m[0])
        UDPServerSocket.sendto(msg.encode(), clientAddress)
    #clientIP = "Client IP Address:{}".format(address)


    #print(clientMsg)
    #print(clientIP)

    # Sending a reply to client

    #UDPServerSocket.sendto(bytesToSend, address)


print("end")








