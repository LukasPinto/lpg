import getopt, sys
import re
from subprocess import Popen,PIPE
import socket

archivo=Popen(["curl","-0","https://gitlab.com/wireshark/wireshark/-/raw/master/manuf"],stdout=PIPE)
archivo=archivo.communicate()[0].decode("utf-8")
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
    try:
        optlist,args=getopt.getopt(commandLineArgs,unixOptions,gnuOptions)
        
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    if optlist==[]:
        print("Error: No ingresó ningun parametro")
        usage()
        sys.exit()
    for o, a in optlist:
        if o in ("--help") or o in ("-h"):
            usage()
            sys.exit()
        elif o in ("--ip") or o in ("-i"):
            output,param=a,o
            return output,param
        elif o in ("--mac") or o in ("-m"):
            output,param=a,o
            return output,param
        else:
            print("Error: Faltan parametros obligatorios.")
            usage()
            sys.exit()
if __name__=="__main__":
    output,param=main()
    lineas=[]
    output=output.upper()
    lineas_parser=archivo.split("\n")
    for linea in lineas_parser:
        lineas.append(str(linea).split("\t"))
    for linea in lineas:
        if "#" in linea[0] or linea[0] in "":

            lineas.pop(lineas.index(linea)) 
    print("\n\n-----------------------------------\n\n")       
    if checkMAC(output) and len(output)>0 and (param=="-m" or param=="--mac"):
        output=output.replace("-",":")
        for linea in lineas:
            if(linea[0]==output[:8]):
                print("MAC address : "+output)
                print("Vendor      : "+linea[2])
                break
            elif(linea==lineas[len(lineas)-1]):
                print("MAC address : "+output)
                print("Vendor      : Not found")
                break
    elif(checkIP(output) and len(output)!=0) and (param=="-i" or param=="--ip"):
        commandLine=Popen(["arp","-n",output],stdout=PIPE)
        s=commandLine.communicate()[0].decode("utf-8")
        if s.find(output)==-1:
            print("Error: ip is outside the host network")
        else:
            if(re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s)==None):
            	print("Error: ip is outside the host network ")
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
