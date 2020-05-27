import socket, threading, urllib.request, config, webbrowser
mainIp = config.serverIp
HOST = '0.0.0.0'
PORT = config.PORT


def portFinder(ip):
    global PORT
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


def nodeHandler(c, data, key):
    global PORT
    message = tDecode(data, key)
    i = message.find(';')
    if i == -1:
        ip = message
        print(ip)
        webbrowser.open(ip)
        fp = urllib.request.urlopen(ip)
        message = fp.read().decode("utf8")
        fp.close()
    else:
        ip = message[:i]
        message = message[i+1:]
        n = portFinder(ip)
        print(message)
        n.send(message.encode())
        message = n.recv(9999999).decode()
        message = tEncode(message, key)
    print(message)
    c.send(message.encode())



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
            c, addr = server.accept()
            s.recv(0).decode()
            data = s.recv(1024).decode()
            print(data)
            if data == "confirmed":
                data = c.recv(9999999).decode()
                threading.Thread(target=nodeHandler, args=(c, data, key)).start()
        except:
            continue
            

if __name__ == '__main__':
    main()

