import importlib



class agent:
    def __init__(self,type_of_agent='G1-Raspberry'):
        self.agent=importlib.import_module(type_of_agent)
        self.agent.init()

    def action(self,action,args):
        self.agent.action(action,args)
    
    def get_sensor_list(self):
        return self.agent.get_sensor_list()

    def get_sensor_data(self,sensor_id):
        return self.agent.get_sensor(sensor_id)

    def get_state(self):
        return self.agent.get_state()
