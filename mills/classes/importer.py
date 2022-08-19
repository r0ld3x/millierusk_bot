import os,sys, glob
from importlib import import_module
from pathlib import Path
import inspect


from mills.utils.logger import log
from mills.plugins import ADMIN_HELP, MOD_HELP



class ImportError(Exception):
    
    def __init__(self, path:str , message:str = "Can't Import!", *args: object) -> None:
        self.path = path
        self.message = message
        super().__init__(self.message)




class Importer():
    
    def __init__(self, path: str, import_all: bool = True):
        self.path = path
        self.import_all = import_all
        self.importer()
    
    def get_modules(self, path: str):
        path = glob.glob(f"{path}/*.py")
        # log.debug("Trying to import %s modules from %s", len(path), Path(x).name for x in path)
        all_mod = []
        for file in sorted(path):
            if '__init__' in file: continue
            if '__pycache__' in file: continue
            module = file.replace("/", ".").replace('\\', '.')
            module = module.replace(".py", "")
            if module not in all_mod:
                all_mod.append(module)
        return all_mod
        
    def loader(self, module, name_of_plug = "main"):
        name = name_of_plug
        try:
            log.debug("Importing {}".format(module))
            x = import_module(module)
        except ImportError as e:
            log.exception(e)
            sys.exit(1)
            
        plugin = Path(x.__file__).stem
        if (
            not module.startswith('_') 
            and (x and hasattr(x, '__doc__'))
            and not plugin.startswith('_')
        ):
            doc = x.__doc__
            if name == 'admins':
                try:
                    ADMIN_HELP.update({plugin: doc})
                except Exception as e:
                    log.exception(e)
                    sys.exit(1)
            else:
                if name in MOD_HELP.keys():
                    mod_main = MOD_HELP[name]
                    try:
                        mod_main.update({plugin: doc})
                    except Exception as e:
                        log.exception(e)
                        sys.exit(1)
                else:
                    try:
                        MOD_HELP.update({name: {plugin: doc}})
                    except Exception as e:
                        log.exception(e)
                        sys.exit(1)

    def importer(self):
        if not self.import_all:
            module = self.get_modules(self.path)
            for mod in module:
                self.loader(mod)
        elif self.import_all:
            dirs = [self.path]
            for file in os.listdir(self.path):
                d = os.path.join(self.path, file)
                if os.path.isdir(d) :
                    if d.endswith('_'): continue
                    dirs.append(d)
            for file in sorted(dirs):
                module = self.get_modules(file)
                for mod in module:
                    name = mod.split('.')[-2]
                    if name.startswith('_'): continue
                    self.loader(mod, name_of_plug = name)