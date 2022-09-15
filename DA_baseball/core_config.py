# -*- coding: utf-8 -*-

"""
Definition the Settings in here.

Description:
The Settings will try to find the arguments from os.environ.
If the argument is missing in os.environ, ValidationError
will be raised.

History:
2022/09/15 Created by Gallon
"""
import json

class Settings:
    """
    Collect arguments from os.environ in this class.

    It try to find the arguments from os.environ.
    If the argument is missing, ValidationError will be raised.
    """

    # logger conf file path
    LOGGER_CONF_PATH = "./logger_conf.json"
    LOGGER_CONF = None
    LOGGER_LEVEL = "INFO"

_settings = Settings()
with open(_settings.LOGGER_CONF_PATH, 'r') as f:
    logger_conf = json.load(f)
_settings.LOGGER_CONF = logger_conf
settings = _settings