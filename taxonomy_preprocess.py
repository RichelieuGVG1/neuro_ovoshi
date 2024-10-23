import csv
import os
import time
import logging
import io
import sys
import re

global input_name
global taxonomy
global find_pattern

taxonomy = []

def taxonomy_data_loader():
    with open('taxonomy_of_all_plants.txt', 'r', encoding="utf-8") as file:
        text = file.read()
        file.close()
    pattern = r'\s{2,}'
    elements = re.split(pattern, text)
    for _ in elements:
        taxonomy.append(_)

'''
def remove_until_last_space(input_name):
    last_space_index = input_name.rfind(' ')
    if last_space_index != -1:
        return input_name[last_space_index + 1:]
    else:
        return None
'''

def make_csv(string):
    elements = string.split('_')
    elements = [element.replace('0', '') for element in elements]
    elements = [''] * 2 + elements

    with open('taxonomy.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(elements)
    
    #file.close()


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
        
        if first_space_index != -1:
            second_space_index = part.find(' ', first_space_index + 1)
            if second_space_index != -1:
                parts[i] = part[:second_space_index].strip()

        if part.endswith('.'):
            parts[i] = part[:part.find(' ')].strip()

    #return '_'.join(parts)
    return input_string


def find_path(taxonomy, input_name):
    #print(1)
    #print(input_name)
    pattern = re.compile(re.escape(input_name))

    for index, item in enumerate(taxonomy, start=1):
        if re.search(pattern, item):
            return index, item

    # find_path(taxonomy, remove_until_last_space(input_name))
    if input_name.rfind(' ') != -1:
        # find_path(taxonomy, input_name[:input_name.rfind(' ')])
        return find_path(list(map(lambda x: x.lower(), taxonomy)), input_name[:input_name.rfind(' ')])
        return 0
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

    #print(remove_trash_from_string(returned_string), 1)
    if tax_index == 7: #ВАЖНЫЙ ИНДЕКС ДЛЯ ДОБАВЛЕНИЯ НОВЫХ ТАКСОНОВ!!!
        return print_stroke(concat(string, remove_trash_from_string(returned_string), find_pattern[tax_index]))
    else:
        return find_taxonomy(index, tax_index + 1, concat(string, remove_trash_from_string(returned_string), find_pattern[tax_index]))


def main(input_name):
    start_time = time.time()

    print('program started.')
    #print(input_name)
    #input_name = input('Enter certain name of species>')

    index, found_string = find_path(list(map(lambda x: x.lower(), taxonomy)), input_name.lower().strip())

    #print(remove_trash_from_string(taxonomy[index-1]), 2)

    if found_string is not None:
        output=remove_brackets(find_taxonomy(index, 1, concat('', remove_trash_from_string(taxonomy[index-1]), '[species]'))[:-1])
        if '*' in output:
            output = output[:-1] + input_name
        #print(output)
        #make_csv(output)

        return output
    else:
        print("no matches found")
        return None
        #quit()

    #OPTIONAL!!
    print(time.time() - start_time)
    #os.system('pause')

    #return remove_brackets(find_taxonomy(index, 1, concat('', found_string, '[species]'))[:-1].lower())

#if __name__ == '__main__':
#    main()