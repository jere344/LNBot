import glob
import importlib

file_list = glob.glob("commands/[!_]*")
module_list = [
    e.replace(".py", "").replace("\\", ".").replace("/", ".") for e in file_list
]

for module in module_list:
    print(module)
    importlib.import_module(module)
