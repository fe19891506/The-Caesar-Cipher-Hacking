# coding=UTF-8
'''
Простой перебор ключей c проверкой слов по словарю. Поддерживается только русский язык.
(Словарь взят с сайта Национального Корпуса Русского Языка)
'''
import caesar_cipher

def cc_hack(enc_txt, alphabet):
    '''
    Возращает список возможных ключей
    '''
    import re
    
    if alphabet == caesar_cipher.RUS_ALPH:
        word_dict = get_rus_word_dict()
        
    decr_keys = {k: 0.0 for k in range(len(alphabet))}
    for k in decr_keys.keys():
        decr_txt = caesar_cipher.decrypt_string(enc_txt, k)
        #разобьём на уникальные слова
        decr_word_set = set(re.split(ur"(?u)\W+",decr_txt))
        #посчитаем количество совпадений со словарём
        for word in decr_word_set:
            if word in word_dict:
                decr_keys[k] += 1.0 / len(decr_word_set)
    #print(decr_keys)            
    #уберём лишние ключи (цифра 0,2 взята "с потолка" и требует дополнительного анализа) 
    decr_keys = [k for k, v in decr_keys.items() if v > 0.2 ]
    return decr_keys
        
def get_rus_word_dict():
    import csv
    the_dict = []
    f = open("freqrnc2011.csv", "rb")
    try:
        for row in csv.DictReader(f):
            the_dict.append(row['Lemma'].decode("UTF-8"))
    finally:
        f.close()
    return the_dict
    
if __name__ == '__main__':
    
    
    test_str2 = u"""ъпл квзэ1ь мнлюкэь опнлзэ о
ялдянэплй зэнвпзе е pljb bkdifpe tlo#ap! Е ъпл дэйвфэпвищкл."""
    #test_str2 = caesar_cipher.decrypt_string(test_str2, -3)
    #print(test_str2)
    
    test_str3 = u"""ахс ринг1в тусдргв фхуснг ф
ескеугхсп нгуихнл л vrph hqjolvk zru#gv! Л ахс кгпиъгхиоярс."""
    
    test_str = u"""это нека1я пробная строка с
возвратом каретки и some english wor#ds! И это замечательно."""
    #print(caesar_cipher.encrypt_string(test_str, 3))
    
    import os.path
    if os.path.isfile("decr_text.txt"):
        print("начали...")
        with open("decr_text.txt", "r") as f:
            try:
                the_result = cc_hack(f.read().decode('UTF-8'), caesar_cipher.RUS_ALPH)
                print("список ключей: {}".format(the_result))
            finally:
                f.close()
    else:
        print(cc_hack(test_str3, caesar_cipher.RUS_ALPH))
    
    '''
    f = open("text2encode.txt", "r")
    try:
        decr_txt = caesar_cipher.encrypt_string(f.read().decode('UTF-8'), 17)
        d_f = open("decr_text.txt", "w+")
        d_f.write(decr_txt.encode('UTF-8'))
        d_f.close()
    finally:
        f.close()
    '''
    
    
    