from funcs import *
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    file_transfer("./src/static", "./docs")
    generate_pages_recursive("./src/content", "./template.html", "./docs", basepath)
    print("<----------Generation Complete!---------->")



main()
