'''
Question 1 :

    the message is : KEEP THE SECRET SAFE

encrypted : LTTN EKT YTJRTE YQGT

Question 2 :

    the message is : ERVYE DXVR SXFPJ

decrypted : TRUST YOUR LOGIC


'''


message = '''
EKT YTJRTE BTYYQFT PY KPZZTO PO EKPY NQRQFRQNK.
STEETR GRTCVTOJD ZXTY OXE RTHTQS EKT IKXST LTD,
MVE PE FPHTY Q FXXZ YEQRE.
SXXL GXR JXBBXO IXRZY, RTNTQETZ NQEETROY,
QOZ YKXRE IXRZY.
IKTO DXV RTJXHTR EKT BTYYQFT,
EKT HPFTOTRT LTD KQY GXVR STEETRY.
'''


most_frequent_list = ["E", "T", "R", "S", "O" ,"A", "H", "N", "D", "I", "G", "L"]

def compute_frequency(message):
    frequency = {}
    for char in message:
        if 'A' <= char <= 'Z':
            frequency[char] = frequency.get(char, 0) + 1
    frequency = sorted(frequency.keys(), key=lambda x: frequency[x], reverse=True)
    return frequency

frequency = compute_frequency(message)
frequency = frequency[:len(most_frequent_list)]


def generate_mapping(message):
    mapping = {}
    for i in range(len(frequency)):
        mapping[frequency[i]] = most_frequent_list[i]
    return mapping

def apply_mapping(mapping, message):
    message_list = list(message)
    for i, char in enumerate(message_list):
        message_list[i] = mapping.get(char, char)

    new_message = "".join(message_list)
    return new_message


mapping = generate_mapping(message)

# Adding manually some keys
mapping['B'] = 'M'
mapping['J'] = 'C'
mapping['N'] = 'P'
mapping['H'] = 'V'
mapping['I'] = 'W'
mapping['V'] = 'U'
mapping['M'] = 'B'
mapping['G'] = 'F'
mapping['D'] = 'Y'
mapping['L'] = 'K'
mapping['C'] = 'Q'

new_message = apply_mapping(mapping, message)
print(new_message)
'''
result = 

'''

def vigenere_decrypt(message, key):
    shift_idx = []
    for char in key:
        shift_idx.append(ord(char) - 65)
    key_index = 0
    message_list = list(message)
    for i, char in enumerate(message_list):
        if 'A' <= char <= 'Z':
            shift = shift_idx[key_index % len(shift_idx)]
            new_character = (ord(char) - 65 - shift ) % 26 + 65
            message_list[i] = chr(new_character)

            key_index += 1

    return "".join(message_list)


ciphertext = '''
VVHWGQUIVYHIRSUPGTWXJSVIPCWIUPHGCIVIVVHPGHWITSDTRSDVUSYITMZL
GFHIXSUCVSDQOSPFGFVLQIOHEVHGMSDGJQRPWAQWGSNXJSPSUHIVGEXIPHVC
OPRPCBGYUSLXVCUIECYITHKIMSBAJSQXJSPIUGDKGPHGQAHWEZHETSQXGFWL
GOFGGGVAQFGIEZLTUS

'''


def recover_vigenere_key(message, key_length):
    letters = "".join(char for char in message if 'A' <= char <= 'Z')
    key = ""
    for index in range(key_length):
        group = letters[index::key_length]
        most_frequent = compute_frequency(group)[0]
        shift = (ord(most_frequent) - ord('E')) % 26
        key += chr(ord('A') + shift)
    return key


key = recover_vigenere_key(ciphertext, 4)

print("Recovered key:", key)
print(vigenere_decrypt(ciphertext, key))


