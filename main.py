#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

import indeed
import util

if __name__ == '__main__':
    x = argparse.ArgumentParser()
    x.add_argument('what', type=str)
    x.add_argument('--where', type=str, default='')
    x.add_argument('--limit', type=int, default=10)
    x.add_argument('--sleep', type=int, default=2)
    x.add_argument('--out', type=str, default='.')
    x.add_argument('--download', action='store_const', const=True, default=False)
    x.add_argument('--parse', action='store_const', const=True, default=False)
    x.add_argument('--clean', action='store_const', const=True, default=False)
    x.add_argument('--gzip', type=str, default='on')
    args = x.parse_args()

    if args.download and args.parse:
        print("--download and --parse cannot both be True")
        sys.exit(1)

    indeed.download(args)
    indeed.parse(args)
    indeed.clean(args)
