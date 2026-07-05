from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
    )
from forms.user import Form
from aiogram.fsm.context import FSMContext
import aiohttp
import aiosqlite
import asyncio

router = Router()


subscribers = set()

async def notifier(bot: Bot):
    while True:
        if subscribers:
            for user_id in list(subscribers):
                try:
                    await bot.send_message(user_id, "Ваше уведомление")
                except Exception:
                    pass
        await asyncio.sleep(10)

@router.message(Command("start"))
async def start(message: Message):
    await message.answer('Привет!\nКоманда /reg и ваш возраст\n/subscribe\n/unsubscribe\n/subscribers')


@router.message(Command("subscribe"))
async def subscribe(message: Message):
    user_id = message.from_user.id

    subscribers.add(user_id)

    await message.answer("Вы подписались")


@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message):
    user_id = message.from_user.id

    subscribers.discard(user_id)

    await message.answer("Вы отписались")


@router.message(Command("subscribers"))
async def subscribers_cmd(message: Message):
    if not subscribers:
        await message.answer("Пусто")
        return
    
    text = "Подписчики\n"
    for uid in subscribers:
        text += f"{uid}\n"
    await message.answer(text)













# #--------


# DB_NAME="qwe.sql"

# #--------

# async def init_db():
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                          id INTEGER PRIMARY KEY,
#                          full_name TEXT,
#                          age INTEGER
#                          )                        
#                          """)
#         await db.commit()

# async def add_user(full_name,age):
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute("INSERT INTO users (full_name, age) VALUES(?,?)",(full_name,age))
#         await db.commit()

# async def get_users():
#     async with aiosqlite.connect(DB_NAME) as db:
#         cursor = await db.execute("SELECT full_name, age FROM users")
#         result = await cursor.fetchall()
#         return result


# #  -------

# @router.message(Command("start"))
# async def start(message: Message):
#     await init_db()
#     await message.answer('Привет!\nКоманда /reg и ваш возраст')

# @router.message(Command("reg"))
# async def reg(message: Message):
#     parts = message.text.strip().split()

#     if len(parts) != 2 or not parts[1].isdigit():
#         await message.answer("Введи команду верно")
#         return
    
#     await add_user(message.from_user.full_name, int(parts[1]))

#     await message.answer('Молодец')

# @router.message(Command("users"))
# async def users(message: Message):
#     users = await get_users()

#     if not users:
#         await message.answer("В базе нет пользователей")
#         return
#     text = "Пользователи есть\n\n"
#     for full_name, age in users:
#         text += f'- {full_name} - <code>{age}</code>\n'

#     await message.answer(text, parse_mode='HTML')


# async def get_product(product_id):
#     url = f"https://fakestoreapi.com/products/{product_id}"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             if resp.status == 404:
#                 return None
#             if resp.status != 200:  
#                 raise Exception(f"API вернул статус {resp.status}")
#             data = await resp.json()
#             return data 
# #  -------



# @router.message(Command("start"))
# async def start(message: Message):
#     await message.answer('Привет!')
 
# @router.message(Command("product"))
# async def get_product_cmd(message: Message):
#     parts = message.text.split()

#     if len(parts) != 2:
#         await message.answer('Используй /product 1')
#         return
    
#     product_id = parts[1]
#     if not product_id.isdigit():
#         await message.answer('ID товара - число')
#         return

#     await message.answer(f'Ищу товар с id {product_id}')

#     try:
#         product = await get_product(int(product_id))
#     except Exception as e:
#         print(f"ОШИБКА: {e}")
#         await message.answer(f'Не удалось\n{product_id}')
#         return

#     if product is None:
#         await message.answer('Товара нет')
#         return

#     title = product.get('title', "Без названия")
#     price = product.get('price', "Без цены")
#     description = product.get('description', "Без описания")
#     category = product.get('category', "Без категории")
#     image = product.get('image',)

#     text = (
#         f"<b>{title}</b>\n\n"
#         f"Цена: <i>{price}</i>\n"
#         f"Описание: <b>{description}</b>\n"
#         f"Категория: <b>{category}</b>"
#     )    

#     photo = FSInputFile("images.jpg")
#     await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")




#1111111111111111111111111111111111111111111111111111
# from aiogram import Router
# from aiogram.filters import Command
# from aiogram.types import Message
# import aiohttp
# import asyncio
# import sys

# router = Router()

# async def get_product(product_id):
#     """Получает товар из FakeStoreAPI"""
#     url = f"https://fakestoreapi.com/products/{product_id}"
    
#     try:
#         timeout = aiohttp.ClientTimeout(total=10)
#         async with aiohttp.ClientSession(timeout=timeout) as session:
#             async with session.get(url) as resp:
#                 if resp.status == 404:
#                     return None
#                 if resp.status != 200:
#                     print(f"⚠️ Статус {resp.status} для ID {product_id}")
#                     return None
                
#                 data = await resp.json()
#                 return data
                
#     except asyncio.TimeoutError:
#         print(f"⏱️ Таймаут для ID {product_id}")
#         return None
#     except aiohttp.ClientError as e:
#         print(f"🔌 Ошибка соединения: {e}")
#         return None
#     except Exception as e:
#         print(f"💥 Неизвестная ошибка: {e}")
#         return None

# @router.message(Command("product"))
# async def get_product_cmd(message: Message):
#     print(f"📩 Команда: {message.text}")  # Логируем
    
#     # Разбираем команду
#     parts = message.text.split()
    
#     if len(parts) != 2:
#         await message.answer('❌ Используй: /product 1')
#         return
    
#     product_id_str = parts[1]
    
#     if not product_id_str.isdigit():
#         await message.answer('❌ ID должен быть числом')
#         return
    
#     product_id = int(product_id_str)
    
#     # FakeStoreAPI: ID от 1 до 20
#     if product_id < 1 or product_id > 20:
#         await message.answer('❌ ID должен быть от 1 до 20')
#         return
    
#     await message.answer(f'🔍 Ищу товар с ID {product_id}...')
    
#     # Получаем товар
#     product = await get_product(product_id)
    
#     if product is None:
#         await message.answer(f'❌ Товар с ID {product_id} не найден')
#         return
    
#     # Формируем ответ
#     title = product.get('title', 'Без названия')
#     price = product.get('price', 0)
#     description = product.get('description', 'Без описания')
#     category = product.get('category', 'Без категории')
#     image = product.get('image')
    
#     text = (
#         f"<b>{title}</b>\n\n"
#         f"💰 Цена: <i>${price}</i>\n"
#         f"📝 Описание: {description[:200]}...\n"
#         f"📂 Категория: {category}"
#     )
    
#     # Отправляем с фото или без
#     if image:
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(image) as resp:
#                     if resp.status == 200:
#                         image_data = await resp.read()
#                         await message.answer_photo(
#                             photo=image_data,
#                             caption=text,
#                             parse_mode="HTML"
#                         )
#                     else:
#                         await message.answer(text, parse_mode="HTML")
#         except Exception as e:
#             print(f"Ошибка при загрузке фото: {e}")
#             await message.answer(text, parse_mode="HTML")
#     else:
#         await message.answer(text, parse_mode="HTML")
    
#     print(f"✅ Товар {product_id} отправлен")  # Логируем успех
#1111111111111111111111111111111111111111111111111111



#00000000000000000000000000000000000000000000000000

# from aiogram import Router, F, Bot
# from aiogram.filters import Command
# from aiogram.types import (
#     Message,
#     CallbackQuery,
#     ReplyKeyboardMarkup,
#     KeyboardButton,
#     InlineKeyboardMarkup,
#     InlineKeyboardButton,
#     FSInputFile
#     )
# from forms.user import Form
# from aiogram.fsm.context import FSMContext
# import aiohttp

# router = Router()

# #  -------
 
# async def get_product(product_id):
#     url = f"https://fakestoreapi.com/products/{product_id}"
#     async with aiohttp.ClientSession as session:
#         async with session.get(url) as resp:
#             if resp.status == 404:
#                 return None

#             data = await resp.json()
#             return data 
# #  -------



# @router.message(Command("start"))
# async def start(message: Message):
#     await message.answer('Привет!')
 
# @router.message(Command("product"))
# async def get_product_cmd(message: Message):
#     parts = message.text.split()

#     if len(parts) != 2:
#         await message.answer('Используй /product 1')
#         return
    
#     product_id = parts[1]
#     if not product_id.isdigit():
#         await message.answer('ID товара - число')
#         return

#     await message.answer(f'Ищу товар с id {product_id}')

#     try:
#         product = await get_product(int(product_id))
#     except Exception:
#         await message.answer(f'Не удалось\n{product_id}')
#         return

#     if product is None:
#         await message.answer('Товара нет')
#         return

#     title = product.get('title', "Без названия")
#     price = product.get('price', "Без цены")
#     description = product.get('description', "Без описания")
#     category = product.get('category', "Без категории")
#     image = product.get('image',)

#     text = (
#         f"<b>{title}</b>\n\n"
#         f"Цена: <i>{price}</i>\n"
#         f"Описание: <b>{description}</b>\n"
#         f"Категория: <b>{category}</b>"
#     )    

#     photo = FSInputFile("images.jpg")
#     await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")

#0000000000000000000000000000000000000000000000000




    # if image:
    #     await message.answer_photo(photo=image, caption=text, parse_mode="HTML")
    # else:
    #     await message.answer(text, parse_mode="HTML")


# @router.message(Command('cancel'))
# async def cancel_form(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer('Иди нахуй')



# @router.message(Form.name, F.text)
# async def process_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
  
#     await message.answer('Отлично\n Теперь напиши свой возраст')
#     await state.set_state(Form.age)


# @router.message(Form.age, F.text)
# async def process_age(message: Message, state: FSMContext):
#     if not message.text.isdigit():
#         await message.answer("Возраст должен быть числом")
#         return
    
#     if 1 < int(message.text) > 100:
#         await message.answer("Введите другой актуальный сука возраст, падаль блять")
#         return


#     await state.update_data(age=int(message.text))
  
#     await message.answer('Отлично\n Теперь ваш Email')
#     await state.set_state(Form.email)

# @router.message(Form.email, F.text)
# async def process_email(message: Message, state: FSMContext):
#     email_text = message.text
#     if "@" not in email_text or "." not in email_text:
#         await message.answer("Уебан, нормально пиши")
#         return
    
#     await state.update_data(email=email_text)
  
#     data = await state.get_data()
#     name = data["name"]
#     age = data["age"]
#     email = data["email"]


#     await message.answer(
#         f'Бля буду красавчик\nИмя: {name}\nВозраст: {age}\nПочта: {email}'
#         )
#     await state.clear()


# @router.message(F.photo)
# async def proccess_photo(message: Message):
#     photo = message.photo[-1]
#     file_id = photo.file_id
 
#     await message.answer(
#         f"Вы отправили фото, ну крутой пиздец\nИди нахуй теперь <code>{file_id}</code>",
#         parse_mode="HTML"                 
#     )
#     await message.answer_photo(file_id, caption='Съебался в страхе')

    
# @router.message(F.video)
# async def proccess_video(message: Message):
#     video = message.video
#     file_id = video.file_id
#     duration = video.duration
#     duration_minutes = duration // 60
#     duration_seconds = duration % 60

#     if duration_minutes > 0:
#         time = f"{duration_minutes} мин. {duration_seconds} сек."
#     else:
#         time = f"{duration_seconds} сек."
    
#     await message.answer(
#         f"Вы отправили видео, ну крутой пиздец\n"
#         f"Длительность твоего поноса: {time} в будущем\n"
#         f"Иди нахуй теперь <code>{file_id}</code>",
#         parse_mode="HTML"                 
#     )
#     await message.answer_video(file_id, caption='Съебался в страхе')


# @router.message(F.animation)
# async def proccess_animation(message: Message):
#     animation = message.animation
 
#     await message.answer(
#         f"Вы отправили анимацию, ну крутой пиздец\n"
#         f"Длительность твоего поноса: {animation} в будущем\n"
#         f"Иди нахуй теперь <code>{animation.file_id}</code>",
#         parse_mode="HTML"                 
#     )
#     await message.answer_video(animation.file_id, caption='Съебался в страхе')

# @router.message(F.document)
# async def proccess_document(message: Message, bot: Bot):
#     document = message.document
#     file_id = document.file_id

#     file = await bot.get_file(file_id)
#     file_path = file.file_path

#     local_path = f'downloads/{document.file_name}'

#     await bot.download_file(file_path=file_path, destination=local_path)

#     await message.answer('Файл сохранен')


# @router.message(Command("file"))
# async def send_file(message: Message):
#     file = FSInputFile('files/example.txt')

#     await message.answer_document(file)











#####################################################

# def get_main_reply_keyboard():
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text=('О боте'))], [KeyboardButton(text=('Съебался в страхе'))],
#             [KeyboardButton(text=('Старт'))],[KeyboardButton(text=('Помощь'))]
#         ],
#         resize_keyboard=True
#     )
#     return keyboard


# def get_main_inline_keyboard():
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text='Открыть сайт', url="https://tarotap.com/ru")],
#             [InlineKeyboardButton(text='Подробнее', callback_data='info_more')]
            
#         ]
#     )

#     return keyboard


# @router.callback_query(lambda c: c.data == 'info_more')
# async def proccess_more_info(callback: CallbackQuery):
#      await callback.message.answer('Вот и иди нахуй')
#      await callback.answer



# @router.message(Command('start'))
# @router.message(F.text.lower() == 'старт')
# async def start(message: Message ):
#     await message.answer(
#         'Расскажу тебе за весь твой *кучерявый базар*, сейчас тусанем карты и _наебанем_ расклад на таро\n\nЕсли вопросы по всей этой мурзилке будут, пиши /help',
#         parse_mode='Markdown')
    


# @router.message(Command('help'))
# async def help(message: Message ):
#     await message.answer(
#         'Команды:\n/start - <b>Запустить</b>\n/help - <i>список</i> <a href="https://tarotap.com">команд</a>\n/about - про меня',
#         parse_mode='HTML',
#         reply_markup = get_main_reply_keyboard())
    

# @router.message(Command('about'))
# async def hello(message: Message ):
#     await message.answer(f'Расскажу про себя {message.from_user.first_name}', reply_markup=get_main_inline_keyboard())

# @router.message()
# async def hello(message: Message ):
#     await message.answer('Лол')