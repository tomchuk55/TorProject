import socket, webbrowser, os, tkinter as tk, config
mainIp = config.serverIp
PORT = config.PORT


def tEncode(data, key):
    newdata = ""
    for x in data:
        newdata += chr(ord(x)+key)
    return newdata


def tDecode(data, key):
    newdata = ""
    for x in data:
        newdata += chr(ord(x)-key)
    return newdata


def mConstruct(data, req):
    for x in data:
        req = tEncode(req, x[2])
        req = x[1] + ";" + req
    i = req.find(';')
    req = req[:i]
    return req


def mDeConstruct(data, ans):
    for x in data:
        ans = tDecode(ans, x[2])
    return ans


def request(req):
    s = socket.socket()
    s.connect((mainIp, PORT))
    s.send("I am a client".encode())
    data = s.recv(1024).decode().split(";")
    message = mConstruct(data, req)
    s.close()
    s.connect((data[2][1], PORT))
    s.send(message.encode())
    message = s.recv().decode()
    message = mDeConstruct(data, message)
    f = open('datafile.html', 'w')
    f.write(message)
    webbrowser.open_new_tab('datafile.html')
    f.close()
    os.remove('datafile.html')


def getAddres():
    req = myEntry.get()
    request(req)
    return


def main():
    root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    myCanvas = tk.Canvas(root, width=400, height=400)
    myCanvas.pack()
    myEntry = tk.Entry(root)
    myCanvas.create_window(200, 140, window=myEntry)
    myButton = tk.Button(text='Tor!', command=getAddres)
    myCanvas.create_window(200, 180, window=myButton)
    main()
