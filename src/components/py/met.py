import csv
import copy
import json
import pprint
import requests
import random
from pathlib import Path
import pprint as pp

from urllib.parse import quote, urlencode, urljoin

def clean_objects(objects, filtered_keys):
    # objects = list of dictionaries
    # filtered_keys = a list of keys
    # return a list of dicts

    filtered_paintings = []
    public_domain_paintings = is_public_domain_painting(objects)
    for painting in public_domain_paintings:
        new_painting = {}
        if "|" not in painting['Artist Display Name'] and "unidentified" not in painting['Artist Display Name'].lower() and "painter" not in painting['Artist Display Name'].lower():
            for key, value in painting.items():
                if key == "Tag":
                # if key in filtered_keys and "|" in value:
                    new_painting[key] = value.split("|")
                elif key in filtered_keys:
                    new_painting[key] = value
            filtered_paintings.append(new_painting)
    return filtered_paintings


def get_url(paintings, artist_names, departments):
    # artists = list of unique artist names
    # departments and artist_names = a list of unique departments and artist names
    # return a dict of all painting urls for each artist

    filtered_paintings = {}
    for department in departments:
        for artist in artist_names:
            artist_paintings = filter_painting_by_category(paintings, 'Artist Display Name', artist)
            artist_department = get_unique_values(artist_paintings, 'Department')
            if len(artist_paintings) >= 3:
                if department in artist_department:
                    artist_ids = get_object_id(artist_paintings)
                    for i in range(len(artist_ids)):
                        artist_ids[i] = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{artist_ids[i]}"
                    filtered_paintings[artist] = artist_ids

        # for painting in paintings:
        #     if painting['Department'] == department and painting['Artist Display Name'] not in included_artist_names:
        #         included_artist_names.append(painting['Artist Display Name'])
        #         paintings_by_artist = filter_painting_by_category(paintings, 'Artist Display Name', painting['Artist Display Name'])
        #         for painting in paintings_by_artist:
        #             department_dict[department] = {painting['Artist Display Name']: get_object_id(paintings_by_artist)}
        # filtered_paintings.append(department_dict)
    return filtered_paintings

def filter_painting_by_category(paintings, category, string):
    # objects = list of dictionaries
    # category = string of the dict key
    # return a list of dicts

    filtered_paintings = []
    for painting in paintings:
        if painting[category].lower() == string.lower():
            filtered_paintings.append(painting)
    return filtered_paintings


def get_unique_values(paintings, category):
    # objects = list of dictionaries
    # return a list of unique artist names

    unique_values = []
    for painting in paintings:
        value = painting[category]
        if value and value not in unique_values:
            if "|" in value:
                for individual_value in value.split("|"):
                    if individual_value not in value:
                        unique_values.append(individual_value)
            else:
                unique_values.append(value)
    unique_values.sort()
    return unique_values


def get_object_id(objects):
    # objects = list of dictionaries
    # return a dict of object IDs for each artist

    object_id = []
    for object in objects:
        object_id.append(object['Object ID'])
    return object_id


def is_public_domain_painting(objects):
    # objects = list of dictionaries
    # return a filtered list of dicts

    filtered_objects = []
    for object in objects:
        if object['Is Public Domain'] == 'True' and "Paintings" in object['Classification'] and object['Artist Display Name']:
            new_object = {}
            for key, value in object.items():
                new_object[key] = value
            filtered_objects.append(new_object)
    return filtered_objects

def read_csv(filepath, encoding="utf-8", newline="", delimiter=","):
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list of lists,
    wherein each nested list represents a single row from the input file.

    WARN: If a byte order mark (BOM) is encountered at the beginning of the first line of decoded
    text, call < read_csv > and pass 'utf-8-sig' as the < encoding > argument.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
    may not be interpreted correctly by the csv.reader.

    Parameters:
        filepath (str): The location of the file to read
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested "row" lists
    """

    with open(filepath, "r", encoding=encoding, newline=newline) as file_obj:
        data = []
        reader = csv.reader(file_obj, delimiter=delimiter)
        for row in reader:
            data.append(row)
        return data

def read_csv_to_dicts(filepath, encoding="utf-8-sig", newline="", delimiter=","):
    """
    Accepts a file path for a .csv file to be read, creates a file object,
    and uses csv.DictReader() to return a list of dictionaries
    that represent the row values from the file.

    Parameters:
        filepath (str): path to csv file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested dictionaries representing the file contents
    """

    with open(filepath, "r", newline=newline, encoding=encoding) as file_obj:
        data = []
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        for line in reader:
            data.append(line)
        return data

def read_json(filepath, encoding="utf-8"):
    """Reads a JSON file and converts it to a Python dictionary.

    Parameters:
        filepath (str): a path to the JSON file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """
    with open(filepath, "r", encoding=encoding) as file_obj:
        data = json.load(file_obj)
    return data

def write_csv(filepath, data, headers=None, encoding="utf-8", newline=""):
    """
    Writes data to a target CSV file. Column headers are written as the first
    row of the CSV file if optional headers are specified.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted
    fields may not be interpreted correctly by the csv.reader. On platforms that utilize
    `\r\n` an extra `\r` will be added.

    Parameters:
        filepath (str): path to target file (if file does not exist it will be created)
        data (list | tuple): sequence to be written to the target file
        headers (seq): optional header row list or tuple
        encoding (str): name of encoding used to encode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences

    Returns:
        None
    """

    with open(filepath, "w", encoding=encoding, newline=newline) as file_obj:
        writer = csv.writer(file_obj)
        if headers:
            writer.writerow(headers)
            for row in data:
                writer.writerow(row)
        else:
            writer.writerows(data)

def write_dicts_to_csv(filepath, data, fieldnames, encoding="utf-8", newline=""):
    """
    Uses csv.DictWriter() to write a list of dictionaries to a target CSV file as row data.
    The passed in fieldnames list is used by the DictWriter() to determine the order
    in which each dictionary's key-value pairs are written to the row.

    Parameters:
        filepath (str): path to target file (if file does not exist it will be created)
        data (list): dictionary content to be written to the target file
        fieldnames (seq): sequence specifying order in which key-value pairs are written to each row
        encoding (str): name of encoding used to encode the file
        newline (str): specifies replacement value for newline '\n'
        or '\r\n' (Windows) character sequences.

    Returns:
        None
    """

    with open(filepath, "w", encoding=encoding, newline=newline) as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def write_json(filepath, data, encoding="utf-8", indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file

        data (dict)/(list): the data to be encoded as JSON and written to
        the file

        encoding (str): name of encoding used to encode the file

        indent (int): number of "pretty printed" indention spaces applied to
        encoded JSON

    Returns:
        None
    """

    with open(filepath, "w", encoding=encoding) as file_obj:
        json.dump(data, file_obj, indent=indent)

def main():

    filepath_objects = Path("./MetObjects.csv").absolute()
    objects = read_csv_to_dicts(filepath_objects)

    # for object in objects:
    #     if object['Object ID'] == "459193":
    #         pp.pprint(object)

    # pp.pprint(objects[459193])

    filtered_categories = ['Artist Display Name',
                     'Department',
                     'Link Resource',
                     'Medium',
                     'Object Date',
                     'Object ID',
                     'Tags',
                     'Title'
                     ]

    filtered_paintings = clean_objects(objects, filtered_categories)
    # pp.pprint(filtered_paintings[:10])

    departments = get_unique_values(filtered_paintings, 'Department')
    # pp.pprint(departments)

    filtered_departments = ['European Paintings',
                            'Robert Lehman Collection']

    unique_artist_names = get_unique_values(filtered_paintings, 'Artist Display Name')
    # write_json("./artist_names.json", unique_artist_names)

    # van_gogh = filter_painting_by_category(filtered_paintings, 'Artist Display Name', 'Vincent van Gogh')
    # # pp.pprint(van_gogh)
    # # print(len(van_gogh))

    # van_gogh_id = get_object_id(van_gogh)
    # # print(van_gogh_id)

    # painting_urls_all_departments = get_url(filtered_paintings, unique_artist_names, departments)
    # write_json("./painting_ids_all_departments.json", painting_urls_all_departments)

    painting_urls = get_url(filtered_paintings, unique_artist_names, filtered_departments)
    write_json("./painting_urls.json", painting_urls)

    # painting_ids = []
    # for artist_name in unique_artist_names:
    #     artist_paintings = filter_painting_by_category(filtered_paintings, 'Artist Display Name', artist_name)
    #     if len(artist_paintings) >= 3:
    #         artist_painting_ids = get_object_id(artist_paintings)
    #         artist_dict = {}
    #         artist_dict[artist_name] = artist_painting_ids
    #         painting_ids.append(artist_dict)

    # # pp.pprint(painting_ids)
    # write_json("./painting_ids.json", painting_ids)

    random_artists = random.sample(list(painting_urls.keys()), 2)
    pp.pprint(random_artists)
    first_artist_ids = random.sample(painting_urls[random_artists[0]], 3)
    second_artist_ids = random.choice(painting_urls[random_artists[1]])

    print("Incorrect answers: ", first_artist_ids)
    print("Correct answers: ", second_artist_ids)




if __name__ == "__main__":
    main()