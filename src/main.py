from funcs import *
from textnode import *
from parentnode import *
from leafnode import *

def main():
    file_transfer("/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/static", "/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/public")
    generate_page("/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/src/content/index.md", "/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/template.html", "/home/lyle/workspace/github.com/Daxin319/Static-Site-Generator/public/index.html")




main()