from CommandServer import CommandServer
from MagtekUsbCardReader import MagtekUsbCardReader
import HealthInsuranceCardInterpreter
class ObserverbleTest():
    def __init__(self):
        print "start"
        self.myCommandServer = CommandServer()
        self.myCommandServer.registerObserver(self)
        self.myCommandServer.start()
        
        self.myMagtekUsbCardReader = MagtekUsbCardReader()
        self.myMagtekUsbCardReader.registerObserver(self)
        self.myMagtekUsbCardReader.startReading()
    def notify(self, subjectName, message):
        if subjectName == "CommandServer":
            self.handleTcpMessages(message)
            print subjectName + " says, got the message: " + message
        elif subjectName == "CardReader":
            cardString = HealthInsuranceCardInterpreter.Interpitate(message)
            print cardString
            print self.createCommandString(cardString)
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
            
    def createCommandString(self, list):
        if list == None:
            return
        returnString  = "guestInfo:name:" + str(list[0]) + "#"
        returnString += " birthday:" + str(list[3]) + "#"
        returnString += " zipcode:" + str(list[2]) + "#"
        returnString += "sex:" + str(list[4]) + "#"
        returnString += " status:" + "welcomed#"
        returnString += "lastVisit:NA"
        returnString += "#"
        return returnString 
myObserverbleTest = ObserverbleTest()  # starts the class 
