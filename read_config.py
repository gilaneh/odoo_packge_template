import os

url = ''
LOG_FILE = 'odoo_food_devices.log'
def read(config_file):
    with open(config_file, 'r') as f:
        config_file = f.readlines()

    for line in config_file:
        line_splite = line.split('=')
        if len(line_splite) == 2:
            if line_splite[0].strip() == 'url':
                url = line_splite[1].strip() 
            elif line_splite[0].strip() == 'LOG_FILE': 
                LOG_FILE = line_splite[1].strip()
                if not os.path.isdir(os.path.dirname(LOG_FILE)):
                    os.makedirs(os.path.dirname(LOG_FILE))

    return (url, LOG_FILE)
