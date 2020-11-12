import getopt, sys, os
import re
import string
from subprocess import Popen,PIPE
import socket

archivo=open("manuf.txt","r")
def checkMAC(Mac):
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", Mac.lower()):
        return True
    else:
        return False
def usage():
    print("Use: ./OUILookup --ip <IP> | --mac <MAC>. [--help]\n--ip : specify the IP of the host to query.\n--mac: specify the MAC address to query(AA:BB:CC:00:00:00).)\n--help: show this message and quit.\n")
def checkIP(Ip):  
    try:
        socket.inet_aton(Ip)
        return True
    except:  
        return False
def main():
    commandLineArgs = sys.argv[1:]
    unixOptions="hi:m:"
    gnuOptions=["help","ip=","mac="]
    output = None
    #verbose=False
    try:
        optlist,args=getopt.getopt(commandLineArgs,unixOptions,gnuOptions)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for o, a in optlist:
        #if o=="-v":
         #   verbose=True
        if o in ("--help"):
            usage()
            sys.exit()
        elif o in ("--ip"):
            output,param=a,o
            return output,param
        elif o in ("--mac"):
            output,param=a,o
            return output,param
        else:
            assert False, "unhandled option"
if __name__=="__main__":
    output,param=main()
    #print(output,param)
    #print(checkMAC(output))
    lineas=[]
    output=output.upper()
    for i in archivo:
        lineas.append(i.split("\t"))
    if checkMAC(output) and len(output)>0 and (param=="-m" or param=="--mac"):
        output=output.replace("-",":")
        #print(lineas)
        for linea in lineas:
            if(linea[0]==output[:8]):
                print("MAC address : "+output)
                print("Vendor      : "+linea[2])
                break
            elif(linea==lineas[len(lineas)-1]):
                print("MAC address : "+output)
                print("Vendor      : Not found")
                break
    elif(checkIP(output) and len(output)!=0) and (param=="-p" or param=="--ip"):
        #print("es una IP valida")
        commandLine=Popen(["arp","-n",output],stdout=PIPE)
        s=commandLine.communicate()[0].decode("utf-8")
        print(s)
        if s.find(output+" ("+output+")")!=-1:
            print("Error: ip is outside the host network")
        else:
            mac=re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]
            for linea in lineas:
                if(linea[0]==mac[:8].upper()):
                    print("MAC address : "+mac)
                    print("Vendor      : "+linea[2])
                    break
                elif(linea==lineas[len(lineas)-1]):
                    print("MAC address : "+mac)
                    print("Vendor      : Not found")
                    break


    else:
        usage()
        sys.exit()
archivo.close()
