import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from pydantic import ValidationError
from settings import settings
from schemes.schemes import UserParams  # Import the Pydantic model

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher with in-memory storage
bot = Bot(token=settings.api_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Dynamically create states from UserParams fields
class UserData(StatesGroup):
    for field in UserParams.__fields__:
        locals()[field] = State()

# Start command handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome! I am your Nutro Bot. Let's collect some data to generate your menu. Please enter your gender (e.g., male or female):")
    logger.info(f"{message=}")
    await UserData.gender.set()

# Gender handler
@dp.message_handler(state=UserData.gender)
async def process_gender(message: types.Message, state: FSMContext):
    logger.info(f"{message=}")
    try:
        await state.update_data(gender=message.text)
        await message.reply("Enter your weight (in kg):")
        await UserData.weight.set()
    except ValidationError as e:
        await message.reply(f"Invalid input: {e.errors()[0]['msg']}")

# Weight handler
@dp.message_handler(state=UserData.weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        await state.update_data(weight=weight)
        await message.reply("Enter your age (in years):")
        await UserData.age.set()
    except (ValueError, ValidationError) as e:
        await message.reply("Please enter a valid number for weight.")

# Age handler
@dp.message_handler(state=UserData.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await message.reply("Enter your activity level (e.g., low, moderate, high):")
        await UserData.activity.set()
    except (ValueError, ValidationError) as e:
        await message.reply("Please enter a valid number for age.")

# Activity handler
@dp.message_handler(state=UserData.activity)
async def process_activity(message: types.Message, state: FSMContext):
    await state.update_data(activity=message.text)
    await message.reply("Enter the complexity of the menu (e.g., easy, medium, hard):")
    await UserData.complexity.set()

# Complexity handler
@dp.message_handler(state=UserData.complexity)
async def process_complexity(message: types.Message, state: FSMContext):
    await state.update_data(complexity=message.text)
    await message.reply("Enter the number of days for the menu (e.g., 7):")
    await UserData.period.set()

# Period handler
@dp.message_handler(state=UserData.period)
async def process_period(message: types.Message, state: FSMContext):
    try:
        period = int(message.text)
        await state.update_data(period=period)
        await message.reply("Enter the number of portions per meal (e.g., 2):")
        await UserData.portions.set()
    except (ValueError, ValidationError) as e:
        await message.reply("Please enter a valid number for the period.")

# Portions handler
@dp.message_handler(state=UserData.portions)
async def process_portions(message: types.Message, state: FSMContext):
    try:
        portions = int(message.text)
        # user_data = {"portions": portions}
        # UserParams(**user_data)  # Validate portions
        await state.update_data(portions=portions)

        # Retrieve all user data
        user_data = await state.get_data()

        # Validate all collected data
        try:
            validated_data = UserParams(**user_data)
            # Display collected data
            await message.reply(
                f"Thank you! Here is the data you provided:\n"
                f"Gender: {validated_data.gender}\n"
                f"Weight: {validated_data.weight} kg\n"
                f"Age: {validated_data.age} years\n"
                f"Activity: {validated_data.activity}\n"
                f"Complexity: {validated_data.complexity}\n"
                f"Period: {validated_data.period} days\n"
                f"Portions: {validated_data.portions} per meal\n"
            )
        except ValidationError as e:
            await message.reply(f"Validation error: {e.json()}")

        # Finish the conversation
        await state.finish()
    except (ValueError, ValidationError) as e:
        await message.reply("Please enter a valid number for portions.")

# Cancel handler
@dp.message_handler(commands=['cancel'], state='*')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Data collection has been canceled.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    logger.info("Bot successfully started")