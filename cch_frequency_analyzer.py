# coding=UTF-8
'''
Взлом шифра Цезаря простым частотным анализом. Проверка по пограничным интервалам распределения. 
'''

import caesar_cipher

#По данным Национального корпуса русского языка (НКРЯ)
RUS_ALPH_FREQ_ = {u'А' : 40487008, u'Б' : 8051767, u'В' : 22930719, u'Г' : 8564640, u'Д' : 15052118, u'Е' : 42691213, u'Ё' : 184928, u'Ж' : 4746916, u'З' : 8329904, u'И' : 37153142, u'Й' : 6106262, u'К' : 17653469, u'Л' : 22230174, u'М' : 16203060, u'Н' : 33838881, u'О' : 55414481, u'П' : 14201572, u'Р' : 23916825, u'С' : 27627040, u'Т' : 31620970, u'У' : 13245712, u'Ф' : 1335747, u'Х' : 4904176, u'Ц' : 2438807, u'Ч' : 7300193, u'Ш' : 3678738, u'Щ' : 1822476, u'Ъ' : 185452, u'Ы' : 9595941, u'Ь' : 8784613, u'Э' : 1610107, u'Ю' : 3220715, u'Я' : 10139085, }
RUS_ALPH_FREQ_TOT_ = 505266851
RUS_ALPH_FREQ = \
    {
        u'А' :     0.080129951    ,
        u'Б' :     0.0159356724    ,
        u'В' :     0.045383383    ,
        u'Г' :     0.0169507261    ,
        u'Д' :     0.0297904325    ,
        u'Е' :     0.0844924082    ,
        u'Ё' :     0.0003660007    ,
        u'Ж' :     0.0093948692    ,
        u'З' :     0.0164861478    ,
        u'И' :     0.0735317227    ,
        u'Й' :     0.0120852219    ,
        u'К' :     0.034938902    ,
        u'Л' :     0.0439968978    ,
        u'М' :     0.0320683219    ,
        u'Н' :     0.0669722958    ,
        u'О' :     0.109673692    ,
        u'П' :     0.0281070725    ,
        u'Р' :     0.0473350368    ,
        u'С' :     0.054678117    ,
        u'Т' :     0.0625827124    ,
        u'У' :     0.0262152801    ,
        u'Ф' :     0.0026436466    ,
        u'Х' :     0.0097061107    ,
        u'Ц' :     0.0048267702    ,
        u'Ч' :     0.014448193    ,
        u'Ш' :     0.0072807824    ,
        u'Щ' :     0.0036069574    ,
        u'Ъ' :     0.0003670377    ,
        u'Ы' :     0.0189918277    ,
        u'Ь' :     0.0173860861    ,
        u'Э' :     0.0031866468    ,
        u'Ю' :     0.0063742852    ,
        u'Я' :     0.0200667924    ,
    }
    
ENG_ALPH_FREQ = \
    {
        u'A' :     0.08167    ,
        u'B' :     0.01492    ,
        u'C' :     0.02782    ,
        u'D' :     0.04253    ,
        u'E' :     0.12702    ,
        u'F' :     0.02228    ,
        u'G' :     0.02015    ,
        u'H' :     0.06094    ,
        u'I' :     0.06966    ,
        u'J' :     0.00153    ,
        u'K' :     0.00772    ,
        u'L' :     0.04025    ,
        u'M' :     0.02406    ,
        u'N' :     0.06749    ,
        u'O' :     0.07507    ,
        u'P' :     0.01929    ,
        u'Q' :     0.00095    ,
        u'R' :     0.05987    ,
        u'S' :     0.06327    ,
        u'T' :     0.09056    ,
        u'U' :     0.02758    ,
        u'V' :     0.00978    ,
        u'W' :     0.0236    ,
        u'X' :     0.0015    ,
        u'Y' :     0.01974    ,
        u'Z' :     0.00074    , 
    }

def cc_hack(enc_txt, alphabet):
    '''
    Возращает список возможных ключей
    '''
    BOUNDARY_DISTANCE = 5
    BOUNDARY_INTERSECTION_LIMIT = BOUNDARY_DISTANCE - 2
    
    if alphabet == caesar_cipher.RUS_ALPH:
        alph_freq = RUS_ALPH_FREQ
    elif alphabet == caesar_cipher.ENG_ALPH:
        alph_freq = ENG_ALPH_FREQ
    
    decr_keys = {k: 0.0 for k in range(len(alphabet))}
    
    alph_freq_max_boundary = sorted(alph_freq, key=alph_freq.__getitem__, reverse=True)[:BOUNDARY_DISTANCE]
    alph_freq_min_boundary = sorted(alph_freq, key=alph_freq.__getitem__,)[:BOUNDARY_DISTANCE]
    
    enc_freq = get_alphabet_frequency(enc_txt, alphabet)
    enc_freq_max_boundary = sorted(enc_freq, key=enc_freq.__getitem__, reverse=True)[:BOUNDARY_DISTANCE]
    enc_freq_min_boundary = sorted(enc_freq, key=enc_freq.__getitem__,)[:BOUNDARY_DISTANCE]
    
    for k in decr_keys.keys():
        #dec_freq_boundary сделаем типа set
        dec_freq_max_boundary = {caesar_cipher.decrypt_chr(c, alphabet, k) for c in enc_freq_max_boundary}
        dec_freq_min_boundary = {caesar_cipher.decrypt_chr(c, alphabet, k) for c in enc_freq_min_boundary}
        #запишем длину пересечений с граничными интервалами эталона
        decr_keys[k] += len(dec_freq_max_boundary & set(alph_freq_max_boundary)) + \
            len(dec_freq_min_boundary & set(alph_freq_min_boundary))
    # уберём ключи длина пересечений которых меньше заданой константы
    decr_keys = [k for k, v in decr_keys.items() if v > BOUNDARY_INTERSECTION_LIMIT ]
    return decr_keys

def get_alphabet_frequency(atxt, alphabet):
    #уберем все лишние символы
    the_txt = filter(lambda c: c.upper() in alphabet, atxt)
    the_txt = the_txt.upper()
    char_frequency = {c : 0.0 for c in alphabet}
    #цикл по анализируемому тексту. исключая из текста анализируемый символ, увеличиваем делитель на кол-во его вхождений
    freq_delim = float(len(the_txt))
    while len(the_txt) > 0:
        char_count = float(the_txt.count(the_txt[0]))
        char_frequency[the_txt[0]] = char_count / freq_delim
        the_txt = the_txt.replace(the_txt[0], "")
        freq_delim += char_count
    return char_frequency
    
if __name__ == '__main__':
    import os
    if os.path.isfile("decr_text.txt"):
        with open("decr_text.txt", "r") as f:
            try:
                the_result = cc_hack(f.read().decode('UTF-8'), caesar_cipher.RUS_ALPH)
                print("список ключей: {}".format(the_result))
            finally:
                f.close()
    else:
        test_str2 = u"""ъпл квзэ1ь мнлюкэь опнлзэ о
ялдянэплй зэнвпзе е pljb bkdifpe tlo#ap! Е ъпл дэйвфэпвищкл."""
        the_result = cc_hack(test_str2, caesar_cipher.RUS_ALPH)
        print("список ключей: {}".format(the_result))
        for k in the_result:
            print(caesar_cipher.decrypt_string(test_str2, k))
    '''
    f = open("text2encode.txt", "r")
    try:
        cc_hack(f.read().decode('UTF-8'), caesar_cipher.RUS_ALPH) 
    finally:
        f.close()
    '''
    
    
    
        
        