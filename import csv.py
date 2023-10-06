
import pandas as pd
from time import sleep
import re
import chardet
import json
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import re
import chardet

from google.colab import files

def read_csv(filename):
    count=0
    df = pd.read_csv(filename, sep=";", encoding='windows-1254')
    for index, row in df.iterrows():
        birth_year = row['birth_year']
        name = row['name']
        if pd.isna(birth_year) or str(birth_year).strip() == '':
            print(name)
            count=count+1
    print(count)
# Replace 'filename.csv' with the actual path to your CSV file

    
def mergeing_ageWcomperhensiveData():
    # Read the contents of the files
    with open("27.Donem_Milletvekili_Link.txt", "r", encoding="utf-8") as link_file:
        link_data = link_file.readlines()

    with open("27Donem_age.csv", "r", encoding="windows-1254") as age_file:
        age_reader = csv.DictReader(age_file, delimiter=";")
        age_entries = [entry for entry in age_reader]

    # Merge the data
    link_entries = []
    for line in link_data:
        entry = json.loads(line)
        link_entries.append(entry)

    for link_entry in link_entries:
        for age_entry in age_entries:
            if (
                link_entry["name"] == age_entry["name"]
                and str(link_entry["term"]) == age_entry["term"]
                and link_entry["party"] == age_entry["party"]
                and link_entry["city"] == age_entry["city"]
            ):
                link_entry["birth_year"] = age_entry["birth_year"]
                break

    # Convert the merged data back to a string
    merged_data = "\n".join(json.dumps(entry, ensure_ascii=False) for entry in link_entries)

    # Write the merged data to a new file
    output_file_path = "27.txt"
    with open(output_file_path, "w", encoding="utf-8") as merged_file:
        merged_file.write(merged_data)


def obtaningBirthYearWithSelenium(name):

    df = pd.read_csv(name, sep=";", encoding='windows-1254')
    print(df.head())

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    for i, row in df.iterrows():
        # Only search for people without birth years
        if pd.isnull(row["birth_year"]):
            name = row["name"]
            
            # navigate to Google
            driver.get("https://www.google.com")
            sleep(2)

            # find the search box, clear it, enter query and submit
            search_box = driver.find_element(By.NAME, "q")
            search_box.clear()
            search_box.send_keys(name + " yaş")
            search_box.send_keys(Keys.RETURN)
            sleep(2)

            # extract the birth year information
            try:
                birth_info = driver.find_element(By.CSS_SELECTOR, '.yxAsKe').text
                # Extract birth year using regex
                birth_year = re.search(r"\d{4}", birth_info).group()

                # Update DataFrame
                df.loc[i, "birth_year"] = birth_year
            except Exception as e:
                print(f"Birth year for {name} could not be retrieved due to error: {e}")

    # close the driver
    driver.quit()

    # Write DataFrame back to CSV
    df.to_csv("22DONEM_AGE.csv", index=False)


def convert_BirthYearToAge (fileName, year):
    # Read the contents of the text file
    with open(fileName, 'r') as file:
        data = file.readlines()

    # Process each JSON object
    new_data = []
    for line in data:
        # Parse the JSON object
        json_obj = json.loads(line)
        # Extract the birth_year and calculate the age
        birth_year = float(json_obj['birth_year'])
        age = year - birth_year

        # Change the column name to 'age'
        json_obj['age'] = age
        del json_obj['birth_year']

        # Append the modified JSON object to the new data list
        new_data.append(json.dumps(json_obj, ensure_ascii=False))

    # Join the JSON objects with newline characters
    new_json = '\n'.join(new_data)

    # Write the modified JSON objects to a new file
    with open('27.Donem_Milletvekili_Link.txt', 'w') as file:
        file.write(new_json)

    # Download the modified data file
    files.download('27.Donem_Milletvekili_Link.txt')
