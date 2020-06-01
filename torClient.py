import socket, webbrowser, os, tkinter as tk, config
mainIp = config.serverIp
PORT = config.PORT
serverIp = ""


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


def mConstruct(data, req):
    print(data)
    req = serverIp + "|" + req
    for x in data:
        print(x)
        print(x[1])
        req = tEncode(req, x[1])
        req = x[0] + ";" + req
    i = req.find(';')
    req = req[i+1:]
    return req


def mDeConstruct(data, message):
    data.reverse()
    for x in data:
        print(x[1])
        message = tDecode(message, x[1])
    return message


def request(req):
    s = socket.socket()
    s.connect((mainIp, PORT))
    s.send("I am a client".encode())
    data = s.recv(1024).decode().split("*")
    print(data)
    if data[0] == 'NES':
        return
    nodeList = []
    for x in data:
        nodeList.append(x.split(";"))
    message = mConstruct(nodeList, req)
    print(message)
    s.close()
    s = socket.socket()
    s.connect((nodeList[2][0], PORT))
    s.send(message.encode())
    message = s.recv(1024).decode()
    message = mDeConstruct(nodeList, message)
    print(message)


def getAddres():
    req = myEntry.get()
    request(req)
    return


def main():
    root.mainloop()
    try:
        os.remove('datafile.html')
    except:
        return


if __name__ == '__main__':
    root = tk.Tk()
    myCanvas = tk.Canvas(root, width=400, height=400)
    myCanvas.pack()
    myEntry = tk.Entry(root)
    myCanvas.create_window(200, 140, window=myEntry)
    myButton = tk.Button(text='Tor!', command=getAddres)
    myCanvas.create_window(200, 180, window=myButton)
    main()
