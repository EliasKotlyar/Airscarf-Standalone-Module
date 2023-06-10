import socket
import gc
from common.logger import logger
from common.globalstate import state
import uasyncio, usocket


class Dns:
    def setup(self):
        pass

    async def run(self):

        wifi_mode = state.getState('wifi_mode')

        if wifi_mode == 1:
            logger.info('DNS not required, quitting')
            return
        elif wifi_mode == 0:
            logger.info('Starting DNS')

        ip_address = '192.168.4.1'
        port = 53
        logger.info("> starting catch all dns server on port {}".format(port))

        socket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        socket.setblocking(False)
        socket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
        socket.bind(usocket.getaddrinfo(ip_address, port, 0, usocket.SOCK_DGRAM)[0][-1])
        while True:
            try:
                yield uasyncio.core._io_queue.queue_read(socket)
                request, client = socket.recvfrom(256)
                response = request[:2]  # request id
                response += b"\x81\x80"  # response flags
                response += request[4:6] + request[4:6]  # qd/an count
                response += b"\x00\x00\x00\x00"  # ns/ar count
                response += request[12:]  # origional request body
                response += b"\xC0\x0C"  # pointer to domain name at byte 12
                response += b"\x00\x01\x00\x01"  # type and class (A record / IN class)
                response += b"\x00\x00\x00\x3C"  # time to live 60 seconds
                response += b"\x00\x04"  # response length (4 bytes = 1 ipv4 address)
                response += bytes(map(int, ip_address.split(".")))  # ip address parts
                socket.sendto(response, client)
                #logger.info("Replying: {:s} -> {:s}".format(DNS.domain, SERVER_IP))
            except Exception as e:
                logger.error(e)
