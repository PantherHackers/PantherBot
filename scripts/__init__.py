import os
commands = {}
for module_file in os.listdir(os.path.dirname(__file__)):
    mod_name = module_file[:-3]
    mod_ext = module_file[-3:]

    if module_file == '__init__.py' or mod_ext != '.py':
        continue
    module = __import__(mod_name, locals(), globals())
    get_alias = getattr(module, "return_alias")
    list_of_alias = get_alias()
    for alias in list_of_alias:
        commands[alias] = module
