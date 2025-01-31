# utils/exception_handler.py
def handle_exception(func):
    """
    Decorator to handle exceptions in functions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    return wrapper
