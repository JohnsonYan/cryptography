import sys
import random
import cryptomath
import freqAnalysis
SYMBOLS = """ABCDEFGHIJKLMNOPQRSTUVWXYZ"""

def main():
    while True:
        Mode = raw_input(">encrypt or decrypt?(q to quit)")
        if Mode == 'q':
            sys.exit('GoodBye')
        Message = raw_input(">Please enter Message:")
        Message = Message.upper()
        keyA = int(raw_input(">Please enter keyA:"))
        keyB = int(raw_input(">Please enter keyB:"))

        if Mode == 'encrypt':
            translated = encryptMessage(keyA,keyB,Message)
        elif Mode == 'decrypt':
            translated = decryptMessage(keyA,keyB,Message)
        print "keyA: %s" % keyA
        print "keyB: %s" % keyB
        print "%sed text:" % Mode.title()
        print translated
        print "The frequency of text:"
        print freqAnalysis.getFrequency(translated)

def checkKeys(keyA,keyB,mode):
    if keyA < 0 or keyB < 0 or keyB > 25:
        sys.exit('illegal key!')
        if cryptomath.gcd(keyA,26) != 1:
            sys.exit('gcd(keyA,26)!=1')

def encryptMessage(keyA,keyB,Message):
    checkKeys(keyA,keyB,'encrypt')
    ciphertext = ''
    for symbol in Message:
        if symbol in SYMBOLS:
            symIndex = SYMBOLS.find(symbol)
            ciphertext += SYMBOLS[(symIndex * keyA + keyB) % 26]
        else:
            ciphertext += symbol
    return ciphertext

def decryptMessage(keyA,keyB,Message):
    checkKeys(keyA,keyB,'decrypt')
    plaintext = ''
    modInverse = cryptomath.findModInverse(keyA,26)

    for symbol in Message:
        if symbol in SYMBOLS:
            symIndex = SYMBOLS.find(symbol)
            plaintext += SYMBOLS[(symIndex - keyB) * modInverse % 26]
        else:
            plaintext += symbol
    return plaintext

main()
