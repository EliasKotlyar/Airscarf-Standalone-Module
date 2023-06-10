from common.logger import logger
from config.advanced import AdvancedConfig
from config.profiles import ProfilesConfig
from config.wifi import WifiConfig
from lib.microdot_asyncio import Microdot
from lib.microdot_asyncio import send_file
from processes.api.monitor import api_monitor
from processes.api.set_profile import api_profile

class Webserver:

    def start(self):
        app = Microdot()

        app.mount(api_monitor, url_prefix='/api/monitor')
        app.mount(api_profile, url_prefix='/api/current_profile')
        app.mount(AdvancedConfig().get_microdot_config(), url_prefix='/api/advanced')
        app.mount(ProfilesConfig().get_microdot_config(), url_prefix='/api/profiles')
        app.mount(WifiConfig().get_microdot_config(), url_prefix='/api/wifi')


        # Index Route:
        @app.route('/')
        def index(request):
            return send_file('/static/index.html')

        # Captive Portal Android
        @app.route('/generate_204')
        def index(request):
            return send_file('/static/index.html')

        # Captive Portal Microsoft
        @app.route('/fwlink')
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

        @app.errorhandler(RuntimeError)
        def runtime_error(request, exception):
            return 'Runtime error'

        @app.after_error_request
        def func(request, response):
            # ...
            return response

        logger.info("Starting Webserver...")
        app.run(port=80, debug=False)
