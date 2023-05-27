def send_result(*args, **kargs):
    _args = _prepare_arguments(args, kargs)
    return True

def _prepare_arguments(*args, **kargs):
    _args = {}
    
    for key, value in kargs.items():
        _args[key] = value

    i = 0
    for value in args:
        while f"arg{i}" in _args:
            i += 1

        _args[f"arg{i}"] = value

    return _args
