import threading, socket, random
HOST = '0.0.0.0'
PORT = 5000
serverList = []


def clientHandler(s):
    if len(serverList) < 3:
        # checks if there's enough servers online
        s.send("NES".encode())
        s.close()
        return
    a = random.sample(serverList, 3)
    for x in a:
        try:
            x[0].send("".encode())
        except:
            serverList.remove(x)
            clientHandler(s)
            return
    for x in a:
        s.send(';'.join(x[1:]).encode())
    s.close()


def main():
    # Creating connection with new server
    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(5)
    while True:
        try:
            s, addr = server.accept()
            data = s.recv(1024).decode()
            if data == "I am a server":
                key = random.randint(1, 255)
                s.send(key.encode())
                serverList.append([s, addr[0], key])
            else:
                threading.Thread(target=clientHandler, args=(s,)).start()
        except:
            continue


if __name__ == '__main__':
    main()
