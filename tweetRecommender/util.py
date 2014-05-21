import argparse
import inspect

def call_asmuch(fun, kwargs):
    args = inspect.getargspec(fun).args
    filtered_kwargs = dict((key, value) for (key, value)
            in kwargs.items() if key in args)
    return fun(**filtered_kwargs)


def set_vars(**varz):
    class SetVarsAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            for var, value in varz.items():
                setattr(namespace, var, value)
    return SetVarsAction
