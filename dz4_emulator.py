import sys # system params and function
import paho.mqtt.client as mqtt # mqtt paho
import json # json converter
import time # for sleep
from datetime import datetime # for date
from random import randint as rnd

# Координаты для автоуправления
coordinates = [(37.62359503704834, 55.74997322822742),
                   (37.61329197494335, 55.74796357031646),
                   (37.609365220945534, 55.74949455675656),
                   (37.61093163101024, 55.75240677878754),
                   (37.61233434274682, 55.75462901425888),
                   (37.61564743126333, 55.757111149696975),
                   (37.618161229063425, 55.75851171981781),
                   (37.62576194158182, 55.75950658848819),
                   (37.63022664932467, 55.7565759711743),
                   (37.63347497374119, 55.7536879726804),
                   (37.63209095388951, 55.74966111805039)]

# Получаем координаты по индексу. Индекс сохраняется к файле.
def get_coordinates(index):
    try: 
        indexCoordinates = int(index)
    except:
        print("Index is invalid!")
        return
        
    if indexCoordinates < len(coordinates):
        return (coordinates[indexCoordinates][0], coordinates[indexCoordinates][1])
    else:
        print("Index must be less than %d. Initial coordinates were returned." % (len(coordinates)))
        return (coordinates[0][0], coordinates[0][1])

def number_coordinates():
    return len(coordinates)

### machine and logic
class Machine():
    def __init__(self, mqtt_client, autocontrol = True, indexCoordinates = 0, longtitude = coordinates[0][0], latitude = coordinates[0][1], speed = 0, state = False):
        self.mqtt_client = mqtt_client     
        self.topic_data = "data/state"
        self.topic_change_state = "command/change_state"
        self.topic_change_control = "command/change_control"
        self.autocontrol = autocontrol
        self.indexCoordinates = indexCoordinates
        self.longtitude = longtitude
        self.latitude = latitude
        self.speed = speed 
        self.state = state
                
        self.mqtt_client.subscribe(self.topic_change_state)
        self.mqtt_client.message_callback_add(self.topic_change_state, self.command_change_state)
        self.mqtt_client.subscribe(self.topic_change_control)
        self.mqtt_client.message_callback_add(self.topic_change_control, self.command_change_control)

    def command_change_state(self, client, userdata, message):
        print("CMD: Change state, value: %s" % message.payload)   
        try:
            self.state = bool(message.payload.decode())
        except:
            print("can't change state to %s" % message.payload)
            
    def command_change_control(self, client, userdata, message):
        print("CMD: Change control, value: %s" % message.payload)   
        try:
            self.autocontrol = bool(message.payload.decode())
        except:
            print("can't change control to %s" % message.payload)
    
    # Автоматическое управление
    def circle_control(self):   
        if self.state:      # Если состояние Включен, то едем, изменяем координаты
            if self.indexCoordinates >= number_coordinates() - 1:
                self.indexCoordinates = 0
            else:
                self.indexCoordinates = self.indexCoordinates + 1
            
            coordinate = get_coordinates(self.indexCoordinates)
            self.longtitude = coordinate[0]
            self.latitude = coordinate[1]
            self.speed = rnd(0, 30)
        else:                
            self.speed = 0      # Иначе стоим
       
    # Ручное управление - просим ввести скорость и координаты
    def manual_control(self):
        message = input("Input speed: ")
        try:
            self.speed = int(message)
        except:
            print("can't set speed to %s. Speed = 0" % message)
            self.speed = 0
        message = input("Input longtitude: ")
        try:
            self.longtitude = float(message)
        except:
            print("can't set longtitude to %s. Longtitude = 0" % message)
            self.longtitude = 0
        message = input("Input latitude: ")
        try:
            self.latitude = float(message)
        except:
            print("can't set latitude to %s. Latitude = 0" % message)
            self.latitude = 0
        

    def data_upd(self):
        
        if self.autocontrol:
            self.circle_control()
        else:
            self.manual_control()
           
        print("longtitude= %f " % ( self.longtitude))
        print("latitude= %f " % ( self.latitude))
        print("speed = %d " % ( self.speed))
        print("index = %d " % ( self.indexCoordinates))
        
        try:
            f = open('./state_machine.txt', 'r')
            file = f.read()
            config = json.loads(file)    
            f.close()
        except:
            config = {}
        f = open('./state_machine.txt', 'w')
        config["index"] = self.indexCoordinates
        config["longtitude"] = self.longtitude
        config["latitude"] = self.latitude
        config = json.dumps(config)
        f.write('%s' % config)
        f.close()

    def get_data(self):
        data = json.dumps({"state":self.state, "autocontrol":self.autocontrol, "speed":self.speed, "longtitude":self.longtitude, "latitude":self.latitude, "time": str(datetime.now())})
        return data

# init mqtt
def init(clientid, clientUsername="", clientPassword=""):
    client = mqtt.Client(client_id=clientid)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username = clientUsername, password = clientPassword)
    return client
# connect reaction
def on_connect(client, userdata, flags, rc):
    print("Connected with result code %s" % str(rc))
    if rc == 0:
        isConnect = 1
        client.publish("connect", "true", 1)
    if rc == 5:
        print("Authorization error")
# default message reaction
def on_message(client, userdata, message):
    print("Some message received topic: %s, payload: %s" % (message.topic, message.payload))   
# connect to server
def publish_data(client, topic, data):
    print(topic, data)
    return client.publish(topic, data) 

def run(client, host="127.0.0.1", port=1883):
    client.connect(host, port, 60)
    client.loop_start()
# function for publish data

# body of emulator
def main():
    # create mqtt with id clinet_id
    mqtt_client = init("client_id")
    run(mqtt_client)
    # read config
    autocontrol = True
    indexCoordinates = 0
    longtitude = get_coordinates(0)[0]
    latitude = get_coordinates(0)[1]
    argv = sys.argv;
    try:
        path_to_config = argv[1] if len(argv) > 1 else "./state_machine.txt"
        f = open(path_to_config, 'r')
        file = f.read()
        config = json.loads(file)    
        f.close()   
        indexCoordinates = int(config["index"])
        longtitude = get_coordinates(indexCoordinates)[0]
        latitude = get_coordinates(indexCoordinates)[1]
        print("read config %s" %config)
    except:
        pass
    
    # Включение автоуправления, изменить можно по сообщению с брокера
    while True:
        msg = input("Is Autocontol ON?(yes/no): ").lower() 
        if msg == "yes":
            autocontrol =  True
            break
        if msg == "no":
            autocontrol =  False
            break
        print("Input yes or no. Is Autocontol ON? ")
    
    # init machine
    machine = Machine(mqtt_client, autocontrol, indexCoordinates, longtitude, latitude)

    while True:
        time.sleep(2)
        machine.data_upd()
        ret = publish_data(mqtt_client, machine.topic_data, machine.get_data())
        
        if ret[0] != 0:
            print("Fail publish. Save this message if you need")
        else:
            pass

        
if __name__ == '__main__':
    main()