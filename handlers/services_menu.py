from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.services_api import list_services

router = Router()

PAGE_SIZE = 8

class BookForm(StatesGroup):
    selecting_service = State()
    waiting_for_date = State()
    waiting_for_time = State()

def fmt_service_line(name: str, price: float | None, duration: int | None) -> str:
    tail = []
    if price is not None:
        tail.append(f"{int(price) if price.is_integer() else price}₽")
    if duration:
        tail.append(f"{duration} мин")
    return f"{name}" + (f" • {' · '.join(tail)}" if tail else "")

def build_services_kb(items, page: int, total: int):
    kb = InlineKeyboardBuilder()
    for svc in items:
        text = fmt_service_line(svc.name, svc.price, svc.duration_minutes)
        # короткий callback, чтобы не выйти за лимит
        kb.button(text=text, callback_data=f"svc:{svc.id}")
    kb.adjust(1)

    # пагинация
    pages = (total + PAGE_SIZE - 1) // PAGE_SIZE
    nav_row = []
    if page > 1:
        nav_row.append(("« Prev", f"pg:{page-1}"))
    if page < pages:
        nav_row.append(("Next »", f"pg:{page+1}"))

    if nav_row:
        kb.row(*[{"text": t, "callback_data": d} for t, d in nav_row])

    kb.row({"text": "Cancel", "callback_data": "svc_cancel"})
    return kb.as_markup()

@router.message(Command("book"))
async def book_start(message: Message, state: FSMContext):
    await state.set_state(BookForm.selecting_service)
    page = 1
    page_data = await list_services(page=page, size=PAGE_SIZE, active=True)
    await message.answer(
        "Выберите услугу:",
        reply_markup=build_services_kb(page_data.items, page_data.page, page_data.total)
    )

@router.callback_query(F.data.startswith("pg:"))
async def services_page(cb: CallbackQuery, state: FSMContext):
    if await state.get_state() != BookForm.selecting_service:
        await cb.answer()
        return
    page = int(cb.data.split(":")[1])
    page_data = await list_services(page=page, size=PAGE_SIZE, active=True)
    await cb.message.edit_text(
        "Выберите услугу:",
        reply_markup=build_services_kb(page_data.items, page_data.page, page_data.total)
    )
    await cb.answer()

@router.callback_query(F.data.startswith("svc:"))
async def service_selected(cb: CallbackQuery, state: FSMContext):
    if await state.get_state() != BookForm.selecting_service:
        await cb.answer()
        return
    service_id = int(cb.data.split(":")[1])
    # сохраняем выбранную услугу в FSM
    await state.update_data(service_id=service_id)
    await cb.answer("Услуга выбрана")

    # Переходим к следующему шагу — спросим дату
    await state.set_state(BookForm.waiting_for_date)
    await cb.message.edit_text("Когда хотите записаться? Укажите дату в формате ДД.ММ (например, 25.10).")

@router.callback_query(F.data == "svc_cancel")
async def service_cancel(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.edit_text("Ок, отменил выбор услуги.")
    await cb.answer()
