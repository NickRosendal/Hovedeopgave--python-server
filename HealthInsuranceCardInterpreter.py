import re
import datetime
def Interpitate(rawString):
    rawString = rawString.replace("[", "AE")
    rawString = rawString.replace("\\", "OE")
    rawString = rawString.replace("]", "AA")
    
    reobj = re.compile(r"'%(.*?)\^(.*?)   (\w.*?)   \d{3}(\d{4})\?;92081004(\d{6})(\d{4})\d{12}(\d{1})")
    match = reobj.search(rawString)
    if match:
        returnList = []
        returnList.append(match.group(2).strip() + " " + match.group(1))
        returnList.append(datetime.datetime.strptime(str(match.group(5)), "%d%m%y").date().__str__())
        returnList.append("M" if match.group(7) == "1" else "F")
        return returnList
    else:
        return None

    
if __name__ == '__main__':
    print Interpitate("M'%JANSEN^JESPER WOLFRAM             HEDEPARKEN 7 7 E                  1512750?;9208100403089115671015725084151250712?")
    print Interpitate("M'%LINDHARD^KIM GRAVE                GR]SPURVEVEJ 55 4 -3              1012400?;9208100421078214611005452084101021211?")
    print Interpitate("M'%JOHANSEN^SIGNE                    GR\DSVG]RDS ALLE 109                1903500?;9208100423128617740010146084190180310?")
    print Interpitate("M'%ROSENDAL^NICK LYNGGAARD           NAKSKOVVEJ 1 B 2 TH               1012500?;9208100403028832501001449084101010510?")