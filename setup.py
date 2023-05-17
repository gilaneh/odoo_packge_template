import sys
from setuptools import setup, Extension

setup(
    entry_points="""
[console_scripts]
odoo_food_devices = odoo_food_devices:main
""",
)