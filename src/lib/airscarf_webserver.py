from microdot_asyncio import send_file
from utime import sleep
from microdot_asyncio import Microdot
import machine


class Webserver:
    def __init__(self, airscarf, configReader):
        self.airscarf = airscarf
        self.configReader = configReader

    def start(self):
        app = Microdot()

        # Index Route:
        @app.route('/')
        def index(request):
            return send_file('/static/index.html')

        @app.route('/profile.html')
        def profile(request):
            return send_file('/static/profile.html')

        # Static Files(Jquery)
        @app.route('/assets/<path:path>')
        def static(request, path):
            if '..' in path:
                # directory traversal is not allowed
                return 'Not found', 404
            return send_file('static/assets/' + path)

        # Api Routes:
        @app.route('/api/livedata.json')
        def getLiveData(request):
            return self.airscarf.getLiveData()
            pass

        @app.route('/api/wifi.json')
        def getLiveData(request):
            return self.configReader.readWlanConfig()
            pass

        @app.route('/api/profiles.json')
        def getProfiles(request):
            return self.configReader.readProfiles()
            pass

        # Setters:

        @app.post('/api/setWifi')
        def setData(request):
            data = request.json
            self.configReader.writeWlanConfig(data)
            machine.reset()
            return {'success': True}

        @app.post('/api/setProfiles')
        def writeProfiles(request):
            data = request.json
            self.configReader.writeProfiles(data)
            self.airscarf.reload()
            return {'success': True}

        app.run(port=80)
