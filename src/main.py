from funcs import *
import sys

def main():
    if len(sys.argv) <= 2:
        basepath = "/"
    else:
        basepath = sys.argv[2]
    print(basepath)
    file_transfer("/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/src/static", "/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/docs")
    generate_pages_recursive("/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/src/content", "/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/template.html", "/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/docs", basepath)
    print("<----------Generation Complete!---------->")



main()
