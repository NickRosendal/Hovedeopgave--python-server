'''
Created on Apr 12, 2013
M'%ROSENDAL^NICK LYNGGAARD           NAKSKOVVEJ 1 B 2 TH               1012500?;9208100403028831491001449084101010510?
M'%LINDHARD^KIM GRAVE                GR]SPURVEVEJ 55 4 -3              1012400?;9208100421078212631005452084101021211?
M'%JANSEN^JESPER WOLFRAM             HEDEPARKEN 7 7 E                  1512750?;9208100403089116671015725084151250712?
M'%JOHANSEN^SIGNE                    GRG]RDS ALLE 109                  1903500?;9208100423128617741010146084190180310?
'''
import re
def Interpitate(rawString):
    rawString = rawString.replace("[", "AE")
    rawString = rawString.replace("\\", "OE")
    rawString = rawString.replace("]", "AA")
    
    reobj = re.compile(r"'%(.*?)\^(.*?)   (\w.*?)   \d{3}(\d{4})\?;92081004(\d{6})\d{16}(\d{1})")
    match = reobj.search(rawString)
    if match:
        returnList = []
        for matchItem in match.groups():
            returnList.append(matchItem.strip())
        #returnList[1] = re.split(" ", returnList[1])
        #tempLastName = returnList[0]
        returnList[0] = returnList[1] + " " + returnList[0]
        del returnList[1]
        returnList[4] = "Male" if returnList[4] == "1" else "Female"
        
        return returnList
    else:
        return None

    
if __name__ == '__main__':
    print Interpitate("M'%JANSEN^JESPER WOLFRAM             HEDEPARKEN 7 7 E                  1512750?;9208100403089116671015725084151250712?")
    print Interpitate("M'%LINDHARD^KIM GRAVE                GR]SPURVEVEJ 55 4 -3              1012400?;9208100421078212631005452084101021211?")
    print Interpitate("M'%JOHANSEN^SIGNE                    GR\DSVG]RDS ALLE 109                1903500?;9208100423128617741010146084190180310?")