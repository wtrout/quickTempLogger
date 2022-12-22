import network
import machine
import utime

class nets:
    def __init__(self, ssid, password, status_LED=machine.Pin("LED",machine.Pin.OUT)):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.LED = status_LED

    def get_wlan_status(self, wlan):
        # Make sense of the wlan.status() numbers that are returned
        status = self.wlan.status()
        if status == network.STAT_IDLE:
            return 'STAT_IDLE'
        elif status == network.STAT_CONNECTING:
            return 'STAT_CONNECTING'
        elif status == network.STAT_WRONG_PASSWORD:
            return 'STAT_WRONG_PASSWORD'
        elif status == network.STAT_NO_AP_FOUND:
            return 'STAT_NO_AP_FOUND'
        elif status == network.STAT_CONNECT_FAIL:
            return 'STAT_CONNECT_FAIL'
        elif status == network.STAT_GOT_IP:
            return 'STAT_GOT_IP'
        else:
            return "Unknown wlan status: {}".format(status) 

    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        max_wait = 20
        while max_wait > 0:
            self.LED.toggle()
            if self.wlan.isconnected():
                print("Connected to wifi")
                self.LED.on()
                break
            
            max_wait -= 1
            print("Waiting for connection... (" + self.get_wlan_status(self.wlan) + ")")
            utime.sleep(1)

    def doWithWifi(self,task):
        if self.wlan.isconnected():
            print("Doing task...")
            task()
        else:
            # Try and re-connect to wifi
            print("Disconnected from wifi")
            self.LED.off()
            self.wlan.disconnect()
            self.wlan.connect(self.ssid, self.password)
            
            if self.wlan.isconnected():
                print("Re-connected to wifi")
                self.LED.on()
            else:
                print("Failed to re-connect to wifi")