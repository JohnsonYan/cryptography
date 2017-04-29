#coding=utf-8
import random

def fastExpMod(b,e,m):
    # b^e mod m
    result = 1
    while e != 0:
        # e为奇数，即e mod 2 != 0
        if (e&1) == 1:
            result = (result * b) % m
        # e = e/2,不考虑e-1,因为e/2取了地板数
        e >>= 1
        b = (b*b) % m
    return result

def primeTest(n):
    q = n - 1
    k = 0
    # 寻找 k,q,满足 2^k * q = n - 1
    while q % 2 == 0:
        k += 1
        q /= 2
    a = random.randint(2,n-2)
    # 如果 a^q mod n = 1,n 可能是素数
    if fastExpMod(a,q,n) == 1:
        return "Uncertain"
    # 如果存在 j 满足 a ^ ((2^j)*q) mod == n-1,n 可能是素数
    for j in range(0,k):
        if fastExpMod(a,(2**j)*q,n) == n - 1:
            return "Uncertain"
    # 不是素数
    return "Fail"

def findPrime(halfkeyLength):
    while True:
        n = random.randint(0,1<<halfkeyLength)
        if n % 2 != 0:
            found = True
            for i in range(0,10):
                if primeTest(n) == "Fail":
                    found = False
                    break
            if found:
                return n

def extendedGCD(a,b):
    # a*xi + b*yi = ri
    if b == 0:
        return (1,0,a)
    # a*x1 + b*y1 = a
    x1 = 1
    y1 = 0
    # a*x2 + b*y2 = b
    x2 = 0
    y2 = 1
    while b != 0:
        q = a / b
        # ri = r(i-2) % r(i-1)
        r = a % b
        a = b
        b = r
        # xi = x(i-2) - q*x(i-1)
        x = x1 - q*x2
        x1 = x2
        x2 = x
        # yi = y(i-2) - q*y(i-1)
        y = y1 - q*y2
        y1 = y2
        y2 = y
    return (x1,y1,a)

def selectE(fn,halfkeyLength):
    while True:
        e = random.randint(0,1<<halfkeyLength)
        (x,y,r) = extendedGCD(e,fn)
        if r == 1:
            return e

def computeD(fn,e):
    (x,y,r) = extendedGCD(fn,e)
    if y < 0:
        return fn + y
    return y

def keyGeneration(keyLength):
    p = findPrime(keyLength/2)
    q = findPrime(keyLength/2)
    n = p * q
    fn = (p-1)*(q-1)
    e = selectE(fn,keyLength/2)
    d = computeD(fn,e)
    return (n,e,d)

def encryption(M,e,n):
    # RSA C = M^e mod n
    return fastExpMod(M,e,n)

def decryption(C,d,n):
    # RSA M = C^d mod n
    return fastExpMod(C,d,n)

dictionary = {' ':'00','A':'01','B':'02','C':'03','D':'04','E':'05','F':'06','G':'07',
              'H':'08','I':'09','J':'10','K':'11','L':'12','M':'13','N':'14','O':'15',
              'P':'16','Q':'17','R':'18','S':'19','T':'20','U':'21','V':'22','W':'23',
              'X':'24','Y':'25','Z':'26'}
dictionary_1 = {'00':' ','01':'A','02':'B','03':'C','04':'D','05':'E','06':'F','07':'G',
              '08':'H','09':'I','10':'J','11':'K','12':'L','13':'M','14':'N','15':'O',
              '16':'P','17':'Q','18':'R','19':'S','20':'T','21':'U','22':'V','23':'W',
              '24':'X','25':'Y','26':'Z'}
Text = 'I LOVE NANJING UNIVERSITY OF AERONAUTICS AND ASTRONAUTICS'
X = ''
for i in Text:
    X += dictionary[i]
X = int(X,10)
# Test
(n,e,d) = keyGeneration(1024)
# 7^563 mod 561
print "7^563 mod 561 :",fastExpMod(7,563,561)
C = encryption(X,e,n)
M = decryption(C,d,n)

# int to str
decryptedText = str(M)
if len(decryptedText) % 2 != 0:
    decryptedText = '0'+decryptedText
result = ''
for i in range(0,len(decryptedText)/2):
    temp = decryptedText[i*2:i*2+2]
    result += dictionary_1[temp]

print "Plain Text:",Text
print "Encryption of plaintext:",C
print "Decryption of plaintext:",result
print "Correct:",Text == result
