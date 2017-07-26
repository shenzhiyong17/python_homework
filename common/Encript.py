import base64


class AESCipher:
    def __init__(self, key, bs=None, iv=None):

        from Crypto.Cipher import AES

        self.AES = AES

        if bs is None:
            bs = AES.block_size

        self.key = key

        self.pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
        self.unpad = lambda s: s[0:-ord(s[-1])]

        if iv is None:
            iv = '\0' * bs

        self.iv = iv

    def encrypt(self, raw):
        cipher = self.AES.new(self.key, self.AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(self.pad(raw)))

    def decrypt(self, encrypt_string):
        cipher = self.AES.new(self.key, self.AES.MODE_CBC, self.iv)
        return self.unpad(cipher.decrypt(base64.b64decode(encrypt_string)))

    def ecb_encrypt(self, raw):
        cipher = self.AES.new(self.key, self.AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(self.pad(raw)))

    def ecb_decrypt(self, encrypt_string):
        cipher = self.AES.new(self.key, self.AES.MODE_ECB)
        return self.unpad(cipher.decrypt(base64.b64decode(encrypt_string)))
