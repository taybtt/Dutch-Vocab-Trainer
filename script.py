import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


word_dict = {}
lemmatizer = WordNetLemmatizer()


def transform_into_csv():
    """Transforms the text file input into csv."""
    # df = pd.read_csv("translated dutch vocab from the b1 book.txt")
    df.to_csv("word_bank.csv",sep=':', index=None)

def create_dict():
    """Creates a dictionary from the word_bank csv."""
    df = pd.read_csv("word_bank.csv", sep=':')
    for index, row in df.iterrows():
        if row.iloc[0].strip() not in word_dict.keys(): #if the dutch word is not in the dictionary
            word_dict.update({row.iloc[0].strip(): row.iloc[1].strip()})
        else: #if the dutch word is in the dictionary
            if isinstance(word_dict.get(row.iloc[0].strip()), list): #if the english word is a list already
                word_dict.get(row.iloc[0].strip()).append(row.iloc[1].strip())
            else: #if there is only one of the same key, we make it a list
                word_dict.update({row.iloc[0].strip(): [word_dict.get(row.iloc[0].strip()), row.iloc[1].strip()]})
            
            print(word_dict.get(row.iloc[0].strip()))

    print(len(word_dict.keys()))

def run_lemma_similarity():
    """Checks whether a word has been entered with the same translation multiple times. 
    If so, removes it from the dictionary. This function does not remove different meanings of the same Dutch word."""
    for key in word_dict.keys():
        translations = word_dict.get(key)
        if isinstance(translations, list): #if there are multiple translations for the same dutch word
            tokens = [word_tokenize(word) for word in translations]
            lemmatized_words = []
            for token_group in tokens: #token group is the group of tokens resulting from one translation
                translated_word = "" #combination of multiple tokens from one translation back together
                for token in token_group:
                    translated_word += lemmatizer.lemmatize(token)
                lemmatized_words.append(translated_word)
            index_same_words_to_remove = []
            for i in range(len(lemmatized_words)): #check which translations are the same after lemmatization
                for j in range(i+1, len(lemmatized_words)):
                    if lemmatized_words[i] == lemmatized_words[j]: #if the translations are the same, add the second to be removed
                        if not (j in index_same_words_to_remove):
                            index_same_words_to_remove.append(j)
            for i in range(len(index_same_words_to_remove)):#remove the words to be removed
                translations.pop(index_same_words_to_remove[i]-i)
            word_dict.update({key: translations})
            print(word_dict.get(key))

def check_lemma_similarity(dutch_word, english_word):
    """Checks whether the dutch word that is already in the dictionary appears with one of the same translations or a new one. 
    Returns True when the dutch word and its translation already appear in the dictionary, 
    False when the dutch word exists but the translation inputed is a new translation (for words with multiple meanings)"""
    #should be the intersection of what single lemma similarity needs and what run lemma similarity is
    return False


def single_lemma_similarity(dutch_word, english_word):
    # TODO SHOULD ALSO BE ADDING THE NEW ADDITIONS TO THE DICTIONARY TO THE WORDBANK CSV FILE
    """Handles the lemma similarity check and its result for a single dutch word and its inputed translated"""
    if dutch_word not in word_dict.keys():
        word_dict.update({dutch_word:english_word})
        return True
    else:
        if check_lemma_similarity(dutch_word, english_word): # the dutch word and its translation already exists in the dictionary
            return False
        else: # the dutch word is in the dictionary but its translation is new
            translations = word_dict.get(dutch_word)
            translations.append(english_word)
            word_dict.update({dutch_word:translations})
            return True
            


def engage():
    """The general working function for the whole system. Engages the system."""
    create_dict()
    run_lemma_similarity()
    intake = input("Enter a command to be directed to a work station. Enter 'help' to see possible commands. \n")
    match intake:
        case "supply_vocab":
            handle_supply_vocab()
        case "vocab_trainer":
              handle_vocab_trainer()

def handle_supply_vocab():
    """Handles the Adding Words to the Word Bank Function & Its Work Station"""
    print("Welcome to the Word Bank Input.")
    while(True):
        intake = input("Please enter the word you want to insert into the Word Bank in such format: 'dutch_word:english_word'\nWhenever, you want to leave this work station, please input 'quit'\n")
        if (intake == 'quit'): #when quit is called
            break
        while(len(intake.split(':')) != 2 or len(intake.split(':')[0]) == 0 or len(intake.split(':')[1]) == 0): #checking if the format is correct
            intake = input("Please input the string in the correct format: 'dutch_word:english_word'\n")
        
        dutch_word = intake.split(':')[0]
        english_word = intake.split(':')[1]
        single_lemma_similarity(dutch_word, english_word)
        print(dutch_word, english_word, word_dict.get(dutch_word))


def handle_vocab_trainer():
    """Handles the training of the Vocab from the dictionary and the csv file"""
    print("Welcome to the Vocab Trainer. Please enter the parameters of the training programme:")
     

#main
# transform_into_csv()
engage()

