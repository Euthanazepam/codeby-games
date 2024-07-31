import tarfile

from requests import get

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_173db536-19e0-4510-8516-624e74ff619f_data"
filename = "task"
filetype = "tar"


def download_tar() -> None:
    """
    Downloads a tar file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"RSA Basics 1/{filename}.{filetype}", "wb") as f:
            f.write(response.content)
    except FileNotFoundError:
        with open(f"{filename}.{filetype}", "wb") as f:
            f.write(response.content)


def unpack() -> None:
    """
    Unpacks a tar file into the current directory.
    """

    download_tar()

    try:
        with tarfile.open(f"RSA Basics 1/{filename}.{filetype}", 'r:*') as tar:
            tar.extractall(path=f"RSA Basics 1/")
    except FileNotFoundError:
        with tarfile.open(f"{filename}.{filetype}", 'r:*') as tar:
            tar.extractall(path=".")


def get_flag() -> str:
    """
    https://codeby.games/en/categories/cryptography/173db536-19e0-4510-8516-624e74ff619f
    """

    unpack()

    try:
        with open("RSA Basics 1/data.txt", "r") as f:
            data = f.readlines()
    except FileNotFoundError:
        with open("data.txt", "r") as f:
            data = f.readlines()

    try:
        with open("RSA Basics 1/flag.txt", "rb") as f:
            flag_txt = f.read()
    except FileNotFoundError:
        with open("flag.txt", "rb") as f:
            flag_txt = f.read()

    n = int(data[0][2:].replace(',', '').replace('\n', ''))
    e = int(data[1][2:].replace(',', '').replace('\n', ''))
    p = int(data[2][2:].replace(',', '').replace('\n', ''))
    q = n // p
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    c = int.from_bytes(flag_txt)

    """
    References:
        1. RSA Decoder — https://www.dcode.fr/rsa-cipher
    
    ======================================================================
    
    A bit of theory:
        m — message (plain text)
        c — cipher text
        
        n = p * q
        φ(n) = (p - 1) * (q - 1)
        
        d — secret exponent
        d = e^(-1) mod φ(n)
        
        Public key:     (n, e)
        Private key:    (n, d)
        
        Encryption:     c = m^e mod n
        Decryption:     m = c^d mod n
    """

    decrypted_message = pow(c, d, n)

    # The key length is 1024 bits. The flag is at the end of the message.
    flag = decrypted_message.to_bytes(1024, 'big')[-29:].decode()

    return flag


if __name__ == '__main__':
    print(get_flag())
