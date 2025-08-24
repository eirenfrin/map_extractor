import consts as c
import functools

def default_to_constant(params_dict):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for param, corresponding_const in params_dict.items():
                if param not in kwargs:
                    kwargs[param] = getattr(c, corresponding_const)
            return func(*args, **kwargs)
        return wrapper
    return decorator