from CommandServer import CommandServer
class ObserverbleTest():
    def __init__(self):
        print "start"
        self.myCommandServer=CommandServer()
        self.myCommandServer.start()
        self.myCommandServer.registerObserver(self)
        
    def notify(self, subjectName, message):
        if subjectName == "CommandServer":
            self.handleTcpMessages(message)
            print subjectName + " says, got the message: " + message
        else:
            print subjectName + " says " + message
    def handleTcpMessages(self, message):
        if message == "pending":
            self.myCommandServer.sendMessage("connection accepted")
        elif message == "start video server":
            self.myCommandServer.sendMessage("video server is ready")
        elif message == "take picture":
             self.myCommandServer.sendMessage("image is ready")   
        elif message == "pretendToSwipe":
            self.myCommandServer.sendMessage("guestInfo:name:Kim Lindhard# birthday:1982-07-21# zipcode:2400# status:welcomed# lastVisit:2013-01-02##")
        elif message == "die":
            self.myCommandServer.stop()
myObserverbleTest = ObserverbleTest() # starts the class 