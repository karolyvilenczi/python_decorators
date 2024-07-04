from time import sleep, perf_counter
import cProfile
from functools import wraps

# from decohints import decohints # https://pypi.org/project/decohints/
# to use add @decohints to the decorators 

# -----------------------------------------------------------------
def log_this(message:str="Called"):
    """
    Logs the function call with a custom message set in the decorator parameter.
    :message - Custom debug message prefix

    Example output: 
        DEBUG:root:Called 'test_log' with args=() & kwargs={}
    """

    import logging
    logging.basicConfig(level=logging.DEBUG)
  
    def decorator(func):
        @wraps(func)
        def wrapper_log(*args, **kwargs):
            msg = f"{message} '{func.__name__}' with {args=} & {kwargs=}"
            logging.debug(msg)
            return func(*args, **kwargs)
        
        return wrapper_log
    return decorator

# -----------------------------------------------------------------
def time_this(custom_args=None):
    """
    Decorator to measure the function execution using time.perf_counter()
    Example output: 
        Function 'test_time' ran for 3.0003 s.
    """
    def decorator(func):

        @wraps(func)
        def wrapper_time(*args, **kwargs):
            time_start = perf_counter()

            ret_val = func(*args, **kwargs)
            
            time_end = perf_counter()
            dur = time_end-time_start
            print(f"Funcion '{func.__name__}' ran for {round(dur, 4)} s.")

        return wrapper_time
    return decorator

# -----------------------------------------------------------------
def profile_this(profile_name:str = '', dump:bool=False):
    """
    Decorator to profile a function using cProfile.
    prof_name: sets a name for the profile
    dump: if set to true the profile will be dumped into a file named set by the profile_name parameter.

    Example output: 
    
        5 function calls in 3.000 seconds

    Ordered by: standard name

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    3.000    3.000 decorators.py:60(test_func)
            1    0.000    0.000    3.000    3.000 decorators.py:79(test_profile_w_file)
            1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
            1    3.000    3.000    3.000    3.000 {built-in method time.sleep}
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

    """
    def decorator(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            prof = cProfile.Profile()
            retval = prof.runcall(func,*args, **kwargs)
            if dump:
                prof.dump_stats(profile_name)
            
            prof.print_stats()
            return retval
        
        return wrapper
    return decorator

# -----------------------------------------------------------------

def test_func(a:int = 0, b:int = 0) -> int:
    sleep(3)
    result = a+b
    print(f"Result will be:{result}")
    return result

@log_this()
def test_log(a:int = 0, b:int = 0) -> int:
    return test_func(a, b)

@time_this()
def test_time(a:int = 0, b:int = 0) -> int:
    return test_func(a, b)


@profile_this()
def test_profile(a:int = 0, b:int = 0) -> int:
    return test_func(a, b)

@profile_this(prof_name="prof_for_test_profile", dump=True)
def test_profile_w_file(a:int = 0, b:int = 0) -> int:
    return test_func(a, b)


# -----------------------------------------------------------------
def main():
    print("------- Demos -------")

    print("\n1. log_this")
    test_log()

    print("\n2. time_this")
    test_time()

    print("\n3.1 profile_this")
    test_profile()

    print("\n3.1 profile_this with file")
    test_profile_w_file()

# -----------------------------------------------------------------
if __name__ == "__main__":
    print(f"Called directly")
    main()
else:
    print(f"Called as a module.")
    main()
