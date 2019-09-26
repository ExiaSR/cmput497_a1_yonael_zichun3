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

            elif token.startswith("[[Category:"):
                category = self.category_relation(token)

                relations.append(
                    {
                    "predicate": 'Category',
                    "object": self.category_relation(token),
                    "evidence": token,
                    }
                )






        return relations

    # Gets all the categories
    def category_relation(self, text):
        category = re.search(r"\:(.*)(.*?)\]", text)
        category = category.group()
        regex = re.compile('[^a-zA-Z0-9]')
        clean_category = regex.sub(' ', category).strip()
        return clean_category
        #print("this is the length of category {}".format(len(category)))


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

    def strip_brackets(self, object_raw):
        object_search = re.search(r"\[\[(.*?)\]\]", object_raw)
        return object_search.group(1) if object_search else object_raw

    def subst_space_by_underscore(self, object_raw):
        return object_raw.replace(" ", "_")

    def remove_star_sign(self, object_raw: str):
        return object_raw.replace("* ", "")

    def normalize_object_name(self, object_raw):
        return self.subst_space_by_underscore(self.remove_star_sign(self.strip_brackets(object_raw)))

    # Goes through token and finds the plainlist and outputs the subject and object
    # TODO : remove duplicate names and maybe non-capitalized words
    def get_relations(self, token):
        # Gets everything from '| [text] Plainlist' to }
        plainlist = re.findall("(\|.*?\=\s+{{[P|p]lainlist\s*[\s\S]*?(?=\}))", token)
        result_buffer = []
        if len(plainlist) > 0:
            # goes through plainlist items
            for plainlist_item in plainlist:

                # finds the predicate (located between '|' and '=' )
                # removes non alphabetical chars
                predicate = re.findall("(\|.*?\=)", plainlist_item)
                evidence = predicate
                predicate = re.sub("[^a-zA-Z]", "", predicate[0])

                # splits on new lines and removes the predicate (index 0) from the list
                objects = plainlist_item.splitlines()
                objects.pop(0)

                # goes through subjects
                for object_raw in objects:
                    subject = re.sub("[^a-zA-Z]", " ", object_raw).strip()
                    result_buffer.append(
                        {"predicate": predicate, "object": self.normalize_object_name(object_raw), "evidence": plainlist_item}
                    )

        # math pattern like `| xxx = {{ubl`
        unbulleted_list = re.findall(r"(\|.*?\=\s+{{ubl\s*[\s\S]*?(?=\}))", token)
        for list_item in unbulleted_list:
            predicate = re.findall(r"(?<=\| )(.*)(?=\= )", list_item)[0].strip()
            objects_raw = re.search(r"\{{ubl\|(.*)", list_item, re.DOTALL).group(1) # get everything after `{{ubl|`
            objects_list_raw = re.split(r"\|", objects_raw) # split raw objects by `|`
            for object_list_item in objects_list_raw:
                result_buffer.append(
                    {
                        "predicate": predicate,
                        "object": self.normalize_object_name(object_list_item),
                        "evidence": list_item,
                    }
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
            object_text_raw = object_raw.group(1).strip()
            if (
                object_raw
                and not object_text_raw.lower().startswith("{{plainlist")
                and not object_text_raw.lower().startswith("{{ubl")
            ):
                object_name = self.normalize_object_name(object_text_raw)
            else:
                continue  # continoue to parse next relation

            result_buffer.append(
                {"predicate": predicate, "object": object_name, "evidence": relation_raw}
            )
        return result_buffer


def main():
    extracter = Extracter()
    fn = "data/Loving_Vincent.wiki"
    relatinos = extracter.file_extract(fn)


if __name__ == "__main__":
    main()
