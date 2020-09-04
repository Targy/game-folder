import bs4
import requests
from bs4 import BeautifulSoup as Soup







def sudoku_crapper(url):
    suduko =  [[0 for i in range(9)] for j in range(9)]
    page = requests.get(url)
    result = Soup(page.content, "html.parser")
    big = result.findAll("div",  {"class": "grid"})
    grid = big[0].findAll("tr", {"class": "grid"})
    for i in range(9):
        elements = grid[i].findAll("td")
        for j in range(9):
            suduko[i][j] = elements[j].get_text()
            
            b = bytes(elements[j].get_text(), "utf-8")
            if b == b"\xc2\xa0":
                suduko[i][j] = "-1"
    table = big[0].findAll("table")
    text = table[0].next_sibling
    texts = text.split()


    num = texts[-1]
    return suduko, num










sudoku_crapper("http://www.menneske.no/sudoku/eng/random.html?diff=3")

