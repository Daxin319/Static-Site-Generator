from funcs import *


def main():
    file_transfer("/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/static", "/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/public")
    generate_pages_recursive("/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/src/content", "/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/template.html", "/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/public")




main()