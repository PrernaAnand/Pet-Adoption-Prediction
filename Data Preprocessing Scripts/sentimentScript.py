import json
import os
import openpyxl as xl

def main(argc, argv):

    json_folder_path = "/Users/SagarChadha/Documents/Year3-APS360-AIFundamentals/Project/petfinder-adoption-prediction/test_sentiment"
    excel_path = "/Users/SagarChadha/Documents/Year3-APS360-AIFundamentals/Project/SentimentAddition/test.xlsx" 
    
    score_mapping = {}
    for file in os.listdir(json_folder_path):
        file_path = json_folder_path + '/' + file
        pet_id = file.strip('.json')

        # Opening the json file
        with open(file_path) as json_file:
            data = json.load(json_file)
        score_mapping[pet_id] = data['documentSentiment']['score']
    
    avg_value = sum(score_mapping.values())/len(score_mapping.values())

    workbook = xl.load_workbook(excel_path)
    sheet = workbook.active

    for cell in sheet["V"]:
        if cell.coordinate == "V1":
            new_value = "SentimentScore" 
        else:
            pet_id = cell.value
            # print(pet_id)
            if pet_id in score_mapping:
                new_value = score_mapping[pet_id]
            else:
                new_value = avg_value
        # print(new_value)
        sheet[cell.coordinate.replace("V", "Y")] = new_value

    workbook.save(excel_path.replace("test.xlsx", "testWithSent.xlsx"))
 
    return 0

if __name__ == "__main__":
    import sys
    main(len(sys.argv), sys.argv)
