import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


word_dict = {}
lemmatizer = WordNetLemmatizer()


def transform_into_csv():
    """Transforms the text file input into csv."""
    df = pd.read_csv("translated dutch vocab from the b1 book.txt")
    df.to_csv("word_bank.csv",sep=';', index=None)

def create_dict():
    """Creates a dictionary from the word_bank csv."""
    df = pd.read_csv("word_bank.csv")
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
            print(index_same_words_to_remove)
            for i in range(len(index_same_words_to_remove)):#remove the words to be removed
                translations.pop(index_same_words_to_remove[i]-i)
            word_dict.update({key: translations})
            print(word_dict.get(key))



#main
create_dict()
run_lemma_similarity()