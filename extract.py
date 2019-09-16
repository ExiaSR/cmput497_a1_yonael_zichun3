from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer

import os

# we tokenize the sentences then lemmatize them
import re


class Extracter:
    def file_extract(self, fn):
        lemmatizer = WordNetLemmatizer()
        with open(fn, "r") as f:
            for line in f:
                tokens = self.token_maker(f.read())

        for token in tokens:
            self.re_starring(token)

    def token_maker(self, f_content):
        tokens = sent_tokenize(f_content)
        return tokens

    def meta_data_extractor(self, filename):
        with open(filename, "r") as f:
            tokens = self.token_maker(f.read())
        return tokens[0]

    def lemma_maker(self, lemmatizer, tokens):
        lemmatizer.lemmatize(tokens)

    def re_starring(self, token):
        print(token)
        print("\n\n\n\n")


def get_wiki_metadata(dir="data"):
    (dirpath, _, filenames) = next(os.walk(dir))
    wiki_file_list = [
        {"path": os.path.join(dirpath, filename), "name": filename}
        for filename in filenames
        if filename.endswith(".wiki")
    ]

    extracter = Extracter()
    result_buffer = []
    for wiki_file in wiki_file_list:
        metadata = extracter.meta_data_extractor(wiki_file["path"])
        result_buffer.append({"name": wiki_file["name"], "metadata_raw": metadata})

    return result_buffer


if __name__ == "__main__":
    get_wiki_metadata()
