import argparse
import os
import sys
from webbrowser import open_new_tab
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

from uploader import PasteryUploader


def main():
    config = ConfigParser.SafeConfigParser()
    config.read([os.path.expanduser('~/.config/bakeit.cfg')])
    try:
        pastery = dict(config.items("pastery"))
    except:
        sys.exit(
            "Config file not found. Make sure you have a config file"
            " at ~/.config/bakeit.cfg with a [pastery] section containing"
            " your Pastery API key, which you can get from your"
            " https://www.pastery.net account page."
        )

    if "api_key" not in pastery:
        sys.exit(
            "Pastery API key not found in the config. Get it from your"
            " https://www.pastery.net account page."
        )

    parser = argparse.ArgumentParser(description="Upload a file to Pastery, the "
            " best pastebin in the world.")
    parser.add_argument("filename", metavar="filename", type=str, default="", nargs="?",
                       help="the name of the file to upload (or stdin, if omitted)")
    parser.add_argument("-t", "--title", metavar="title", type=str,
                       help="the title of the paste")
    parser.add_argument("-l", "--language", metavar="lang", type=str,
                       help="the language highlighter to use")
    parser.add_argument("-d", "--duration", metavar="minutes", type=int,
                       help="the duration (in minutes) before the paste expires")
    parser.add_argument("-v", "--max-views", metavar="views", type=int,
                       help="how many times this paste can be viewed before it expires")
    parser.add_argument("-b", "--open-browser", action="store_true",
                       help="automatically open a browser window when done")

    args = parser.parse_args()
    if args.filename:
        content = open(args.filename, "r").read()
    else:
        print("Type your paste and press Ctrl+D to upload.")
        content = sys.stdin.read()
    print(args)

    pu = PasteryUploader(pastery["api_key"])
    url = pu.upload(
            content,
            title=args.title,
            language=args.language,
            duration=args.duration,
            max_views=args.max_views,
            )
    print("Paste URL: %s" % url)
    if args.open_browser:
        open_new_tab(url)
