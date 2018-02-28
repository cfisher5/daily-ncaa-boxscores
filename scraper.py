from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def get_links(year, month, day):

    links = []
    url = "http://www.sports-reference.com/cbb/boxscores/index.cgi?month=" + str(month) + "&day=" + str(day) + "&year=" + str(year)
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    for situation in soup.findAll('tbody'):
        info = []
        for games in situation.findAll('tr'):
            for link in games.findAll('td', attrs={'class': 'right gamelink'}):
                info.append(link.a['href'])
            for x in games.findAll('td'):
                if x.string is None:
                    info.append(x.a.string)
                else:
                    info.append(x.string)
        game = []
        game.append(info[0])
        game.append(info[1])
        game.append(info[2])
        game.append(info[4])
        game.append(info[5])
        links.append(game)

    return links


def scrape_box_scores(links, year, month, day):

    filename = "boxscores_" + year + '-' + month + "-" + day + ".csv"
    file = open(filename, 'a')
    file.write(",MP,FG,FGA,FG%,2P,2PA,2P%,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,DATE,TEAM,OPP,H/A,W/L\n")
    for link in links:
        url = "http://www.sports-reference.com/" + link[0]
        page = urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        r_table = soup.findAll('table', id=re.compile("^box-score-basic-*"))

        if r_table is None:
            print("end of data")
            break

        i = 1
        for table in r_table:

            for row in table.findAll("tr"):
                col = 0
                for name in row.findAll('th', class_="left"):
                    col += 1
                    print(name.string)
                    file.write(name.string + ',')

                cells = row.findAll("td")
                for cell in cells:
                    col += 1
                    if cell.string is None:
                        if cell.find("a") is not None:
                            value = cell.find("a").string.replace(",", "")
                            file.write(value + ",")
                        else:
                            file.write(',')
                    else:
                        value = cell.string.replace(",", "")
                        file.write(value + ',')

                if col > 1:
                    file.write(year + '-' + month + '-' + day + ',')

                    if i == 1:

                        file.write(link[1] + ',')
                        file.write(link[3] + ',')
                        file.write("A,")
                        if link[2] > link[4]:
                            file.write("W" + ',')
                        else:
                            file.write("L" + ',')

                    else:

                        file.write(link[3] + ',')
                        file.write(link[1] + ',')
                        file.write("H,")
                        if link[4] > link[2]:
                            file.write("W" + ',')
                        else:
                            file.write("L" + ',')

                file.write('\n')
            i += 1

    file.close()










