import re
import csv
import os
import errno
import logging
import argparse

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
def remove_duplicate_relations(relations):
    relations_buffer = {}
    for relation in relations:
        # slow, but better way to clean up duplicate relations
        relations_buffer["{}::{}".format(relation["predicate"], relation["object"])] = relation[
            "evidence"
        ]

    return [
        {"predicate": key.split("::")[0], "object": key.split("::")[1], "evidence": value}
        for key, value in relations_buffer.items()
    ]


def main(dir="data", output="output"):
    wiki_files = get_wiki_files()
    extractor = Extracter()
    for wiki_file in wiki_files:
        subject = wiki_file["name"].replace(".wiki", "")
        logger.debug("----Start parsing {}----".format(wiki_file["name"]))
        relations = extractor.file_extract(wiki_file["path"])
        clean_relations = remove_duplicate_relations(relations)
        save_to_tsv(subject, clean_relations, output_dir=output)
        logger.debug(
            "Total: {} Duplicate: {}".format(len(relations), len(relations) - len(clean_relations))
        )
        logger.debug("----Done parsing {}----\n".format(wiki_file["name"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract relations from wiki files.")
    parser.add_argument(
        "--input", type=str, default="data", help="Provide path to directory of input wiki files"
    )
    parser.add_argument(
        "--output", type=str, default="output", help="Provide path to save output TSV files"
    )
    args = parser.parse_args()
    main(args.input, args.output)
