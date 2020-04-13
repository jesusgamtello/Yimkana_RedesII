#!/usr/bin/python3

from socket import *
import re
import hashlib
from base64 import b64encode
import struct
import array


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
                print(msg.decode())
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

        msg=sock.recv(1024)
        print(msg.decode())

        return msg.decode().split(":")[1]

    #YAP               
    def reto5(self,key):
        sock=socket(AF_INET,SOCK_DGRAM)
        server=('node1',7000)
        final_key=key.split('\n')[0]
        
        final_key=b64encode(final_key.encode())
        checksum= '0'
        header=b'YAP'+b'\x00\x00'+b'\x00'+checksum.encode()
        msg=header+final_key
        checksum=str(self.checksum(str(msg)))
        print("ultimo metodo\n",checksum)

        checksum1=str(self.checksum1(str(msg)))
        print("primer metodo\n",checksum1)

        header=b'YAP'+b'\x00\x00'+b'\x00'+checksum.encode()
        msg=header+final_key
        print(msg)
        sock.sendto(msg,server)
        msg,server=sock.recvfrom(1024)
        print(msg)

    def checksum1(self,msg):
        s = 0
        # loop taking 2 characters at a time
        for i in range(0, len(msg), 2):
            w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
            s = s + w

            s = (s>>16) + (s & 0xffff)
            s = s + (s >> 16)

            #complement and mask to 4 byte short
            s = ~s & 0xffff

            return s


    '''def checksum(self,data, sum=0):
        # make 16 bit words out of every two adjacent 8 bit words in the packet
        # and add them up
        for i in range(0,len(data),2):
            if i + 1 >= len(data):
                sum += ord(data[i]) & 0xFF
            else:
                w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i+1]) & 0xFF)
                sum += w

        # take only 16 bits out of the 32 bit sum and add up the carries
        while (sum >> 16) > 0:
            sum = (sum & 0xffff) + (sum >> 16)

        # one's complement the result
        sum = ~sum

        return sum & 0xffff'''

    def checksum(self,pkt):
        if len(pkt) % 2 == 1:
                pkt += "\0"
        s = sum(array.array("H", pkt))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        s = ~s
        
        return s & 0xffff or 0xffff

def main():
    y=yinkana()

    
    key=y.reto0()
    key=y.reto1(key)
    key=y.reto2(key)
    key=y.reto3(key)
    key=y.reto4(key)
    y.reto5(key)

main()