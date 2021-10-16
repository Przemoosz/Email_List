from bs4 import BeautifulSoup


def scrap_persons(page):
    soup = BeautifulSoup(page, 'lxml')
    list_of_persons = []
    for person in soup.find_all('li'):
        if person.find('a',href=True) == None:
            continue
        if 'osoba' not in person.find('a',href=True).attrs['href']:
            continue
        link = person.find('a',href=True).attrs['href']
        list_of_persons.append(link)
    return list_of_persons

