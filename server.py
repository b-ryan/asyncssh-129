import logging
import asyncio, asyncssh, sys
from asyncssh.listener import SSHTCPClientListener
from asyncssh import ChannelOpenError, OPEN_CONNECT_FAILED

logging.basicConfig(level=logging.DEBUG, filename="output.log")
logger = logging.getLogger(__name__)


class MySSHServer(asyncssh.SSHServer):
    def __init__(self, loop):
        self.loop = loop
        self.conn = None

    def connection_lost(self, exc):
        if exc:
            logger.exception("CONN EXCEPTION", exc_info=exc)

    def connection_requested(self, dest_host, dest_port, orig_host, orig_port):
        return True

    def server_requested(self, listen_host, listen_port):
        return True


async def start_server(loop):
    factory = lambda: MySSHServer(loop)
    await asyncssh.create_server(factory, "", 8022,
                                 server_host_keys=["ssh_host_key"],
                                 authorized_client_keys="ssh_user_ca")


def main():
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_server(loop))
    except (OSError, asyncssh.Error) as exc:
        sys.exit("SSH server failed: " + str(exc))

    loop.run_forever()

if __name__ == "__main__":
    main()
