from bs4 import BeautifulSoup

'''
Creator: Przemysław Szewczak
Version: 1.0.1
Update date: 17.10.2021
Python: 3.9.7
Sync function file, you should not change anything here!
'''


# Scraps urls from cathedral page and returns a list of urls (persons)
def scrap_persons(page):
    print('19 % - Started persons urls scraping')
    soup = BeautifulSoup(page, 'lxml')
    list_of_persons = []
    for person in soup.find_all('li'):
        if person.find('a', href=True) is None:
            continue
        if 'osoba' not in person.find('a', href=True).attrs['href']:
            continue
        link = person.find('a', href=True).attrs['href']
        list_of_persons.append(link)
    print('25 % - Finished scraping urls')
    return list_of_persons


# Scraps person page to get information about title, name and surname
def scrap_person_info(http_responses, url_lists):
    print('55 % - Started first stage person scraping')
    persons_info = []
    for page in http_responses:
        soup = BeautifulSoup(page, 'lxml')
        name = soup.find('h1').text
        title = ',' + soup.find('td', class_='title').text
        # print(name+title)
        persons_info.append(name + title)
    print('61 % - Finished first stage')
    # We need more information so we pass list of tuples with title,name and url to getting_better_info
    return getting_better_info(list(zip(persons_info, url_lists)))


# The function which takes a list of tuples and manipulates them to take the info about gender and pass
# more friendly list of tuples with information about the person
def getting_better_info(information_list):
    print('67 % - Started second stage person scraping')
    returning_list = []

    for i in information_list:
        if len(i[0].split(',')) == 3:
            # print(i[0].split(','))
            name = i[0].split(',')[0].split(' ')[0]
            title = i[0].split(',')[1]
            if name[-1] == 'a':
                plec = 'F'
            else:
                plec = 'M'
            returning_tuple = (i[0].split(',')[0], title, plec, i[0].split(',')[2], i[1])
            returning_list.append(returning_tuple)
        else:
            continue
    print('73 % - Finished second stage')
    return returning_list


# Function which read template file and returns it
def file_read():
    with open('mail_context.txt', 'r', encoding='utf-8') as file:
        text = file.read()
        return text
