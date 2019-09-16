from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer 

# we tokenize the sentences then lemmatize them 
import re

class Extracter:
    def __init__(self):
        movies = [] 
    
    def file_extract(self, fn):
        lemmatizer = WordNetLemmatizer()
        with open(fn, 'r') as f:
            for line in f:
                tokens = self.token_maker(f.read())
        
        for token in tokens:
            self.re_starring(token)

    

    def token_maker(self, f_content):
        tokens = (sent_tokenize(f_content))
        return tokens 
    
    def lemma_maker(self, lemmatizer, tokens):
        lemmatizer.lemmatize(tokens)

    def re_starring(self, token):
        print(token)


                

def main():
    extracter = Extracter()
    fn = "Finding_Nemo.wiki"
    extracter.file_extract(fn)

main()

                
        
           
