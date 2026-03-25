import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()
CURRENCY = 'XTR'
CHANNEL_ID = 123

new_text = """Привелегии, которые вы получите при покупке доступа:

1. 📷 Эксклюзивный контент
2. ✉️ Безграничные и бесплатные сообщение в директ канала
3. ♾️ Бесконечный доступ в приватку

Цена: 40 звезд/навсегда
"""

from PrivatkaBot import bot
import app.keyboard as kb
from database_core.database import session_factory
from database_core.orm import insert_user, get_admins
from database_core.models import UsersOrm

ADMINS = get_admins()


class Register(StatesGroup):
    don = State()


@router.message(CommandStart())
async def cmd_main(message: Message):
    await message.reply(f"Привет, {message.from_user.first_name}! Это бот канала <a href='url'>name</a>. Бот исполняет продажу услуг.", parse_mode="HTML", disable_web_page_preview=True, 
                        reply_markup=kb.main)
    print(f"[LOGS] Введена команда /start. Пользователь: @{message.from_user.username}")
    if insert_user(f"@{message.from_user.username}"):
        print(f"[LOGS] Пользователь @{message.from_user.username} уже в БД")
    else:
        user = UsersOrm(username=f"@{message.from_user.username}")
        with session_factory() as session:
            session.add_all([user])
            session.commit()
        print(f"[SUCCESS] Пользователь @{message.from_user.username} успешно добавлен в БД")

@router.message(F.text == "Услуги")
async def cmd_privatka(message: Message):
    await message.reply("Выберите услугу:", reply_markup=kb.privatka)

@router.message(F.text == "Пользовательское соглашение")
async def cmd_privatka(message: Message):
    await message.answer("Покупая услуги, вы подтверждаете, что вам исполнилось 18 лет.")
    print(f"[LOGS] Введена команда 'Пользовательское соглашение'. Пользователь: @{message.from_user.username}")

@router.callback_query(F.data == 'privatka')
async def cmd_buy_privatka(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
    if chat_member.status in ['member', 'administrator', 'creator']:
        await callback.message.answer("Вы уже в канале!", show_alert=True)
        return
    else:
        await callback.message.edit_text(text=new_text, reply_markup=kb.privatka_end)

@router.callback_query(F.data == "back")
async def back_to_cmd(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Выберите услугу:", reply_markup=kb.privatka)

@router.callback_query(F.data == "privatka_end")
async def cmd_buy_priv_end(callback: CallbackQuery):
    await callback.answer("")
    prices = [LabeledPrice(label=CURRENCY, amount=40)]
    await callback.message.answer_invoice(
        title="Приватка",
        description="Доступ в приватку",
        prices=prices,
        provider_token="",
        payload="channel_private",
        currency=CURRENCY,
    )

@router.pre_checkout_query()
async def pre_check(pre_check: PreCheckoutQuery):
    await pre_check.answer(ok=True)

@router.callback_query(F.data == 'donate')
async def cmd_donate(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(Register.don)
    await callback.message.edit_text("""(Если хотите отменить действие, нажмите на кнопку "Отмена" под этим сообщением)
Введите сумму, которую хотите пожертвовать:""", reply_markup=kb.cancel)
    print(f"[LOGS] Введена команда donate.")

@router.callback_query(F.data == 'cancel', Register.don)
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Вы отменили действие.')
    print(f"[CANCEL] Отмена команды donate.")
    await callback.message.edit_text("Выберите услугу:", reply_markup=kb.privatka)

@router.message(Register.don)
async def cmd_don_donate(message: Message, state: FSMContext):
    try:
        await state.update_data(don=message.text)
        data = await state.get_data()
        prices = [LabeledPrice(label=CURRENCY, amount=data['don'])]
        await message.answer_invoice(
            title="Донат",
            description="Пожертвование на развитие проекта",
            prices=prices,
            provider_token="",
            payload="donate",
            currency=CURRENCY,
            )
        await state.clear()
    except Exception as e:
        await message.answer("Ввёден неправильный диапозон числа. Повторите попытку:")
        print(f"[CANCEL] Введен неверный диапозон числа для доната. Повтор попытки... (Пользователь: @{message.from_user.username})")

@router.pre_checkout_query()
async def pre_check(pre_check: PreCheckoutQuery):
    await pre_check.answer(ok=True)
    print(f"[INFO] Проверка подленности платежа...")

@router.message(F.successful_payment)
async def proc_suc_pay(message: Message):
    payload = message.successful_payment.invoice_payload

    if payload == 'donate':
        user_id = message.from_user.id
        try:
            await message.answer(f"✅🎉Огромное спасибо за донат! Мы запомним ваш подвиг на всю историю проекта. Большая вам благодарность!")
            print(f"[SUCCESS] Платеж для пользователя @{message.from_user.username} прошел успешно. Услуга 'Донат'")
            
        except Exception as e:
            print(f"[ERROR] Ошибка: {e}")
            await message.answer("Произошла ошибка.")
            print(f"[ERROR] У пользователя @{message.from_user.username} произошла ошибка при оплате.")
    
    elif payload == 'channel_private':
        user_id = message.from_user.id
        try:
            invite_link = await bot.create_chat_invite_link(
                chat_id=CHANNEL_ID,
                member_limit=1,
                creates_join_request=False
            )
            await message.answer(f"✅🎉Благодарим за покупку! Ваша ссылка: {invite_link.invite_link}")
            print(f"[SUCCESS] Платеж для пользователя @{message.from_user.username} прошел успешно. Услуга 'Приватка'")
            
        except Exception as e:
            print(f"[ERROR] Ошибка: {e}")
            await message.answer("Ошибка, обратитесь к админу", show_alert=True)
            print(f"[ERROR] У пользователя @{message.from_user.username} произошла ошибка при оплате.")
        
    else:
        print('error')


@router.message(F.text == "О боте")
async def cmd_about(message: Message):
    await message.answer("""Бот продает доступ в закрытый телеграмм канал, а также принимает пожертвования на развитие проекта.

Бот канала: name""", disable_web_page_preview=True)
    print(f"[LOGS] Введена команда 'О боте'. Пользователь: @{message.from_user.username}")