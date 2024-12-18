import datetime
import os
import json
import requests
from bs4 import BeautifulSoup


def logger(path):
    """
    Parameterized decorator for logging function calls.

    :param path: Path to the file where logs will be written.
    """

    def __logger(old_function):
        """
        Inner decorator that takes a function to be logged.

        :param old_function: The function being decorated.
        :return: A wrapped function.
        """

        def new_function(*args, **kwargs):
            """
            Wrapper function that saves function call information to a file.

            :param args: Positional arguments.
            :param kwargs: Keyword arguments.
            :return: Result of the decorated function.
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
            with open(path, mode='a') as file:
                file.write(json.dumps(log_entry) + '\n')

            return result

        return new_function

    return __logger


def test_2():
    """
    Test function to check the parameterized decorator's functionality.

    Deletes existing log files, creates new decorated functions,
    checks their correctness, and verifies the log file contents.
    """
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            """A simple function that returns the string 'Hello World'."""
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            """Adds two numbers."""
            return a + b

        @logger(path)
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

        # Additional tests for the summator function
        summator(4.3, b=2.2)

    for path in paths:
        # Check the existence of the log file
        assert os.path.exists(path), f'файл {path} должен существовать'

        # Read the contents of the log file
        with open(path) as log_file:
            log_file_content = log_file.read()

        # Ensure the function name appears in the logs
        assert 'summator' in log_file_content, 'должно записаться имя функции'

        # Ensure specific values appear in the logs
        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == "__main__":
    test_2()

    import requests
    from bs4 import BeautifulSoup

    KEYWORDS = ['дизайн', 'фото', 'web', 'python']

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }

    @logger('find_arcticles.txt')
    def find_articles_with_keywords(url):
        """
        The function returns a list with the date, title and link to the article
        param: url - link to resource
        return: relevant_articles - a list with the date, title and link to the article
        """
        # Send a get request to the specified page with headers
        response = requests.get(url, headers=HEADERS)

        # Checking the success of the response
        if response.status_code == 200:
            # Parsing HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Finding all article blocks
            articles = soup.find_all('article', class_='tm-articles-list__item')

            # Filter articles by keywords
            relevant_articles = []
            for article in articles:
                preview_info = article.text.lower()

                # Check for the presence of at least one keyword
                if any(keyword in preview_info for keyword in KEYWORDS):
                    date_element = article.find('time', class_='tm-article-snippet__datetime-published')
                    title_element = article.find('a', class_='tm-article-snippet__title-link')
                    link_element = article.find('a', class_='tm-article-snippet__title-link')

                    # Check that the elements are found
                    if date_element and title_element and link_element:
                        date = date_element.get('title')
                        title = title_element.text
                        link = link_element['href']

                        # Form the output string
                        output_string = f"{date} – {title} – {link}"
                        relevant_articles.append(output_string)
                    else:
                        print("Не удалось найти элементы для одной из статей.")

            return relevant_articles
        else:
            print(f"Произошла ошибка при получении страницы: статус-код {response.status_code}")
            return []


    # Specify the URL of the page with fresh articles
    url = 'https://habr.com/ru/articles/'

    # Call the function to get a list of relevant articles
    relevant_articles = find_articles_with_keywords(url)

    # Output the matching articles to the console
    if relevant_articles:
        for article in relevant_articles:
            print(article)
    else:
        print("Нет статей, содержащих указанные ключевые слова.")