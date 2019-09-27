"""
Dominick Taylor
Fall 2019
Python file for opening a text file with the assumption that it was obtained from Project Gutenburg and
attempting to pull out relevant metadata, i.e. title, author, etc.
"""

import json
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Scrape a set of specified text files for metadata.")
    parser.add_argument("-d", "--scrape-dir", default="books", dest="scrape_dir")
    argl = parser.parse_args()

    if not os.path.exists(argl.scrape_dir):
        raise NotADirectoryError("Given path to files not found.")

    for file in os.listdir(argl.scrape_dir):
        print(file)

        with open(os.path.join(argl.scrape_dir, file)) as fp:

            for line in fp:

                line = line.strip().split(":")

                print(line)

        break
