import asyncio
import aiohttp
from asyncfunctions import (http_req,
                            http_request_first_page,
                            save)
from functions import scrap_person_info
from decorators import func_timer

'''
Creator: Przemysław Szewczak
Version: 1.0.2
Creation date: 16.10.2021
Update date: 18.10.2021
Python: 3.9.7

Important Note:
Make sure you have modules such as: aiohttp, aiofiles, BeautifulSoup4(bs4).
Also check your python version,you should use Python 3.9.7 (not sure if its working on other version).
You should not change anything here not related to @func_timer or url!
Also You should not change mail_context.txt which is template related to this project. 

Description: 
This is the main.py file. This program takes workers from AGH cathedral and scarps data about them,
then it creates a mail template and saves it into maile folder. The program can not get email addresses,
because agh page request javascript (I don't know why) so you have to do it by your self.
But I pass the URL address to the top of .txt file so you can do it easily.

Another important note:
Some workers do not have "doktor" or "profesor" title etc. then you should
manually replace ... in a file with their name/title. Also always checks title and gender.
I am not sure if all mails are written correctly, so i do not take any responsibilities for 
wrong written emails.

Edit info:
Change @func_timer mode to False to turn of timer.
Comment input, and paste your own url to skip input function

How to run:
1) First read everything above.
2) pass "python3 main.py" to cmd or run this program from editor ex. pycharm

Error codes:
001 - Problem with internet connection.
002 - Problem with url, probably url is not defined.
003 - Provided wrong url.
004 - Mail template is not in cwd. Paste it in with correct name.
'''


@func_timer(mode=True)
def main():
    # Here you can pass your own url
    url = 'https://skos.agh.edu.pl/jednostka/akademia-gorniczo-hutnicza-im-stanislawa-staszica-w-krakowie' \
          '/wydzial-elektrotechniki-automatyki-informatyki-i-inzynierii-biomedycznej' \
          '/katedra-elektrotechniki-i-elektroenergetyki-108.html'
    print('0 % - Started process execution')
    # Comment/Uncomment this line to skip input function/to run input function
    # url = input("Pass url to cathedral workers (skos only!): ")
    print('7 % - Making HTTP request to get persons list')
    try:
        list_of_persons = asyncio.run(http_request_first_page(url))
    except aiohttp.ClientConnectorError:
        print('Can not connect to the internet, check your connection before restart!')
        exit('Exit with error code: 001')
    except NameError:
        print('Provide url to url variable or to input function. Check description for more')
        exit('Exit with error code: 002')
    except aiohttp.InvalidURL:
        print('Provided wrong url. Check url variable or input before restart')
        exit('Exit with error code: 003')
    print('31 % - Got person list, passing it to async request function')
    try:
        http_response = asyncio.run(http_req(list_of_persons))
    except aiohttp.ClientConnectorError:
        print('Can not connect to the internet, check your connection before restart!')
        exit('Exit with error code: 001')
    print('49 % - Finished HTTP request, got all files without problems, passing to scrap function')
    better_info = scrap_person_info(http_response, list_of_persons)
    print('79 % - Starting last stage - file write')
    try:
        asyncio.run(save(better_info))
    except FileNotFoundError:
        print('Template file not found!')
        exit('Exit with error code: 004')
    print('100 % - Everything done, file saved to "maile" folder')


if __name__ == '__main__':
    main()
