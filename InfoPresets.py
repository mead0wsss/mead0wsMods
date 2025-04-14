__version__ = (1, 0, 0)

# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods

# scope: heroku_only
# meta developer: @mead0wssMods
# meta banner: https://x0.at/GHOP.png

import json
import os
from telethon.tl.types import Message
from ..inline.types import InlineCall
from .. import loader, utils
import logging

logger = logging.getLogger(__name__)

@loader.tds
class InfoPresets(loader.Module):
    """Управление пресетами для HerokuInfo"""
    strings = {
        "name": "InfoPresets",
        "preset_exists": "🚫 Пресет с таким именем уже существует!",
        "preset_created": "✅ Пресет '{}' создан. Теперь настройте параметры.",
        "file_created": "✅ Файл InfoPresets.json создан",
        "param_set": "✅ Параметр '{}' установлен в '{}' для пресета '{}'",
        "preset_not_found": "🚫 Пресет '{}' не найден!",
        "preset_deleted": "✅ Пресет '{}' удален",
        "no_presets": "🚫 Нет сохраненных пресетов",
        "preset_loaded": "✅ Пресет '{}' загружен",
        "enter_value": "✍️ Введите значение для параметра '{}':",
        "invalid_bool": "🚫 Значение должно быть True или False",
        "param_not_set": "🚫 Параметр '{}' не установлен в пресете '{}'",
        "config_menu": "⚙️ Настройка пресета '{}'\nВыберите параметр:",
        "file_deleted": "✅ Файл с пресетами удален",
        "file_not_found": "🚫 Файл с пресетами не найден",
        "preset_list": "📋 Список пресетов:\n\n{}",
        "preset_info": "🔹 {}:\n{}",
        "param_info": "  • {}: {}",
        "done": "✅ Готово",
        "cancel": "❌ Отмена"
    }

    async def client_ready(self, client, db):
        self._client = client
        self.db = db
        self.presets_file = "InfoPresets.json"
        self.ensure_presets_file()
        self._waiting_param = None
        self._active_forms = {}

    def ensure_presets_file(self):
        if not os.path.exists(self.presets_file):
            with open(self.presets_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    async def createprcmd(self, message: Message):
        """Создать новый пресет."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "🚫 Укажите название пресета")
            return

        with open(self.presets_file, "r+", encoding="utf-8") as f:
            try:
                presets = json.load(f)
            except json.JSONDecodeError:
                presets = {}

            if args in presets:
                await utils.answer(message, self.strings["preset_exists"])
                return

            presets[args] = {}
            f.seek(0)
            json.dump(presets, f, indent=4)
            f.truncate()

        await self.edit_preset(message, args)

    async def edit_preset(self, message: Message, preset_name: str):
        """Редактирование пресета с инлайн-кнопками"""
        buttons = [
            [
                {"text": "✏️ custom_message", "callback": self._param_callback, "args": (preset_name, "custom_message")},
                {"text": "🖼️ pp_to_banner", "callback": self._param_callback, "args": (preset_name, "pp_to_banner")}
            ],
            [
                {"text": "🔗 banner_url", "callback": self._param_callback, "args": (preset_name, "banner_url")},
                {"text": "⚙️ show_heroku", "callback": self._param_callback, "args": (preset_name, "show_heroku")}
            ],
            [
                {"text": self.strings["done"], "callback": self._done_callback, "args": (preset_name,)}
            ]
        ]

        form = await self.inline.form(
            message=message,
            text=self.strings["config_menu"].format(preset_name),
            reply_markup=buttons,
            silent=True
        )
        self._active_forms[preset_name] = form

    async def _param_callback(self, call: InlineCall, preset_name: str, param: str):
        """Обработчик выбора параметра"""
        await call.edit(
            self.strings["enter_value"].format(param),
            reply_markup=[
                [{"text": self.strings["cancel"], "callback": self._cancel_callback, "args": (preset_name,)}]
            ]
        )
        self._waiting_param = (call.from_user.id, preset_name, param, call)

    async def _cancel_callback(self, call: InlineCall, preset_name: str):
        """Обработчик отмены"""
        if preset_name in self._active_forms:
            await self._active_forms[preset_name].edit(
                self.strings["config_menu"].format(preset_name),
                reply_markup=[
                    [
                        {"text": "✏️ custom_message", "callback": self._param_callback, "args": (preset_name, "custom_message")},
                        {"text": "🖼️ pp_to_banner", "callback": self._param_callback, "args": (preset_name, "pp_to_banner")}
                    ],
                    [
                        {"text": "🔗 banner_url", "callback": self._param_callback, "args": (preset_name, "banner_url")},
                        {"text": "⚙️ show_heroku", "callback": self._param_callback, "args": (preset_name, "show_heroku")}
                    ],
                    [
                        {"text": self.strings["done"], "callback": self._done_callback, "args": (preset_name,)}
                    ]
                ]
            )

    async def _done_callback(self, call: InlineCall, preset_name: str):
        """Обработчик завершения"""
        await call.delete()
        if preset_name in self._active_forms:
            del self._active_forms[preset_name]

    async def watcher(self, message: Message):
        """Обработчик ввода значений параметров"""
        if not hasattr(self, "_waiting_param"):
            return
            
        user_id, preset_name, param, call = self._waiting_param
        
        if message.sender_id != user_id:
            return
            
        value = message.raw_text
        
        if param in ["pp_to_banner", "show_heroku"]:
            if value.lower() not in ["true", "false"]:
                await utils.answer(message, self.strings["invalid_bool"])
                return
            value = value.lower() == "true"

        with open(self.presets_file, "r+", encoding="utf-8") as f:
            presets = json.load(f)
            if preset_name not in presets:
                await utils.answer(message, self.strings["preset_not_found"].format(preset_name))
                return

            presets[preset_name][param] = value
            f.seek(0)
            json.dump(presets, f, indent=4)
            f.truncate()

        await utils.answer(message, self.strings["param_set"].format(param, value, preset_name))
        

        if preset_name in self._active_forms:
            await self._active_forms[preset_name].edit(
                self.strings["config_menu"].format(preset_name),
                reply_markup=[
                    [
                        {"text": "✏️ custom_message", "callback": self._param_callback, "args": (preset_name, "custom_message")},
                        {"text": "🖼️ pp_to_banner", "callback": self._param_callback, "args": (preset_name, "pp_to_banner")}
                    ],
                    [
                        {"text": "🔗 banner_url", "callback": self._param_callback, "args": (preset_name, "banner_url")},
                        {"text": "⚙️ show_heroku", "callback": self._param_callback, "args": (preset_name, "show_heroku")}
                    ],
                    [
                        {"text": self.strings["done"], "callback": self._done_callback, "args": (preset_name,)}
                    ]
                ]
            )
        
        delattr(self, "_waiting_param")
        
    async def delprcmd(self, message: Message):
        """Удалить пресет."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "🚫 Укажите название пресета")
            return

        with open(self.presets_file, "r+", encoding="utf-8") as f:
            presets = json.load(f)
            if args not in presets:
                await utils.answer(message, self.strings["preset_not_found"].format(args))
                return

            del presets[args]
            f.seek(0)
            json.dump(presets, f, indent=4)
            f.truncate()

        await utils.answer(message, self.strings["preset_deleted"].format(args))

    async def delfileprcmd(self, message: Message):
        """Удалить файл с пресетами."""
        if not os.path.exists(self.presets_file):
            await utils.answer(message, self.strings["file_not_found"])
            return
            
        os.remove(self.presets_file)
        self.ensure_presets_file()
        await utils.answer(message, self.strings["file_deleted"])

    async def uploadprcmd(self, message: Message):
        """Загрузить файл с пресетами."""
        if not os.path.exists(self.presets_file):
            await utils.answer(message, "🚫 Файл пресетов не найден")
            return

        with open(self.presets_file, "r", encoding="utf-8") as f:
            presets = json.load(f)
            if not presets:
                await utils.answer(message, self.strings["no_presets"])
                return

        await self._client.send_file(
            message.chat_id,
            self.presets_file,
            caption="📁 Файл с пресетами"
        )
        await message.delete()

    async def listprcmd(self, message: Message):
        """Показать список всех пресетов."""
        if not os.path.exists(self.presets_file):
            await utils.answer(message, self.strings["file_not_found"])
            return

        with open(self.presets_file, "r", encoding="utf-8") as f:
            try:
                presets = json.load(f)
            except json.JSONDecodeError:
                await utils.answer(message, self.strings["no_presets"])
                return

            if not presets:
                await utils.answer(message, self.strings["no_presets"])
                return

            result = []
            for preset_name, params in presets.items():
                param_lines = []
                for param, value in params.items():
                    param_lines.append(self.strings["param_info"].format(param, value))
                result.append(self.strings["preset_info"].format(
                    preset_name, "\n".join(param_lines) if param_lines else "⏺ Нет параметров"
                ))

            await utils.answer(
                message,
                self.strings["preset_list"].format("\n\n".join(result))
            )

    async def loadprcmd(self, message: Message):
        """Загрузить пресет."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "🚫 Укажите название пресета")
            return

        with open(self.presets_file, "r", encoding="utf-8") as f:
            presets = json.load(f)
            if args not in presets:
                await utils.answer(message, self.strings["preset_not_found"].format(args))
                return

            preset = presets[args]
            heroku_info = self.lookup("HerokuInfo")
            
            if not heroku_info:
                await utils.answer(message, "🚫 Модуль HerokuInfo не найден!")
                return

            for param, value in preset.items():
                if param in heroku_info.config:
                    heroku_info.config[param] = value
                else:
                    logger.warning(f"Параметр {param} не найден в конфиге HerokuInfo")
        await utils.answer(message, self.strings["preset_loaded"].format(args))
