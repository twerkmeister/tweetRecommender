import importlib
import pkgutil


GATHER_PACKAGE = 'tweetRecommender.gather'
GATHER_METHOD = 'gather'
SCORE_PACKAGE = 'tweetRecommender.rank'
SCORE_METHOD = 'score'
SCORE_INFO_FIELDS = 'fields'
FILTER_PACKAGE = 'tweetRecommender.filter'
FILTER_METHOD = 'filter'


def load_component(package, module, component):
    package, module = package.strip(), module.strip()
    try:
        mod = importlib.import_module(package + '.' + module)
    except ImportError, e:
        raise ImportError("error importing '%s.%s': %s" % (package, module, e))
    try:
        return getattr(mod, component)
    except AttributeError, e:
        raise ImportError("error importing '%s.%s.%s': %s" %
                (package, module, component, e))


def find_components(package):
    modules = pkgutil.iter_modules(importlib.import_module(package).__path__)
    for module_loader, name, ispkg in modules:
        if not ispkg:
            yield name

def get_display_name(package, module):
    display_name = module
    try:
        display_name = load_component(package, module, "DISPLAY_NAME")
    except AttributeError:
        pass
    return display_name
