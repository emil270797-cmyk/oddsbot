from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup,
                           InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton)
from . import formatting as fmt

router = Router()

MAIN_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Сегодня"), KeyboardButton(text="Лайв")],
              [KeyboardButton(text="Таблица")]],
    resize_keyboard=True)


def matches_kb(matches):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=fmt.match_title(m), callback_data=f"m:{m.id}")] for m in matches])


@router.message(CommandStart())
async def start(msg: Message):
    await msg.answer("Футбол: линия, лайв, коэффициенты, прогрузы, составы, события.",
                     reply_markup=MAIN_KB)


async def _list(msg: Message, providers, live: bool):
    ms = await providers.matches.list_matches(live=live)
    if not ms:
        await msg.answer("Матчей нет.")
        return
    await msg.answer("Лайв:" if live else "Сегодня:", reply_markup=matches_kb(ms))


@router.message(F.text == "Сегодня")
async def today(msg: Message, providers):
    await _list(msg, providers, live=False)


@router.message(F.text == "Лайв")
async def live(msg: Message, providers):
    await _list(msg, providers, live=True)


@router.message(F.text == "Таблица")
async def table(msg: Message, providers):
    rows = await providers.matches.get_standings("default")
    await msg.answer(fmt.table(rows), parse_mode="HTML")


@router.callback_query(F.data.startswith("m:"))
async def match_card(cb: CallbackQuery, providers, db):
    mid = cb.data[2:]
    m = await providers.matches.get_match(mid)
    if not m:
        await cb.answer("Матч не найден", show_alert=True)
        return
    odds = await providers.odds.get_odds(mid)
    flow = await providers.moneyflow.get_moneyflow(mid)
    events = await providers.matches.get_events(mid)
    lineups = await providers.matches.get_lineups(mid)
    if odds:
        db.save_odds(odds)
    if flow:
        db.save_flow(flow)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔄 Обновить", callback_data=f"m:{mid}")]])
    await cb.message.edit_text(fmt.match_card(m, odds, flow, events, lineups),
                               parse_mode="HTML", reply_markup=kb)
    await cb.answer()
