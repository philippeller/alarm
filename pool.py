from Foundation import *

#pool decorator
def pool(fn):
    def pool_wrapper(*args,**kwargs):
        pool = NSAutoreleasePool.alloc().init()
        fn(*args,**kwargs)
        del pool
    return pool_wrapper

