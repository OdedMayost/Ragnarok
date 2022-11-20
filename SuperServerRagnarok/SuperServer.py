from tcp_by_size import send_by_size, receive_by_size
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
from DataBase import *
import threading
import hashlib
import random
import base64
import socket

port = 55555
ip = "0.0.0.0"

threads = []

threads_mode = {}  # key - client's ID, value - Is the handle thread is in life
threads_mode_lock = threading.Lock()

clients = {}  # key - client's ID, value - list of messages to send to the client
clients_lock = threading.Lock()
users = {}  # key - client's ID, value - another player (enemy)
users_lock = threading.Lock()

users_keys = {}

connect_bowling = None
connect_bowling_lock = threading.Lock()
connect_Rock_Hero = None
connect_Rock_Hero_lock = threading.Lock()


def connect_player(user_id, type_game):
    global users
    global users_lock
    global connect_bowling
    global connect_bowling_lock
    global connect_Rock_Hero
    global connect_Rock_Hero_lock

    print(type_game)

    if type_game == "bowling game":
        connect_bowling_lock.acquire()
        if connect_bowling is None:
            connect_bowling = user_id
            message = "START~1~1"
        else:
            users_lock.acquire()
            users[user_id] = connect_bowling
            users[connect_bowling] = user_id
            users_lock.release()
            connect_bowling = None
            message = "START~1~2"
        connect_bowling_lock.release()
        while connect_bowling == user_id:
            pass

    elif type_game == "Rock Hero":
        connect_Rock_Hero_lock.acquire()
        if connect_Rock_Hero is None:
            connect_Rock_Hero = user_id
            message = "START~2~1"
        else:
            users_lock.acquire()
            users[user_id] = connect_Rock_Hero
            users[connect_Rock_Hero] = user_id
            users_lock.release()
            connect_Rock_Hero = None
            message = "START~2~2"
        connect_Rock_Hero_lock.release()
        while connect_Rock_Hero == user_id:
            pass

    return message


def handle_client_messages(client_socket, user_id):
    global clients
    global clients_lock
    global threads_mode

    while threads_mode[user_id]:
        if len(clients[user_id]) != 0:
            clients_lock.acquire()
            client_message = clients[user_id].pop(0)
            clients_lock.release()
            send_by_size(client_socket, client_message.encode())
            print("Sent --> " + str(client_message))


def client_service(client_socket, client_address):
    global clients
    global clients_lock
    global users
    global users_lock
    global users_keys
    global threads

    db = "database.db"
    database = DataBase(db)
    db_lock = threading.Lock()

    type_game = None
    user_id = ""
    enemy_id = None
    user_ip = ""

    thread = None

    while True:
        data = receive_by_size(client_socket).decode("utf8")
        if data == "":
            threads_mode_lock.acquire()
            threads_mode[user_id] = False
            threads_mode_lock.release()
            if thread is not None:
                thread.join()
            print("Client Disconnected")
            break

        print("Received --> " + data)
        data = data.split("~")

        if data[0] == "HELLO":
            computer_ip = client_address[0]
            db_lock.acquire()
            computer_id = database.add_computer(computer_ip)
            db_lock.release()
            if computer_id != 0:
                message = "COMID~" + str(computer_id)
            else:
                print("ERROR: Computer ID")

        elif data[0] == "COMID":
            db_lock.acquire()
            computer_ip = database.get_by_value("Computers", "ComputerID", data[1])
            db_lock.release()
            if computer_ip != 0:
                computer_ip = computer_ip[0][1]
                user_ip = computer_ip
                message = "COMIP~" + str(computer_ip)
            else:
                print("ERROR: Computer IP")

        elif data[0] == "DIFHL":
            A, p, g = tuple(data[1:4])
            b = random.randint(10000, 50000)
            B = (int(g) ** b) % int(p)
            K = (int(A) ** b) % int(p)
            users_keys[user_ip] = str(K)[:16].encode()
            message = "DIFHL~" + str(B)
            send_by_size(client_socket, message.encode())
            print("Sent --> " + str(message))
            print("Android Client Disconnected")
            break

        elif data[0] == "SGNUP":
            computer_ip = client_address[0]
            username = data[1]
            cipher = AES.new(users_keys[user_ip], AES.MODE_ECB)
            password = base64.b64decode(data[2].encode())
            password = unpad(cipher.decrypt(password), AES.block_size)
            password = hashlib.sha256(password).hexdigest()
            name = data[3]
            phone_number = data[4]
            db_lock.acquire()
            user_id = database.add_user(computer_ip, username, password, name, phone_number)
            db_lock.release()
            if user_id != 0:
                message = "REGIS~1"
                clients_lock.acquire()
                clients[user_id] = []
                clients_lock.release()
                threads_mode_lock.acquire()
                threads_mode[user_id] = True
                threads_mode_lock.release()
                thread = threading.Thread(target=handle_client_messages, args=(client_socket, user_id))
                thread.start()
            else:
                message = "REGIS~2"
                print("ERROR: signup")

        elif data[0] == "SGNIN":
            computer_ip = client_address[0]
            username = data[1]
            cipher = AES.new(users_keys[user_ip], AES.MODE_ECB)
            password = base64.b64decode(data[2].encode())
            password = unpad(cipher.decrypt(password), AES.block_size)
            password = hashlib.sha256(password).hexdigest()
            db_lock.acquire()
            user_id = database.user_login(username, password, computer_ip)
            db_lock.release()
            if user_id != 0:
                message = "LOGIN~1"
                clients_lock.acquire()
                clients[user_id] = []
                clients_lock.release()
                threads_mode_lock.acquire()
                threads_mode[user_id] = True
                threads_mode_lock.release()
                thread = threading.Thread(target=handle_client_messages, args=(client_socket, user_id))
                thread.start()
            else:
                message = "LOGIN~2"
                print("ERROR: signin")

        elif data[0] == "TYGAM":
            type_game = data[1]
            if type_game == "1":
                type_game = "bowling game"
                message = connect_player(user_id, type_game)
            elif type_game == "2":
                type_game = "Rock Hero"
                message = connect_player(user_id, type_game)
                send_by_size(client_socket, message.encode())
                print("Sent --> " + str(message))
                type_music = random.randint(0, 4)
                message = "GSONG~" + str(type_music)
            users_lock.acquire()
            enemy_id = users[user_id]
            users_lock.release()
            database.update_number_games(user_id)

        if type_game == "bowling game":
            if data[0] == "ENDED":
                clients_lock.acquire()
                clients[enemy_id].append(data[0])
                clients_lock.release()
                database.update_number_losses(user_id)
                database.update_number_wins(enemy_id)
                type_game = None

            if data[0] == "RNDOV":
                clients_lock.acquire()
                clients[enemy_id].append(data[0])
                clients_lock.release()

            elif data[0] == "PINUM":
                enemy_message = "ENPIN~" + data[1]
                clients_lock.acquire()
                clients[enemy_id].append(enemy_message)
                clients_lock.release()

            elif data[0] == "PMOVE":
                enemy_message = "ENMOV~" + data[1]
                clients_lock.acquire()
                clients[enemy_id].append(enemy_message)
                clients_lock.release()

            elif data[0] == "ACLRT":
                enemy_message = "ENACL~" + data[1] + "~" + data[2]
                clients_lock.acquire()
                clients[enemy_id].append(enemy_message)
                clients_lock.release()

        elif type_game == "Rock Hero":
            if data[0] == "ENDED":
                clients_lock.acquire()
                clients[enemy_id].append(data[0])
                clients_lock.release()
                database.update_number_losses(user_id)
                database.update_number_wins(enemy_id)
                type_game = None

            if data[0] == "PRESS":
                data = "ENKEY~" + data[1]
                clients_lock.acquire()
                clients[enemy_id].append(data)
                clients_lock.release()

            if data[0] == "MISSA":
                data = "EMISS"
                clients_lock.acquire()
                clients[enemy_id].append(data)
                clients_lock.release()

            if data[0] == "ARROW":
                data = "~".join(data)
                clients_lock.acquire()
                clients[enemy_id].append(data)
                clients_lock.release()

        send_by_size(client_socket, message.encode())
        print("Sent --> " + str(message))

    client_socket.close()


def main():
    global ip
    global port

    srv_socket = socket.socket()
    srv_socket.bind((ip, port))

    srv_socket.listen(10)

    while True:
        (client_socket, client_address) = srv_socket.accept()
        thread = threading.Thread(target=client_service, args=(client_socket, client_address))
        thread.start()
        threads.append(thread)
    for process in threads:
        process.join()
    srv_socket.close()


if __name__ == "__main__":
    main()
