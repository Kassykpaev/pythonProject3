from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher


class CustomState(State):
    async def set(self , user=None):
        """Option to set state for concrete user"""
        state = Dispatcher.get_current().current_state(user=user)
        await state.set_state(self.state)


class BlankOrder(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_phone_number = State()
    waiting_for_lottery = State()
    waiting_for_video = State()
    waiting_for_grade = CustomState()
