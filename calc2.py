#!/usr/bin/env python
"""
SYNOPSIS

    calc [-h, --help] [-m, --maxcups N]

DESCRIPTION
    This script calculates the optimum upgrade purchase path
    in the Office Space minigame.

EXAMPLES

    TODO: Show some examples of how to use this script.


AUTHOR

    TODO: Tony Nelson <hhubris@gmail.com>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    $Id$
"""

import sys
import os
import traceback
import argparse
import math


def main(options, args):
    print("hello world")


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description='Calculate Purchase Order for Office Space',
            usage=globals()['__doc__'], version='$Id$')
        parser.add_option('-f', '--file', action='store')
        parser.add_option('-m', '--max', action='store',
                          type='int', default=10000,
                          help='Maximum tier1 count [10000 default]')
        parser.add_option('-v', '--verbose', action='store_true',
                          default=False, help='verbose output')
        (options, args) = parser.parse_args()
        main(options, args)
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:  # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)
