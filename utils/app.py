import requests
from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bs4 import BeautifulSoup
from selenium import webdriver

from notify_admins import on_startup_notify
from utils.config import ADMINS, BOT_TOKEN

user_id = ADMINS
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

topics_list = []
compete_link = []

# Topic name without first symbol #
button_text = []

# Dict witn topic name and link
stringList = {}

keyboard_inline = InlineKeyboardMarkup()


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    url = "https://uk.wikipedia.org/w/index.php?go=Перейти&search=" + message.text
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")

    if message.text.isalpha():
        await message.answer(text='Ваш запит обробляється, зачекайте 10 секунд')

    links = soup.find_all("div", class_="mw-search-result-heading")

    if len(links) > 0:
        url = "https://uk.wikipedia.org" + links[0].find("a")["href"]

    option = webdriver.ChromeOptions()
    option.add_argument('--headless=new')
    driver = webdriver.Chrome(options=option)
    driver.get(url)

    driver.execute_script("window.scrollTo(0, 170)")
    driver.save_screenshot("screenshot.png")
    driver.quit()

    photo = open("screenshot.png", 'rb')

    # General parsing of topics
    for link in soup.select('.toclevel-1'):
        url_more = link.find('a').get('href')
        topics_list.append(url_more)

    # Created clicable link after concatination 'url' + topic name
    for topic in topics_list:
        current_url = url + topic
        compete_link.append(current_url)

    # Removed # in topic name #Переваги => Переваги
    for counter, topic in enumerate(topics_list):
        global stringList
        topic = topic[1:]
        button_text.append(topic)
        stringList.update({topic: compete_link[counter]})

    # Added inline buttons
    for counter, inl_button in enumerate(button_text):
        but_on = InlineKeyboardButton(text=f"{inl_button}", url=compete_link[counter])
        keyboard_inline.add(but_on)

    await bot.send_photo(message.chat.id, photo=photo, caption=f'Посилання на статтю: <a href="{url}">натисни тут</a>',
                         parse_mode="HTML", reply_markup=keyboard_inline)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup_notify)
