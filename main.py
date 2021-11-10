import json
from pprint import pprint
import wikipediaapi
import time
from progress.bar import Bar
import os
import hashlib
countries = []


class WikiIterator:
    def __iter__(self):
        return self

    def __init__(self, countries_list):
        self.countries_list = countries_list

    def __next__(self):
        if self.countries_list:
            country = self.countries_list.pop(0)
            page_py = wiki_wiki.page(country)
            if page_py.exists():
                #print(page_py.fullurl)
                return {country: page_py.fullurl}
        else:
            raise StopIteration


def file_str_generator(filepath):
    with open(filepath, "r") as read_file:
        for line in read_file:
            hash_object = hashlib.md5(line.strip().encode())
            yield hash_object.hexdigest()


if __name__ == '__main__':
    with open("countries.json", "r") as read_file:
        data = json.load(read_file)
    for i in data:
        countries.append(i["name"]["common"])
    progress_bar = Bar('Составление списка стран и ссылок на статьи в Википедии: ', max=len(countries))
    wiki_wiki = wikipediaapi.Wikipedia('en')

    iter = WikiIterator(countries)
    counry_and_url = {}
    for i in iter:
        counry_and_url.update(i)
        progress_bar.next()
    progress_bar.finish()
    #pprint(counry_and_url)
    with open('counry_and_url.json', 'w') as f:
        json.dump(counry_and_url, f, indent=4)

    fsg = file_str_generator('counry_and_url.json')
    for i in fsg:
        print(i)
    os.system('pause')



