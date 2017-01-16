#from os.path import dirname, basename, isfile
#import glob
#modules = glob.glob(dirname(__file__)+"/*.py")
#__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

import os
commands = {}
for module in os.listdir(os.path.dirname(__file__)):
	mod_name = module[:-3]
	mod_ext = module[-3:]

	if module == '__init__.py' or mod_ext != '.py':
		continue
	commands[mod_name] = __import__(mod_name, locals(), globals())
