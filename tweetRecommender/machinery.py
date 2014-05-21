import importlib
import pkgutil


def load_component(package, module, component):
    mod = importlib.import_module(package + '.' + module)
    return getattr(mod, component)

def find_components(package):
    modules = pkgutil.iter_modules(importlib.import_module(package).__path__)
    for module_loader, name, ispkg in modules:
        if not ispkg:
            yield name
