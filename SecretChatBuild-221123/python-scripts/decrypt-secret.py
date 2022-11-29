from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def decode_base64(b64):
    return base64.b64decode(b64)


def read_from_base64():
    return [decode_base64(input()), decode_base64(input())]


def decrypt_secret(secret, priKey):
    # PKCS#1 OAEP를 이용한 RSA 복호화 구현
    rsa = RSA.importKey(priKey)
    pkcs = PKCS1_OAEP.new(rsa)
    pkcs_de_secret = pkcs.decrypt(secret)
    result = base64.b64encode(pkcs_de_secret)
    return result


[secret, prikey] = read_from_base64()
result = decrypt_secret(secret, prikey).decode('ascii')

print(result)
