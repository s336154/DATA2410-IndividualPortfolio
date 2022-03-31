# -*- coding: utf-8 -*-

#packages imported and used in the exercises

import threading #enables having several clients/connections at the same time
import socket #creats a socket object
import random #to shuffle variables inside a list\set\sequence
import time #used here to slow-down\block processes
import datetime #to access the current time and date
import sys #to import command line parameters


#checking if user asked for help
if str(sys.argv[1]) in ("--help", "-h"):
    print("\n\n >>  Instruction : Please insert the Port number after the name of the python file \n >>  Example: >  "
          "python server.py 8104 \n\n\n\n")

#when server is running
else:
    #function to obtain IP address
    host = socket.gethostbyname(socket.gethostname())

    # Port number, specified by user and obtained from command line
    port = int(sys.argv[1])

    #establishes a socket object for the server in the Internet domain
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #a systemcall that associates a socket with a particular port and Ip-address
    server.bind((host, port))

    #TCP/IP stack will start accepting incoming TCP connections on the port the socket is binded to
    server.listen()



     #declaring lists & variables used
    current_time = None ; clients=[]; names=[]; warn=[]

    #Function to broadcast specific messages to all connected clients
    def broadcast(message): #(Brace B., 2020)
        for client in clients:
                    client.send(message)


    # Function to handle clients'connections
    def handle_client(client):
        #An infinte loop
        while True:
            try:
                current_time = datetime.datetime.now() #obtaining/updating time

                #obtaining index of the client that sent a message
                index = clients.index(client)

                #decoding the message sent by the client
                message = client.recv(1024).decode("utf-8")

                # suggestions intended to be sent when only 1 client is connected
                action1 = random.choice(
                    ["school", "rest", "learn", "wish", "cry", "invest", "fish", "think", "copy", "protest", "volunteer",
                     "parent", "discover", "annoy", "invent", "work", "plant", "tour", "suggest", "exit", "pray", "diet",
                     "climb", "train", "clean", "steal", "cook", "suffer", "read", "help", "paint"]) # (Alzarqawee A.N.J, 2022)

                # suggestions intended to be sent when upto four clients are connected
                action2 = random.choice(
                    ["flirt", "swing", "weep", "touch", "meet", "speak", "party", "punch", "box", "kiss", "suggest", "fall",
                     "shower", "annoy", "kiss", "undress", "greet", "marry", "suggest", "talk", "guess", "act", "mimic",
                     "text", "dream", "stalk", "bath", "drink", "ask", "send", "sing", "laugh", "develop", "discuss", "dress",
                     "cook", "school", "rest", "learn", "wish", "cry", "invest", "fish", "think", "copy", "protest", "volunteer",
                     "parent", "discover", "annoy", "invent", "work", "plant", "tour", "suggest", "exit", "pray", "diet",
                     "climb", "train", "clean", "steal", "suffer", "read", "help", "paint"]) # (Alzarqawee A.N.J, 2022)

                #List containing words to be  banned during the connection/chat
                toxic = ["Noob", "Fuck", "Fking", "Bitch", "Fuk", "Hoe", "Whore", "Horny", "Ass", "Penis",
                         "Tit", "Pussy", "Sex", "Fuggot", "Grop", "Dick", "Boob", "Cock", "Bustard", "Dumb", "Stupid",
                         "Idiot", "Butt", "Shutup", "Suck", "Hook"]

                # List containing words to be  banned during the connection/chat
                toxicL = ["noob", "fuck", "fking", "bitch", "fuk", "hoe", "whore", "horny", "ass", "penis",
                          "tit", "pussy", "sex", "fuggot", "grop", "dick", "boob", "cock", "bustard", "dumb", "stupid",
                          "idiot", "butt", "shutup", "suck", "hook"]

                #intitiating the warning flag
                warned = False

                #checking if the message received contains any words in banned words lists
                for i in range(0, len(toxicL)):

                    #checking the content of the message
                    if toxicL[i] in message or toxic[i] in message:

                        #deciphering abusive message content
                        messageR = message.replace(message, "%@#!%&$#!@#")

                        #Warning message to be sent to the client
                        clients[index].send(
                            f'\n\n {current_time} >>   Host : Warning! The last message had provoking content.\n {current_time} >>   Host : It has '
                            f'being banned. \n'.encode("utf-8"))

                        #replacing the banned message with deciphered message
                        for c in range(0, len(clients)):

                            #sending deciphered message to all clients except the one that sent it
                            if clients[c] != clients[index]:
                                clients[c].send(f'\n {current_time} >> {names[index]}: {messageR}'.encode("utf-8"))
                            else:
                                continue

                            #incrementing the counter variable for warning(s) sent in the warn list
                            warn.append(1)

                            #dispalying information on screen regarding banned messages
                            print("\nProvoking content has being banned successfully\n")
                            print(" {} message(s) has being banned so far                       << <<  {}"
                                  "\n\n".format(len(warn), current_time))

                        warned= True # changing the warned flag to true if a message has been banned

                #forwarding messages among client
                if ("Stop" not in message and warned == False and "Disconnect" not in message and "--help" not in message) or \
                        ("Stop" not in message and warned == False and "Exit" not in message and "--help" not in message) :
                    for c in range(0, len(clients)):
                        if clients[c] != clients[index]:
                            clients[c].send(f'\n {current_time} >> {names[index]}: {message}\n'.encode("utf-8"))
                            time.sleep(3.3) # slowing down the process and blocking I\O

                #checking if a client requested to exit the chat room
                if "Exit" in message or "Disconnect" in message:

                    #obtaining the index of the client
                    index = clients.index(client)

                    #starting connection termination process
                    clients[index].send('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nLogging out ... '.encode("utf-8"))
                    time.sleep(4.3) # slowing down the process and blocking I\O

                    #displaying Chat bot logo
                    clients[index].send(
                        f'\n||||##############################################################################################||||'.encode(
                            "utf-8"))
                    clients[index].send(
                        f'||||######################################  SariBot®  #############################################||||'.encode(
                            "utf-8"))
                    clients[index].send(
                        f'\n||||##############################################################################################||||'.encode(
                            "utf-8"))
                    clients[index].send('\n\nSariBot® Chat Room' .encode("utf-8"))
                    clients[index].send('\nCopyright (C) SariBot Co. All rights reserved®  \n'.encode("utf-8"))
                    time.sleep(3.5)  # slowing down the process and blocking I\O
                    clients[index].send("\n\n    ||§§****--------->>>   G O O D D B Y E   <<<---------****§§||   ".encode("utf-8"))
                    time.sleep(2.5) # slowing down the process and blocking I\O

                    #deleting client information from list of active clients
                    clients.remove(client)
                    client.close() #ending the connection

                    #obtaining client username based on his index
                    nkname = names[index]

                    #Informing other clients about the client that left the chat newly
                    broadcast('\n{} has exited the chat room! \n'.format(nkname).encode("utf-8"))

                     #displaying info on screen regarding disconnected and current active clients
                    print('\n\n{} has exited the chat room!'.format(nkname))
                    print('Active connections: {}   << <<  {} \n\n'.format(len(clients), current_time))

                    #removing the username from the names list
                    names.remove(nkname)
                    #terminating the process
                    break

                #terminating suggestions if only Stop was sent
                elif message == "Stop":
                    continue

                #checking if the client sent a command for help
                elif ("Disconnect" not in message and "--help" in message) or ("Exit" not in message and "--help" in message):

                    #printing the instructions in the client's screen
                    clients[index].send('\n\n >>   Instruction : You will probably get random suggestions in few moments'
                                        ' ..'.encode("utf-8"))
                    clients[index].send(
                        ' >>   Instruction : Start your messages with "Stop" to end the bot ..'.encode("utf-8"))
                    clients[index].send(
                        '\n >>   Instruction : Please, respond to the very first message you receive.'.encode("utf-8"))
                    clients[index].send('\n >>   Instruction : Enter "Exit" or "Disconnect" to exit the chat room ..'
                                        .encode("utf-8"))
                    clients[index].send(
                        '\n >>   Instruction : You may respond with whatever you wish, eg:I like/hate/love based on'
                        ' preferences.\n'.encode("utf-8"))
                    clients[index].send(
                        f' >>   Instruction : Insert "Bot" in command line inorder to activate the bot feature during '
                        f'the chat \n\n'.encode("utf-8"))
                    time.sleep(5) # slowing down the process and blocking I\O

                #Checking conditions for a request to stop sending suggestions
                elif "Stop" in message and warned == False and "--help" not in message:

                 #modifying the message content by removing word Stop from message
                    messagex = message.replace("Stop", "")
                    for c in range(0, len(clients)):
                        if clients[c] != clients[index]:
                            clients[c].send(f'\n {current_time} >> {names[index]}: {messagex}\n'.encode("utf-8"))
                            time.sleep(3.3) # slowing down the process and blocking I\O

                # broadcasting suggestions to initiate conversations
                elif "Stop" not in message and warned == False and "--help" not in message:
                    # broadcasting suggestions when only one client is connected
                    if len(clients) == 1:
                        broadcast(
                            "\n {} >>   Host : Why haven't you started {}ing instead ?  (Start every message with"
                            " 'STOP' if "
                            "you wish to end the suggestions)\n".format(current_time,
                                action1).encode("utf-8"))
                        time.sleep(3.3)  # slowing down the process and blocking I\O

                    # broadcasting suggestions when upto four client are connected
                    elif len(clients) > 1 and len(clients) < 5:
                        broadcast(
                            "\n {} >>   Host : Why don't you rather start {}ing ? (Start every message with "
                            "'STOP' to end the bot or  '--help' for help)\n".format(current_time,
                                action2).encode("utf-8"))
                        time.sleep(3.3)  # slowing down the process and blocking I\O


                else:
                    continue

            #Handling an exception in which in client exits without sending a request
            except: #(Brace B., 2020)

                current_time = datetime.datetime.now()
                #obtianing the index of the client
                index = clients.index(client)
                #removing information about the client from active clients
                clients.remove(client)
                #terminating the connection with the client
                client.close()
                #obtaining the username for the client
                nkname = names[index]
                #informing other clients about the client that has newly left chat room
                broadcast('\n{} has left the chat room!\n'.format(nkname).encode("utf-8"))

                #displaying a message to the server screen stating the terminated connection
                print('\n\n{} has left the chat room! '.format(nkname))

                #displaying number of active clients at the moment
                print('Active connections: {}            << <<  {}\n\n'.format(len(clients),current_time))

                #removing the username of that client from the names list
                names.remove(nkname)
                break

    # Main function to receive the clients connection
    def receive():
        while True:
            current_time = datetime.datetime.now()

            #blank screen for the server
            if len(clients) < 1:
                print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

            #displaying a message to the screen confirming the start of connections approval process
            print('\n\nServer is running and listening ... \n\n')

            #saving information about new connection with a client in two varables
            client, address = server.accept()

            # displaying information about a new connection with a client
            print('Connection is established with {}'.format(str(address)))

            #sending a sign to request the username for the new client
            client.send('logged?'.encode("utf-8")) #(Brace B., 2020)

            #storing the username in a varibale after recieving
            nkname = client.recv(1024) #(Brace B., 2020)

            #storing the username in a names list
            names.append(nkname) #(Brace B., 2020)

            #storing information about the client
            clients.append(client) #(Brace B., 2020)

            # displaying the name of the new client on server screen
            print('The username of this client is {}' .format(nkname))

            # displaying the current number of active clients
            print('Active connections: {}                                       << <<  {}' .format(len(clients), current_time))

            #notifying already connected clients about the entrance of a new client
            if len(clients) > 1: #(Brace B., 2020)
                index = clients.index(client)
                for c in range(0, len(clients)):
                    if clients[c] != clients[index]:
                     clients[c].send('\n\n {} has joined the chat room\n\n'.format(nkname).encode("utf-8"))
            time.sleep(1.35) # slowing down the process and blocking I\O

            # Introductory presentation
            if len(clients) < 2:
                index = clients.index(client)
                client.send('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nYou are now connected ...  '
                            .encode("utf-8"))
                time.sleep(2) # slowing down the process and blocking I\O
                client.send(
                    '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nLoading...'.encode("utf-8"))
                time.sleep(2.8) # slowing down the process and blocking I\O

                # Chat bot logo
                client.send(
                    f'\n||||##############################################################################################||||'.encode(
                        "utf-8"))
                client.send(
                    f'||||######################################  SariBot®  #############################################||||'.encode(
                        "utf-8"))
                client.send(
                    f'\n||||##############################################################################################||||'.encode(
                        "utf-8"))
                client.send('\n\nSariBot® Chat Room'.encode("utf-8"))
                client.send('\nCopyright (C) SariBot Co. All rights reserved® '.encode("utf-8"))
                time.sleep(4.5) # slowing down the process and blocking I\O
                client.send(
                    "\n    <<<---------****§§||   WELCOME TO WORLD'S COOLEST CHAT BOT   ||§§****--------->>>   \n"
                    .encode("utf-8"))
                time.sleep(5) # slowing down the process and blocking I\O
                client.send(f'\n\n\n'.encode("utf-8"))
                # Instructions about chatroom
                clients[index].send(
                    f' >>   Instruction : You will probably get random suggestions in few moments ..'.encode("utf-8"))
                time.sleep(3.45) # slowing down the process and blocking I\O
                clients[index].send(
                    f' >>   Instruction : Please, respond to the very first message you receive.'.encode("utf-8"))
                time.sleep(3.45) # slowing down the process and blocking I\O
                clients[index].send(
                    f' >>   Instruction : You may respond with whatever you wish, eg:I like/hate/love based on preferences.'.encode(
                        "utf-8"))
                time.sleep(3.6) # slowing down the process and blocking I\O
                clients[index].send(
                    f' >>   Instruction : Enter "Exit" or "Disconnect" to exit the chat room ..'.encode("utf-8"))
                time.sleep(4.65) # slowing down the process and blocking I\O
                clients[index].send(
                    f' >>   Instruction : Insert "Bot" inorder to activate the bot feature during the chat'.encode(
                        "utf-8"))

                time.sleep(3.6) #slowing down the process and blocking I\O
                clients[index].send(
                    f' >>   Instruction : Enter "--help" for help ..'.encode("utf-8"))
                time.sleep(4.65) # slowing down the process and blocking I\O
                client.send('\n\n\n\n\n\n\n\nLoading ... '.encode("utf-8"))
                time.sleep(7)# slowing down the process and blocking I\O

            #blank screen for clients
            client.send('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'.encode("utf-8"))

            #now the client can start chatting
            client.send('Type in a new message now (Enter "Exit" or "Disconnect" to exit or "--help" for help) >> \n\n'.encode("utf-8"))

            #enabling threads\separated-processes for the handle_client() function
            thread = threading.Thread(target=handle_client, args=(client,)) #(Brace B., 2020)
            thread.start() #starting the thread

    #starting the recieve() function
    if __name__ == "__main__": #(Brace B., 2020)
        receive()



