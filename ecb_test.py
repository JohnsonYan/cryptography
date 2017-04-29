from Crypto.Cipher import DES3
import binascii

def hex_s(str):
    re = ''
    for i in range(0,len(str)):
        re += "\\x"+binascii.b2a_hex(str[i])
    return re

key = '1234567812345678'

plain = 'aaaabbbbaaaabbbb'
plain1 = 'xaaabbbbaaaabbbb'
plain2 = 'aaaabbbbxaaabbbb'

o = DES3.new(key, 1) # arg[1] == 1 means ECB MODE

print "1 : "+hex_s(o.encrypt(plain))
print "2 : "+hex_s(o.encrypt(plain1))
print "3 : "+hex_s(o.encrypt(plain2))
