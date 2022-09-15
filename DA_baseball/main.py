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
    # game_sno = int(df_cpbl_info.game_sno.max() +1)
    logger.info(f'Get pre-data.')
except:
    df_cpbl_info = pd.DataFrame(columns=['game_sno', 'game_date', 'home_team_name', 'visiting_team_name', 'audience_cnt'])
    logger.info(f'Create new.')

game_sno = 1
keep_getting = True
last_game_date = ''
# for game_sno in range(1, 5):
while keep_getting:
    logger.info(f"""
        ================================================
        Start get date from game_sno: {game_sno}.
        ================================================
    """)
    if game_sno in df_cpbl_info.game_sno.to_list():
        game_sno += 1
        continue
    try:
        op = CpblInfoGetting(
            year=2022,
            game_sno=game_sno
        )
        game_info = op.execute()
        last_game_date = game_info['game_date']
        df_cpbl_info = pd.concat([df_cpbl_info, pd.DataFrame(game_info, index=[0])]).reset_index(drop=True)
    except:
        logger.error(f'Can not get info from game_sno: {game_sno}. Last game date is {last_game_date}')
        break
    
    # if game_sno > 20:
    #     break
    game_sno += 1
    time.sleep(random.random())

df_cpbl_info.to_excel('./output/cpbl_info.xlsx', index=0)
