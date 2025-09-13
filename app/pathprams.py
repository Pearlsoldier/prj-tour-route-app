from urllib.parse import urlparse, parse_qs


def main():

    url = "https://api.example.com/v1/places/nearby?q=東京駅&radius=500&category=cafe"
    parsed_url = urlparse(url)
    print(parsed_url)
    query_params = parse_qs(parsed_url.query)
    print(query_params)


if __name__ == "__main__":
    main()
