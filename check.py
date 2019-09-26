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
                    our_output[each[1]] = each[2]
                else:
                    print(each)

            for each in samp_reader:
                if len(each) >= 3:
                    sample_output[each[1]] = each[2]

        for predicate, object_name in sample_output.items():
            # special handling for predicate "musicComposer",
            # no clue how the sample dataset name it "musicComposer"
            if predicate == "musicComposer":
                predicate = "music"

            if predicate == "country":
                object_name = object_name.replace(" ", "_")

            if (
                not our_output.get(predicate, None)
                or not our_output.get(predicate, None) == object_name
            ):
                print("Missing: {} {}".format(predicate, object_name))

        print("Done comparing {} and {}\n".format(output_path, sample_path))


if __name__ == "__main__":
    main()
