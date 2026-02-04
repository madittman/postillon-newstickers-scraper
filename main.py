from url_builder import UrlBuilder


if __name__ == '__main__':
    url_builder: UrlBuilder = UrlBuilder()
    for i in range(10):
        print(url_builder.raw_url)
        url_builder += 1