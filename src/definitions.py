CONF_FILE_PATH = '/etc/odoo/odoo_food_devices.conf'
LOG_FILE = '/var/log/odoo/odoo_food_autorun.log'
SERVICE_PATH = '/usr/lib/systemd/system/odoo_food_devices.service'
url = ''
LOG_FILE = 'odoo_food_devices.log'

SERVICE = '''
Description=Food Data Collector Service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
User=root
Group=root
ExecStart=/usr/bin/odoo_food_devices.py -conf /etc/odoo/odoo_food_devices.conf

StandardInput=tty-force

[Install]
WantedBy=multi-user.target
'''

CONF = '''
url = http://star.oeid.ir
LOG_FILE = /var/log/odoo/odoo_food_devices.log
'''