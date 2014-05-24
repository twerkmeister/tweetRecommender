import argparse

def set_vars(**varz):
    class SetVarsAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            for var, value in varz.items():
                setattr(namespace, var, value)
    return SetVarsAction
