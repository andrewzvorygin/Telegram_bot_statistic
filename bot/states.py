from aiogram.dispatcher.filters.state import StatesGroup, State


class Statistic(StatesGroup):
    UserCountChange = State()
    NumberViewsRecord = State()
    ChoiceChannel = State()