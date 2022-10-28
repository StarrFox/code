"""
A sample application for cmd2.
"""
import argparse
import sys
import cmd2

class CmdLineApp(cmd2.Cmd):
    """ Example cmd2 application. """

    def __init__(self):
        super().__init__()
        self.prompt = "test"



    speak_parser = argparse.ArgumentParser()
    speak_parser.add_argument('-p', '--piglatin', action='store_true', help='atinLay')
    speak_parser.add_argument('-s', '--shout', action='store_true', help='N00B EMULATION MODE')
    speak_parser.add_argument('-r', '--repeat', type=int, help='output [n] times')
    speak_parser.add_argument('words', nargs='+', help='words to say')

    @cmd2.with_argparser(speak_parser)
    def do_speak(self, args):
        """Repeats what you tell me to."""
        words = []
        for word in args.words:
            if args.piglatin:
                word = '%s%say' % (word[1:], word[0])
            if args.shout:
                word = word.upper()
            words.append(word)
        repetitions = args.repeat or 1
        for i in range(min(repetitions, self.maxrepeats)):
            # .poutput handles newlines, and accommodates output redirection too
            self.poutput(' '.join(words))

    do_say = do_speak  # now "say" is a synonym for "speak"
    do_orate = do_speak  # another synonym, but this one takes multi-line input

    mumble_parser = argparse.ArgumentParser()
    mumble_parser.add_argument('-r', '--repeat', type=int, help='how many times to repeat')
    mumble_parser.add_argument('words', nargs='+', help='words to say')


if __name__ == '__main__':
    app = CmdLineApp()
    sys.exit(app.cmdloop())
