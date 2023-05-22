import subprocess
from importlib.metadata import version
# print(subprocess.run(['pip3', 'list']))
import odoo_package_template
# print(dir(odoo_package_template))
print(version('odoo_package_template'))
odoo_package_template.main()
