#!/usr/bin/env python3

import time

def timing(method):
    '''
    Quick and dirty time function: it will record the time when
    it is calling a function, record the time when it returns and
    compute the difference. There'll be some overhead, so it is not
    very precise, but it will suffice
    '''

    def timed(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()

        execution_time = end - start
        if execution_time <0.001:
            print(f'{method.__name__} took {execution_time*1000} milliseconds')
        else:
            print(f'{method.__name__} took {execution_time*1000} seconds')

        return result
    return timed
