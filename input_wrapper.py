def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args,**kwargs)
        except IndexError:
            return "Invalid input or command syntax. Please re-enter the command."
        except ValueError as e:
            msg = str(e)
            if msg and "not enough values" in msg:
                return "Missing arguments. Please check the command syntax."
            elif msg and "too many values" in msg:
                return "Too many arguments. Please check the command syntax."
            elif msg and "invalid literal" in msg:
                return "Invalid argument type. Please check the command syntax."
            else:
                return msg or "An error occurred. Please check your input."
        except AttributeError:
            return "Contact not found or command used incorrectly."
        
    return inner