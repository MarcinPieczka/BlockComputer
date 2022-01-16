#!python3

import argparse
import os
from datetime import datetime

import dateutil.parser

from config_handler import config


def shutdown(test=True):
    if not test:
        os.system('poweroff')
    else:
        print("would shutdown")


def execute():
    now = datetime.now()
    if now < config.options.block_until:
        shutdown()
    if config.options.time_block_start < now < config.options.time_block_end:
        shutdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blocks computer, helps with screen addiction')
    parser.add_argument('--days', default=0, type=int)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--schedule-between', nargs=2, type=dateutil.parser.parse,
                        help='block everyday between specified hours, format hh:mm')
    args = parser.parse_args()
    config.save_from_args(args)
    if args.execute:
        execute()
