def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args,**kwargs)
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
            
        except KeyError:
            return "Contact not found"
        except IndexError:
            return "Please enter your username"
        except AttributeError:
            return "Contact not found or command used incorrectly."
        except TypeError:
            return "Incorrect command usage. Please verify syntax."
        
    return inner
