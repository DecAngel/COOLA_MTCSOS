import time
import threading
import os
import lib.transform.data_send_recv_agent as data_agent
import lib.transform.order_send_recv_agent as order_agent
import lib.hardware.agent as hard_agent
import lib.control.order_config as config
class agent:

    def __init__(self,center_host):
        self.orderor=order_agent.agent(center_address=center_host)
        time.sleep(10)
        self.id=self.orderor.get_id()
        self.dataor=None
        if self.id!=None:
            self.dataor=data_agent.agent(self.id)
        self.agent=hard_agent.agent('raspberrypi')

    def fetch_order(self):
        return self.orderor.get_message()

    def __deal_task(self):
        while True:
            order = self.fetch_order()
            if order is None:
                time.sleep(0.2)
                continue
            elif order[0]['TYPE']==config.TYPE_ACTION:
                pass
            elif order[0]['TYPE']==config.TYPE_SEND_FILE:
                self.recv_file_from(order)
            elif order[0]['TYPE']==config.TYPE_MKDIR:
                self.mkdir(path=order[1]['PATH'])

    def send_floder_to(self,target_id,folder_path,target_path='None'):
        def __send_folder(target_id,folder_path,target_path='None'):
            folder_info=[]
            for i,j,k in os.walk(folder_path):
                folder_info.append([i,j,k])
            start=folder_info[0][0].rfind('/')
            for folder in folder_info:
                p_fo=folder[0][start:]
                self.mkdir_to(p_fo,target_id)
                for f in folder[2]:
                    f_p=folder[0]+'/'+f
                    self.send_file_to(target_id,f_p,f_p[start:])
            pass
        t=threading.Thread(target=__send_folder,args=(target_id,folder_path,target_path,))
        t.start()            

    def send_file_to(self,target_id,file_path,save_path):
        filename,filesize,md5=self.dataor.get_info(path=file_path)
        port=self.dataor.get_port()
        message=[
            {
                'ID':self.id,
                'TYPE':config.TYPE_SEND_FILE
            },
            {
                'address':self.dataor.get_local_ip(),
                'port':port,
                'filename':filename,
                'filesize':filesize,
                'md5':md5,
                'path':save_path
            }
        ]
        self.orderor.send_order_to(target_id,message)
        self.dataor.send_file(id=target_id,port=port,path=file_path)
    

    def recv_file_from(self,order):
        add=order[1]['address']
        port=order[1]['port']
        file_info={
            'size':order[1]['size'],
            'name':order[1]['filename'],
            'md5':order[1]['md5']
        }
        save_path=config.BASIC_PATH+order[1]['path']
        self.dataor.recv_file(add,port,file_info,save_path)
              

    def mkdir_to(self,target_path='',target_id=0):
        message=[
            {
                'ID':self.id,
                'TYPE':config.TYPE_MKDIR
            },
            {
                'PATH':target_path
            }
        ]
        self.orderor.send_order_to(target_id,message)


    def mkdir(self,path):
        if os.path.exists(path):
            return
        else:
            os.mkdir(path)

