import asyncio
import threading
import sys


import aioconsole
from aiomonitor import Monitor, start_monitor, cli
from aiomonitor.utils import alt_names, close_server, console_proxy


def init_console_server(host: str, port: int, _locals, loop):
    def _factory(streams=None) -> aioconsole.AsynchronousConsole:
        return NoBannerConsole(locals=_locals, streams=streams, loop=loop)

    coro = aioconsole.start_interactive_server(
        host=host, port=port, factory=_factory, loop=loop
    )
    console_future = asyncio.run_coroutine_threadsafe(coro, loop=loop)
    return console_future


class NoBannerConsole(aioconsole.AsynchronousConsole):
    @asyncio.coroutine
    def _interact(self, banner=None):
        # Get ps1 and ps2
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        # Run loop
        more = 0
        while 1:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                try:
                    line = yield from self.raw_input(prompt)
                except EOFError:
                    self.write("\n")
                    yield from self.flush()
                    break
                else:
                    more = yield from self.push(line)
            except asyncio.CancelledError:
                self.write("\nKeyboardInterrupt\n")
                yield from self.flush()
                self.resetbuffer()
                more = 0


class WizWalkerConsole(Monitor):
    intro =  "WizWalkerCLI\n{tasknum} task{s} running. Use help (?) for commands.\n"
    prompt = "WW > "

    def write(self, message: str):
        self._sout.write(message + "\n")
        self._sout.flush()

    def do_console(self):
        """Switch to async Python REPL"""
        if not self._console_enabled:
            self._sout.write("Python console disabled for this sessiong\n")
            self._sout.flush()
            return

        fut = init_console_server(
            self._host, self._console_port, self._locals, self._loop
        )
        server = fut.result(timeout=3)
        try:
            console_proxy(self._sin, self._sout, self._host, self._console_port)
        finally:
            coro = close_server(server)
            close_fut = asyncio.run_coroutine_threadsafe(coro, loop=self._loop)
            close_fut.result(timeout=15)

    def do_test(self):
        """Test Command"""
        self.write("test")


def proxy_run(loop):
    async def _app():
        print("running")

    future = asyncio.ensure_future(_app(), loop=loop)
    loop.run_forever()


def main():
    loop = asyncio.get_event_loop()
    def _proc():
        with start_monitor(loop, monitor=WizWalkerConsole):
            proxy_run(loop)

    #_proc()

    app_thread = threading.Thread(None, _proc)

    print("Starting")
    app_thread.start()
    cli.monitor_client(cli.MONITOR_HOST, cli.MONITOR_PORT)
    print("Closing")


if __name__ == "__main__":
    main()
