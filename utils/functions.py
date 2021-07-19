from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from loader import _


class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    @classmethod
    async def create(cls, key):
        self = AESCipher()
        self.key = md5(key.encode('utf8')).hexdigest()
        self.block_size = 16
        return self

    async def encrypt(self, raw):
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_ECB)
        result = cipher.encrypt(pad(bytes(raw, 'utf-8'), self.block_size))
        print(result.hex())
        return result.hex()

    async def decrypt(self, enc):
        enc = bytes.fromhex(enc)
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_ECB)
        result = cipher.decrypt(enc)
        return unpad(result, self.block_size).decode('utf8')


# проверка на то, что строка - это число и с плавающей точкой тоже
async def is_digit(string):
    if string.isdigit():
        if int(string) > 0:
            if int(string) == abs(int(string)):
                return True
        else:
            return False
    else:
        try:
            if float(string):
                if float(string) == abs(float(string)):
                    return True
        except ValueError:
            return False


async def text_sum_digit():
    text = _('Ввод должен быть только в виде цифр и больше 0')
    return text


async def check_number_dict():
    text = _('Такой записи не существует. Попробуйте ввести корректный номер')
    return text


async def check_button():
    text = _('Такой кнопки не существует. Попробуйте нажать корректную кнопку')
    return text