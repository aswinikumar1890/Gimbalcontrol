import json
import os
import time

class GimbalControl:
    '''
    controlling, fetching the gimbal current position of pitch,yaw
    '''

    def __init__(self,configfile):
        self.configfile = configfile
        print(self.reset)

    # def initilizegimbal():
        

    def update(self,data={}):
        '''
        updating the parameters of gimbal
        input:dict (json data of updated params)

        '''
        data['log'] = self.get('log')
        data['gimbal'] = self.get('gimbal')
        if self.get('gimbal') == 'active':
            with open(self.configfile,'w') as fileobj:
                json.dump(data,fileobj)
            return True
        else:
            return False

    def get(self,key):

        '''
        Getting the parameters of gimbal
        input:str (key for which the data/values to be retrived)
        output:dict/str (value for specific key)

        '''
        with open(self.configfile,'r') as fileobj:
            data = json.load(fileobj)
            if not data:
                data = {"GimbalControls": {"Stop": 0, "pitchDown": 0, "pitchUP": 0, "yawLeft": 0, "yawRight": 0}, "SweepControls": {"Speed": 5, "Sweep": 0, "angle": 10}, "GimbalStatus": {"error": 0, "ready": 1, "reset": 0}, "GimbalPos": {"pitch": 0.0, "roll": 0.0, "yaw": 0.0}, "Reboot": 0, "GetPos": 0, "SetPos": 0,"opc":0}
        return data.get(key)

    @property
    def getall(self):

        '''
        Getting the parameters of gimbal
        input:str (key for which the data/values to be retrived)
        output:dict/str (value for specific key)

        '''

        with open(self.configfile,'r') as fileobj:
            data = json.load(fileobj)
            if not data:
                data = {"GimbalControls": {"Stop": 0, "pitchDown": 0, "pitchUP": 0, "yawLeft": 0, "yawRight": 0}, "SweepControls": {"Speed": 5, "Sweep": 0, "angle": 10}, "GimbalStatus": {"error": 0, "ready": 1, "reset": 0}, "GimbalPos": {"pitch": 0.0, "roll": 0.0, "yaw": 0.0}, "Reboot": 0, "GetPos": 0, "SetPos": 0,"opc":0}
        return data

    def getdefaultvalues(self):

        '''
        Setting the default values for the gimbal params inorder to perform a single operation at a time
        '''

        posmap_default = {}
        gimbal_controls_reset = {"Stop" : 0,"pitchDown" : 0, "pitchUP" : 0, "yawLeft" : 0, "yawRight" : 0}
        sweepcontrols = {"Speed" : 10,"Sweep" : 0,"angle" : 10}
        gimbalstatus = {"error" : 0,"ready" : 1,"reset" : 0}
        gimbalpos = {"pitch":0.00,"roll":0.00,"yaw":0.00}
        posmap_default['GimbalControls'] = gimbal_controls_reset
        posmap_default['SweepControls'] = sweepcontrols
        posmap_default['GimbalStatus'] = gimbalstatus
        posmap_default['GimbalPos'] = gimbalpos
        posmap_default['Reboot'] = 0
        posmap_default["GetPos"] = 0
        posmap_default["SetPos"] = 0
        posmap_default["GetImu"] = 0
        posmap_default["gimbal"] = 'inactive'
        posmap_default["log"] = 'default log'
        posmap_default["opc"]=0
        posmap_default["imu"] = {"accX" : 0,"accY" : 0,"accZ" : 0,"gyroX" : 0,"gyroY" : 0,"gyroZ" : 0}
        return posmap_default

    @property
    def getposition(self):

        '''
        function for getting the present position of the gimbal pitch & yaw values
        input:NA
        output:dict
        '''
        gimbalparams = self.getall
        gimbalparams['GetPos'] = 1
        self.update(gimbalparams)
        time.sleep(0.1)
        position = self.get('GimbalPos')
        return position

    def moveto(self, op, pos):

        '''
        funtion moves the gimbal to a specific yaw and pitch
        input:str,
        op (operation)i.e. yaw,pitch
        input:float
        pos (position)i.e. 0.00
        '''

        try:
            position = self.getposition
            position[op] = pos
            return self.setposition(position)
        except Exception as e:
            return e

    def setposition(self, pos={"pitch":0.00,"roll":0.00,"yaw":0.00}):

        '''
        function for moving the position of the gimbal pitch/yaw values
        input:dict
        output:bool
        '''
        time.sleep(0.1)
        operation_completed = False
        gimbalparams = self.getdefaultvalues()
        gimbalparams['SetPos'] = 1
        gimbalparams['SweepControls']['Speed'] = self.get('SweepControls')['Speed']

        # pos['roll'] = 0.00
        gimbalparams['GimbalPos'] = pos
        if self.update(gimbalparams):
            time.sleep(0.1)
            while not operation_completed:
                with open(self.configfile,'r') as fileobj:
                    try:
                        data = json.load(fileobj)
                        if data['opc'] == 1:
                            operation_completed = True
                        else:
                            time.sleep(0.1)

                    except:
                        pass
            return True
        else:
            return self.get('log')

    @property
    def moveleft(self):
        gimbalparams = self.getdefaultvalues()
        gimbalparams['GimbalControls']['yawLeft'] = -1
        if not self.update(gimbalparams):
            return self.get('log')
        else:
            return 'operation intiated'
        time.sleep(0.05)
        self.stop

    @property
    def moveright(self):
        gimbalparams = self.getdefaultvalues()
        gimbalparams['GimbalControls']['yawRight'] = 1
        if not self.update(gimbalparams):
            return self.get('log')
        else:
            return 'operation intiated'
        time.sleep(0.05)
        self.stop

    @property
    def moveup(self):
        gimbalparams = self.getdefaultvalues()
        gimbalparams['GimbalControls']['pitchUP'] = 1
        if not self.update(gimbalparams):
            return self.get('log')
        else:
            return 'operation intiated'
        time.sleep(0.05)
        self.stop

    @property
    def movedown(self):
        gimbalparams = self.getdefaultvalues()
        gimbalparams['GimbalControls']['pitchDown'] = -1
        if not self.update(gimbalparams):
            return self.get('log')
        else:
            return 'operation intiated'
        time.sleep(0.05)
        self.stop

    @property
    def stop(self):
        gimbalparams = self.getdefaultvalues()
        gimbalparams['GimbalControls']['Stop'] = 1
        if not self.update(gimbalparams):
            return self.get('log')
        else:
            return 'operation intiated'

    @property
    def reset(self):
        gimbalparams = self.getdefaultvalues()
        gimbalparams['GimbalStatus']['reset'] = 1        
        if not self.update(gimbalparams):
            return self.get('log')
        else:
            return 'operation intiated'

    def setspeed(self,speed):
        gimbalparams = self.getall
        gimbalparams['SweepControls']['Speed'] = speed
        if not self.update(gimbalparams):
            return self.get('log')
        else:
            return 'operation completed'

    @property
    def getspeed(self):
        gimbalparams = self.getall
        return gimbalparams['SweepControls']['Speed']

    @property
    def getgimbalacc(self):
        gimbalparams = self.getall
        gimbalparams["GetImu"] = 1
        self.update(gimbalparams)
        time.sleep(0.1)
        return self.get('imu')

    def sweep(self,angle,speed):
        gimbalparams = self.getdefaultvalues()
        gimbalparams['SweepControls'] = {'Sweep':1,'Speed':speed,'angle':angle}
        if not self.update(gimbalparams):
            return self.get('log')
        else:
            return 'operation intiated'