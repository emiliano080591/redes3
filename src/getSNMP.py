from pysnmp.hlapi import *
import os
import sys
import platform
from datetime import datetime

ips=[]

def consultaSNMP(comunidad,host,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado = varB.split()[2]
    return resultado


def consultaSNMP2(comunidad,host,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
    return varB

def obtener(comunidad, host):
    total_input_traffic = 0
    total_output_traffic = 0
    carga_CPU = 0
    carga_CPU2 = 0
    carga_CPU3 = 0
    try:
        total_input_traffic = (int(consultaSNMP(comunidad,host,'1.3.6.1.2.1.2.2.1.10.3'))/8388608)
        total_output_traffic = (int(consultaSNMP(comunidad,host,'1.3.6.1.2.1.2.2.1.16.3'))/8388608)
        #valor = str(total_input_traffic) + ',' + str(total_output_traffic)
        valor=[]
        valor.append(str(total_input_traffic))
        valor.append(str(total_output_traffic))
        return valor
    except:
        return False

def getDir(ip):
    ips.clear()
    ipDividida = ip.split('.')

    try:
        red = ipDividida[0]+'.'+ipDividida[1]+'.'+ipDividida[2]+'.'
        comienzo = 0
        fin = 10
    except:
        print("[!] Error")


    if (platform.system()=="Windows"):
        ping = "ping -n 1"
    else :
        ping = "ping -c 1"
        
    for subred in range(comienzo, fin+1):
        direccion = red+str(subred)
        response = os.popen(ping+" "+direccion)
        for line in response.readlines():
            if ("ttl" in line.lower()):
                ips.append(direccion)
                break
    return ips
