from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
import re
# everything in square brackets = \[(.*?)\]
# everything in between | | = \|.*?\|
# everything in between '| =' = (\|.*?\=)
# everything after | = (\|.*?$)
#plainlist and after = (\|.*?\=\s+{{Plainlist\s+\|\n.+?)
# everything in the plainlist = (\|.*?\=\s+{{Plainlist\s*[\s\S]*?(?=\}))


class Extracter:
    def file_extract(self, fn):
        with open(fn, 'r') as f:
            for line in f:
                tokens = self.preprocess(f.read())

        for token in tokens:
            # print(token)
            self.get_lists(token)
            
    # finds the balanced open parantheses and brackets then matches them 
    def balanced(self, text):
        open_par = 0

        for i in range(len(text)):
            if (text[i] == '{') or (text[i] == '['):
                open_par += 1 
            
            elif (text[i] == '}') or (text[i] == ']'):
                open_par -= 1
            
            elif open_par == 0: 
                break 

        return i 
    

    
    def preprocess(self, text):
        text = self.remove_comments(text)
        tokens = []
        i = 0
        count = 0
        while i < len(text):
            if (text[i] == '{') or (text[i] == '['):
                i_close = self.balanced(text[i:])
                tokens.append(text[i:i+i_close])
                i = i_close + i 

            
            else:
                i += 1

        return tokens 
    
    # removes all the comments like <-- --> 
    def remove_comments(self, text):
        clean = re.sub('(\<![\-\-\s\w\>\/]*\>)', "", text)
        return clean


    
    # Goes through token and finds the plainlist and outputs the subject and object
    # TODO : remove duplicate names and maybe non-capitalized words 
    # TODO : Add evidence
    def get_lists(self, token):
        # Gets everything from '| [text] Plainlist' to } 
        plainlist = re.findall("(\|.*?\=\s+{{Plainlist\s*[\s\S]*?(?=\}))", token)
        if (len(plainlist) > 0):

            # goes through plainlist items 
            for i in plainlist:

                # finds the predicate (located between '|' and '=' )
                # removes non alphabetical chars 
                predicate = re.findall('(\|.*?\=)', i)
                predicate = re.sub('[^a-zA-Z]', "", predicate[0])

                # splits on new lines and removes the predicate (index 0) from the list 
                subjects = i.splitlines()
                subjects.pop(0)

                # goes through subjects 
                for subject in subjects:
                    subject = re.sub('[^a-zA-Z]', " ", subject).strip()
                    print("Predicate = {} and Subject = {}".format(predicate, subject))

                    
    


                

def main():
    extracter = Extracter()
    fn = "data/Finding_Nemo.wiki"
    extracter.file_extract(fn)

main()

                
        
           
