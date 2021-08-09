# Import libraries
import csv

def main(argc, argv):
    input_path = 'testDraft1.csv'
    input_path2 = 'test(age_and_emotion).csv'
    input_path3 = 'testWithImageData.csv'
    output_path = 'finalTest.csv'

    input_paths = [input_path, input_path2, input_path3]
    input_files = [open(path) for path in input_paths]
    readers = [csv.reader(input_file, delimiter=',') for input_file in input_files]

    output_file = open(output_path, 'w')
    writer = csv.writer(output_file)

    merge_mapping = {}
    extra_row = {}

    for i, reader in enumerate(readers):
        for j, row in enumerate(reader):
            if i == 1:
                # print(row[-2:])
                merge_mapping[j].extend(row[-2:])
            elif i == 2:
                merge_mapping[j].extend(row[-4:])    
            else:
                extra_row[j] = []
                extra_row[j].append(row[-3])
                extra_row[j].append(row[-2])
                del row[-3]
                del row[-2]
                merge_mapping[j] = row

    for row in merge_mapping:
        merge_mapping[row].extend(extra_row[row])
        writer.writerow(merge_mapping[row])

    return 0

if __name__ == "__main__":
    import sys
    main(len(sys.argv), sys.argv)
