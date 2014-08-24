import os, sys
from ctznosx import __version__ as version
from distutils.core import setup
from setuptools.command.install import install
from titantools.system import shell_out

long_description = """
ctznOSX is used by system administrators and
security professionals to profile and record details
relating to organizational wide Mac deployments.
"""

install_requires = ['titantools']

if sys.version_info < (2, 7):
    install_requires += ['argparse']

""" ctznOSX Installer Helper """
class CtznosxInstaller(install):
    """ Preinstall hooks """
    def preinstall(self):
        # Add custom pre-install stuff
        print "Adding ctznOSX User"
        add_user_script = """
dscl . -create /Users/_ctznosx
dscl . -create /Users/_ctznosx RealName "ctznOSX Management User"
dscl . -create /Users/_ctznosx UniqueID 403  # Use something between 100 and 500 to hide the user
dscl . -create /Users/_ctznosx PrimaryGroupID 20
dscl . -create /Users/_ctznosx UserShell /sbin/nologin
dseditgroup -o edit -a _ctznosx -t user admin
dseditgroup -o edit -a _ctznosx -t user wheel"""
        shell_out(add_user_script)
    
    """ Postinstall hooks """
    def postinstall(self):
        # Post install script
        print "Updating permissions for ctznOSX"
        shell_out("chown -R _ctznosx /var/lib/ctznosx")
        shell_out("chgrp -R wheel /var/lib/ctznosx")
        shell_out("chmod -R 0633 /var/lib/ctznosx/logs")
        shell_out("chmod -R 0666 /var/lib/ctznosx/ctznosx.db")
        shell_out("sudo launchctl load /Library/LaunchDaemons/com.ctznosx.runner.plist")
        shell_out("sudo launchctl load /Library/LaunchDaemons/com.ctznosx.watcher.plist")

    """ Runtime hooks """
    def run(self):

        self.preinstall()
        # Call the super run
        install.run(self)
        self.postinstall()

setup(
    name='ctznosx',
    version=version,
    description='ctznOSX: OSX Secure Device Management',
    long_description=long_description.strip(),
    author='Mike Mackintosh',
    author_email='mike@shutterstock.com',
    license='MIT',
    url='http://ctznOSX.com',
    packages=['ctznosx'],
    data_files=[('/etc', ['ctznosx.conf']), 
                ('/var/lib/ctznosx/', ['README.md', 'ctznosx.db']), 
                ('/var/lib/ctznosx/monitors/', ['monitors/README.md']), 
                ('/var/lib/ctznosx/logs/', []),
                ('/Library/LaunchDaemons/', ['plist/com.ctznosx.runner.plist', 'plist/com.ctznosx.watcher.plist']),
                ('/var/lib/ctznosx/reports/', [])
               ],
    package_data={'': ['ctznosx.db', 'ctznosx.conf', 'README.md']},
    include_package_data=True,
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
    cmdclass={
        'install': CtznosxInstaller,
    },
)
