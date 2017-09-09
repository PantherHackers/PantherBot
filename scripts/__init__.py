import os
commands = {}
for module in os.listdir(os.path.dirname(__file__)):
    mod_name = module[:-3]
    mod_ext = module[-3:]

    if module == '__init__.py' or mod_ext != '.py':
        continue
    commands[mod_name] = __import__(mod_name, locals(), globals())
