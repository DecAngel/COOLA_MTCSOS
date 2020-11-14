#config
BASIC_PATH='/home/pi/DATA'
#json包格式
'''
    [
        {
            'ID':self id
            'TYPE':order type
        },
        {
            ...具体指令内容
        }
    ]
'''
#ORDER TYPE
TYPE_ACTION = 1 #行动 如移动 转动云台等
TYPE_SEND_FILE = 2
TYPE_SEND_FOLDER = 3
TYPE_MODEL = 4
TYPE_MKDIR = 5
TYPE_READ_SENSOR = 6
TYPE_SENSOR_LIST = 7