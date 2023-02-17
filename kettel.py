import keyboard, time, msvcrt

class Kettel:
    """Класс чайник"""
    volume: float # объем чайника
    water: float = 0 # количество воды в чайнике
    curTemperature: int = 0 # температура воды в чайнике
    endTemperature: int # температура автоматического выключения чайника
    heatingTime: int # время кипения
    switch: bool = False # состояние выключателя

    def __init__(self, volume, temperature, heatingTime):
        """Конструктор принимает объем чайника, температуру автоматического выключения и время кипения"""
        self.volume = volume
        self.endTemperature = temperature
        self.heatingTime = heatingTime

    def getCurTemperature(self): 
        """Метод для проверки текущей температуры воды"""
        temperature = self.curTemperature
        return temperature

    def getEndTemperature(self):
        """Метод для проверки температуры автоматического выключения"""
        temperature = self.endTemperature
        return temperature
    
    def setWater(self, new_water): 
        """Метод для задания количества воды в чайнике"""
        self.water = new_water

    def increaseTemperature(self): 
        """Метод для повышения температуры воды (за 1 секунду)"""
        self.curTemperature += 100 / self.heatingTime

    def switchOn(self):
        """Метод для включения тумблера"""
        print("вкл (для выключения нажмите любую клавишу...)")
        self.switch = True
    
    def switchOff(self): 
        """Метод для выключения тумблера"""
        self.switch = False
        print("остановлен")

def boiling(kettel, logs):
    """Выводит статистику на консоль и в файл логов до момента выключения чайника, возвращает строку 'выкл' 
    
    Параметры:
    kettel - объект класса Kettel
    logs - файл с логами
    """ 
    while kettel.getCurTemperature() < kettel.getEndTemperature(): 
        log = str(kettel.getCurTemperature()) + "°"
        print(log)
        for i in range(10): # раз в 0.1 секунды проверяет нажатие клавиши для выключения чайника
            time.sleep(0.1)
            if msvcrt.kbhit():
                kettel.switchOff()
                logs.write(str(kettel.getCurTemperature()) + " -> выкл (остановлен)\n")
                return "выкл"   
        kettel.increaseTemperature()
    print(kettel.getCurTemperature(), "°", sep="")
    if kettel.getCurTemperature() == 100:
        print("вскипел")
        logs.write("100° -> выкл\n")
    else:
        print("остановлен автоматически")
        logs.write(str(kettel.getCurTemperature()) + " -> выкл (остановлен автоматически)\n")
    return "выкл"

# считывание данных чайника из файла конфигурации
settings = open("settings.txt", "r")
bVolume = float(settings.readline().split(" ")[-1])
eTemperature = float(settings.readline().split(" ")[-1])
bHeatingTime = float(settings.readline().split(" ")[-1])
settings.close()

logs = open("logs.txt", "w", encoding='utf-8')
vitek = Kettel(bVolume, eTemperature, bHeatingTime)
water = input("налить воды в чайник (от 0 до " + str(bVolume) + "):") 
logs.write("Налито " + str(water) + " воды\n")
print("Для включения нажмите любую клавишу...")
while 1:
    if msvcrt.kbhit():
        msvcrt.getch()
        vitek.setWater(water) 
        vitek.switchOn() 
        logs.write("вкл\n")
        print(boiling(vitek, logs))  
        break
logs.close()
