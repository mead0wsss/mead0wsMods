# -- version --
__version__ = (1, 0, 0)
# -- version --


# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods


# meta developer: @mead0wssMods x @nullmod
# scope: heroku_only

from .. import loader, utils
from herokutl.tl.functions.payments import GetPaymentFormRequest, SendStarsFormRequest
from herokutl.tl.types import InputInvoiceStarGift, TextWithEntities
from herokutl.errors.rpcerrorlist import BadRequestError
import logging

@loader.tds
class SenderGifts(loader.Module):
    """Модуль для отправки подарков"""
    
    strings = {
        "name": "SenderGifts",
        "usage": "<emoji document_id=4958526153955476488>❌</emoji> Используйте в формате: <code>.sendgift @username текст</code>",
        "checking_user": "<emoji document_id=5206634672204829887>🔍</emoji> Проверка пользователя...",
        "user_not_found": "<emoji document_id=4958526153955476488>❌</emoji> Пользователь не найден",
        "gift_menu": "<emoji document_id=5931696400982088015>🎁</emoji> Выберите подарок.\n\n<emoji document_id=6032693626394382504>👤</emoji> Пользователь: {}\n<emoji document_id=5873153278023307367>📄</emoji> Текст: {}",
        "sending_gift": "<emoji document_id=5201691993775818138>🛫</emoji> Отправка подарка...",
        "gift_sent": "<emoji document_id=5021905410089550576>✅</emoji> Подарок успешно отправлен!",
        "not_enough_stars": "<emoji document_id=4958526153955476488>❌</emoji> Недостаточно звезд для отправки подарка {}!",
    }
    
    gifts = [
        [
            {"id": 5170145012310081615, "stars": 15, "emoji": "❤️", "name": "Сердце"},
            {"id": 5170233102089322756, "stars": 15, "emoji": "🧸", "name": "Мишка"},
            {"id": 5170250947678437525, "stars": 25, "emoji": "🎁", "name": "Подарок"},
        ],
        [
            {"id": 5168103777563050263, "stars": 25, "emoji": "🌹", "name": "Роза"},
            {"id": 5170144170496491616, "stars": 50, "emoji": "🎂", "name": "Тортик"},
            {"id": 5170314324215857265, "stars": 50, "emoji": "💐", "name": "Цветы"},
        ],
        [
            {"id": 5170564780938756245, "stars": 50, "emoji": "🚀", "name": "Ракета"},
            {"id": 5168043875654172773, "stars": 100, "emoji": "🏆", "name": "Кубок"},
            {"id": 5170690322832818290, "stars": 100, "emoji": "💍", "name": "Кольцо"},
        ]
    ]

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def sendgift(self, message):
        """Отправить подарок пользователю"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["usage"])
            return
        
        parts = args.split(maxsplit=1)
        if len(parts) < 1:
            await utils.answer(message, self.strings["usage"])
            return
        
        username = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        if username.startswith('@'):
            username = username[1:]
        msg = await utils.answer(message, self.strings["checking_user"])
        try:
            user = await self.client.get_entity(username)
        except Exception as e:
            logging.error(f"User not found: {e}")
            await utils.answer(msg, self.strings["user_not_found"])
            return
        buttons = []
        for row in self.gifts:
            btn_row = []
            for gift in row:
                btn_row.append({
                    "text": gift["emoji"],
                    "callback": self._send_gift,
                    "args": (user.id, gift["id"], text, gift["emoji"], msg.id),
                })
            buttons.append(btn_row)
        await utils.answer(
            msg,
            self.strings["gift_menu"].format(
                f"@{user.username}" if user.username else user.first_name,
                text if text else "-"
            ),
            reply_markup=buttons
        )
    async def _send_gift(self, call, user_id, gift_id, text, gift_emoji, msg_id):
        try:
            await call.edit(
                self.strings["sending_gift"],
                reply_markup=None
            )
            user = await self.client.get_input_entity(user_id)
            inv = InputInvoiceStarGift(
                user,
                gift_id,
                message=TextWithEntities(text, []) if text else TextWithEntities("", [])
            )
            form = await self.client(GetPaymentFormRequest(inv))
            result = await self.client(SendStarsFormRequest(form.form_id, inv))
            
            await call.edit(self.strings["gift_sent"])
        except BadRequestError as e:
            if "BALANCE_TOO_LOW" in str(e):
                await call.edit(
                    self.strings["not_enough_stars"].format(gift_emoji),
                    reply_markup=None
                )
            else:
                logging.error(f"Error sending gift: {e}")
                await call.edit(
                    f"❌ Ошибка при отправке подарка: {str(e)}",
                    reply_markup=None
                )
        except Exception as e:
            logging.error(f"Error sending gift: {e}")
            await call.edit(
                f"❌ Ошибка при отправке подарка: {str(e)}",
                reply_markup=None
            )
