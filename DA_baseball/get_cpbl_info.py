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

    def _get_soup(self):
        tries_max = 5
        tries_num = 0
        keep_try = True
        while keep_try:
            if tries_num > tries_max:
                logger.error(f'Tries achieve limit. Can not get data from {self.url}.')
                raise Exception(f'Tries achieve limit. Can not get data from {self.url}.')
            try:
                res = self._request()
            except:
                logger.error(f'You have tried {tries_num} times. Tries-limit is {tries_max}. Url is {self.url}.')
                tries_num += 1
                continue
            logger.info('Start transforming response to soup.')
            soup = BeautifulSoup(res, "lxml")
            breadcrumbs = soup.findAll('div', {'id': 'Breadcrumbs'})
            if len(breadcrumbs) == 0:
                logger.error(f'Does not render completely(breadcrumbs). year: {self.year}. game_sno: {self.game_sno}.')
                logger.error(f'You have tried {tries_num} times. Tries-limit is {tries_max}. Url is {self.url}.')
                tries_num += 1
                continue
            breadcrumbs = breadcrumbs[0].findAll('li')[1].text.split(' ')
            if breadcrumbs[0] == '0001/01/01':
                raise Exception(f'The game_sno(date=={breadcrumbs[0]}) is not exist: {self.game_sno}.')
            game_date = datetime.datetime.strptime(breadcrumbs[0], '%Y/%m/%d').date()
            game_note = soup.findAll('div', {'class': 'GameNote'})
            if (len(game_note) == 0):
                if (game_date < datetime.datetime.today().date()):
                    if not soup.findAll('div', {'class': 'game_canceled'}):
                        logger.error(f'Does not render completely(game_note). year: {self.year}. game_sno: {self.game_sno}.')
                        logger.error(f'You have tried {tries_num} times. Tries-limit is {tries_max}. Url is {self.url}.')
                        tries_num += 1
                        continue            
            logger.info('Finish transforming response to soup.')
            break
        return soup

    def _parse_from_soup(self, soup):
        logger.info('Finish parsing data.')
        logger.info('Start getting game breadcrumbs.')
        breadcrumbs = soup.findAll('div', {'id': 'Breadcrumbs'})
        breadcrumbs = breadcrumbs[0].findAll('li')[1].text.split(' ')
        game_date = datetime.datetime.strptime(breadcrumbs[0], '%Y/%m/%d').date()
        home_team_name = breadcrumbs[1]
        visiting_team_name = breadcrumbs[3]
        logger.info('Finish getting game breadcrumbs.')
        logger.info('Start getting audience_cnt.')
        if soup.findAll('div', {'class': 'game_canceled'}):
            audience_cnt = 0
        else:
            game_note = soup.findAll('div', {'class': 'GameNote'})
            if len(game_note) == 0:
                if game_date >= datetime.datetime.today().date():
                    audience_cnt = 0
                else:
                    logger.error(f'Does not render completely(game_note). year: {self.year}. game_sno: {self.game_sno}.')
                    raise Exception(f'Does not render completely(game_note).')
            else:
                audience_cnt = game_note[1].findAll('li')[1].text[2:]
                if len(audience_cnt) == 0:
                    logger.error(f'The number of audience is wrong: {audience_cnt}. year: {self.year}. game_sno: {self.game_sno}.')
                    raise Exception(f'The number of audience is wrong: {audience_cnt}.')
                audience_cnt = int(audience_cnt)
        logger.info('Finish getting audience_cnt.')
        game_info = {
            'game_sno': self.game_sno,
            'game_date': game_date,
            'home_team_name': home_team_name,
            'visiting_team_name': visiting_team_name,
            'audience_cnt': audience_cnt
        }
        logger.info('Finish parsing data.')
        return game_info

    def execute(self):
        soup = self._get_soup()
        game_info = self._parse_from_soup(soup=soup)
        logger.info(f'game_info: {game_info}')
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
        game_sno=151
    )
    op.execute()
