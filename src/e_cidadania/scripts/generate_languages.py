#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script automates the creation of all the language catalogs for
e-cidadania project.
"""

import sys
import os
import subprocess

__author__ = "Oscar Carballal"
__copyright__ = "Copyright 2011, Cidadania Sociedade Cooperativa Galega"
__credits__ = ["Oscar Carballal"]
__license__ = "GPLv3"
__version__ = "0.4"
__maintainer__ = "Oscar Carballal"
__email__ = "oscar.carballal@cidadania.coop"
__status__ = "Prototype"

print "\n>>>> e-cidadania language catalog generator <<<<"
print "\nPlease note that this script must be run from the project root or from \
the scripts directory. If you run it from somewhere else it won't work."
raw_input('\nPress any key to continue or Ctrl-C to exit...')

class Language():

    """
    """
    def __init__(self):
        
        """
        """
        # Get current work directory and add it to sys.path so we can import
        # the project settings.
        self.cwd = os.getcwd().strip('scripts')
        sys.path.append(self.cwd)

        # Get the languages configured in settings.py and the installed
        # e-cidadania modules.
        import settings

        self.applications = settings.ECIDADANIA_MODULES
        self.languages = settings.LANGUAGES
        self.apps = []
        
        # Spit out the information
        print "\n>> Languages to generate:"
        for lang in self.languages:
            print ' - ' + lang[1]

        print "\n>> Installed applications:"
        for app in self.applications:
            self.got_it = app.split('.')[2]
            print ' - ' + self.got_it
            self.apps.append(self.got_it)

    def _iterator(self, command, type):

        """
        This method iterates over the applications and languages making
        what the command says.
        """
        for module in self.apps:
            os.chdir(self.cwd + '/apps/' + module)
            print '\n>> %s language catalogs for %s' % (type, module)
            for lang in self.languages:
                a = subprocess.Popen(command + '%s' % (lang[0]), shell=True)
                subprocess.Popen.wait(a)

        print '\n>> %s site root language catalogs' % (type)
        os.chdir(self.cwd)
        for lang in self.languages:
            a = subprocess.Popen(command + '%s' % (lang[0]), shell=True)
            subprocess.Popen.wait(a)

            
    def generate_catalog(self):
        
        """
        Generate the language catalogs for the application and site root
        """
        self._iterator('django-admin.py makemessages -l ', 'Generating')


    def compile_catalog(self):

        """
        """
        for module in self.apps:
            os.chdir(self.cwd + '/apps/' + module)
            print '\n>> Compiling all messages for %s' % (module)
            a = subprocess.Popen('django-admin.py compilemessages ',
                                 shell=True)
            subprocess.Popen.wait(a)

        print '\n>> %s site root language catalogs' % (type)
        os.chdir(self.cwd)
        a = subprocess.Popen('django-admin.py compilemessages ', shell=True)
        subprocess.Popen.wait(a)


    def clean_catalogs(self):

        """
        """
        print '\n>> WARNING: This command will remove ALL the language \
catalogs, having to rebuild and translate them all.'
        raw_input('\n Continue? (Ctrl-C to quit)')
        self._iterator('rm -rf locale/', 'Cleaning')

lang = Language()

if sys.argv[1] == 'make':
    lang.generate_catalog()
elif sys.argv[1] == 'compile':
    lang.compile_catalog()
elif sys.argv[1] == 'clean':
    lang.clean_catalogs()
else:
    print '\nChoices are: make, compile, clean'