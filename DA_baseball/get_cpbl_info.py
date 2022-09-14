from requests_html import HTMLSession
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class CpblInfoGetting:
    def __init__(self, url):
        self.url = url

    def _request(self):
        logger.info('Start getting response from CPBL web.')
        session = HTMLSession()
        with session.get(self.url, verify=False) as r:
            logger.info('Start rendering')
            r.html.render(sleep=10)
            logger.info('Finish rendering')
            res = r.html.raw_html
        logger.info('Finish getting response from CPBL web.')
        return res

    def _parse(self, res):
        logger.info('Start parsing response.')
        soup = BeautifulSoup(res, "lxml")
        logger.info('Start getting audience_cnt.')
        game_note = soup.findAll('div', {'class': 'GameNote'})
        if len(game_note) == 0:
            raise Exception(f'Does not render completely.')
        audience_cnt = game_note[1].findAll('li')[1].text[2:]
        logger.info('Finish getting audience_cnt.')
        if len(audience_cnt) == 0:
            raise Exception(f'The number of audience is wrong: {audience_cnt}.')
        audience_cnt = int(audience_cnt)
        logger.info('Finish parsing response.')
        return audience_cnt

    def execute(self):
        res = self._request()
        audience_cnt = self._parse(res=res)
        logger.info(f'The number of audience is: {audience_cnt}.')


if __name__ == '__main__':
    BASIC_FORMAT = "%(asctime)s-%(levelname)s-%(message)s"
    chlr = logging.StreamHandler()
    chlr.setFormatter(logging.Formatter(BASIC_FORMAT))
    logger.setLevel('DEBUG')
    logger.addHandler(chlr)

    # CpblInfoGetting
    op = CpblInfoGetting(
        url='https://www.cpbl.com.tw/box/index?gameSno=3&year=2022&kindCode=A'
    )
    op.execute()
