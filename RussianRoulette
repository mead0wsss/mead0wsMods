__version__ = (1, 0, 0)

# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods

# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @mead0wssMods

from telethon.tl.functions.channels import LeaveChannelRequest
import asyncio
import random
from .. import loader, utils

@loader.tds
class RouletteMod(loader.Module):
    """Модуль для игры в Русскую рулетку. При поражении выкидывает с чата."""
    strings = {"name": "Roulette"}

    async def roulettecmd(self, message):
        """Начать игру в Русскую рулетку"""
        await message.edit('😶🔫 Прикладываю пистолет к виску и медленно нажимаю курок...')
        await asyncio.sleep(2)
        
        choice = random.choice([1, 2])
        if choice == 1:
            await message.edit('😵 Смерть... Всем пока!')
            await message.client(LeaveChannelRequest(message.chat_id))
        else:
            await message.edit('😄 Выжил! Остаюсь в чате.')
