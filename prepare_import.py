"""
Splits a Wordpress export file into multiple parts.

Useful to when the export file exceeds the 2MB limit and needs to be imported
in parts.

Usage: python prepare_import.py [foo.wordpress.xml] [n=10]

The divided parts will be called "wxrN.xml" where N is an arbitrary int.

Note, this requires 'header.xml' and 'footer.xml' to function correctly.
"""
import sys

HEADER = "header.xml"
FOOTER = "footer.xml"

ITEM_START = "<item>"
ITEM_END = "</item>"


def get_items(filename):
    """Get the items in a wxr file.

    Items can media or posts.
    """
    items = []
    with open(filename) as f:
        item = ""
        reading_item = False
        for line in f:
            if ITEM_START in line:
                reading_item = True
            elif ITEM_END in line:
                item += line
                items.append(item)
                item = ""
                reading_item = False
            if reading_item:
                item += line
    return items


def main(filename, n=10):
    """Split a wxr file into n valid wxr files."""
    with open(HEADER) as f:
        header_text = f.read()
    with open(FOOTER) as f:
        footer_text = f.read()
    items = get_items(filename)
    j = len(items) / n
    i = 0
    while i < len(items):
        item_group = items[i:i + j]
        with open("wxr%s.xml" % i, 'w') as f:
            f.write(header_text)
            for item in item_group:
                f.write(item)
            f.write(footer_text)
        i += j

if __name__ == "__main__":
    try:
        n = int(sys.argv[2])
    except IndexError:
        n = None
    main(sys.argv[1], n)
