# Bibliotheken laden
from machine import Pin
from utime import sleep
from microdot import Microdot
import mm_wlan
from airscarf import AirScarf
from microdot import send_file

airscarf = AirScarf()


app = Microdot()
mm_wlan.connect_to_network(ssid, password)
# Index Route:
@app.route('/')
def index(request):
    return send_file('/static/index.html')
# Static Files(Jquery)
@app.route('/assets/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/assets/' + path)
# Api Routes:
@app.route('/api/data.json')
def getData(request):
    return airscarf.getData()

@app.post('/api/setData')
def setData(request):
    data = request.json
    #return data
    rpm_freq = data.get('rpm_freq')
    rpm_duty = data.get('rpm_duty')
    if rpm_freq and rpm_duty:
        rpm_freq = int(rpm_freq)
        rpm_duty = int(rpm_duty)
        airscarf.setRpm(rpm_freq,rpm_duty)
    return {'success': True}


app.run(port=80)

