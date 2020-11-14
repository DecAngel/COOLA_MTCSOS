import socket
import threading
import queue
import json
import struct
import fcntl

class agent():
    def __init__(self,center_address):
        self.__sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_recv=queue.Queue()
        self.__lock_message_recv=threading.Lock()
        self.active_socks={}
        self.__lock_socks=threading.Lock()
        self.allow_id=set()
        self.id=-1
        self.__connect_center(center_address)
        threading.Thread(target=self.__wait_connect).start()

    def send_order_to(self,id,order):
        sock=self.get_socks(id)
        sock.send(json.dumps(order).encode())
        return True
        
    def get_id(self):
        if self.id!=-1:
            return self.id
        else:
            return None
    
    def __connect_center(self,address):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        #等待中心分配id
        mess=json.loads(sock.recv(1024).decode())
        if mess[0]['id']==0:
            self.id=mess[1]['id']
            self.active_socks[0]=sock
            ##ack
            ack=0
            ackm=[
                {
                    'id':self.id
                },
                {
                    'state':ack
                }
            ]
            self.active_socks[0].send(json.loads(ackm).encode())
            threading.Thread(target=self.__listen,args=(0,)).start()
            return True
        return False
    
    def get_local_ip(self,ifname='wlan0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15],'utf-8')))[20:24])

    def __wait_connect(self):
        self.__sock_server.bind((self.get_local_ip(),10000))
        self.__sock_server.listen(5)
        while True:
            c,a=self.__sock_server.accept()
            threading.Thread(target=self.__put_socket,args=(c,a,)).start()
            
    def __put_socket(self,sock,address):
        #等待对方id信息
        idmessage=json.loads(sock.recv(1024).decode())
        
        id=idmessage[0]['id']
        if id in self.allow_id:
            self.__lock_socks.acquire()
            self.active_socks[id]=sock
            self.__lock_socks.release()
            self.__send_ack_to(id)
            threading.Thread(target=self.__listen,args=(id,)).start()
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
    
    def __deal_message(self,buf):
        while True:
            end=buf.find(']')
            if end!=-1:
                self.put_message(buf[:end+1])
                buf=buf[end+1:]
            else:
                break
        return buf

    def __send_id_to(self,sock):
        idm=[
            {
                'id':self.id
            },
            {
                'state':None
            }
        ]
        sock.send(json.dumps(idm).encode())

    def __send_ack_to(self,id):
        ack=0
        ackm=[
                {
                    'id':self.id
                },
                {
                    'state':ack
                }
            ]
        self.active_socks[id].send(json.dumps(ackm).encode())

    def delete_connect(self,id):
        if id==0:
            return False
        self.__lock_socks.acquire()
        self.active_socks[id].close()
        self.__lock_socks.release()
        self.allow_id.discard(id)
        return True

    def wait_id_connect(self,id):
        self.allow_id.add(id)

    def create_socket_to_connect(self,ip,port):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip,port))
        self.__send_id_to(sock)
        message=json.loads(sock.recv(1024).decode())
        if message[1]['state']==0:
            self.__lock_socks.acquire()
            self.active_socks[message[0]['id']]=sock
            self.__lock_socks.release()
            threading.Thread(target=self.__listen,args=(message[0]['id'],)).start()
            return True
        return False
        
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