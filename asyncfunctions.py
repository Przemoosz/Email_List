import asyncio
import aiohttp
from functions import scrap_persons,scrap_person_info
from decorators import func_timer


#@func_timer(mode=True)
def main():
    url = 'https://skos.agh.edu.pl/jednostka/akademia-gorniczo-hutnicza-im-stanislawa-staszica-w-krakowie' \
          '/wydzial-elektrotechniki-automatyki-informatyki-i-inzynierii-biomedycznej' \
          '/katedra-elektrotechniki-i-elektroenergetyki-108.html'
    list_of_persons = asyncio.run(http_request_first_page(url))
    #list_of_persons = ['https://skos.agh.edu.pl/osoba/marek-szczerbinski-3280.html']
    http_response = asyncio.run(http_req(list_of_persons))
    scrap_person_info(http_response,list_of_persons)


def tasks_creation(session, list_of_persons):
    tasks = []
    for i in list_of_persons:
        tasks.append(asyncio.create_task(session.get(i, ssl=False)))

    return tasks
    pass


async def http_req(list_of_persons):
    async with aiohttp.ClientSession() as session:
        tasks = tasks_creation(session, list_of_persons)
        responses = await asyncio.gather(*tasks)
        text_responses=[]
        for i in responses:
            text_responses.append(await i.text())
        #print(responses)
        return text_responses

async def http_request_first_page(url):
    async with aiohttp.ClientSession() as sesion:
        page = await sesion.get(url, ssl=False)
        p = await page.text()
        return scrap_persons(p)


@func_timer(mode=True)
def foo():
    [print(i) for i in range(100)]
    pass


main()
# foo()
