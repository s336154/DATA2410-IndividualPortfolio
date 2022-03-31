# -*- coding: utf-8 -*-

#packages imported and used in the exercise
import threading #enables having several clients/connections at the same time
import socket #creats a socket object
import random #to shuffle variables inside a list\set\sequence
import time #used here to slow-down\block processes
import sys #to import command line parameters



print('\n\n')

#Condition for displaying logging in instructions
if str(sys.argv[1]) in ("--help", "-h"):
    print("\n\n  >>  Instruction : Please insert the IP address and Port number for the Chat Bot followed ")
    print( "  >>  by your username after the name of the python file.\n  >>  Example: > python client.py 192.168.56.1 8104 Ronald \n\n\n\n")

#when client is connected
else:

    #obtaining chosen username from command line
    nkname = str(sys.argv[3]).capitalize() #(Brace B., 2020)

    #asking user for patience if delay happens
    print("\nThis might take few moments, please be patient.")
    print('Connecting ... ')

    #creating a socket object for the client in the Internet domain
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #obtaining IP-address for the server from the command line
    server = str(sys.argv[1])

    #obtaining port number associated with the server IP address given in command line
    port = int(sys.argv[2])

    #Establishing a connection for the provided IP-address and port number
    client.connect((server, port))

    #declaring list and sets used
    hsuggest = []; bad_things= set(); good_things= set()


    #Function that will send responses
    def bot(pot): #(Alzarqawee A.N.J, 2022)

        #declaring global lists
        global bad_things; global good_things

        #filling list with default disliked\liked activities
        bad_things1 = {"fight", "cry", "suffer", "read", "school", "suffer", "learn", "help"}
        good_things1 = {"sing", "play", "sleep", "eat", "act", "kiss", "flirt", "paint"}

        #updating the globle sets with the default lists values
        bad_things.update(bad_things1)
        good_things.update(good_things1)


        #random function will pick random responses
        actionG = random.choice(tuple(good_things))

         #response sent if activity is stored in a set as not desirable
        if pot in bad_things or pot in bad_things1:
            return "Naaah! Why don't we rather start {}ing!\n".format(actionG)

        #response sent if activity is stored in a set as desirable
        elif pot in good_things or pot in good_things1:
            return "YESS!! Time for {}ing!".format(pot)

        #Otherwise, if activty was not stored in both sets
        else:
         return "Whatever, I don't care !"



    #Function handling received messages
    def client_receive():
        #infinte loop will keep handling incoming messages via server
        while True:
            try:
                #Decoding message received
                message = client.recv(1024).decode('utf-8')

                #declaring local variables
                ex= None; exm = None

                #sending username chosen
                if message == 'logged?': #(Brace B., 2020)
                   client.send(nkname.encode('utf-8'))

                #displaying received message on screen
                print(message)

                #checking if a suggestion for an activity was sent
                if ("Why" in message and "ing" in message and "?" in message) or  ("why" in message and "ing" in message and "?" in message):

                    #declaring variables that will check the content of the suggestions
                    target = "ing"; espace = " "

                    index = message.index(target)
                    start = index - 19
                    for m in range(0, len(message)):
                        if message[m] == espace:
                            ex = message[start:index]
                    for n in range(0, len(ex)):
                        if ex[n] == espace:
                            exm = ex[n + 1:]

                    #storing suggested activty in list "hsuggest"
                    hsuggest.append(exm)

                    #Can take away hashtag to display the information on screen
                   # print("\n\nAction {} has been added to suggestion list.".format(exm))
                   # print("Total suggestion(s) :  {}  ".format(len(hsuggest)))

                    #default responses frequency
                    scheck = len(hsuggest) % 5

                    # sending default responses
                    if scheck == 0 and len(hsuggest) < 50:
                        stop = "Stop"
                        client.send(bot(exm).encode('utf-8'))
                        print(bot(exm))
                        client.send(stop.encode('utf-8'))
                        time.sleep(2.5)# timer to slow down the process
                    else:
                        pass

                    #terminating suggetions if the total suggestions recieved exceeds a certain limit
                    if len(hsuggest) > 99:
                        stop = "Stop"
                        client.send(stop.encode('utf-8'))
                    else:
                        pass
                else:
                   pass

            #Exception handling disconnections from server
            except: #(Brace B., 2020)
                print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                print('CONNECTION LOST ..')
                client.close()
                break

    #Function handling sent messages from client
    def client_send():
        #infinte loop
        while True:

            #Input containing client's message
            text = input(f" ").capitalize() #(Brace B., 2020)

            # declaring variable and sets used
            sugges = None; global good_things; global bad_things

            #sending default responses
            if "Bot" in text:
                last = len(hsuggest) - 1
                sugges = hsuggest[last] #obtaining last recieved suggestion from stored suggestions

                client.send(bot(sugges).encode('utf-8')) #sends default response through function bot
                print(bot(sugges)) #displays message to be sent on screen
                time.sleep(2.5) # slowing down the process and blocking I\O

            #Storing disliked activities based on text input  content
            elif ("ing" in text and "t like" in text) or ("ing" in text and "bad" in text) or ("ing" in text and "hate" in text):

                #declaring local variables
                target = "ing"; bxm=None; bx = None; espace = " "

                index = text.index(target)
                start = index - 10

                #looping through message content
                for m in range(0, len(text)):
                  if text[m] == espace:
                   bx = text[start:index]
                for n in range(0, len(bx)):
                    if bx[n] == espace:
                        bxm = bx[n+1:]
                if bxm not in bad_things:
                    bad_things.add(bxm) #storing suggetion in disliked suggestions list

                    # Can take away hashtag to display the information on screen
                   # print("\n\nAction {} has been added to bad things list.".format(bxm))
                   # print("Total bad action(s) :  {} ".format(len(bad_things)))
                    #print(bad_things)

                client.send(text.encode('utf-8'))  # forwarding message typed to server
                time.sleep(2.5)  # slowing down the process and blocking I\O

            # storing desirable activities based on input content
            elif ("ing" in text and "love" in text) or ("ing" in text and "good" in text) or \
             ("ing" in text and "like" in text) or ("ing" in text and "adore" in text) or ("ing" in text and "prefer" in text):

                #declaring local variables
                target = "ing"; gxm=None; gx = None; espace = " "

                index = text.index(target)
                start = index - 10

                #looping through input content
                for m in range(0, len(text)):
                  if text[m] == espace:
                   gx = text[start:index]

                for n in range(0, len(gx)):
                    if gx[n] == espace:
                        gxm = gx[n + 1:]

                if gxm not in good_things:
                    good_things.add(gxm) #storing suggestion in liked suggestions list

                    #Can take away hashtag to display the information on screen
                   # print("\n\nAction {} has been added to good things list.".format(gxm))
                    #print("Total good action(s) :  {} ".format(len(good_things)))
                    #print(good_things)
                else:
                    pass

                client.send(text.encode('utf-8'))  #forwarding message typed to server
                time.sleep(2.5) #slowing down the process and blocking I\O


            else:
                client.send(text.encode('utf-8'))  #forwarind message typed to server
                time.sleep(2.5) #slowing down the process and blocking I\O


    # enables messages recieving process to run independently
    receive_thread = threading.Thread(target=client_receive) #(Brace B., 2020)
    receive_thread.start()

    #enables messages sending process to run independently
    send_thread = threading.Thread(target=client_send) #(Brace B., 2020)
    send_thread.start()



