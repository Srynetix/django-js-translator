"""Shell."""

import argparse
import textwrap
import sys

from django_js_translator.version import __version__
from django_js_translator.translator import prepare_translation


def entry_point():
    """Main entry-point function."""
    description = textwrap.dedent("""
        django-js-translator {0}
        Prepare translation files for JS.
    """.format(__version__))

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parser.add_argument("config_path", help="configuration file path")
    parser.add_argument("--dry-run", action="store_true", help="only print output")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    prepare_translation(args)
