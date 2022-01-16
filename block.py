import argparse
import os
from datetime import datetime
import dateutil.parser

from config_handler import config


def poweroff():
    os.system('/sbin/poweroff')


def execute(test_time=None):
    test = test_time is not None
    now = test_time or datetime.now()
    shutdown = False
    if config.options.block_until and now < config.options.block_until:
        shutdown = True
    elif (config.options.time_block_start and config.options.time_block_end
          and config.options.time_block_start < now < config.options.time_block_end):
        shutdown = True

    if shutdown:
        if test:
            print("would block")
        else:
            poweroff()
    elif test:
        print("would not block")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blocks computer, helps with screen addiction')
    parser.add_argument('--days', default=0, type=int)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--dry-run', type=dateutil.parser.parse)
    parser.add_argument('--schedule-between', nargs=2, type=dateutil.parser.parse,
                        help='block everyday between specified hours, format hh:mm')
    args = parser.parse_args()
    config.save_from_args(args)
    if args.execute:
        execute(test_time=args.dry_run)
