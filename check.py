"""
Check whether we find all relations from the sample data set
"""

import csv
import os


def get_output_files(dir="output"):
    (dirpath, _, filenames) = next(os.walk(dir))
    return {
        filename: os.path.join(dirpath, filename)
        for filename in filenames
        if filename.endswith(".tsv")
    }


def main():
    output_list = get_output_files("output")
    sample_list = get_output_files("data")

    for filename, output_path in output_list.items():
        sample_path = sample_list[filename]
        print("Start comparing {} and {}".format(output_path, sample_path))

        our_output = {}
        sample_output = {}
        with open(output_path) as out_f, open(sample_path) as samp_f:
            out_reader = csv.reader(out_f, delimiter="\t")
            samp_reader = csv.reader(samp_f, delimiter="\t")

            for each in out_reader:
                if len(each) >= 3:
                    our_output["{}::{}".format(each[1], each[2])] = each[2]
                else:
                    print(each)

            for each in samp_reader:
                if len(each) >= 3:
                    sample_output["{}::{}".format(each[1], each[2])] = each[2]

        for predicate_object_name, object_name in sample_output.items():
            # special handling for predicate "musicComposer",
            # no clue how the sample dataset name it "musicComposer"
            if predicate_object_name.startswith("musicComposer"):
                predicate_object_name = "music::{}".format(object_name)

            if predicate_object_name.startswith("country"):
                predicate_object_name = "country::{}".format(object_name.replace(" ", "_"))

            if predicate_object_name.startswith("studio"):
                predicate_object_name = "studio::{}".format(object_name.replace(" ", "_"))

            if not our_output.get(predicate_object_name, []) or not our_output.get(
                predicate_object_name, None
            ):
                if predicate_object_name.startswith("writer") and our_output.get(
                    "screenplay::{}".format(object_name), None
                ):
                    continue
                if predicate_object_name.startswith("producer") and our_output.get(
                    "producers::{}".format(object_name), None
                ):
                    continue
                print("Missing: {}".format(predicate_object_name))

        print("Done comparing {} and {}\n".format(output_path, sample_path))


if __name__ == "__main__":
    main()
