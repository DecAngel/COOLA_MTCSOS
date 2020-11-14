import socket
import hashlib
import json
import threading
import os
import time
import sys
import struct
import fcntl

class agent():
    def __init__(self,id):
        self.id=id
        self._port_temp=0

    def __send_message(self,sock,message):
        message=json.dumps(message)
        sock.send(message.encode())

    def get_info(self,path):
        filename=os.path.basename(path)
        filesize=os.path.getsize(path)
        md5=self.__get_md5(path)
        return filename,filesize,md5    

    def __get_md5(self,path):
        with open(path,'rb') as fr:
            md5=hashlib.md5()
            md5.update(fr.read())
            md5=md5.hexdigest()
            return md5

    def get_port(self):
        port=20000
        self._port_temp+=1
        #to do
        return port+self._port_temp
    
    def get_local_ip(self,ifname='wlan0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15],'utf-8')))[20:24])

    def send_file(self,id,port,path):
        def __send_file(id,port,path):
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.bind((self.get_local_ip(),port))
            sock.listen(5)
            for _ in range(5):
                client,_=sock.accept()
                time.sleep(0.1)
                info=json.loads(client.recv(1024).decode())
                if info[0]['id']==id:
                    if info[1]['state']==True:
                        #ready for send data
                        with open(path,encoding= 'utf-8') as fr:
                            sent_size=0
                            file_size=os.path.getsize(path)
                            while sent_size<file_size:
                                remained_size = file_size - sent_size
                                send_size = 1024 if remained_size>1024 else remained_size
                                send_file=fr.read(send_size)
                                sent_size+=send_size
                                client.send(send_file.encode())
                            client.close()
                            return
                else:
                    client.close()
        t=threading.Thread(target=__send_file,args=(id,port,path,))
        t.start()

    def recv_file(self,add,port,file_info,path):
        
        def __recv_file(add,port,file_info,path):
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((add,port))
            hello_message=[
                {
                    'id':self.id,
                },
                {
                    'state':True
                }
            ]
            hello_message=json.dumps(hello_message)
            sock.send(hello_message.encode())
            file_name=path
            file_size=file_info['size']
            md5=file_info['md5']
            
            recved_size=0
            with open(file_name,'wb') as fw:
                while recved_size < file_size:
                    remained_size=file_size-recved_size
                    recv_size = 1024 if remained_size>1024 else remained_size
                    recv_file=sock.recv(recv_size)
                    temp_size=len(recv_file)
                    if temp_size!=recv_size:
                        print('error for recv size')
                    recved_size=recved_size+recv_size
                    fw.write(recv_file)
                fw.close()
            md5_recv=self.__get_md5(file_name)
            if md5!=md5_recv:
                print('error for file recv')
                return False
            else:
                return True
        t=threading.Thread(target=__recv_file,args=(add,port,file_info,path,))
        t.start()
        