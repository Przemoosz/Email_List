import asyncio
import aiohttp
import aiofiles
from functions import scrap_persons, scrap_person_info, getting_better_info, file_read
from decorators import func_timer
import os

'''
Przemysław Szewczak
Python: 3.9.7
Async functions files, you should not change anything here! Expect name variable

'''
# Paste your full name here
name = 'Przemysław Szewczak'

# FUNCKJA TYMCZASOWA BEDZIE PRZENIESIONA DO MAIN.PY
@func_timer(mode=True)
def main():
    url = 'https://skos.agh.edu.pl/jednostka/akademia-gorniczo-hutnicza-im-stanislawa-staszica-w-krakowie' \
          '/wydzial-elektrotechniki-automatyki-informatyki-i-inzynierii-biomedycznej' \
          '/katedra-elektrotechniki-i-elektroenergetyki-108.html'
    list_of_persons = asyncio.run(http_request_first_page(url))
    # list_of_persons = ['https://skos.agh.edu.pl/osoba/zbigniew-galias-818.html']
    http_response = asyncio.run(http_req(list_of_persons))
    info = scrap_person_info(http_response, list_of_persons)
    # print(info)
    better_info = getting_better_info(info)
    # print(better_info)
    # file_write_tasks(file_read(), better_info)
    # asyncio.run(save(better_info)
    asyncio.run(save(better_info))


# Async function which creates first HTTP request to get cathedral workers
async def http_request_first_page(url):
    async with aiohttp.ClientSession() as sesion:
        page = await sesion.get(url, ssl=False)
        p = await page.text()
        return scrap_persons(p)


# Sync function which creates HTTP request tasks
def tasks_creation(session, list_of_persons):
    tasks = []
    for i in list_of_persons:
        tasks.append(asyncio.create_task(session.get(i, ssl=False)))
    return tasks


# Async function which takes tasks and makes a lot of GET requests
# Aiohttp and asyncio allows to make request when we are waiting for response from server
async def http_req(list_of_persons):
    async with aiohttp.ClientSession() as session:
        # Get tasks
        tasks = tasks_creation(session, list_of_persons)
        responses = await asyncio.gather(*tasks)
        text_responses = []
        for i in responses:
            text_responses.append(await i.text())
        return text_responses


# Sync function which takes scraped data and match them with algorithm
# then creates text to save and task for async function
def file_write_tasks(text, list_of_informations):
    tasks = []
    for i in list_of_informations:
        # Matching data to pattern, using title and gender
        if 'profesor' in i[3] and i[2] == 'M':
            answers = [i[0], i[4], "Szanowny Panie Profesorze", "Pana", "zechciałby Pan", "Pana", "Pan zainteresowany",
                       "Pana", "Panu", name]
        elif 'profesor' in i[3] and i[2] == 'F':
            answers = [i[0], i[4], "Szanowna Pania Profesor", "Pani", "zechciałaby Pani", "Pani", "Pani zainteresowana",
                       "Pani", "Pani", name]
        elif 'dr' in i[1] and i[2] == 'M':
            answers = [i[0], i[4], "Szanowny Panie Doktorze", "Pana", "zechciałby Pan", "Pana", "Pan zainteresowany",
                       "Pana", "Panu", name]
        elif 'dr' in i[1] and i[2] == 'F':
            answers = [i[0], i[4], "Szanowna Pani Doktor", "Pani", "zechciałaby Pani", "Pani", "Pani zainteresowana",
                       "Pani", "Pani", name]
        elif i[2] == 'F':
            answers = [i[0], i[4], "Szanowna Pani ...", "Pani", "zechciałaby Pani", "Pani", "Pani zainteresowana",
                       "Pani", "Pani",
                       name]
        else:
            answers = [i[0], i[4], "Szanowny Panie ...", "Pana", "zechciałby Pan", "Pana", "Pan zainteresowany", "Pana",
                       "Panu", name]
        text_to_save = text.format(*answers)

        path = 'maile\\' + '_'.join(i[0].split(" ")) + '.txt'

        tasks.append(asyncio.create_task(file_write(text_to_save, path)))

    return tasks


# Async saving functions
async def save(better_info):
    # Checking if directory cwd\maile exists
    path_for_project = os.getcwd() + '\\maile'
    if not os.path.exists(path_for_project):
        os.makedirs(path_for_project)
    # Creating list of tasks using sync file_write_tasks function
    list_of_tasks = file_write_tasks(file_read(), better_info)
    # Awaiting tasks
    await asyncio.gather(*list_of_tasks)


# Async file write function
async def file_write(text, path):
    async with aiofiles.open(path, 'w', encoding='utf-8') as file:
        await file.write(text)


#main()
