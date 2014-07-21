import os, sys
from ctznosx import __version__ as version
from distutils.core import setup

long_description = """
ctznOSX is used by system administrators and
security professionals to profile and record details
relating to organizational wide Mac deployments.
"""

install_requires = ['titantools']

if sys.version_info < (2, 7):
    install_requires += ['argparse']

setup(
    name='ctznosx',
    version=version,
    description='ctznOSX: OSX Secure Device Management',
    long_description=long_description.strip(),
    author='Mike Mackintosh',
    author_email='mike@shutterstock.com',
    license='MIT',
    url='https://github.com/ctznOSX',
    packages=['ctznosx'],
    data_files=[('/etc', ['ctznosx.conf'])],
    package_data={'ctznosx': ['data/*/*']},
    scripts=['scripts/ctznosx', 'scripts/ctznosx-watcher'],
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
)
