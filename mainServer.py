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
    a = []
    x = random.sample(range(len(serverList)), 3)
    print(x)
    for i in x:
        a.append(serverList[i])
    print(a)
    for x in a:
        try:
            x[0][0].send("".encode())#TODO add another '[0]' in x and y
        except:
            serverList.remove(x)
            for y in a:
                if y == x:
                    break
                y[0][0].send("cancel".encode())
            clientHandler(s)
            return
    for x in a:
        x[0][0].send("confirmed".encode())
        print(x)
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
                print("new server")
                key = str(random.randint(1, 255))
                print(key)
                s.send(key.encode())
                serverList.append([[s], addr[0], key])
                print("append")
            elif data == "I am a client":
                print('new client')
                threading.Thread(target=clientHandler, args=(s,)).start()
        except:
            continue


if __name__ == '__main__':
    main()
