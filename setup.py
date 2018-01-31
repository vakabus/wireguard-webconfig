"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""


from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='wireguard-webconfig',
    version='0.1.0',
    description='Flask-based configuration interface for WireGuard VPN',
    # long_description=long_description,  # Optional
    # url='https://github.com/pypa/sampleproject',  # Optional
    author='Vaclav Sraier',
    author_email='pip+wireguard-webconfig@vakabus.cz',
    py_modules=["webconfig"],
    install_requires=['flask'],
    data_files=[
        ('/etc/systemd/system', ['wireguard-webconfig.service']),
        ('/etc/wireguard/', ['wg0.example.conf']),
    ],
    entry_points={
        'console_scripts': [
            'wireguard-webconfig=webconfig:main',
        ],
    },
)