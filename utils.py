
def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except IndexError:
            return "Invalid data.", "error"
        except KeyError:
            return "No contact with that name.", "warning"
        except ValueError:
            return "Invalid command.", "error"
        except TypeError:
            return "Invalid command.", "error"
    return inner
