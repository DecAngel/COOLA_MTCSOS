import socket
import threading
import queue
import json
import struct
import fcntl

class agent():
    def __init__(self,id=0):
        self.id=id
        self.__sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active_socks={}
        self.message_recv=queue.Queue()
        self.__lock_message_recv=threading.Lock()
        self.__lock_socks=threading.Lock()
        threading.Thread(target=self.__wait_connect).start()
    
    def get_local_ip(self,ifname='wlan0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15],'utf-8')))[20:24])

    def __wait_connect(self):
        self.__sock_server.bind((self.get_local_ip(),10000))
        self.__sock_server.listen(5)
        while True:
            c,a=self.__sock_server.accept()
            threading.Thread(target=self.__put_socket,args=(c,a,)).start()
    
    def __new_id(self):
        newid=-1
        for i in range(1,100):
            if i in self.active_socks:
                continue
            newid=i
            return newid
        return None

    def __put_socket(self,sock,address):
        #分配id信息
        newid=self.__new_id()
        idm=[
            {
                'id':0
            },
            {
                'id':newid
            }
        ]
        sock.send(json.dumps(idm).encode())

        mess=json.loads(sock.recv(1024).decode())
        if mess[0]['id']==newid and mess[1]['state']==0:
            self.__lock_socks.acquire()
            self.active_socks[newid]=sock
            self.__lock_socks.release()
            threading.Thread(target=self.__listen,args=(newid,)).start()
            return True
        return False
    
    def __listen(self,id):
        sock_c=self.get_socks(id)
        buf=''
        while True:
            message = sock_c.recv(1024)
            message=message.decode()
            buf=buf+message
            buf=self.__deal_message(buf)
            
    def send_order_to(self,id,order):
        sock=self.get_socks(id)
        sock.send(json.dumps(order).encode())
        return True

    def __deal_message(self,buf):
        while True:
            end=buf.find(']')
            if end!=-1:
                self.put_message(buf[:end+1])
                buf=buf[end+1:]
            else:
                break
        return buf

    def get_socks(self,id):
        self.__lock_socks.acquire()
        c=self.active_socks.get(id)
        self.__lock_socks.release()
        return c
        
    def put_message(self,message):
        self.__lock_message_recv.acquire()
        self.message_recv.put(message)
        self.__lock_message_recv.release()

    def get_message(self):
        self.__lock_message_recv.acquire()
        if self.message_recv.empty():
            mess=None
        else:
            mess=json.loads(self.message_recv.get())
        self.__lock_message_recv.release()
        return mess
    