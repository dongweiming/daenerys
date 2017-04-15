import sys

from app import app

context = {"go": app.dispatch_url}


def main():
    url = sys.argv[1]
    context['url'] = url
    pkg = app.dispatch_url(url)
    context['pkg'] = pkg
    for item in pkg.to_dict().items():
        print '{} = {}'.format(*item)

    def prepare_readline():
        import os
        import readline
        import atexit

        readline.parse_and_bind('tab: complete')
        histfile = os.path.expanduser("~/.daenerys_history")

        try:
            readline.read_history_file(histfile)
        except IOError:
            pass

        def savehist(histfile):
            readline.write_history_file(histfile)

        atexit.register(savehist, histfile)
        del atexit

    try:
        from IPython.terminal.interactiveshell import TerminalInteractiveShell
        shell = TerminalInteractiveShell(user_ns=context)
        shell.mainloop()
    except ImportError:
        import code
        shell = code.InteractiveConsole(locals=context)
        shell.runcode(prepare_readline.__code__)
        shell.interact()

if __name__ == "__main__":
    main()
