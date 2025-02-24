import yaml, os
from ruamel.yaml import YAML
from uuid import uuid4
from aiogram import types
from random import choice
from asyncio import Semaphore

class ConfigurationYaml:
    def __init__(
        self,
        mapping: int = 2,
        sequence: int = 4,
        offset: int = 2,
        default_fs: bool = False,
        enc: str = "utf-8",
    ) -> None:
        yaml2 = YAML()
        yaml2.indent(mapping=mapping, sequence=sequence, offset=offset)
        yaml2.default_flow_style = default_fs
        yaml2.encoding = enc
        self.yaml_conf = yaml2


class UGUtils:
    def __init__(self, yaml_file: str) -> None:
        self.path = yaml_file
        self.data = self.get_yaml()

    def get_yaml(self) -> dict:
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as file:
                file.write("")

        with open(self.path, encoding="utf-8") as file:
            data = yaml.safe_load(file)

            if not data:
                return {}
            return data


    def update_yaml(self, data: dict):
        yaml_config = ConfigurationYaml().yaml_conf
        with open(self.path, "w", encoding="utf-8") as file:
            data = yaml_config.dump(data, file)

        if data:
            return data
        return {}



class DatabseConfig:
    def __init__(self, data : dict) -> None:
        self.user = data.get('user', 'postgres')
        self.pasword = data.get("pasword", '1234')
        self.database = data.get("database", 'database')
        self.port = data.get('port', 5432)
        self.host = data.get('host', 'localhost')


class ParamInlineButton:
    def __init__(self, data : list[list[dict]]) -> types.InlineKeyboardMarkup:
        self.buttons = []
        for row in data:
            row_data = []
            for button in row:
                row_data.append(types.InlineKeyboardButton(button.get('text', "tugma"), 
                                                           callback_data=button.get('callback_data'), 
                                                           url=button.get('url')))
            self.buttons.append(row_data)
    

    @property
    def replay_markup(self) -> types.InlineKeyboardMarkup:
        if self.buttons:
            return types.InlineKeyboardMarkup(inline_keyboard=self.buttons)

class InlineAd:
    def __init__(self, data : dict | None = {}) -> None:
        self.id : str = data.get('id', uuid4().hex)
        self.message_id : int = data.get('message_id')
        self.thumb_url : str = data.get('thumb_url')
        self.title : str = data.get('title')
        self.type : str = data.get('type')
        self.file_id : str = data.get('file_id')
        self.description : str = data.get('description', '➡️ Buyerga bosing')
        self.caption : str = data.get('caption')
        self.parse_mode : str = data.get('parse_mode')
        self.buttons = ParamInlineButton(data.get('buttons', []))
        self.mime_type = data.get('mime_type', 'video/mp4')
    
    @property
    def row_data(self) -> dict:
        return {'id': self.id, 'message_id' : self.message_id, 'thumb_url': self.thumb_url, 'title': self.title, 'description': self.description, 'buttons': self.buttons}

    @property
    def inline_resolt(self) -> types.InlineQueryResultArticle:
        if self.type == 'text':
            return types.InlineQueryResultArticle(id=self.id, 
                                              title=self.title, 
                                              description=self.description, 
                                              thumb_url=self.thumb_url, 
                                              reply_markup= self.buttons.replay_markup,
                                              input_message_content=types.InputTextMessageContent(self.caption, parse_mode=self.parse_mode))

        elif self.type == 'photo':
            return types.InlineQueryResultPhoto(id = self.id, 
                                                photo_url= self.thumb_url, 
                                                thumb_url=self.thumb_url,
                                                # photo_width = 20,
                                                # photo_height = 20,
                                                title=self.title,
                                                description=self.description,
                                                reply_markup=self.buttons.replay_markup, 
                                                caption=self.caption, 
                                                parse_mode=self.parse_mode)

        elif self.type == 'video':
            return types.InlineQueryResultVideo(id = self.id, 
                                                video_url= self.file_id, 
                                                title=self.title, 
                                                mime_type = self.mime_type,
                                                description=self.description, 
                                                thumb_url=self.thumb_url, 
                                                reply_markup=self.buttons.replay_markup, 
                                                caption=self.caption, 
                                                parse_mode=self.parse_mode)


class Chanel:
    def __init__(self, data : dict):
        self.id : str = data.get('id')
        self.username : str = data.get('username')
        self.name = data.get('name')
        self.url = data.get('url')
        self.request_join = data.get('request_join', False)
        self.auto_join = data.get('auto_join', False)
        self.user_count = data.get('user_count', 0)

    @property
    def row_data(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'url': self.url,
            'request_join': self.request_join,
            'auto_join': self.auto_join,
            'user_count': self.user_count
        }
    
    def __str__(self):
        return str({
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'url': self.url,
            'requet_join': self.request_join,
            'auto_join': self.auto_join,
            'user_count': self.user_count
        })


class ParamsDB:
    def __init__(self, config_path : str) -> None:
        self.yaml = UGUtils(config_path)
        self.params_data = self.yaml.get_yaml()
        self.paramas_sem = Semaphore()
    
        self.config = DatabseConfig(self.params_data.get('database', {}))
        self.TOKEN = self.params_data.get('token')
        self.DATA_CHANEL_ID : int = self.params_data.get('data_chanel_id')
        self.DEV_ID : list[int] = self.params_data.get('dev_id')
        self.HELP_CONTENT = self.params_data.get('help_video')
        self.INLINE_CACHE_TIME : int = self.params_data.get('inline_cache_time', 60**2)
        self.LOGO_URL : str = self.params_data.get('logo_url')
        self.NO_FOUND_URL : str = self.params_data.get('no_found_url')
        self.DOMEN : str = self.params_data.get('domen')
        self.API_ID : int =  self.params_data.get('api_id')
        self.API_HASH : str = self.params_data.get('api_hash')
        self.QIZQARLI_OVOZLAR : list[list[dict[str, int]]] = self.params_data.get('qizqarli_ovozlar')
        self.SHERLAR : list[list[dict[str, int]]] = self.params_data.get('sherlar')
        self.TABRIKLAR : list[list[dict[str, int]]] = self.params_data.get('tabriklar')
        self.ovozlar_data : dict[str, int] = {}
        self.PINED_VOICES : list[int] = self.params_data.get('pined_voices', [])
        self.inline_ads = self.params_data.get('inline_ads', [])
        self.inline_ads : list[InlineAd] = [InlineAd(ad) for ad in self.inline_ads]
        self.CHANELS : list[Chanel] = [Chanel(chanel) for chanel in self.params_data.get('chanels', [])]
        self.CHANELS_DICT = {chanel.id : chanel for chanel in self.CHANELS}

        for row in self.QIZQARLI_OVOZLAR + self.SHERLAR + self.TABRIKLAR:
            for button in row:
                for name, id in button.items():
                    self.ovozlar_data[name] = id

    def update_chanel_dict(self):
        self.CHANELS_DICT = {chanel.id : chanel for chanel in self.CHANELS}
        
    def update_params(self):
        self.yaml.update_yaml(self.params_data)


    @property
    def ads_exsis(self) -> bool:
        return bool(self.inline_ads)
    
    @property
    def random_ads(self) -> types.InlineQueryResultArticle:
        if len(self.inline_ads) == 1:
            return self.inline_ads[0].inline_resolt

        elif len(self.inline_ads) > 1:
            return choice(self.inline_ads).inline_resolt