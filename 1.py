import datetime
import os
import json


def logger(old_function):
    """Decorator for logging function calls."""

    def new_function(*args, **kwargs):
        """
        Wrapper for the decorated function.

        Saves information about the function call to the 'main.log' file.
        """
        # Get current date and time
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Function name
        function_name = old_function.__name__

        # Arguments passed to the function
        arguments = args
        keyword_arguments = kwargs

        # Call the original function and get its result
        result = old_function(*args, **kwargs)

        # Format the log entry
        log_entry = {
            "timestamp": now,
            "function_name": function_name,
            "arguments": arguments,
            "keyword_arguments": keyword_arguments,
            "return_value": result
        }

        # Write to the log file
        with open('main.log', mode='a') as file:
            file.write(json.dumps(log_entry) + '\n')

        return result

    return new_function


def test_1():
    """
    Test function to verify the decorator's functionality.

    Creates and deletes the 'main.log' file, checks the correctness of the
    decorated functions.
    """
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        """Simple function that returns the string 'Hello World'."""
        return 'Hello World'

    @logger
    def summator(a, b=0):
        """Sums two numbers."""
        return a + b

    @logger
    def div(a, b):
        """Divides the first number by the second."""
        return a / b

    # Check the output of the hello_world function
    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"

    # Check the output of the summator function
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'

    # Check the output of the div function
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    # Verify the existence of the 'main.log' file
    assert os.path.exists(path), 'файл main.log должен существовать'

    # Additional tests for the summator function
    summator(4.3, b=2.2)
    summator(a=0, b=0)

    # Read the contents of the 'main.log' file
    with open(path) as log_file:
        log_file_content = log_file.read()

    # Ensure the function name appears in the logs
    assert 'summator' in log_file_content, 'должно записаться имя функции'

    # Ensure specific values appear in the logs
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == "__main__":
    test_1()