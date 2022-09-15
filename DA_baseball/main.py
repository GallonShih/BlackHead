import pandas as pd
import datetime
import time
import random

from get_cpbl_info import CpblInfoGetting
from logging import config as logger_config
from core_config import settings
import logging

logger_config.dictConfig(settings.LOGGER_CONF)
logger = logging.getLogger(__name__)

try:
    df_cpbl_info = pd.read_excel('./output/cpbl_info.xlsx')
    game_sno = int(df_cpbl_info.game_sno.max() +1)
    logger.info(f'Get pre-data. Start in: {game_sno}')
except:
    df_cpbl_info = pd.DataFrame()
    game_sno = 1
    logger.info(f'Create new. Start in: {game_sno}')

keep_getting = True
error_limit = 5
error_num = 0
today_dt = datetime.datetime.today().date()
# for game_sno in range(1, 5):
while keep_getting:
    logger.info(f"""
        ================================================
        Start get date from game_sno: {game_sno}.
        ================================================
    """)
    op = CpblInfoGetting(
        year=2022,
        game_sno=game_sno
    )
    game_info = op.execute()
    if game_info:
        last_game_date = game_info['game_date']
        df_cpbl_info = pd.concat([df_cpbl_info, pd.DataFrame(game_info, index=[0])]).reset_index(drop=True)
    else:
        logger.info(f'Can not get info from game_sno: {game_sno}. Last game date is {last_game_date}')
        error_num += 1
        if error_num > error_limit:
            logger.info(f'The error times achieve the limit. Last game_sno: {game_sno}')
            break

    game_sno += 1
    time.sleep(random.random())

df_cpbl_info.to_excel('./output/cpbl_info.xlsx', index=0)