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

"""diff --git a/CommandServer.py b/CommandServer.py
index 45938fc..4a7bd9a 100644
--- a/CommandServer.py
+++ b/CommandServer.py
@@ -3,16 +3,15 @@ import socket, select, time, threading
 class CommandServer(threading.Thread):
    
     packageSize = 1024
-    delimiter = "\0"
+    delimiter = "\n"
     messageToSend = []
-    def __init__(self,adress="", port=5000, maxClients=1):
+    def __init__(self,adress="", port=5000, maxClients=1, checkConnectionEvery=5):
         threading.Thread.__init__(self)
         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
-               
+        self.checkConnectionEvery = checkConnectionEvery
         self.s.bind((adress,port))
         self.s.listen(maxClients)
-        self.running = True
     def sendMessage(self, message):
         self.messageToSend.append(message)
     def run(self):
@@ -20,13 +19,16 @@ class CommandServer(threading.Thread):
         while waitForConnections:
             print "Waiting on connection"
             self.Client, self.Adr=(self.s.accept())
+            self.messageToSend = [] # clean up message cue
             print('Got a connection from: '+str(self.Adr)+'.')
             line = ""
             networkReadBuffer = ""
+            timeToCheckConnection = time.time() + (self.checkConnectionEvery)
             keepConnectionOpen = True
             while keepConnectionOpen:
                 try:
-                    self.messageToSend.append("\0") # TODO
+                    mytime = time.time()
+                    
                     readable, writable, exceptional = select.select([self.Client], [self.Client], [])
                     if readable:
                         data = self.Client.recv(self.packageSize)
@@ -36,20 +38,22 @@ class CommandServer(threading.Thread):
                             print("message recived: " + line)
                         if line == "quit":
                             keepConnectionOpen = False
-                        if line == "got anything for me?":
-                            self.messageToSend.append("Yes, I just want you to know that you are the best client ever")
+                        if line == "hello":
+                            self.messageToSend.append("Hi, how may I serve you?")
                     if writable:
-                            while len(self.messageToSend) >0:
-                                self.Client.sendall(self.messageToSend.pop())
+                        if mytime >= timeToCheckConnection:
+                            self.Client.sendall("") # to check connection
+                            timeToCheckConnection = time.time() + (self.checkConnectionEvery)
+                        while len(self.messageToSend) >0:
+                            self.Client.sendall(self.messageToSend.pop() + self.delimiter)
                 except IOError as err:
                     print(str(err))
                     keepConnectionOpen = False # client must be gone
-
-                
         #Cleanup
         self.s.close()
         
 myServer=CommandServer()
 myServer.start()
-time.sleep(5)
-myServer.sendMessage("message") 
\ No newline at end of file
+while True:
+    time.sleep(10)
+    myServer.sendMessage("I a ma chatterhead") 
\ No newline at end of file
"""