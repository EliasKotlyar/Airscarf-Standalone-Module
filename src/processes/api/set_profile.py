from common.globalstate import state
from lib.microdot_asyncio import Microdot

api_profile = Microdot()


@api_profile.post('/setData')
def setData(request):
    data = request.json
    current_profile = int(data["current_profile"])
    state.setCurrentProfile(current_profile)
    state.setState('error', "")

    return {'success': True}


@api_profile.get('/data.json')
def get_orders(request):
    return {
        "current_profile": state.getState("current_profile"),
        "error": state.getState("error")
    }
