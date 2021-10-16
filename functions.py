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

def scrap_person_info(http_responses,url_lists):
    persons_info=[]
    for page in http_responses:
        soup = BeautifulSoup(page,'lxml')
        persons_info.append(soup.find('h1').text)
    print(list(zip(persons_info,url_lists)))
