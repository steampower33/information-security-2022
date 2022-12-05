from Crypto import Random
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64, json

def decode_base64(b64):
    return base64.b64decode(b64)

def encode_base64(p):
    return base64.b64encode(p).decode('ascii')

def make_cert_hash(name, pubKeyBase64):
	message = name + pubKeyBase64 # 해시 생성 방법 -> H(name + pubKey)
	return SHA256.new(message.encode('utf-8'))

def read_as_json():
	json_str = decode_base64(input()).decode('utf-8')
	json_obj = json.loads(json_str)
	return json_obj

# https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
def verify(hash, key, signature):
    # PKCS #1 v1.5 를 이용한 전자서명 검증, 성공시 True, 실패시 False 리턴
	k = RSA.import_key(decode_base64(key))
	sign = decode_base64(signature)
	try:
		pkcs1_15.new(k).verify(hash, sign)
		print True
	except (ValueError, TypeError):
		print False

cert = read_as_json()

hash_compare = make_cert_hash(cert)# 비교할 해시 생성
print(cert)

server_pubkey = cert("serverPubKey") # bytes:서버 공개키 (HINT: JSON에는 BASE64 형태로 제공되어 있음)
signature = cert("signature") # bytes:서버 서명 (HINT: JSON에는 BASE64 형태로 제공되어 있음)

cert['isValid'] = verify(hash_compare, server_pubkey, signature) # 인증서 내 서명 검증

json_str = json.dumps(cert).encode('utf-8')

print(encode_base64(json_str))