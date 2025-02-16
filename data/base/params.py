import yaml, os
from ruamel.yaml import YAML
from uuid import uuid4


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

class ParamsDB:
    def __init__(self, config_path : str) -> None:
        self.yaml = UGUtils(config_path)
        self.params_data = self.yaml.get_yaml()
    
        self.config = DatabseConfig(self.params_data.get('database', {}))
        self.TOKEN = self.params_data.get('token')
        self.DATA_CHANEL_ID : int = self.params_data.get('data_chanel_id')
        self.DEV_ID : int = self.params_data.get('dev_id')
        self.HELP_CONTENT = self.params_data.get('help_video')
        self.INLINE_CACHE_TIME : int = self.params_data.get('inline_cache_time', 60**2)
        self.LOGO_URL : str = self.params_data.get('logo_url')
        self.NO_FOUND_URL : str = self.params_data.get('no_found_url')
        self.DOMEN : str = self.params_data.get('domen')
        self.API_ID : int =  self.params_data.get('api_id')
        self.API_HASH : str = self.params_data.get('api_hash')

    def update_params(self):
        self.yaml.update_yaml(self.params_data)