import socket, select, threading, time

class CommandServer(threading.Thread):
    packageSize = 1024
    delimiter = "\n"
    messageToSend = []
    def __init__(self,adress="", port=5000, maxClients=1):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((adress,port))
        self.s.listen(maxClients)
        self.checkConnectionEvery = 5
        self.keepConnectionOpen = True
    def sendMessage(self, message):
        self.messageToSend.append(message)
    def closeConnection(self):
        self.keepConnectionOpen = False
    def stop(self):
        self.keepConnectionOpen = False
        self.waitForConnections = False
    def run(self):
        self.waitForConnections = True
        while self.waitForConnections:
            self.notify("status", "Waiting for a connection")
            self.Client, self.Adr=(self.s.accept())
            self.messageToSend = [] # clean up message cue
            self.notify("status", "Got a connection from: "+str(self.Adr)+'.')
            line = ""
            networkReadBuffer = ""
            timeToCheckConnection = time.time() + (self.checkConnectionEvery)
            self.keepConnectionOpen = True
            while self.keepConnectionOpen:
                try:
                    readable, writable, exceptional = select.select([self.Client], [self.Client], [])
                    if readable:
                        data = self.Client.recv(self.packageSize)
                        if data:
                            networkReadBuffer += data
                        else:
                            self.keepConnectionOpen = False
                        while networkReadBuffer.find(self.delimiter) != -1:
                            line, networkReadBuffer = networkReadBuffer.split(self.delimiter, 1)
                            self.notify("message", line)
                    if writable:
                        if time.time() >= timeToCheckConnection:
                            self.Client.sendall("") # to check connection
                            timeToCheckConnection = time.time() + (self.checkConnectionEvery)
                        while len(self.messageToSend) >0:
                            self.Client.sendall(self.messageToSend.pop() + self.delimiter)
                except IOError as err:
                    print(str(err))
                    self.keepConnectionOpen = False # client must be gone
        #Cleanup
        self.s.close()
    observers = []
    SUBJECT_NAME = "CommandServer"
    def registerObserver(self, observer):
        self.observers.append(observer)
    def unRegisterObserver(self, observer): 
        if observer in self.observers:
            self.observers.remove(observer)
    def notify(self, eventType, event):
        for eachObserver in self.observers:
            eachObserver.notify(self.SUBJECT_NAME, eventType, event)
