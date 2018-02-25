import sys
import logging
import asyncio
import async_timeout
import asyncssh
import aiohttp

logging.basicConfig(level=logging.WARN)


async def ssh_client():
    conn = await asyncssh.connect("localhost", 8022, known_hosts=None,
                                  client_keys=["./ssh_host_key"])
    server = await conn.forward_remote_port("", 20202, "localhost", 10101)
    listener = await conn.forward_local_port("", 30303, "localhost", 20202)
    return conn, server, listener


async def tcp_fetch(loop):
    reader, writer = await asyncio.open_connection(
        "127.0.0.1", 30303, loop=loop)
    writer.write(b"foo\n")
    data = await reader.read(100)
    writer.close()
    return data.decode()


async def run(loop):
    conn, server, listener = await ssh_client()
    for _ in range(100):
        resp = await tcp_fetch(loop)
    conn.close()
    await conn.wait_closed()


def main():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(loop))
    except (OSError, asyncssh.Error) as exc:
        sys.exit("SSH connection failed: " + str(exc))


if __name__ == "__main__":
    main()
