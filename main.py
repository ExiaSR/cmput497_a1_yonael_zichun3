import re
import csv
import os

from regex_extractor.extract import Extracter
from nltk.tokenize import RegexpTokenizer


def save_to_tsv(subject, relations, output_dir="output"):
    """
    Archieve relations from a wiki into TSV file
    """
    with open("{}/{}.tsv".format(output_dir, subject), "wt") as output_file:
        tsv_writer = csv.writer(output_file, delimiter="\t")
        rows = [
            [subject, relation["predicate"], relation["object"], relation["evidence"]]
            for relation in relations
        ]
        tsv_writer.writerows(rows)


def get_wiki_files(dir="data"):
    (dirpath, _, filenames) = next(os.walk(dir))
    return [
        {"path": os.path.join(dirpath, filename), "name": filename}
        for filename in filenames
        if filename.endswith(".wiki")
    ]


def main():
    wiki_files = get_wiki_files()
    extractor = Extracter()
    for wiki_file in wiki_files:
        subject = wiki_file["name"].replace(".wiki", "")
        print("----Start parsing {}----".format(wiki_file["name"]))
        relations = extractor.file_extract(wiki_file["path"])
        save_to_tsv(subject, relations)
        print("----Done parsing {}----\n".format(wiki_file["name"]))


if __name__ == "__main__":
    main()
