-> ![TitanOSX](titan.png) <-

TitanOSX
=========
------------------

titanOSX is an enterprise monitoring solution for Mac deployments. It is open-source and allows for monitoring of devices which could easily become compromised and present extreme risk to corporate operations.

titanOSX spawned from the hard work of the MIDAS/Tripyarn project, a Etsy/Facebook masterpiece. 

----------------------------------------------------------------------------------

Features
--------
titanOSX was built to solve one problem; the visibility of device contents. In the event a developer or systems engineer had their device was lost or stolen, security teams could easily assess the impact that a malicious user could have on the infrastructure.a

  - Inventory Management (if configured)
  - Built-in Reporting
  - Configurable Endpoints
  - Easy Configuration Management (key for Chef/Puppet)
  - Easy Installation of Modules and Extensions
  
Installation
------------
titanOSX at its core is just a Python script. So installation is pretty simple using Python's setuptools:

###From Source:    

    git clone https://github.com/titanosx/cli.git titan
    cd titan && sudo python setup.py install

### From PyPi

    sudo pip install titantools titan

Configuration
-------------
The main configuration file exists at `/etc/titan.conf`. 

Usage
-----
After installation, you can run titanOSX with the following script at `/usr/local/bin/titan`. You can add this script to your `PATH`, although `setup.py` should do this for you.

You can then execute commands and view the usage/help dialog with just:

    titan
   
There is a second script which is called `titan-watcher`. The watcher script is designed to relay the data upstream to a reporting endpoint. This would generally not be invoked manually unless you'd like to test, debug or force data transmit. 

**!#@ OMGZS SO EFFN IMPRTNT NOTE !!**: The endpoint should be configured with TLS, as failure to do so could lead to leaked data if network traffic is sniffed.

Upgrade
-------
You can upgrade titanOSX by either using `git pull` if you checked out manually, or by issuing `sudo pip install titan --upgrade`

Modules
-------
titanOSX doesn't call modules, modules. We call them monitors. You can make anything a monitor as long as it's a script within a git repo. Our auto-includer will detect it and run it. 

You can find some open-source monitors here: [https://github.com/titan-modules](https://github.com/titan-modules)

### Installing Monitors

To install a monitor, use:

    titan monitor install <git-repo-path>
    
### Upgrading Monitors

To upgrade a monitor, use:

    titan monitor upgrade <name>

### Removing Monitors

To remove a monitor, use:

    titan monitor remove <name>

Reporting
---------
What good would something like this be if you couldn't see what it was capturing?! For this simple result, we created the ability for users to run a self-destructing report.

The report will aggregate all the data recorded and display it in your browser automatically.

    titan report

----------------------------------------------------------------------------------

Contributors
---------------------------

#### titanOSX Contributors

+ __Mike Mackintosh__ ([![@mikemackintosh][twitter]](http://twitter.com/mikemackintosh)
 [@mikemackintosh](https://twitter.com/mikemackintosh))

#### Original MIDAS Contributors

+ __Mike Arpaia__ ([![@mikearpaia][twitter]](http://twitter.com/mikearpaia)
[@mikearpaia](https://twitter.com/mikearpaia))
+ __Chris Biettchert__ ([![@chrisbiettchert][twitter]](http://twitter.com/chrisbiettchert)
[@chrisbiettchert](https://twitter.com/chrisbiettchert))
+ __Ben Hughes__ ([![@benjammingh][twitter]](http://twitter.com/benjammingh)
[@benjammingh](https://twitter.com/benjammingh))
+ __Zane Lackey__ ([![@zanelackey][twitter]](http://twitter.com/zanelackey)
[@zanelackey](https://twitter.com/zanelackey))
+ __mimeframe__ ([![@mimeframe][twitter]](http://twitter.com/mimeframe)
[@mimeframe](https://twitter.com/mimeframe))

Enjoy.

  [twitter]: http://i.imgur.com/wWzX9uB.png
  [github]: http://i.imgur.com/9I6NRUm.png
