#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import json
import datetime
import time

class TestScreen:
    def getScreenFile(self,filnepath):
        fuac=open(filnepath,"r")
        uacLine=fuac.readlines()
        fuac.close()
        output={}
        output["statistics"]={}
        output["repartition"]={}

        for idx in range(len(uacLine)):
            line=uacLine[idx]
            if line.find("Timestamp") != -1:
                timestamp=datetime.datetime.strptime(re.sub("^.*Timestamp\s*:\s*","",line).strip(),"%c")
                output["timestamp"]=str(time.mktime(timestamp.timetuple()))
            if line.find("Total-time") != -1:
                sepidx=[]
                words=re.sub("\s+"," ",line).strip().split()
                for word in words:
                    sepidx.append(line.find(word))
                sepidx.append(-1)
                lastline=line
                idx+=1
                line=uacLine[idx]
                for i in range(len(sepidx)-1):
                    key=lastline[sepidx[i]:sepidx[i+1]].strip().replace(" ","-").lower()
                    val=line[sepidx[i]:sepidx[i+1]].strip()
                    output[key]=val

            if line.find("Unexpected-Msg") != -1:
                suboutput=[]
                msgidx=line.find("Messages")
                retransidx=line.find("Retrans")
                timeoutidx=line.find("Timeout")
                unexpectedidx=line.find("Unexpected")

                dirsidx=-1
                dirtidx=-1
                typesidx=-1
                typetidx=-1

                while True:
                    idx+=1
                    line=uacLine[idx]
                    # calliburation
                    if dirsidx==-1:
                        dirsidx=line[:msgidx].find("<--")
                        if dirsidx==-1:
                            dirsidx=line[:msgidx].find("---")
                        dirtidx=dirsidx+len(re.sub("\s+"," ",line[:msgidx][dirsidx:]).split()[0])
                        if line.strip()[0] == "<" or line.strip()[0] == "-" or line.strip()[0] == "[":
                            typesidx=dirtidx+1
                            typetidx=msgidx
                        else:
                            typesidx=0
                            typetidx=dirsidx

                            

                    if line.find("Waiting for active calls to end.") != -1:
                        break
                    if len(line.strip())==0:
                        continue
                    subsuboutput={}
                    if line[dirsidx] == "-":
                        subsuboutput["direction"]="sent"
                        if typesidx>dirsidx:
                            subsuboutput["direction"]="recieved"
                    elif line[dirsidx] == "<":
                        subsuboutput["direction"]="recieved"
                        if typesidx>dirsidx:
                            subsuboutput["direction"]="sent"
                    else:
                        subsuboutput["information"]=line[dirsidx:dirtidx]
                    subsuboutput["message-type"]=line[typesidx:typetidx].strip().split()[0].strip()
                    subsuboutput["messages"]=line[msgidx:retransidx].strip()
                    subsuboutput["retrans"]=line[retransidx:timeoutidx].strip()
                    subsuboutput["timeout"]=line[timeoutidx:unexpectedidx].strip()
                    subsuboutput["unexcepted"]=line[unexpectedidx:].strip()
                    suboutput.append(subsuboutput)
                output["messages"]=suboutput

            if line.find("Statistics Screen") != -1:
                for i in range(3):
                    idx+=1
                    words=re.sub("\s+"," ",uacLine[idx]).split("|")
                    output["statistics"][words[0].strip()]=words[1].split()[2]
            
            if line.find("Counter Name") != -1:
                output["statistics"]["periodic"]={}
                output["statistics"]["cummulative"]={}
                for i in range(20):
                    idx+=1
                    line=uacLine[idx]
                    if line.find("Waiting for active calls to end.")!=-1:
                        break
                    if line.find("-----") != -1:
                        continue
                    words=re.sub("\s+"," ",line).split("|")
                    output["statistics"]["periodic"][words[0].strip().replace(" ","-").lower()]=words[1].strip()
                    output["statistics"]["cummulative"][words[0].strip().replace(" ","-").lower()]=words[2].strip()

            if line.find("Average Response Time") != -1:
                output["repartition"]["average-response-time"]={"fields":[],"values":[]}
                for i in range(9):
                    idx+=1
                    line=uacLine[idx]
                    words=re.sub("\s+"," ",line).split(":")
                    output["repartition"]["average-response-time"]["fields"].append(words[0].strip())
                    output["repartition"]["average-response-time"]["values"].append(words[1].strip())

            if line.find("Average Call Length") != -1:
                output["repartition"]["average-call-length"]={"fields":[],"values":[]}
                for i in range(8):
                    idx+=1
                    line=uacLine[idx]
                    words=re.sub("\s+"," ",line).split(":")
                    output["repartition"]["average-call-length"]["fields"].append(words[0].strip())
                    output["repartition"]["average-call-length"]["values"].append(words[1].strip())

        return output

if __name__ == "__main__":
    test=TestScreen()
    print "["
    print json.dumps(test.getScreenFile("/tmp/uac_screen_file"))
    print ","
    print json.dumps(test.getScreenFile("/tmp/uas_screen_file"))
    print "]"


