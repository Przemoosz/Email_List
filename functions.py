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
        name = soup.find('h1').text
        title = ','+soup.find('td',class_='title').text
        #print(name+title)
        persons_info.append(name+title)
    return list(zip(persons_info,url_lists))


def getting_better_info(information_list):
    returning_list=[]

    for i in information_list:
        if len(i[0].split(',')) == 3:
            #print(i[0].split(','))
            name = i[0].split(',')[0].split(' ')[0]
            title = i[0].split(',')[1]
            if name[-1] == 'a':
                plec = 'F'
            else:
                plec = 'M'
            returning_tuple = (title, plec)
            returning_tuple = (i[0].split(',')[0],title,plec,i[0].split(',')[2],i[1])
            returning_list.append(returning_tuple)
        else:
            continue

    return returning_list