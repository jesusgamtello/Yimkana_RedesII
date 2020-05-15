#!/usr/bin/python3

from socket import *
import re
import hashlib
from base64 import b64encode
from base64 import b64decode
import struct
import json
import urllib.request
import urllib.response
import datetime 
import locale

class yinkana():
   
    def reto0(self):

        sock=socket(AF_INET,SOCK_STREAM)
        server=('node1',2000)
        sock.connect(server)


        msg=sock.recv(1024)
        #print(msg.decode())

        sock.send("jesus.gamero".encode())
        msg=sock.recv(1024)
        sock.close()
        key_to_reto=msg.decode().split('\n')[0]
        return key_to_reto

        

    def reto1(self,key):
        sock=socket(AF_INET,SOCK_DGRAM)
        server=('node1',3000)
        port=1515
        sock.bind(('0.0.0.0',port))
        msg=str(port)+' '+key
        sock.sendto(msg.encode(),server)
        msg,server=sock.recvfrom(1024)
        sock.close()
        key_to_reto=msg.decode().split('\n')[0]
        return key_to_reto


    #Word counter
    def reto2(self,key):
        sock=socket(AF_INET,SOCK_STREAM)
        server=('node1',4000)
        sock.connect(server)
        salir=0
        msg=sock.recv(1024)
        while True:
            for i in msg.decode().split():
                if i=="that's":
                    salir=1
                    break
            msg=msg+sock.recv(1024)
            if salir==1:
                break

        

        contador=0
        for i in msg.decode().split():
            if i!="that's":
                contador+=1
            else:
                break
       
        mensaje=key.split(':')[1]+' '+str(contador)
        sock.send(mensaje.encode())
        
        while True:
            msg=sock.recv(1024)
            
            if msg.decode().split(':')[0]=='code':
                break

        
       
        sock.close()
        return msg.decode().split(':')[1]
    
    #Reverse
    def reto3(self,key):
        sock=socket(AF_INET,SOCK_STREAM)
        server=('node1',6000)
        sock.connect(server)
        pat = re.compile("\w+")
        final_message='--'+key.split('\n')[0]+'--'
        salir=0
        aux=''

        msg=sock.recv(1024)
        while True:
            msg=msg+sock.recv(1024)
            for i in msg.decode().split():
                if self.palindrome(i):
                    salir=1
                    break
            
            if salir==1:
                break
            
            
        aux=''
        for i in msg.decode().split():
            if i.isdigit():
                if aux=='':
                    aux+=i
                else:
                    aux+=' '+i
            else:
                if not self.palindrome(i):
                    if aux=='':
                        aux+=pat.sub(self.invert_method, i)
                    else:
                        aux+=' '+pat.sub(self.invert_method, i)
                else:
                    break

    
        sock.send(aux.encode())
        sock.send(final_message.encode())

        while True:
            msg=sock.recv(1024)
            
            
            if msg.decode().split(':')[0]=='code':
                break

        sock.close()
        return msg.decode().split(':')[1]

    def invert_method(self,m):
        return m.group(0)[::-1]

    def palindrome(self,s):
        s=s.lower()
        if not s.isdigit() and len(s)>1:
            if s == s[::-1]:
                return True
            else: 
                return False
        else:
            return False
    

    #MD5
    def reto4(self,key):
        sock=socket(AF_INET,SOCK_STREAM)
        server=('node1',10000)
        sock.connect(server)
        final_key=key.split('\n')[0]
        
        sock.send(final_key.encode())
        msg=sock.recv(1024)
        sum=msg.split(b':',1)[1]
        size=msg.split(b':',1)[0].decode()
        m=hashlib.md5()
       
        while int(size)!=len(sum):
            sum+=sock.recv(1024)

        m.update(sum)
        md5=m.digest()
        sock.send(md5)

        msg=sock.recv(2048)
        print(msg.decode())

        return msg.decode().split(":")[1]

    #YAP               
    def reto5(self,key):
        sock=socket(AF_INET,SOCK_DGRAM)
        server=('node1',7000)
        final_key=key.split('\n')[0]
        
        final_key=b64encode(final_key.encode())
        checksum= '0'
        header=struct.pack('!3sBHH',b'YAP',0,0,0)
        msg=header+final_key
        checksum=self.checksum(msg)
       
        header=struct.pack('!3sBHH',b'YAP',0,0,checksum)
        msg=header+final_key
        sock.sendto(msg,server)
        msg,server=sock.recvfrom(2048)
        msg=msg[8:]
        msg=b64decode(msg)
        print(msg.decode())

        return msg.decode().split(":")[1]
       
    #codigo sacado de https://bitbucket.org/DavidVilla/inet-checksum/src/master/inet_checksum.py
    def sum16(self,data):
        if len(data) % 2:
            data += '\0'.encode()

        return sum(struct.unpack("!%sH" % (len(data) // 2), data))

    def checksum(self,data):
       
        sum_as_16b_words  = self.sum16(data)
        sum_1s_complement = self.sum16(struct.pack('!L', sum_as_16b_words))
        _1s_complement    = ~sum_1s_complement & 0xffff
        return _1s_complement


    def reto6(self,key):
        
        final_key=key.split('\n')[0]
        sock = socket(AF_INET,SOCK_STREAM)
        server = ('node1', 8003)
        sock.connect(server)
        msg=(final_key+' '+'1515').encode()
        sock.send(msg)
       


        sock_serverhttp=socket(AF_INET,SOCK_STREAM)
        sock_serverhttp.bind(('0.0.0.0',1515))
        sock_serverhttp.listen(100)
        while True:
            sck,server=sock_serverhttp.accept()
            msg=sck.recv(1024)
            print(msg.decode())

            rfc=msg.decode()
            peticion=rfc.split('\n')[0]
            getorpost=peticion.split()[0]
            print(getorpost)
            if getorpost=='POST':
                print('la cabecera es ',getorpost)
                nuevo_reto=rfc.split("code:")[1]
                print(nuevo_reto.split()[0])
                return nuevo_reto.split()[0]
        

            rfc=rfc[rfc.find('rfc'):rfc.find('HTTP')-1]
            #print(rfc)
            
            req= urllib.request.Request(url='https://uclm-arco.github.io/ietf-clone/rfc/'+rfc)
        
            with urllib.request.urlopen(req) as url:
                texto=url.read().decode("utf-8")

            date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') 
            '''sck.send('HTTP/1.1 200 OK\r\n'.encode("utf-8"))
            sck.send(('Date: '+date+'\r\n').encode("utf-8"))
            sck.send('Content-Type: text/plain\r\n'.encode("utf-8"))
            sck.send(('Content-Length: '+str(len(texto))+'\r\n').encode("utf-8"))
            sck.send('\n'.encode("utf-8"))'''

            cabecera='HTTP/1.1 200 OK\r\n'+'Date: '+date+'\r\n'+'Content-Type: text/plain\r\n'+'Content-Length: '+str(len(texto))+'\r\n'
            paquete=cabecera+texto+'\r\n'
            
            sck.send(paquete.encode())
            #sck.send('\r\n'.encode("utf-8"))
            print('envio')
       
        sock_serverhttp.close()
        sock.close()
    
    def reto7(self,key):
        sock = socket(AF_INET,SOCK_STREAM)
        server = ('node1', 33333)
        sock.connect(server)
        msg=(key).encode()
        sock.send(msg)
        msg=sock.recv(1024)
        print(msg.decode())
        

def main():
    y=yinkana()

    
    key=y.reto0()
    key=y.reto1(key)
    key=y.reto2(key)
    key=y.reto3(key)
    key=y.reto4(key)
    key=y.reto5(key)
    key=y.reto6(key)
    y.reto7(key)

main()