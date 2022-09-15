from requests_html import HTMLSession
from bs4 import BeautifulSoup
import datetime
import warnings
import logging

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)

class CpblInfoGetting:
    def __init__(self, year, game_sno):
        self.year = year
        self.game_sno = game_sno
        self.url = f'https://www.cpbl.com.tw/box/index?gameSno={self.game_sno}&year={self.year}&kindCode=A'

    def _request(self):
        logger.info('Start getting response from CPBL web.')
        session = HTMLSession()
        try:
            with session.get(self.url, verify=False) as r:
                logger.info('Start rendering')
                r.html.render(retries=3, sleep=10)
                logger.info('Finish rendering')
                res = r.html.raw_html
        except:
            logger.error(f'The url: {self.url} is wrong.')
            raise Exception(f'The url: {self.url} is wrong.')
        finally:
            session.close()
        logger.info('Finish getting response from CPBL web.')
        return res

    def _parse(self, res):
        logger.info('Start parsing response.')
        soup = BeautifulSoup(res, "lxml")
        logger.info('Start getting game breadcrumbs.')
        breadcrumbs = soup.findAll('div', {'id': 'Breadcrumbs'})
        if len(breadcrumbs) == 0:
            logger.error(f'Does not render completely(breadcrumbs). year: {self.year}. game_sno: {self.game_sno}.')
            raise Exception(f'Does not render completely(breadcrumbs).')
        breadcrumbs = breadcrumbs[0].findAll('li')[1].text.split(' ')
        if len(breadcrumbs) != 4:
            logger.error(f'The breadcrumbs is wrong: {breadcrumbs}.')
            raise Exception(f'The breadcrumbs is wrong: {breadcrumbs}. year: {self.year}. game_sno: {self.game_sno}.')
        game_date = datetime.datetime.strptime(breadcrumbs[0], '%Y/%m/%d').date()
        home_team_name = breadcrumbs[1]
        visiting_team_name = breadcrumbs[3]
        logger.info('Finish getting game breadcrumbs.')
        if game_date < datetime.datetime.today().date():
            logger.info('Start getting audience_cnt.')
            game_note = soup.findAll('div', {'class': 'GameNote'})
            if len(game_note) == 0:
                logger.error(f'Does not render completely(game_note). year: {self.year}. game_sno: {self.game_sno}.')
                raise Exception(f'Does not render completely(game_note).')
            audience_cnt = game_note[1].findAll('li')[1].text[2:]
            if len(audience_cnt) == 0:
                logger.error(f'The number of audience is wrong: {audience_cnt}. year: {self.year}. game_sno: {self.game_sno}.')
                raise Exception(f'The number of audience is wrong: {audience_cnt}.')
            audience_cnt = int(audience_cnt)
        else:
            audience_cnt = 0
            logger.info(f'game_date{game_date} > today{datetime.datetime.today().date()}')
        logger.info('Finish getting audience_cnt.')
        game_info = {
            'game_sno': self.game_sno,
            'game_date': game_date,
            'home_team_name': home_team_name,
            'visiting_team_name': visiting_team_name,
            'audience_cnt': audience_cnt
        }
        logger.info('Finish parsing response.')
        return game_info

    def execute(self):
        tries_max = 5
        tries_num = 0
        keep_try = True
        while keep_try:
            try:
                res = self._request()
                game_info = self._parse(res=res)
                break
            except:
                tries_num += 1
                if tries_num > tries_max:
                    logger.info(f'Tries achieve limit. Can not get data from {self.url}.')
                    game_info = None
                    keep_try = False
        # logger.info(f'The game_info is: {game_info}.')
        return game_info


if __name__ == '__main__':
    BASIC_FORMAT = "%(asctime)s-%(levelname)s-%(message)s"
    chlr = logging.StreamHandler()
    chlr.setFormatter(logging.Formatter(BASIC_FORMAT))
    logger.setLevel('DEBUG')
    logger.addHandler(chlr)

    # CpblInfoGetting
    op = CpblInfoGetting(
        year=2022,
        game_sno=3
    )
    op.execute()
