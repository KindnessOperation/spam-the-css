import aiohttp
import asyncio
import csv
import logging
import sys
import random
import string

basic_config = logging.basicConfig(filename="logs/bot.log", 
    level=logging.INFO,
    format="%(name)s - %(asctime)s-%(levelname)s:%(message)s", 
    datefmt="%X")

console = logging.StreamHandler(stream=sys.stdout) # sys.stderr
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

logger = logging.getLogger(__name__)

async def task(response: str):
    logger.info("Sending \'%s\' to Google Form" % response)
    async with aiohttp.ClientSession() as sess:
        data = {
            'entry.1189518362': response,
        }
        if (random.randint(1, 2) == 1):
            data['entry.1792022938'] = 'Option 1'
        await sess.post('https://docs.google.com/forms/u/0/d/e/1FAIpQLSeM6U79oB-Axf7nmQQRAEJB75nktwmCBIaYbygYaOI3pGt8ww/formResponse', data=data)

async def main():
    lines = []
    with open('data.csv', 'r', encoding='utf-8') as f:  # Blocking ! But negligible & only at startup
        reader = csv.DictReader(f)
        for row in reader:
            if (row['Kind'] == '1'):
                lines.append(row['Response'])
    
    while True:
        random.shuffle(lines)
        for response in lines:
            await task(response)
            sleeptime = random.randint(60, 60*10)
            await asyncio.sleep(sleeptime)
        logger.info("Cycling & Shuffling Responses...")

async def spam(tasks_num: int):
    def get_random_str(a):
        return "".join([random.choice(string.ascii_letters + string.digits) for i in range(a)])

    tasks = []
    for i in range(tasks_num):
        tasks.append(task(get_random_str(random.randint(1, 100))))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    # asyncio.run(task("HAI"))
    # asyncio.run(main())
    asyncio.run(spam(1000))