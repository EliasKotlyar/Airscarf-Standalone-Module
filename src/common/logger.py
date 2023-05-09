from lib import ulogger

handler_to_term = ulogger.Handler(
    level=ulogger.INFO,
    colorful=True,
    fmt="&(time)% - &(level)% - &(name)% - &(fnname)% - &(msg)%",
    clock=None,
    direction=ulogger.TO_TERM,
)

logger = ulogger.Logger(
    name = __name__,
    handlers = [
        handler_to_term,
    ]
)

