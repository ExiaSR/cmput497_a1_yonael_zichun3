from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
import re

# everything in square brackets = \[(.*?)\]
# everything in between | | = \|.*?\|
# everything in between '| =' = (\|.*?\=)
# everything after | = (\|.*?$)
# plainlist and after = (\|.*?\=\s+{{Plainlist\s+\|\n.+?)
# everything in the plainlist = (\|.*?\=\s+{{Plainlist\s*[\s\S]*?(?=\}))


class Extracter:
    def file_extract(self, fn):
        with open(fn, "r") as f:
            for line in f:
                tokens = self.preprocess(f.read())

        relations = []
        for token in tokens:
            # only look for relations in `Infobox`
            if token.startswith("{{Infobox"):
                relations.extend(self.get_relations(token))

        return relations

    # finds the balanced open parantheses and brackets then matches them
    def balanced(self, text):
        open_par = 0

        for i in range(len(text)):
            if (text[i] == "{") or (text[i] == "["):
                open_par += 1

            elif (text[i] == "}") or (text[i] == "]"):
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
            if (text[i] == "{") or (text[i] == "["):
                i_close = self.balanced(text[i:])
                tokens.append(text[i : i + i_close])
                i = i_close + i
            else:
                i += 1

        return tokens

    # removes all the comments like <-- -->
    def remove_comments(self, text):
        clean = re.sub("(\<![\-\-\s\w\>\/]*\>)", "", text)
        return clean

    # Goes through token and finds the plainlist and outputs the subject and object
    # TODO : remove duplicate names and maybe non-capitalized words
    # TODO : Add evidence
    # TODO: rename "subject" to "object" cuz we're extracing object not subject
    def get_relations(self, token):
        # Gets everything from '| [text] Plainlist' to }
        plainlist = re.findall("(\|.*?\=\s+{{[P|p]lainlist\s*[\s\S]*?(?=\}))", token)
        result_buffer = []
        if len(plainlist) > 0:
            # goes through plainlist items
            for i in plainlist:

                # finds the predicate (located between '|' and '=' )
                # removes non alphabetical chars
                predicate = re.findall("(\|.*?\=)", i)
                evidence = predicate
                predicate = re.sub("[^a-zA-Z]", "", predicate[0])

                # splits on new lines and removes the predicate (index 0) from the list
                subjects = i.splitlines()
                subjects.pop(0)

                # goes through subjects
                for subject in subjects:
                    subject = re.sub("[^a-zA-Z]", " ", subject).strip()
                    result_buffer.append(
                        {"predicate": predicate, "object": subject, "evidence": evidence}
                    )

        # Extract none plainlist relations
        relations_raw = re.findall(r"^\|.*$", token, re.MULTILINE)
        for relation_raw in relations_raw:
            predicate = None
            object_name = None

            # extract predicate
            # look for everything between '|' and '='
            predicate_raw = re.findall(r"(?<=\| )(.*)(?=\= )", relation_raw)
            if predicate_raw:
                predicate = predicate_raw[0].replace(" ", "")
            else:
                continue  # continoue to parse next relation

            # extract object
            # look for everything after '='
            object_raw = re.search(r"\=(.*)", relation_raw, re.DOTALL)
            if object_raw and not object_raw.group(1).strip().startswith(
                "{{Plainlist"
            ):  # and not object_raw.group(1).strip().startswith("{{Plainlist"):
                object_name = object_raw.group(1).strip().replace(" ", "_")
            else:
                continue  # continoue to parse next relation

            result_buffer.append(
                {"predicate": predicate, "object": object_name, "evidence": relation_raw}
            )
        return result_buffer


def main():
    extracter = Extracter()
    fn = "data/Finding_Nemo.wiki"
    relatinos = extracter.file_extract(fn)


if __name__ == "__main__":
    main()
