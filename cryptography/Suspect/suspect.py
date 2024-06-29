import requests

from zipfile import ZipFile

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_2f3f6f75-915d-4516-b193-41bd5ce6a4c0_data"
filename = "Suspect"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = requests.get(url=url)

    try:
        with open(f"Suspect/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Suspect/{filename}.{filetype}") as zf:
            zf.extractall(path="Suspect/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path=".")
            return zf.namelist()[0]


def get_flag() -> str:
    """
    https://codeby.games/en/categories/cryptography/2f3f6f75-915d-4516-b193-41bd5ce6a4c0
    """

    file_name = unzip()

    try:
        with open(f"Suspect/{file_name}", "r") as f:
            sus = f.read()
    except FileNotFoundError:
        with open(f"{file_name}", "r") as f:
            sus = f.read()

    hex_string = hex(int(sus))[2:]
    flag = bytes.fromhex(hex_string).decode('utf-8')

    return flag


if __name__ == '__main__':
    print(get_flag())
