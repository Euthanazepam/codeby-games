from requests import get
from zipfile import ZipFile

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_b0967cfb-8c27-4491-b9a4-4278635c2ccd_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"RSA 2 Basics/{filename}.{filetype}", "wb") as f:
            f.write(response.content)
    except FileNotFoundError:
        with open(f"{filename}.{filetype}", "wb") as f:
            f.write(response.content)


def unzip() -> None:
    """
    Unpacks a zip file into the current directory.
    """

    download_zip()

    try:
        with ZipFile(f"RSA 2 Basics/{filename}.{filetype}") as zf:
            zf.extractall(path="RSA 2 Basics/")
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path=".")


def get_flag() -> str:
    """
    https://codeby.games/en/categories/cryptography/b0967cfb-8c27-4491-b9a4-4278635c2ccd
    """

    unzip()

    try:
        with open("RSA 2 Basics/data.txt", "r") as f:
            data = f.readlines()
    except FileNotFoundError:
        with open("data.txt", "r") as f:
            data = f.readlines()

    try:
        with open('RSA 2 Basics/flag.txt', 'rb') as f:
            flag_txt = f.read()
    except FileNotFoundError:
        with open("flag.txt", "rb") as f:
            flag_txt = f.read()

    """
    References:
        1. RSA Decoder — https://www.dcode.fr/rsa-cipher
        2. FactorDB — http://factordb.com
    """

    c = int.from_bytes(flag_txt)
    n = int(data[0][2:].strip(',\n'))
    e = int(data[1][2:].strip('\n'))

    # Use http://factordb.com to factorize n
    p = 14140603756509138613
    q = 5489043545622560409897785028566430416075633798236408932642930675468814810653708075840730291972288015238274091948233904557841559838718158786423410742419035086994989171455091568288674915165515311452426323545560344982020250485952248735228291934709722380663393848767700125976591262399497436679527222262943418842072565225327647854320637789258227639897812114788852645420993407774316547877362035059374175651247828946347364181645826552407428743571106909351678126961036066914677925384048546337178509073652573598168405397260159188896104584750070548973004265977567759439373120260491594222271563482686282269250693279645404435932690274055811271813138143298472040386549378712338608478738073854829905194280579884534175220225021547253274290965465975666584741751463978766666898066907553211529000548203774337096785800877745069690142001875020429229998627784965888338845781812930932675394051677955055323067964288859246239227629223831713839864787

    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)

    decrypted_message = pow(c, d, n)

    # The key length is 2048 bits. The flag is at the end of the message.
    flag = decrypted_message.to_bytes(2048, 'big')[-41:].decode()

    return flag


if __name__ == '__main__':
    print(get_flag())
