import re
import csv
import os
import errno
import logging

from regex_extractor.extract import Extracter
from nltk.tokenize import RegexpTokenizer

logger = logging.getLogger(__name__)

if os.getenv("DEBUG", False):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# https://stackoverflow.com/a/23794010
def safe_open_w(path, mode="wt"):
    mkdir_p(os.path.dirname(path))
    return open(path, mode)


def save_to_tsv(subject, relations, output_dir="output"):
    """
    Archieve relations from a wiki into TSV file
    """
    with safe_open_w("{}/{}.tsv".format(output_dir, subject), "wt") as output_file:
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


# Taken from https://stackoverflow.com/a/9428041
def remove_duplicate_relations(relations: dict):
    return [i for n, i in enumerate(relations) if i not in relations[n + 1 :]]


def main():
    wiki_files = get_wiki_files()
    extractor = Extracter()
    for wiki_file in wiki_files:
        subject = wiki_file["name"].replace(".wiki", "")
        logger.debug("----Start parsing {}----".format(wiki_file["name"]))
        relations = extractor.file_extract(wiki_file["path"])
        # save_to_tsv(subject, relations, output_dir="output_old")
        save_to_tsv(subject, remove_duplicate_relations(relations), output_dir="output")
        logger.debug("----Done parsing {}----\n".format(wiki_file["name"]))


if __name__ == "__main__":
    main()
