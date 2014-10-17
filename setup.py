import os, sys
from titan import __version__ as version
from distutils.core import setup
from setuptools.command.install import install
from titan.tools.system import shell_out

long_description = """
titanOSX is used by system administrators and
security professionals to profile and record details
relating to organizational wide Mac deployments.
"""

#install_requires = ['titantools']

if sys.version_info < (2, 7):
    install_requires += ['argparse']

""" titanOSX Installer Helper """
class TitanInstaller(install):
    """ Preinstall hooks """
    def preinstall(self):
        # Add custom pre-install stuff
        print "Adding titanOSX User"
        add_user_script = """
dscl . -create /Users/_titan
dscl . -create /Users/_titan RealName "titanOSX Management User"
dscl . -create /Users/_titan UniqueID 403  # Use something between 100 and 500 to hide the user
dscl . -create /Users/_titan PrimaryGroupID 20
dscl . -create /Users/_titan UserShell /sbin/nologin
dseditgroup -o edit -a _titan -t user admin
dseditgroup -o edit -a _titan -t user wheel"""
        shell_out(add_user_script)
    
    """ Postinstall hooks """
    def postinstall(self):
        # Post install script
        print "Updating permissions for titanOSX"
        shell_out("chown -R _titan /var/lib/titan")
        shell_out("chgrp -R wheel /var/lib/titan")
        shell_out("chmod -R 0633 /var/lib/titan/logs")
        shell_out("chmod -R 0666 /var/lib/titan/titan.db")
        shell_out("sudo launchctl load /Library/LaunchDaemons/com.titan.runner.plist")
        shell_out("sudo launchctl load /Library/LaunchDaemons/com.titan.watcher.plist")

    """ Runtime hooks """
    def run(self):

        self.preinstall()
        # Call the super run
        install.run(self)
        self.postinstall()

setup(
    name='titan',
    version=version,
    description='titanOSX: OSX Secure Device Monitoring',
    long_description=long_description.strip(),
    author='Mike Mackintosh',
    author_email='mike@shutterstock.com',
    license='MIT',
    url='http://titanOSX.com',
    packages=['titan'],
    data_files=[('/etc', ['titan.conf']), 
                ('/var/lib/titan/', ['README.md', 'titan.db']), 
                ('/var/lib/titan/monitors/', ['monitors/README.md']), 
                ('/var/lib/titan/logs/', []),
                ('/Library/LaunchDaemons/', ['plist/com.titan.runner.plist', 'plist/com.titan.watcher.plist']),
                ('/var/lib/titan/reports/', [])
               ],
    package_data={'': ['titan.db', 'titan.conf', 'README.md']},
    include_package_data=True,
    scripts=['scripts/titan', 'scripts/titan-watcher'],
#    install_requires=install_requires,
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
        'install': TitanInstaller,
    },
)
