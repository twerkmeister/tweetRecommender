import argparse
import repr as reprlib


def set_vars(**varz):
    class SetVarsAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            for var, value in varz.items():
                setattr(namespace, var, value)
    return SetVarsAction


class Repr(reprlib.Repr):
    def repr_Code(self, obj, level):
        return 'bson.Code(%s, %s)' % (
                self.repr1(str(obj), level - 1), self.repr1(obj.scope, level - 1))
repr_ = Repr().repr
