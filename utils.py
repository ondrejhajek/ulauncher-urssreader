import re


def is_valid_url(url):
    url_pattern = re.compile(r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$')
    return bool(re.match(url_pattern, url))


def sanitize(input_string, max_length):
    input_string = re.sub('<.*?>', '', input_string)
    if len(input_string) > max_length:
        return input_string[:max_length - 3] + "..."
    else:
        return input_string
