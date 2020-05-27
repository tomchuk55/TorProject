import socket, threading, urllib.request, config, webbrowser
mainIp = config.serverIp
HOST = '0.0.0.0'
PORT = config.PORT


def portFinder(ip):
    global PORT
    print(ip)
    print(PORT)
    n = socket.socket()
    PORT += 1
    if PORT == 10000:
        PORT = 5000
    try:
        n.connect((ip, PORT))
        return n
    except:
        portFinder(ip)


def tEncode(data, key):
    key = int(key)
    newdata = ""
    for x in data:
        temp = ord(x) + key
        if temp > 256:
            temp -= 256
        elif temp < 0:
            temp += 256
        newdata += chr(temp)
    return newdata


def tDecode(data, key):
    key = int(key)
    newdata = ""
    for x in data:
        temp = ord(x) - key
        if temp > 256:
            temp -= 256
        elif temp < 0:
            temp += 256
        newdata += chr(temp)
    return newdata


def nodeHandler(s, data, key):
    global PORT
    message = tDecode(data, key)
    print(message)
    i = message.find(';')
    if i == -1:
        ip = message
        print(ip)
        webbrowser.open(ip)
        ip = "http://" + ip
        fp = urllib.request.urlopen(ip)
        message = fp.read().decode("utf8") + "done"
        fp.close()
    else:
        ip = message[:i]
        message = message[i+1:]
        #n = portFinder(ip)
        n = socket.socket()
        n.connect((ip, PORT))
        print(message)
        n.send(message.encode())
        message = n.recv(1024).decode()
        while(message[-4:] != "done"):
            message += n.recv(1024).decode()
        message = message[:-4]
        message = tEncode(message, key) + "done"
    print(message)
    s.send(message.encode())



def main():
    s = socket.socket()
    s.connect((mainIp, PORT))
    s.send("I am a server".encode())
    key = s.recv(1024).decode()
    print(key)
    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(5)
    while True:
        try:
            s.recv(1).decode()
            data = s.recv(1024).decode()
            print(data)
            if data == "confirmed":
                c, addr = server.accept()
                data = c.recv(9999999).decode()
                print(data)
                threading.Thread(target=nodeHandler, args=(c, data, key)).start()
        except:
            continue
            

if __name__ == '__main__':
    main()

