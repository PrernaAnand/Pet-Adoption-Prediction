# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
from collections import OrderedDict 

def setup_breed_structure(input_path):
    input_file = open(input_path)
    reader = csv.reader(input_file, delimiter=',')
    breed_mapping = {}

    for row in reader:
        breed_mapping[row[-1]] = []
    # print(breed_mapping)
    input_file.close()
    return breed_mapping

def convertDog(name):
    return convertCat(name)[:-1]

def convertCat(name):
    finalName = name.split(' ')[1:]
    return ' '.join(finalName)

def scrap_data(url1, url2, breed_mapping):
    topCats = []
    topDogs = []
    for url in [url1, url2]:

        # Connect to the URL
        response = requests.get(url)

        # Parse HTML and save to BeautifulSoup object¶
        soup = BeautifulSoup(response.text, "html.parser")

        for one_a_tag in soup.findAll('h2'):  #'a' tags are for links
            # print(one_a_tag.get_text())
            try:
                if 'dog' in url and convertDog(one_a_tag.get_text()) in breed_mapping:
                    topDogs.append(convertDog(one_a_tag.get_text()))
                elif 'cat' in url and convertCat(one_a_tag.get_text()) in breed_mapping:
                    topCats.append(convertCat(one_a_tag.get_text()))
            except IndexError:
                pass

    topCats = topCats[-10:]
    return topCats, topDogs

def check(topCats, topDogs, name):
    for cat in topCats:
        if cat in name:
            return True
    
    for dog in topDogs:
        if dog in name:
            return True
    return False


def main(argc, argv):
    # Adding the adoption speed to the prediction results
    input_path = '../petfinder-adoption-prediction/breed_labels.csv'
    breed_mapping = setup_breed_structure(input_path)

    urlCats = 'https://cattime.com/lifestyle/781-the-25-most-popular-cat-breeds'
    urlDogs = 'https://dogtime.com/dog-health/general/4333-most-popular-dog-breeds-list'
    topCats, topDogs = scrap_data(urlCats, urlDogs, breed_mapping)

    for key in breed_mapping:
        if key in topCats or key in topDogs or check(topCats, topDogs, key):
            breed_mapping[key].append(1)
        else:
            breed_mapping[key].append(0)
    # print(breed_mapping)

    input_path = 'testWithSent.csv'
    output_path = 'testDraft1.csv'

    input_file = open(input_path)
    output_file = open(output_path, "w")
    reader = csv.reader(input_file, delimiter=',')
    writer = csv.writer(output_file)

    for i, row in enumerate(reader):
        if i == 0:
            row.append('BreedRating')
        else:
            row.append(list(breed_mapping.items())[int(row[3])][1][0])
        writer.writerow(row)
    return 0

if __name__ == "__main__":
    import sys
    main(len(sys.argv), sys.argv)
