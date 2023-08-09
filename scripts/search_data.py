import re
from nltk import ngrams

def loadData(file):
    with open(file, "r") as f1:
        data = f1.read().split("\n")[1:]
        dic = {}
        for d in data:
            d = d.split("\t")
            #name = ngrams(d[1].split(" "), 2)
            name = [' '.join(grams) for grams in ngrams(d[1].split(" "), 2)]
            dic[d[0]] = name
            input(dic)
    return(dic)

def search_func(term):
    print("search!")
    # loop through the data and compare the list of bigrams of TERM against the list of bigrams of NAME
    # collect top matches
    # print on the screen 


if __name__ == '__main__':
    data = loadData("../data/prosopData.csv")
    try:
        while True:
            search_term = input("Paste the name that you want to find: ")
            search_term = "" # transform into a list of bigrams
            search_func(search_term)
    except KeyboardInterrupt:
        pass
