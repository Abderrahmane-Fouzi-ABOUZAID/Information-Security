def caesar_encrypt(message, key):
    result = ""

    for char in message:
        if "A" <= char <= "Z":
            result += chr((ord(char) - ord("A") + key) % 26 + ord("A"))
        elif "a" <= char <= "z":
            result += chr((ord(char) - ord("a") + key) % 26 + ord("a"))
        else:
            result += char

    return result

def caesar_decrypt(message, key):
    result = ""

    for char in message:
        if "A" <= char <= "Z":
            result += chr((ord(char) - ord("A") - key) % 26 + ord("A"))
        elif "a" <= char <= "z":
            result += chr((ord(char) - ord("a") - key) % 26 + ord("a"))
        else:
            result += char

    return result




message = "CRYPTO IS FUN UNTIL THE PROFESSOR SAYS QUIZ"

print(caesar_encrypt(message, 4))

# the result is : GVCTXS MW JYR YRXMP XLI TVSJIWWSV WECW UYMD

message = "GWCL JMBBMZ VWB JM CAQVO BWWTA BW AWTDM BPQA"

print(caesar_decrypt(message, 8))

# the result is : YOUD BETTER NOT BE USING TOOLS TO SOLVE THIS

message = "ESP VPJ TD FYVYZHY ECJ MCFEP QZCNP"

def brute_force_caesar(message):
    for i in range(1, 26, 1):
        decrypted = caesar_decrypt(message, i)
        print(f"For decryption index {i} : ", decrypted)

brute_force_caesar(message)

# the real key is 11 and the message was : THE KEY IS UNKNOWN TRY BRUTE FORCE


