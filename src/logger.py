import logging
# logging.basicConfig(level=logging.DEBUG)

class CustomFormatter(logging.Formatter):

    magenta =  "\x1b[38;5;207m"
    green =    "\x1b[38;5;41m"
    yellow =   "\x1b[38;5;228m"
    red =      "\x1b[38;5;9m"
    red_bg =   "\x1b[48;5;1m"
    reset =    "\x1b[0m"
    format_s = '%(asctime)s|'
    format_e = f'%(levelname)s{reset}|%(filename)s:%(lineno)s|%(message)s'

    FORMATS = {
        logging.DEBUG: format_s + magenta + format_e,
        logging.INFO: format_s + green + format_e,
        logging.WARNING: format_s + yellow + format_e,
        logging.ERROR: format_s + red + format_e,
        logging.CRITICAL: format_s + red_bg + format_e,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
# todo: info and debug level is not working
stream_handler.setLevel(logging.DEBUG)
# stream_format = logging.Formatter('%(filename)s:%(lineno)s|%(levelname)s|%(message)s')
stream_handler.setFormatter(CustomFormatter())
logger.addHandler(stream_handler)

# Create handlers
try:
    file_handler = logging.FileHandler('/var/log/odoo/odoo_package_template.log')
except Exception as e:
    file_handler = logging.FileHandler('odoo_package_template.log')
    logger.error(e)

file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter('%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s')
# file_handler.setFormatter(CustomFormatter())
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)
