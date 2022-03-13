import argparse
import asyncio
import contextlib
import io

_globals = dict()
_locals = dict()


async def execute(reader, writer):
    def log(msg):
        print(f'{client_addr!r} {msg}')

    client_addr = writer.get_extra_info('peername')
    log('connected')

    input_data = await reader.read()
    log(f'{len(input_data)} bytes received')

    untrusted_code = input_data.decode()
    try:
        with contextlib.redirect_stdout(io.StringIO()) as f:
            exec(untrusted_code, _globals, _locals)

        output_data = f.getvalue().encode()
        log('exec success')

    except Exception as e:
        output_data = f'{e!r}\n'.encode()
        log(f'exec failure: {e!r}')

    writer.write(output_data)
    await writer.drain()
    log(f'{len(output_data)} bytes returned')

    writer.close()
    await writer.wait_closed()
    log('closed')


async def listen(host, port):
    server = await asyncio.start_server(execute, host, port)
    sockets = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Listening on {sockets}')

    async with server:
        await server.serve_forever()


def main():
    parser = argparse.ArgumentParser(
        description='A simple, stateful code execution server for Python.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--host', default='127.0.0.1', help='listener host')
    parser.add_argument('--port', default=31337, type=int, help='listener port')

    args = parser.parse_args()
    asyncio.run(listen(args.host, args.port))


if __name__ == '__main__':
    main()
