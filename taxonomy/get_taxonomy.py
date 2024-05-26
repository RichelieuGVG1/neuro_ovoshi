import csv
import os
import time
import re


def make_csv(common_species, common_variety,disease,rot, string):
    elements = string.split('_')
    elements = [element.replace('0', '') for element in elements]
    elements = [common_species, common_variety, disease,rot] + elements

    with open(get_taxonomy, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(elements)


def remove_trash_from_string(string):
    for i, char in enumerate(string[1:], start=1):
        if char.isupper():
            space_index = string.rfind(' ', 0, i)
            if space_index != -1:
                return string[:space_index]
            else:
                return string[:i] 
    return string 


def clear_authors(input_string):
    parts = input_string.split('_')
    for i, part in enumerate(parts):
        first_space_index = part.find(' ')
        if (first_space_index != -1):
            second_space_index = part.find(' ', first_space_index + 1)
            if (second_space_index != -1):
                parts[i] = part[:second_space_index].strip()
        if part.endswith('.'):
            parts[i] = part[:part.find(' ')].strip()
    return input_string


def find_path(taxonomy, input_name):
    pattern = re.compile(re.escape(input_name))
    for index, item in enumerate(taxonomy, start=1):
        if re.search(pattern, item):
            return index, item
    if input_name.rfind(' ') != -1:
        return find_path(list(map(lambda x: x.lower(), taxonomy)), input_name[:input_name.rfind(' ')])
    else:
        return None, None


def remove_brackets(input_string):
    return re.sub(r'\[.*?\]', '', input_string).strip()


def concat(string, new_str, remove_word):
    return f"{string.strip()}_{new_str.replace(remove_word, '').strip()}"


def print_stroke(input_str):
    return '_'.join(reversed(input_str.split('_')))


def find_taxonomy(index, tax_index, string):
    returned_string = ''
    found_flag = 0
    with open('taxonomy_of_all_plants.txt', 'r', encoding="utf-8") as file:
        lines = file.readlines()

    find_pattern = ['[species]', '[genus]', '[subfamily]', '[family]', '[order]', '[class]', '[phylum]', '[kingdom]']

    for line in reversed(lines[:index]):
        if find_pattern[tax_index] in line and not '*' in line:
            returned_string = line.strip()
            found_flag = 1
            break

    if found_flag == 0:
        returned_string = '0'

    if tax_index == 7:
        return print_stroke(concat(string, remove_trash_from_string(returned_string), find_pattern[tax_index]))
    else:
        return find_taxonomy(index, tax_index + 1, concat(string, remove_trash_from_string(returned_string), find_pattern[tax_index]))


def main(common_species, common_variety, disease,rot, input_name):
    start_time = time.time()
    print('program started.')

    index, found_string = find_path(list(map(lambda x: x.lower(), taxonomy)), re.sub(r'<[^>]*>', ' ', input_name).lower().strip())

    if found_string is not None:
        output = remove_brackets(find_taxonomy(index, 1, concat('', remove_trash_from_string(taxonomy[index-1]), '[species]'))[:-1])
        print(output)
        make_csv(common_species, common_variety, disease,rot,  output)
    else:
        print("no matches found")

    print(time.time() - start_time)


def main_batch(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        print(f"Headers found: {headers}")  
        for row in reader:
            species = row.get('species')
            common_species = row.get('common_species', '')
            common_variety = row.get('common_variety', '')
            disease = row.get('disease', '')
            rot = row.get('rot', '')
            if species:
                main(common_species, common_variety,disease,rot, species.strip())
            else:
                print("No 'species' column found in the row")


if __name__ == '__main__':
    taxonomy = []
    get_taxonomy = 'tomato_cultivars/tomato_cultivars_taxonomy.csv'
    name_dataset_information = 'tomato_cultivars/tomato_cultivars_dataset_information.csv'

    with open('taxonomy_of_all_plants.txt', 'r', encoding="utf-8") as file:
        text = file.read()

    pattern = r'\s{2,}'
    elements = re.split(pattern, text)
    for element in elements:
        taxonomy.append(element)

    with open(get_taxonomy, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['common_species', 'common_variety','disease','rot', 'kingdom', 'phylum', 'class', 'order', 'family', 'subfamily', 'genus', 'species'])

    main_batch(name_dataset_information)
