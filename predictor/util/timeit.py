import time


def timeit(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        global logger
        logger.error(
            'func:%r args:[%r, %r] took: %2.4f sec' %
            (f.__name__, args, kw, te - ts))
        return result

    return timed
