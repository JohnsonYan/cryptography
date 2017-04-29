#coding=utf-8
import os
import random
import hashlib

# test dsa example
dsa_key = {
    'Q': 1218442816993522937915646204915776994404649089503L,
    'P': 11220611807188583130302963536190351192186270126479330588604287699892081267588448305835704397593153801135202051719876685351614175538253684346816652027037363L,
    'G': 11189361631195852088154673407566885728548496486362662112597687161142104619469702160215294558351391466982303919803857229515093575816938371433954759500448775L,
    'pub': 4572510396595314270786423212039255215498677297795049756997099191729339616558419010431226927123876238239229467750410441342637393785565872285607741290303779L,
    'priv': 148102768779017960166999813987055538077373228390L}
text = """Its a hard enough life to be living,Why walk when you can fly"""

# 随机选择一个数
def _random_s(min, max):
    s = -1
    # 位数
    digits = random.randint(len(str(min)), len(str(max)))
    while True:
        u = map(ord, os.urandom(digits))
        if u == None:
            continue
        s = int(''.join(str(x) for x in u)[:digits])
        if s <= max and s >= min:
            break
    # 位数为digits的数字
    return s

# 计算模逆
def gcd(a,b):
    while a != 0:
        a,b = b % a,a
    return b

def findModInverse(a,m):
    if gcd(a,m) != 1:
        return None
    u1,u2,u3 = 1,0,a
    v1,v2,v3 = 0,1,m
    while v3 != 0:
        q = u3 // v3
        v1,v2,v3,u1,u2,u3 = (u1 - q * v1),(u2 - q * v2),(u3 - q * v3),v1,v2,v3
    return u1 % m

# a ^ b (mod n)
def fastExpMod(a,b,n):
    result = 1
    while b != 0:
        # b为奇数，即b mod 2 != 0
        if (b&1) == 1:
            result = (result * a) % n
        # b = b/2,不考虑b-1,因为b/2取了地板数
        b >>= 1
        a = (a*a) % n
    return result

def _digits_of_n(n, b):
    digits = []
    while n:
        digits.append(int(n % b))
        n /= b
    return digits

def dsa_sign(q, p, g, x, message):

    s = _random_s(1, q)
    s1 = 0
    s2 = 0
    while True:
        modexp = fastExpMod(g, s, p)
        s1 = modexp % q
        if s1 == 0:
            s = _random_s(1, q)
            continue
        s = findModInverse(s, q) * (message + x * s1)
        s2 = s % q
        if s2 == 0:
            s = _random_s(1, q)
            continue
        return (int(s1), int(s2))


def dsa_verify(s1, s2, g, p, q, y, message):

    if not s1 > 0:
        return False
    if not s1 < q:
        return False
    if not s2 > 0:
        return False
    if not s2 < q:
        return False
    w = findModInverse(s2, q)
    u1 = (message * w) % q
    u2 = (s1 * w) % q

    u1 = fastExpMod(g, u1, p)
    u2 = fastExpMod(y, u2, p)
    v = u1 * u2 % p % q
    if v == s1:
        return True
    return False



if __name__ == "__main__":
    m = hashlib.sha1()
    m.update(text)
    message = int("0x" + m.hexdigest(), 0)
    sig = dsa_sign(dsa_key["Q"], dsa_key["P"], dsa_key["G"], dsa_key["priv"], message)
    print "=" * 80
    print "DSA SIGNATURE TEST"
    print "=" * 80
    print "DSA Group:"
    for k in dsa_key.keys():
        print k, ':', str(dsa_key[k])
    print "-" * 80
    print "Text:"
    print text
    print "-" * 80
    print "SHA-1:",
    print message
    print "-" * 80
    print "DSA Signature:",
    print sig
    print "-" * 80
    print "Verify:",
    print dsa_verify(sig[0], sig[1], dsa_key["G"], dsa_key["P"], dsa_key["Q"], dsa_key["pub"], message)
    print "-" * 80
