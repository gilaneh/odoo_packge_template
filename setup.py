import sys
from setuptools import setup, Extension, find_packages

setup(
    name='odoo_package_template',
    version='1.0.33',
    description='description',
    url='https://github.com/gilaneh/odoo_package_template',
    author='Arash Homayounfar',
    author_email='homayounfar@msn.com',
    # classifiers=[c for c in classifiers.split('\n') if c],
    # license=license,
    # packages=find_packages(),
    entry_points="""
[console_scripts]
odoo_package_template = odoo_package_template:main
""",
    install_requires=[
        'colorama',
        'psutil',
    ]
)
