STOPWORDS = ["a", "the", 'is', 'are', "arent", "can", "cant", "so", "there", "then", "could", "couldnt", "to", "for", "had", "has", "hasnt", "have", "having", "havent"]
PUNCT = [".", ",", ";", "!", "'", '"', "%", "(", ")", ":"]
def main():
    sp = open('sp1.txt', "r")
    sp.readline()
    sp_text = []
    char_dict = {}
    for i in sp:
        i.encode('latin-1')
        i = i.strip()
        print(i)
        l = []
        i = i.strip()
        i = i.split()
        char = i[0]
        ch = char.split(",")
        c = ch[0]
        c = c.lower()
        c = c.strip()
        wor = i[1:]
        words = ""
        for k in wor:
            word = ""
            for letter in k:
                if letter in PUNCT:
                    words += " "
                    next
                else:
                    word+= letter
            if word in STOPWORDS:
                next
            else:
                words += word.lower()
                words += " "
                #print(words)
                #print(advb)
        if c not in char_dict.keys():
            char_dict[c] = words 
        else:
            char_dict[c] += words
            #print(c, ": ", char_dict[c])
    print(char_dict.keys())
    for character in char_dict.keys():
        print("character:", character, ":", char_dict[character])
    sp.close()
main()