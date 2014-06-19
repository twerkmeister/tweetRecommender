from logging import *
import logging
import contextlib
import timeit

class TimedLogger(logging.getLoggerClass()):
    @contextlib.contextmanager
    def measured(self, msg, *args, **kwargs):
        self.info(msg + '..', *args, **kwargs)
        start_time = timeit.default_timer()
        yield
        end_time = timeit.default_timer()
        self.info("%s took %.2fs." % (msg, end_time - start_time),
                *args, **kwargs)

setLoggerClass(TimedLogger)
