import os
import subprocess
from logger import logger
from definitions import CONF_FILE_PATH, CONF, SERVICE_PATH, SERVICE, SERVICE_NAME
from importlib.metadata import version


def package_version():
    return version('odoo_package_template')


def do_install():
    try:
        if not os.path.isdir(os.path.dirname(CONF_FILE_PATH)):
            os.mkdir(os.path.dirname(CONF_FILE_PATH))
        with open(CONF_FILE_PATH, 'w') as f:
            f.write(CONF)
        if os.path.isfile(CONF_FILE_PATH):
            logger.info(f'Config file creation on {CONF_FILE_PATH} [{os.path.isfile(CONF_FILE_PATH)}]')
        else:
            logger.error(f'Config file creation on {CONF_FILE_PATH} [{os.path.isfile(CONF_FILE_PATH)}]')

    except Exception as e:
        logger.error(e)
    try:
        with open(SERVICE_PATH, 'w') as f:
            f.write(SERVICE)
        if os.path.isfile(CONF_FILE_PATH):
            logger.info(f'Config file creation on {SERVICE_PATH} [{os.path.isfile(SERVICE_PATH)}]')
        else:
            logger.error(f'Config file creation on {SERVICE_PATH} [{os.path.isfile(SERVICE_PATH)}]')
    except Exception as e:
        logger.error(e)
    try:
        subprocess.run(['systemctl', 'daemon-reload'])
        subprocess.run(['systemctl', 'enable', SERVICE_NAME])
        subprocess.run(['systemctl', 'start', SERVICE_NAME])
    except Exception as e:
        logger.error(e)

def do_uninstall():
    try:
        subprocess.run(['systemctl', 'stop', SERVICE_NAME])
        subprocess.run(['systemctl', 'disable', SERVICE_NAME])
        subprocess.run(['rm', SERVICE_PATH])
        subprocess.run(['rm', CONF_FILE_PATH])
    except Exception as e:
        logger.error(e)


def do_config():
    url = 'https://star.odoo.ir'
    log = 'a'
    return url, log
