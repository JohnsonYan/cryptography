#coding=utf-8

def generateCipherKey(init,length):
    cipherKey = ""
    for i in range(length*8):
        cipherKey += init[0]  # a1移出
        init = init[1:5] + str(int(init[0])^int(init[3])) # a1 异或 a4,结果移到最后，为a5,利用切片可以方便的进行快速移位
    print "密钥流为：%s" % cipherKey
    return cipherKey

if __name__ == "__main__":
    init = raw_input('请输入初始序列:')
    clearText = raw_input('请输入明文:')
    length = len(clearText) # 明文长度
    cipherKey = generateCipherKey(init,length) # 生成密钥流

    cipherText = "" # 密文
    revertText = "" # 解密后的明文
    for i in range(length):
        clearChar = ord(clearText[i])
        key = int(cipherKey[i*8:i*8+7],2)
        cipherText += chr(key^clearChar)
        revertText += chr(key^ord(cipherText[i]))
    print "加密后的密文为：%s" % cipherText
    print "根据密文解密后的明文为：%s" % revertText
