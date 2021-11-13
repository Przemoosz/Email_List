import asyncio
import aiohttp
from asyncfunctions import (http_req,
                            http_request_first_page,
                            save)
from functions import mp_scrap
from decorators import func_timer
import multiprocessing

'''
Creator: Przemysław Szewczak
Version: Beta 1.1.1 - Multiprocessing support
Creation date: 16.10.2021
Update date: 11.11.2021
Python: 3.9.7
Recommended: No

===Beta Version Info===
This is beta version of program to scrap info about cathedral workers from agh. In this version I added
multiprocessing support to "speed up" program. As you can see program is not working much faster. But why?
Creating processes is a difficult and time-consuming task. For this amount od data, creating 8 process
(For my CPU) takes more time than scraping this info using one process with one thread. There is a chance
to speed up this program if the amount of data is large ex. 1 million html files to scrap,
this program using parallelism will finish tasks much faster than one process program,
even if we include time for creating process. I created this version to show that there is possibility 
to use multiprocessing to reduce CPU bound, but its not effective with this amount of data.
 
Multiprocessing version with 8 process - 13.44065390 secs
Multiprocessing version with 4 process - 9.02717290 secs
Single process version - 3.16778750 secs
That's why this version is not recommended! You can change amount of process in multiprocessing_management
function in "cpu_numbers" variable
Use single process version instead!

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
005 - Can not close process. Executed terminate method.
'''


def multiprocessing_management(http_response, url_lists):
    print('45 % - Getting information about CPU, and splitting tasks between logic processors')
    # Number of logic processors
    cpu_numbers = multiprocessing.cpu_count()
    # Type number of cpu to see the time to execute program on different amount of process
    # cpu_numbers = 4
    # Amount of html files to scrap per cpu
    tasks_per_cpu = (len(http_response) // cpu_numbers)
    # Task for one cpu
    task_cpu = []
    task_url_cpu = []
    # List with lists of tasks per each cpu - html files and url connected to this html
    list_of_html_per_cpu = []
    list_of_urls_per_cpu = []
    i = 0
    # Algorithm that splits files to scrap between each of logic processors
    for x, y in zip(http_response, url_lists):
        task_url_cpu.append(y)
        task_cpu.append(x)
        if len(task_cpu) == tasks_per_cpu and len(list_of_html_per_cpu) != cpu_numbers:
            list_of_html_per_cpu.append(task_cpu)
            list_of_urls_per_cpu.append(task_url_cpu)
            task_cpu = []
            task_url_cpu = []
        # If all cpu got equal amount of task and there are some task not connected to any of Logic cpu,
        # this lines add them to first processors then to second processors etc.
        if len(list_of_html_per_cpu) == cpu_numbers and len(list_of_html_per_cpu[-1]) == tasks_per_cpu:
            list_of_html_per_cpu[i].append(x)
            list_of_urls_per_cpu[i].append(y)
            i += 1
    # Part of a function where process is created, then started, and then closed after
    # returning list
    process_list = []
    queue_results = multiprocessing.Queue()
    barrier = multiprocessing.Barrier(len(list_of_html_per_cpu))
    print('51 % - Creating process')
    for i in range(len(list_of_html_per_cpu)):
        process_list.append(multiprocessing.Process(target=mp_scrap,
                                                    args=(list_of_html_per_cpu[i],
                                                          list_of_urls_per_cpu[i],
                                                          barrier,
                                                          queue_results)))
    print(f'57 % - Starting {cpu_numbers} process')
    [process.start() for process in process_list]
    print(f'59 % - All {cpu_numbers} process started')
    return_list = []
    for _ in range(len(list_of_html_per_cpu)):
        return_list += queue_results.get()
    print('61 % - Getting information back from queue object')
    [process.join() for process in process_list]
    print(f'63 % - Each process performed correctly, start closing method')
    process_list[-1].join()
    [process.close() for process in process_list]
    print(f'65 % - Closed all processes')

    if len(multiprocessing.active_children()) != 0:
        [process.terminate() for process in process_list]
        exit(exit('Exit with error code: 005'))
    print('69 % - Got information from queue, prepared return list - passing to async save function')
    return return_list


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
    http_response = asyncio.run(http_req(list_of_persons))
    print('49 % - Finished HTTP request, got all files without problems, passing to scrap function')
    better_info = multiprocessing_management(http_response, list_of_persons)
    print('79 % - Starting last stage - file write')
    try:
        asyncio.run(save(better_info))
        pass
    except FileNotFoundError:
        print('Template file not found!')
        exit('Exit with error code: 004')
    print('100 % - Everything done, file saved to "maile" folder')


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
