__version__ = (1, 0, 0)

# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods

# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @mead0wssMods
# meta banner: https://x0.at/eoIh.jpg


import requests
from telethon import events
from .. import loader, utils

@loader.tds
class GPTMod(loader.Module):
    """Модуль для работы с нейросетями (ChatGPT)"""
    strings = {"name": "CablyAI"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "model",
                "",
                lambda: "Модель GPT для использования",
                validator=loader.validators.String()
            ),
        )

    async def gptcmd(self, event):
        """Модуль для работы с ChatGPT прямо в Telegram."""
        args = utils.get_args_raw(event)
        if not args:
            await event.reply("Нет вопроса")
            return

        model = self.config.get("model")

        if not model:
            await event.reply("Модель ИИ не указана в конфиге")
            return

        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": args}
            ]
        }

        response = requests.post("https://cablyai.com/v1/chat/completions", headers={
            'Authorization': 'Bearer sk-csPV6DEqRj07V4jGxPvq0NomUcfo6LIxO_rlxBMuenGaebco',
            'Content-Type': 'application/json',
        }, json=data)

        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            await event.edit(f"<b><emoji document_id=5974038293120027938>👤</emoji> Вопрос: <code>{args}</code></b>\n\n<b><emoji document_id=5199682846729449178>🤖</emoji> Ответ: {answer}</b>", parse_mode="HTML")
        else:
            await event.reply("Ошибка при запросе к GPT")
