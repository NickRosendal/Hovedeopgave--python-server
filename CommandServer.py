import socket, select, threading

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
        self.keepConnectionOpen = True
    def sendMessage(self, message):
        self.messageToSend.append(message)
    def closeConnection(self):
        self.keepConnectionOpen = False
    def stop(self):
        self.waitForConnections = False
    def run(self):
        self.waitForConnections = True
        while self.waitForConnections:
            self.notify("Waiting for a connection")
            self.Client, self.Adr=(self.s.accept())
            self.messageToSend = [] # clean up message cue
            self.notify("Got a connection from: "+str(self.Adr)+'.')
            line = ""
            networkReadBuffer = ""
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
                            self.notify(line)
                    if writable:
                        while len(self.messageToSend) >0:
                            self.Client.sendall(self.messageToSend.pop() + self.delimiter)
                except IOError as err:
                    print(str(err))
                    keepConnectionOpen = False # client must be gone
        #Cleanup
        self.s.close()
    observers = []
    SUBJECT_NAME = "CommandServer"
    def registerObserver(self, observer):
        self.observers.append(observer)
    def unRegisterObserver(self, observer): 
        if observer in self.observers:
            self.observers.remove(observer)
    def notify(self, event):
        for eachObserver in self.observers:
            eachObserver.notify(self.SUBJECT_NAME, event)
