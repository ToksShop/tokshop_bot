import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import asyncio

API_TOKEN = os.getenv("BOT_TOKEN")  # Токен з environment

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# --- Кнопки ---
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Каталог"), KeyboardButton(text="🛒 Зробити замовлення")],
        [KeyboardButton(text="🚚 Доставка та оплата"), KeyboardButton(text="📞 Зв’язатися")]
    ],
    resize_keyboard=True
)

# --- Стан машини ---
class OrderForm(StatesGroup):
    name = State()
    contact = State()
    product = State()
    city = State()
    branch = State()
    payment = State()

@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.answer("Вітаємо в ТОКShop 🔌\nОбери дію з меню 👇", reply_markup=main_menu)

@dp.message(F.text == "📦 Каталог")
async def catalog(message: types.Message):
    await message.answer("Каталог товарів незабаром буде доступний онлайн.\nПоки що пиши назви вручну 🧾")

@dp.message(F.text == "🚚 Доставка та оплата")
async def delivery(message: types.Message):
    await message.answer(
        "🚚 *Доставка:*\n• Нова Пошта\n• Укрпошта\n• Кур'єр (за домовленістю)\n\n"
        "💳 *Оплата:*\n• Накладений платіж\n• Передоплата",
        parse_mode="Markdown"
    )

@dp.message(F.text == "📞 Зв’язатися")
async def contact(message: types.Message):
    await message.answer("Пиши нам напряму 👉 @AkulaBost")

@dp.message(F.text == "🛒 Зробити замовлення")
async def order_start(message: types.Message, state: FSMContext):
    await message.answer("Введи своє ім’я:")
    await state.set_state(OrderForm.name)

@dp.message(OrderForm.name)
async def order_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введи номер телефону або @username:")
    await state.set_state(OrderForm.contact)

@dp.message(OrderForm.contact)
async def order_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer("Що бажаєш замовити?")
    await state.set_state(OrderForm.product)

@dp.message(OrderForm.product)
async def order_product(message: types.Message, state: FSMContext):
    await state.update_data(product=message.text)
    await message.answer("Введи своє місто:")
    await state.set_state(OrderForm.city)

@dp.message(OrderForm.city)
async def order_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Номер відділення Нової Пошти:")
    await state.set_state(OrderForm.branch)

@dp.message(OrderForm.branch)
async def order_branch(message: types.Message, state: FSMContext):
    await state.update_data(branch=message.text)
    await message.answer("Тип оплати (накладений/передоплата):")
    await state.set_state(OrderForm.payment)

@dp.message(OrderForm.payment)
async def order_payment(message: types.Message, state: FSMContext):
    await state.update_data(payment=message.text)
    data = await state.get_data()

    order_summary = (
        f"🆕 *Нове замовлення:*\n"
        f"👤 Ім’я: {data['name']}\n"
        f"📞 Контакт: {data['contact']}\n"
        f"📦 Товар: {data['product']}\n"
        f"🏙 Місто: {data['city']}\n"
        f"📍 Відділення: {data['branch']}\n"
        f"💳 Оплата: {data['payment']}"
    )

    await bot.send_message(chat_id=message.chat.id, text="Дякуємо! Замовлення прийнято ✅")
    await bot.send_message(chat_id=2014204053, text=order_summary, parse_mode="Markdown")
    await state.clear()

async def main():
    print("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
