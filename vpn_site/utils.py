from urllib.parse import urlsplit

def extract_website_name(url):
    url_components = urlsplit(url)
    return url_components.netloc