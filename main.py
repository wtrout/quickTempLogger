from machine import ADC, Pin
import utime
import urequests
import pWi


nets = pWi.nets("Network 12", "bricktreecoffeedesk")
adc = ADC(Pin(26))

nets.connect()
utime.sleep(5)


def getTemp():
    adcRatio = 0.050354772259098 # mV/count (3300mV / 16bit int)
    response = 0.1 # °C / mV
    offset   = 500 # mV @ 0°C
    calibration = -1.2

    raw = adc.read_u16()
    temp = raw * adcRatio
    temp -= offset
    temp *= response

    temp += calibration
    
    return temp



def influx():
    temp = getTemp()
    print(f'Temperature is {temp} °C')

    headers = {
        'Authorization': 'Token ijF8-gGq2RP_fOjbtrSSk5lZ-BNUNAmIDByfcC-dDXlrP24Ew7lRoCJWN0JeH1OiCeRwzBu_0gBRvyTxbIYsPg==', # 'logger token'
        'Content-Type': 'text/plain',
        'Accept': 'application/json',
    }

    data = f'bedroom temp={temp}'
    
    print('Sending to InfluxDB...')
    try:
        r = urequests.post('http://192.168.4.244:8086/api/v2/write?org=Trout&bucket=home&precision=ns', headers=headers, data=data)
    except Exception as e:
        print(e)
    print(r.text)



while True:
    #print(getTemp())
    #utime.sleep(5)
    nets.doWithWifi(influx)
    for i in range(0,30):
        utime.sleep(10)
        print(10*i)