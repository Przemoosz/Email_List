import asyncio
from asyncfunctions import (http_req,
                            http_request_first_page,
                            save)
from functions import scrap_person_info,getting_better_info
from decorators import func_timer

@func_timer(mode=True)
def main():
    url = 'https://skos.agh.edu.pl/jednostka/akademia-gorniczo-hutnicza-im-stanislawa-staszica-w-krakowie' \
          '/wydzial-elektrotechniki-automatyki-informatyki-i-inzynierii-biomedycznej' \
          '/katedra-elektrotechniki-i-elektroenergetyki-108.html'
    list_of_persons = asyncio.run(http_request_first_page(url))
    http_response = asyncio.run(http_req(list_of_persons))
    info = scrap_person_info(http_response, list_of_persons)
    better_info = getting_better_info(info)
    asyncio.run(save(better_info))

    pass

if __name__ == '__main__':
    main()