# Email List
This program takes workers from AGH cathedral and scarps data about them,
then it creates a mail template and saves it into "maile" folder. The program can not get email addresses,
because agh page requests javascript (I don't know why) so you have to do it by yourself. There are two versions available:

Final Version - using only asyncio

Multiprocessing Beta version - using asyncio with multiprocessing unit 

## Installation and usage

Make sure you have installed python 3.9.2

Download final or multiprocessing version

Install required libraries - aiohttp, BeautifulSoup4(bs4), aiofiles

```bash
pip install aiohttp
pip install aiofiles
pip install BeautifulSoup
```
Run main.py program using IDE or cmd by typing
```bash
py main.py
```
## Note to multiprocessing version
In this version, I added
multiprocessing support to "speed up" the program. As you can see the program is not working much faster. But why?
Creating processes is a difficult and time-consuming task. For this amount of data, creating 8 process
(For my CPU) takes more time than scraping this info using one process with one thread. There is a chance
to speed up this program if the amount of data is large ex. 1 million HTML files to scrap,
this program using parallelism will finish tasks much faster than a single process program,
even if we include time for creating process. I created this version to show that there is the possibility 
to use multiprocessing to reduce CPU bound, but it's not effective with this amount of data.
 
Multiprocessing version with 8 processes - 13.44065390 secs

Multiprocessing version with 4 processes - 9.02717290 secs

Single process version - 3.16778750 secs

