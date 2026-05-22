# handlers-search.py
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.youtube import search_tracks
from utils.messages import NOT_FOUND, SHORT_QUERY, API_ERROR

router = Router()

@router.message(lambda msg: msg.text and not msg.text.startswith("/") and not msg.text.startswith("🎵") and not msg.text.startswith("🎲") and not msg.text.startswith("ℹ️"))
async def search_handler(message: types.Message):
    query = message.text.strip()

    if len(query) < 2:
        await message.answer(SHORT_QUERY)
        return

    try:
        results = search_tracks(query)
    except Exception:
        await message.answer(API_ERROR)
        return

    if not results:
        await message.answer(NOT_FOUND)
        return

    buttons = []
    for track in results:
        title = track["title"][:50]
        buttons.append([
            InlineKeyboardButton(
                text=f"{title} — {track['channel']}",
                callback_data=f"dl_{track['id']}"
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Вот что я нашёл:", reply_markup=keyboard)
