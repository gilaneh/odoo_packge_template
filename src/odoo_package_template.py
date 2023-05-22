#!/bin/bash/python3
import os
import sys
import signal
import time
# from logger import logger
import argparse
import psutil
# import ins
from utils import *
from tendo import singleton

def signal_handler(signum, frame):
    logger.error(f'Terminated. signal:{signal.Signals(signum).name}')
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def main(args=None):
    verbose = False
    url = ''
    parser = argparse.ArgumentParser(
        prog="%s cloc" % sys.argv[0].split(os.path.sep)[-1],
        # description=textwrap.dedent(__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--url', '-u', help='Base url of the server: e.g. https://oeid.gilaneh.com')
    parser.add_argument('--version', '-v',  action='count', default=0, help=f'Current Version: [ {package_version()} ]')
    parser.add_argument('--install', '-i',  action='count', default=0, help='Creates service and config files. Starts service as well')
    parser.add_argument('--uninstall',  action='count', default=0, help='Removes service and config files')
    parser.add_argument('--config', '-c', help='config file: e.g. /etc/odoo/odoo_package_template.conf')
    opt, unknown = parser.parse_known_args(args)
    if opt.version:
        print(package_version())
        sys.exit(0)

    # if == 1 -> run as service
    if psutil.Process(os.getpid()).ppid() != 1:
        verbose = True

    if opt.install:
        do_uninstall()
        do_install()
        sys.exit(0)

    if opt.uninstall:
        do_uninstall()
        sys.exit(0)

    if opt.config:
        url, _ = do_config()
    try:
        m = singleton.SingleInstance()
    except Exception as e:
        logger.error(f'singleton: {e}')
        sys.exit(-1)

    # logger.info('url:', url)
    while True:
        logger.debug('working')
        logger.info('working')
        logger.warning('working')
        time.sleep(3)


if __name__ == '__main__':
    # m = singleton.SingleInstance()

    main(sys.argv)
