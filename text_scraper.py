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
    parser.add_argument("-o", "--output-dir", default="jsonified", dest="odir")
    argl = parser.parse_args()

    if not os.path.exists(argl.scrape_dir):
        raise NotADirectoryError("Given path to files not found.")

    if not os.path.exists(argl.odir):
        os.makedirs(argl.odir)

    relevant_passages = {
        'Title',
        'Author'
    }

    for file in os.listdir(argl.scrape_dir):
        data = {}

        with open(os.path.join(argl.scrape_dir, file)) as fp:

            text = ""

            for line in fp:
                text += line
                line = line.strip()

                if "://" not in line:
                    # Try to get metadata

                    line = line.split(":")

                    if line[0] in relevant_passages:
                        data[line[0].strip()] = line[1].strip()

                elif "://" in line:
                    # Try to format a URL
                    pages = line.split("/")

                    if len(pages) >= 5:
                        url = line + pages[-2] + ".txt"
                        data["url"] = url

            data["text"] = text

            with open(os.path.join(argl.odir, file + '.json'), 'w') as ofile:
                json.dump(data, ofile, indent=2)


