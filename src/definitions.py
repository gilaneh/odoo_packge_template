SERVICE_NAME = 'odoo_package_template'
CONF_FILE_PATH = '/etc/odoo/odoo_package_template.conf'
LOG_FILE = '/var/log/odoo/odoo_food_autorun.log'
SERVICE_PATH = '/usr/lib/systemd/system/odoo_package_template.service'
url = ''
LOG_FILE = 'odoo_package_template.log'

SERVICE = '''
Description=Odoo Package Template Service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
User=root
Group=root
ExecStart=odoo_package_template -conf /etc/odoo/odoo_package_template.conf
Restart=always
RestartSec=30
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
'''

CONF = '''
url = http://star.gilaneh.com
'''