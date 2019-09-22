import re
import csv
import os

# from regex_extractor.extract import get_wiki_metadata
from regex_extractor.extract import Extracter
from nltk.tokenize import RegexpTokenizer


def extract_infobox_beside_plainlist(raw, subject):
    # look each every line which starts with '|'
    relations = []
    relations_raw = re.findall(r"^\|.*$", raw, re.MULTILINE)
    for relation_raw in relations_raw:
        predicate = None
        object_name = None

        # extract predicate
        # look for everything between '|' and '='
        predicate_raw = re.findall(r"(?<=\| )(.*)(?=\= )", relation_raw)
        if predicate_raw:
            predicate = predicate_raw[0].replace(" ", "")
        else:
            continue

        # extract object
        # look for everything after '='
        object_raw = re.search(r"\=(.*)", relation_raw, re.DOTALL)
        if object_raw:
            object_name = object_raw.group(1).strip().replace(" ", "_")

        print(
            "{}\nSubject: {} Predicate: {} Object: {}\n".format(
                relation_raw, subject, predicate, object_name
            )
        )
        relations.append({"predicate": predicate, "object": object_name, "evidence": relation_raw})

    return relations


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
    # wiki_list = get_wiki_metadata()  # get raw metadata from wiki text
    # for wiki in wiki_list:
    #     subject = wiki["name"].replace(".wiki", "")
    #     print("----Start parsing {}".format(subject))
    #     relations = extract_infobox_beside_plainlist(
    #         wiki["metadata_raw"], subject=subject
    #     )
    #     save_to_tsv(subject, relations)
    #     print("----Done parsing {}\n".format(subject))


if __name__ == "__main__":
    main()
