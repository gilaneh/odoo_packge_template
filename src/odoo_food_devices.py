#!/usr/bin/python3
# odoo_food_devices.py
# version: 1.3
# Author: Arash Homayounfar
# email: homayounfar@msn.com
# Description: This app is intended to collect data from biometric attendance devices and send them to the odoo server.
#

import installer
import read_config
import definitions
from time import sleep
from time import process_time
from time import time
from datetime import datetime
import threading
import requests
import json
from colorama import Fore
import argparse
import os
import sys
import textwrap
from urllib.parse import urlparse, urlunsplit, ParseResult
import logging
from logging.handlers import RotatingFileHandler
LOG_FILE = definitions.LOG_FILE

# try:
#     if not os.path.isfile(definitions.CONF_FILE_PATH):
#         _, LOG_FILE = installer.read(definitions.CONF_FILE_PATH)
#     else:
#         LOG_FILE = definitions.LOG_FILE
#
# except FileNotFoundError:
#     LOG_FILE = definitions.LOG_FILE

# if not os.path.isfile(LOG_FILE):
#     LOG_FILE = 'odoo_food_devices.log'

# logging.basicConfig(filename=LOG_FILE,
#                     level='INFO',
#                     format='%(asctime)s %(levelname)-8s %(name)-6s %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S')
log_formatter = logging.Formatter('%(asctime)s %(levelname)s [%(funcName)s(),%(filename)s:L%(lineno)d] %(message)s')
my_handler = RotatingFileHandler(LOG_FILE, mode='a', maxBytes=10*1024*1024, backupCount=3, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)
app_log.addHandler(my_handler)


import pytz
import sys

try:
    from zk import ZK
except ImportError:
    logging.error("Unable to import pyzk library. Try 'pip3 install pyzk'.")

exit = False
SERVER_PATH = '/sd_food/activate_devices'
THEARED_PREFIX = 'sd_food_device'
en_list = []


def zk_tech_handler(id, tz, url, zk, records, set_time, verbose):
    new_attendance = []
    state = 'undefined'
    try:
        st1 = time()
        conn = zk.connect()
    except Exception as e:
        st2 = time()
        err_text = ''
        err = str(e).lower()
        if 'timed out' in err:
            state = 'timeout'
        elif 'ping' in err:
            state = 'network_error'
        elif 'unauthenticated' in err:
            state = 'wrong_password'
        else:
            state = 'undefined'
            err_text = err
        if verbose: print(f'ID:[{id}] | st2:[{round(st2 - st1, 2)}] | state: {state} | {err_text}')
        logging.error(f'ID:[{id}] | st2:[{round(st2 - st1, 2)}] | state: {state} | {err_text}')

        # response = requests.post(url, json={'device_id': id, 'state': state})

        return (0, 0, state)
    try:
        st2 = time()
        # print(conn.get_time() , datetime.now())
        time_diff = round(abs(conn.get_time().timestamp() - datetime.now().timestamp()), 2)
        if time_diff > 10:
            local_tz = pytz.timezone('Asia/Tehran' or 'GMT')
            dt = datetime.now()
            conn.set_time(dt)
            if verbose: print(Fore.YELLOW, f'ID:[{id}] Set Time, \n  server:[{dt}] \n  device:[{conn.get_time()}]', Fore.RESET)
            logging.warning(f'ID:[{id}] Set Time, server:[{dt}] device:[{conn.get_time()}] def: [{time_diff}sec]')
        conn.get_time()
        # if conn.records:
        #     new_attendance = conn.get_attendance()
        new_attendance = conn.get_attendance()
        # print(new_attendance)
        st3 = time()
        attendances = []
        if new_attendance:
            for att in new_attendance:
                if abs(att.timestamp.timestamp() - datetime.now().timestamp()) > 3600:
                    if verbose: print(f'ID:[{id}] [IGNORED]{att} Latency:{round(abs(att.timestamp.timestamp() - datetime.now().timestamp()), 2)}')
                    logging.error(f'ID:[{id}] [IGNORED]{att} Latency:{round(abs(att.timestamp.timestamp() - datetime.now().timestamp()), 2)}')
                    continue
                if verbose: print(f'ID:[{id}] {att} Latency:{round(abs(att.timestamp.timestamp() - datetime.now().timestamp()), 2)}')
                logging.info(f'ID:[{id}] {att} Latency:{round(abs(att.timestamp.timestamp() - datetime.now().timestamp()), 2)}')
                # in case of wrong device time, it might encounter an error to save timestamp as integer on odoo.
                #  In case, this record would be ignored
                # todo: active it again: default 3600

                attendances.append({'user_id': att.user_id,
                                    'timestamp': int(att.timestamp.timestamp()),
                                    'status': att.status,
                                    'punch': att.punch,
                                    'uid': att.uid, })
            if attendances:
                response = requests.post(url, json={'device_id': id, 'new_attendance': attendances})
                if json.loads(response.text).get('result'):
                    attendance_saved = json.loads(json.loads(response.text).get('result')).get('attendance_saved')
                    if attendance_saved:
                        if conn.is_connect:
                            conn.clear_attendance()
                    else:
                        if verbose: print(f'ID:[{id}] [zk_tech_handler] ERROR to SAVE  attendance date')
                        logging.error(f'ID:[{id}] ERROR to SAVE  attendance date')
            else:
                if conn.is_connect:
                    conn.clear_attendance()
        st4 = time()
        if verbose: print(
                f'ID:[{id}] is live, records: [{records}] >>> st2:[{round(st2 - st1, 2)}] st3:[{round(st3 - st2, 2)}] st4:[{round(st4 - st3, 2)}] ')
        if conn.is_connect:
            conn.enable_device()
            conn.disconnect()
    except Exception as e:
        if verbose: print(f'{sys._getframe().f_lineno}ID:[{id}][zk_tech_handler] Error 2 > {e}')
        logging.error(f'ID:[{id}] Error 2 > {e}')
    return (new_attendance, records, 'ok')


def iFace202(ip_address, port_no, timeout, password, verbose):
    if verbose:
        print(ip_address, port_no, timeout, password)


def device_capture(id, url, verbose):
    records = 0
    set_time = False
    set_time_counter = 0
    state = 'undefined'

    response = requests.post(url, json={'device_id': id, 'device_settings': True, })
    if json.loads(response.text).get('result'):
        device_settings = json.loads(json.loads(response.text).get('result')).get('device_settings')
        # print(device_settings, )
        type_name = device_settings.get('type_name')
        read_live = device_settings.get('read_live')
        ip_address = device_settings.get('ip_address')
        port_no = device_settings.get('port_no')
        timeout = device_settings.get('timeout')
        password = device_settings.get('password')
        tz = device_settings.get('tz')
        zk = ZK(ip_address, port=port_no, timeout=int(timeout), password=password, force_udp=False, ommit_ping=False)
        if verbose: print(zk)
        if verbose: print(f'ID:[{id}] STARTED . . .')
        logging.info(f'ID:[{id}] STARTED . . .')
    while True:
        try:
            set_time_counter += 1
            if set_time_counter == 10:
                set_time = True
                set_time_counter = 0

            st1 = time()
            # print(state)

            response = requests.post(url, json={'device_id': id, 'device_ids': True, 'device_settings': True,
                                                'state': state})
            if json.loads(response.text).get('result'):
                device_ids = set(json.loads(json.loads(response.text).get('result')).get('device_ids'))
                recent_device_settings = json.loads(json.loads(response.text).get('result')).get('device_settings')

                if id not in device_ids or recent_device_settings != device_settings:
                    break

            st2 = time()

            new_attendance = []
            if type_name in ['uFace202', 'H0201']:
                new_attendance, records, state = zk_tech_handler(id, tz, url, zk, records, set_time, verbose)

            elif type_name == 'iFace202':
                new_attendance = iFace202(ip_address, port_no, timeout, password)

            st3 = time()

            st4 = time()
            set_time = False
            sleep(1)
        except Exception as e:
            if verbose: print(f'ID:[{id}] has ERROR:{e}')
            logging.error(f'ID:[{id}] has ERROR:{e}')
            sleep(5)

    if verbose: print(f'ID:[{id}] STOPPED ! ! !')
    logging.info(f'ID:[{id}] STOPPED ! ! !')


def this_loop(url, verbose):
    device_ids = set()
    while not exit:
        try:
            response = requests.post(url, json={'device_ids': True})
            if 'jsonrpc' in str(response.content):
                if json.loads(response.text).get('result'):
                    device_ids = set(json.loads(json.loads(response.text).get('result')).get('device_ids'))
                    en_list = device_ids
                active_threads = {int((tr.name).replace(THEARED_PREFIX + '_', '')) for tr in threading.enumerate()
                                if tr.name[:len(THEARED_PREFIX)] == THEARED_PREFIX}

                #             print('=======', device_ids, active_threads, device_ids.difference(active_threads))
                if device_ids.difference(active_threads):
                    id = list(device_ids.difference(active_threads))[0]
                    tr = threading.Thread(target=device_capture, args=(id, url, verbose), name=f'{THEARED_PREFIX}_{id}')
                    tr.daemon = True
                    tr.start()
            else:
                if verbose: print(f'{os.path.basename(__file__)}:{sys._getframe().f_lineno} ERROR: There is no "jsonrpc" in response. Check your url')
            logging.error(f'ERROR: There is no "jsonrpc" in response. Check your url')
            sleep(3)
        except Exception as e:
            if verbose:
                print(f'{os.path.basename(__file__)}:{sys._getframe().f_lineno} ERROR: {e}')
            logging.error(f'ERROR: {e}')

            sleep(3)
    if verbose:
        print('This Loop Exited')


def main(args):
    verbose = False
    parser = argparse.ArgumentParser(
        prog="%s cloc" % sys.argv[0].split(os.path.sep)[-1],
        # description=textwrap.dedent(__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--url', '-u', help='Base url of the server: e.g. https://oeid.gilaneh.com')
    parser.add_argument('--verbose', '-v',  action='count', default=0)
    parser.add_argument('--install', '-i',  action='count', default=0)
    # parser.add_argument('--config', '-c', help='config file: e.g. /etc/odoo/odoo_food_devices.conf')
    opt, unknown = parser.parse_known_args(args)
    if opt.verbose:
        verbose = True

    if opt.install:
        print(installer.install(logging, verbose))
        sys.exit()

    # if opt.config:
    #     url, LOG_FILE = read_config.read(opt.config)

    if opt.url and urlparse(opt.url).netloc:
        url_parse = urlparse(opt.url)
        if verbose:
            print(url_parse, url_parse.scheme)
        scheme = url_parse.scheme if url_parse.scheme in ['http', 'https'] else 'https'
        url = scheme + '://' + url_parse.netloc + SERVER_PATH
        # todo: write the url to config file
    elif not url:
        # todo: check if url is in config file and use it, if not exit with error.
        logging.error(f'[PARAMS] wrong parameters \n     {str(parser.parse_known_args())}')
        parser.print_help()
        sys.exit()
    
    tr = threading.Thread(target=this_loop, args=(url, verbose), daemon=True)
    tr.start()
    print(f'[SERVICE STARTED]\n        url: {url}')
    print(f'        Use  -v  switch for debug!\n        Press  Ctrl + c  to terminate')
    logging.info(f'{"=" * 10}  [SERVICE STARTED]  {"=" * 10}')
    logging.info(f'url: {url}')
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            print(Fore.RED, f'[SERVICE Terminated] url:{url.split("/")[2]}', Fore.RESET)
            logging.error(f'[SERVICE Terminated] url:{url.split("/")[2]}')
            break
        except Exception as e:
            logging.error(f'[SERVICE SOPPED] {e}')


if __name__ == "__main__":
   main(sys.argv[1:])