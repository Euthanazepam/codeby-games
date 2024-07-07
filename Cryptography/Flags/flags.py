from requests import get
from zipfile import ZipFile

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_a7676d01-1141-4788-a4b2-4bd8b546897b_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Flags/{filename}.{filetype}", "wb") as f:
            f.write(response.content)
    except FileNotFoundError:
        with open(f"{filename}.{filetype}", "wb") as f:
            f.write(response.content)


def unzip() -> str:
    """
    Unpacks a zip file into the current directory.
    :return: Name of file
    """

    download_zip()

    try:
        with ZipFile(f"Flags/{filename}.{filetype}") as zf:
            zf.extractall(path="Flags/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path=".")
            return zf.namelist()[0]


def get_flag() -> str:
    """
    https://codeby.games/en/categories/cryptography/a7676d01-1141-4788-a4b2-4bd8b546897b
    """

    unzip()

    # A useful resource with country flags — https://flagpedia.net.
    message_flags = [
        'Cyprus',
        'Oman',
        'Dominica',
        'Egypt',
        'Brazil',
        'Yemen',
        'Yemen',
        'Oman',
        'Uganda',
        'Albania',
        'Romania',
        'Estonia',
        'India',
        'Niger',
        'Vietnam',
        'Ecuador',
        'Nigeria',
        'Turkey',
        'Italy',
        'Venezuela',
        'Estonia',
    ]

    flag_chars = []

    """
    Take the first letter of the country's name.
    """

    for item in message_flags:
        flag_chars.append(item[0])

    flag = (''.join(flag_chars)[:5] + '{' + ''.join(flag_chars)[6:9].lower() + '_' + ''.join(flag_chars)[9:12].lower()
            + '_' + ''.join(flag_chars)[12:].lower() + '}')

    return flag


if __name__ == '__main__':
    print(get_flag())
