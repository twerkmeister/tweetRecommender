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
    mod = importlib.import_module(package + '.' + module)
    return getattr(mod, component)

def find_components(package):
    modules = pkgutil.iter_modules(importlib.import_module(package).__path__)
    for module_loader, name, ispkg in modules:
        if not ispkg:
            yield name
