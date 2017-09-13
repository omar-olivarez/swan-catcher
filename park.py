import pandas as pd   
import csv  
#from bs4 import BeautifulSoup             
import re
import nltk
#nltk.download()
from nltk.corpus import stopwords # Import the stop word list
#from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
#from sklearn.ensemble import RandomForestClassifier

class Character(object):
    def __init__(self, name, corpus):
        self.name = name
        self.corpus = corpus
        self.rank = -1 # not used yet
        self.special = False # not used yet
        self.total_word_counts = {}
        self.word_count = 0
        self.special_word_count = 0
        self.special_words = [] # special words are words that appear in <= 1% of the population
        self.per_special = 0.0
        self.word_set_count = 0
        self.word_set = set()
    def __str__(self):
        return self.name
    def is_special(self):
        return self.special
    def add_words(self, new_text):
        self.corpus += new_text
        self.corpus+= " "
        return
    def count_words(self):
        words = self.corpus.split()
        for word in words:
            if word not in self.total_word_counts.keys():
                self.total_word_counts[word] = 1
                self.word_count += 1
                self.word_set.add(word)
            else:
                self.total_word_counts[word] += 1
                self.word_count += 1
        self.word_set_count = len(self.word_set)
        return

class CharacterList(object):
    def __init__(self):
        self.clist = [] # list of all characters
        self.word_set = set() # set of unique words across all characters
        self.special_words = {} # dictionary of words used below the cutoff level across all characters, and the people who used them
        self.total_word_count = 0 # total number of words across all characters
        self.word_usage = {} # each word and how frequently it's used across all characters
        self.cutoff = 0 # the max number of people who can use a word for it to be still considered special
        self.special_char = 0
    def __str__(self):
        for character in self.clist:
            print(character)
        return
    def add(self, new_character):
        self.clist.append(new_character)
        return
    def find(self, character):
        for i in self.clist:
            if i.name == character:
                return True
        return False
    def get(self, character):
        for i in self.clist:
            if i.name == character:
                return i
    def count_characters(self):
        return len(self.clist)
        
    def calculate_special_words(self):
        for character in self.clist:
            character.count_words()
            self.word_set.update(character.word_set)
            self.total_word_count += character.word_count
            for word in character.word_set:
                if word not in self.word_usage.keys():
                    self.word_usage[word] = 1
                else:
                    self.word_usage[word] += 1
        self.cutoff = len(self.clist)//100 # words must be used by less than 1% of the population
        for word in self.word_usage.keys():
            if (self.word_usage[word]) <= self.cutoff:
                if word not in self.special_words.keys():
                    self.special_words[word] = []
                    for character in self.clist:
                        if word in character.word_set:
                            self.special_words[word].append(character.name)
        self.label_special_characters()
        return
    def label_special_characters(self):
        print("labeling special characters")
        print()
        for character in self.clist:
            for word in self.special_words.keys():
                if character.name in self.special_words[word]:
                    #print('HEYY')
                    character.special_word_count += character.total_word_counts[word]
                    character.special_words.append(word)
            #print(character.name, character.special_word_count)
            
            if character.special_word_count > 0 and character.word_count > 0: # and character.per_special != 1
                character.per_special = character.special_word_count / character.word_count
            else:
                character.per_special = 0
        #print(qt)
        self.rank_characters()
        return
    def rank_characters(self):
        print("ranking specialness")
        print()
        Clist = []
        slist = []
        newClist = []
        newSlist = []
        rank = 1
        for character in self.clist:
            Clist.append(character.name)
            slist.append(character.per_special)
        for i in range(self.count_characters()):
            place = slist.index(max(slist))
            newClist.append(Clist.pop(place))
            newSlist.append(slist.pop(place))
        for i in range(len(newClist)):
            char = self.get(newClist[i])
            if char.rank==-1:
                numtimes = newSlist.count(newSlist[i]) # count number of times this quantity of per_special appears in the list of per_specials
                #print(numtimes)
                for j in range(numtimes): # for every time that this amount of per_special appears
                    c = self.get(newClist[i + j]) # get the character that also has that per_special amount
                    #print(c)
                    #print(c, len(c.total_word_counts), c.special_word_count)
                    if len(c.total_word_counts) > 30 and c.special_word_count > 10: #if that character says more than 30 different words and says a special word at least 5 times
                        c.rank = rank #give them this rank
                        rank += 1
                    else:
                        c.rank = 0 #else give them 0
            
        # find the largest rank number
        maxrank = 0
        for character in self.clist:
            if character.rank >= maxrank:
                maxrank = character.rank
        # take 5% of that
        cutoffrank = maxrank // 10 # take the top 1% ranking special characters
        # label the characters with these rankings as special
        #print(maxrank, cutoffrank)
        for character in self.clist:
            if character.rank <= cutoffrank and character.rank >0:
                character.special = True
        # make sure to avoid labeling the 0s as special
        return

def review_to_words( text ):

    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", text) 

    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             

    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words )) 

def order(characters):
    output = open("most_different_SP_people_output.txt", 'w')
    perc = characters.special_char / len(characters.clist) *100
    perc = round(perc, 2)
    st = "The %d most different people on Southpark (top %.2f percent)" %(characters.special_char, perc)
    print(st)
    output.write(st)
    output.write("\n")
    for i in range(1,characters.special_char+1):
        for character in characters.clist:
            if character.rank == i:
                print()
                output.write("\n")
                print("---------------------------------------------------------------------------------------------------------")
                output.write("---------------------------------------------------------------------------------------------------------\n")
                st = "Rank: %2d  Name: %-17s  Prop. of words that are special: %f   Num of special words: %3d" %(character.rank, character.name, character.per_special, len(character.special_words))
                print(st)
                output.write(st)
                print()
                output.write("\n\n")
                st = ""
                count = 0
                for j in character.special_words:
                    st += "%17s" %j
                    count += 1
                    if count%6 == 0:
                        st += "\n"
                print(st)
                output.write(st)
                print()
                output.write("\n")
    output.close()
    return

def main():
    corpus = pd.read_csv("All-seasons.csv", delimiter=",")
    character_col = 2
    line_col = 3
    rownum = 1
    characters = CharacterList()
    total_rows = len(corpus.index) - 1
    print("Converting to character dictionary")
    print()
    for i in range(1,total_rows+1):
        character = corpus.iloc[rownum, character_col]
        character = character.lower()
        if not characters.find(character): # returns true if character is found
            text = corpus.iloc[rownum, line_col]
            text = review_to_words(text)
            text += " "
            new_character = Character(character, text)
            characters.add(new_character)
        else:
            text = corpus.iloc[rownum, line_col]
            text = review_to_words(text)
            text += " "
            adding_to = characters.get(character)
            adding_to.add_words(text)
        rownum+=1
        
    print("Analying word counts")
    print()
    count = 0
    characters.calculate_special_words()
    for character in characters.clist:
        if character.is_special():
            count += 1
    characters.special_char = count
    """    for character in characters.clist:
        #print(character.rank)
        if character.is_special():
            print(character, ": ", character.rank, "   ", character.special_word_count, character.per_special)
            count += 1
    print()
    print("Total special characters: ", count)"""
    
    # order the rankings
    order(characters)
    
main()