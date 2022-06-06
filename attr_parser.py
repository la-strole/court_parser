import datetime
import logging
from collections import OrderedDict
from time import sleep
from random import randint

from bs4 import BeautifulSoup
from selenium import webdriver


# from selenium.webdriver.chrome.options import Options


class sudrf_parser:

    def __init__(self, date_from='01.01.2022',
                 date_for='.'.join(datetime.date.today().isoformat().split('-')[::-1])):

        self.title_dict = {'pechorsky': 'Печорский районный суд Псковской области',
                           'pskov': 'Псковский городской суд Псковской области',
                           'oblsud': 'Псковский областной суд',
                           'pskov_voen': 'Псковский гарнизонный военный суд',
                           'bezhanicky': 'Бежаницкий районный суд Псковской области',
                           'velikolukskygor': 'Великолукский городской суд Псковской области',
                           'velikoluksky': 'Великолукский районный суд Псковской области',
                           'gdovsky': 'Гдовский районный суд Псковской области',
                           'dedovichsky': 'Дедовичский районный суд Псковской области',
                           'dnovsky': 'Дновский районный суд Псковской области',
                           'nevelsky': 'Невельский районный суд Псковской области',
                           'novosokolnichesky': 'Новосокольнический районный суд Псковской области',
                           'opochecky': 'Опочецкий районный суд Псковской области',
                           'ostrovsky': 'Островский городской суд Псковской области',
                           'porhovsky': 'Порховский районный суд Псковской области',
                           'pskov_rajon': 'Псковский районный суд Псковской области',
                           'pushkinogorsky': 'Пушкиногорский районный суд Псковской области',
                           'pytalovsky': 'Пыталовский районный суд Псковской области',
                           'sebezhsky': 'Себежский районный суд Псковской области',
                           'strugokrasnensky': 'Стругокрасненский районный суд Псковской области'}

        self.logger_attr_parser = logging.getLogger('attr_parser.py')
        f_handler = logging.FileHandler('file.log')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        self.logger_attr_parser.addHandler(f_handler)

        self.url_court = {'pechorsky': 'http://pechorsky--psk.sudrf.ru/modules.php?',
                          'pskov': 'http://pskovskygor--psk.sudrf.ru/modules.php?',
                          'oblsud': 'http://oblsud.psk.sudrf.ru/modules.php?',
                          'pskov_voen': 'http://gvs.psk.sudrf.ru/modules.php?',
                          'bezhanicky': 'http://bezhanicky.psk.sudrf.ru/modules.php?',
                          'velikolukskygor': 'http://velikolukskygor.psk.sudrf.ru/modules.php?',
                          'velikoluksky': 'http://velikoluksky.psk.sudrf.ru/modules.php?',
                          'gdovsky': 'http://gdovsky.psk.sudrf.ru/modules.php?',
                          'dedovichsky': 'http://dedovichsky.psk.sudrf.ru/modules.php?',
                          'dnovsky': 'http://dnovsky.psk.sudrf.ru/modules.php?',
                          'nevelsky': 'http://nevelsky.psk.sudrf.ru/modules.php?',
                          'novosokolnichesky': 'http://novosokolnichesky.psk.sudrf.ru/modules.php?',
                          'opochecky': 'http://opochecky.psk.sudrf.ru/modules.php?',
                          'ostrovsky': 'http://ostrovsky.psk.sudrf.ru/modules.php?',
                          'porhovsky': 'http://porhovsky.psk.sudrf.ru/modules.php?',
                          'pskov_rajon': 'http://pskovsky.psk.sudrf.ru/modules.php?',
                          'pushkinogorsky': 'http://pushkinogorsky.psk.sudrf.ru/modules.php?',
                          'pytalovsky': 'http://pytalovsky.psk.sudrf.ru/modules.php?',
                          'sebezhsky': 'http://sebezhsky.psk.sudrf.ru/modules.php?',
                          'strugokrasnensky': 'http://strugokrasnensky.psk.sudrf.ru/modules.php?'
                          }

        self.attrs = OrderedDict([('name', 'sud_delo'),  # Судебное делопроизводство
                                  ('srv_num', '1'),
                                  ('name_op', 'r'),  # Административные правонарушения
                                  ('delo_id', '1500001'),
                                  ('case_type', '0'),
                                  ('new', '0'),
                                  ('adm_parts__NAMESS', ''),
                                  ('adm_case__CASE_NUMBERSS', ''),
                                  ('adm_case__JUDICIAL_UIDSS', ''),
                                  ('delo_table', 'adm_case'),
                                  ('adm_case__ENTRY_DATE1D', date_from),  # Искать с числа
                                  ('adm_case__ENTRY_DATE2D', date_for),  # Искать по число
                                  ('adm_case__PR_NUMBERSS', ''),
                                  ('ADM_CASE__JUDGE', ''),
                                  ('adm_case__RESULT_DATE1D', ''),
                                  ('adm_case__RESULT_DATE2D', ''),
                                  ('ADM_CASE__RESULT', '%25C2%25FB%25ED%25E5%25F1%25E5%25ED%25EE%2520%25EF%25EE%25F1'
                                                       '%25F2%25E0%25ED%25EE%25E2%25EB%25E5%25ED%25E8%25E5%2520%25EE'
                                                       '%2520%25ED%25E0%25E7%25ED%25E0%25F7%25E5%25ED%25E8%25E8%2520'
                                                       '%25E0%25E4%25EC%25E8%25ED%25E8%25F1%25F2%25F0%25E0%25F2%25E8'
                                                       '%25E2%25ED%25EE%25E3%25EE%2520%25ED%25E0%25EA%25E0%25E7%25E0'
                                                       '%25ED%25E8%25FF'),  # Вынесено решение о штрафе
                                  ('ADM_CASE__BUILDING_ID', ''),
                                  ('ADM_CASE__COURT_STRUCT', ''),
                                  ('ADM_EVENT__EVENT_NAME', ''),
                                  ('adm_event__EVENT_DATEDD', ''),
                                  ('ADM_PARTS__PARTS_TYPE', ''),
                                  ('adm_parts__LAW_ARTICLESS', ''),

                                  # lawbookarticles%5B%5D generated as multiple args
                                  # where 20.3.3 - paragraph +%F7.{part}
                                  # ex: lawbookarticles%5B%5D=20.3.1&lawbookarticles%5B%5D=20.3.2+%F7.1
                                  ('lawbookarticles%5B%5D', ''),
                                  # 'lawbookarticles%5B%5D' : '20.3.3+%F7.2',

                                  ('adm_parts__INN_STRSS', ''),
                                  ('adm_parts__KPP_STRSS', ''),
                                  ('adm_parts__OGRN_STRSS', ''),
                                  ('adm_parts__OGRNIP_STRSS', ''),
                                  ('adm_document__PUBL_DATE1D', ''),
                                  ('adm_document__PUBL_DATE2D', ''),
                                  ('ADM_CASE__VALIDITY_DATE1D', ''),
                                  ('ADM_CASE__VALIDITY_DATE2D', ''),
                                  ('adm_order_info__ORDER_DATE1D', ''),
                                  ('adm_order_info__ORDER_DATE2D', ''),
                                  ('adm_order_info__ORDER_NUMSS', ''),
                                  ('ADM_ORDER_INFO__STATE_ID', ''),
                                  ('list', 'ON'),  # Всерезультаты на одной странице?
                                  ('Submit', '%CD%E0%E9%F2%E8#')])

        # https://www.consultant.ru/document/cons_doc_LAW_34661/
        self.paragraph_part = ('20.2_1',  # Нарушение организатором публичного мероприятия установленного порядка
                               # организации либо проведения собрания, митинга, демонстрации, шествия
                               # или пикетирования, за исключением случаев, предусмотренных
                               # частями 2 - 4 и 9 настоящей статьи
                               '20.2_2',  # Организация либо проведение публичного мероприятия без подачи в
                               # установленном порядке уведомления о проведении публичного мероприятия,
                               # за исключением случаев, предусмотренных частью 7 настоящей статьи
                               '20.2_3',  # Действия (бездействие), предусмотренные частями 1 и 2 настоящей статьи,
                               # повлекшие создание помех функционированию объектов жизнеобеспечения,
                               # транспортной или социальной инфраструктуры, связи, движению пешеходов и
                               # (или) транспортных средств либо доступу граждан к жилым помещениям или
                               # объектам транспортной или социальной инфраструктуры либо превышение норм
                               # предельной заполняемости территории (помещения), если эти действия
                               # (бездействие) не содержат уголовно наказуемого деяния
                               '20.2_4',  # Действия (бездействие), предусмотренные частями 1 и 2 настоящей статьи,
                               # повлекшие причинение вреда здоровью человека или имуществу, если эти
                               # действия (бездействие) не содержат уголовно наказуемого деяния
                               '20.2_5',  # Нарушение участником публичного мероприятия установленного порядка
                               # проведения собрания, митинга, демонстрации, шествия или пикетирования,
                               # за исключением случаев, предусмотренных частью 6 настоящей статьи
                               '20.2_6',  # Действия (бездействие), предусмотренные частью 5 настоящей статьи,
                               # повлекшие причинение вреда здоровью человека или имуществу, если эти
                               # действия (бездействие) не содержат уголовно наказуемого деяния
                               '20.2_7',  # Организация либо проведение несанкционированных собрания, митинга,
                               # демонстрации, шествия или пикетирования в непосредственной близости от
                               # территории ядерной установки, радиационного источника или пункта хранения
                               # ядерных материалов и радиоактивных веществ либо активное участие в таких
                               # публичных мероприятиях, если это осложнило выполнение работниками указанных
                               # установки, источника или пункта своих служебных обязанностей или создало
                               # угрозу безопасности населения и окружающей среды
                               '20.2_8',  # Повторное совершение административного правонарушения, предусмотренного
                               # частями 1 - 6.1 настоящей статьи, если это действие не содержит уголовно
                               # наказуемого деяния
                               '20.2_10',  # Перечисление (передача) денежных средств и (или) иного имущества для
                               # организации и проведения публичного мероприятия, совершенное лицом,
                               # которое не вправе перечислять (передавать) денежные средства и (или)
                               # иное имущество в этих целях в соответствии с федеральным законом
                               '20.3.2_1',  # Публичные призывы к осуществлению действий, направленных на нарушение
                               # территориальной целостности Российской Федерации, если эти действия
                               # не содержат признаков уголовно наказуемого деяния
                               '20.3.2_2',  # Те же действия, совершенные с использованием средств массовой информации
                               # либо электронных или информационно-телекоммуникационных сетей
                               # (включая сеть "Интернет")
                               '20.3.3_1',  # Публичные действия, направленные на дискредитацию использования
                               # Вооруженных Сил Российской Федерации
                               '20.3.3_2',  # Те же действия, сопровождающиеся призывами к проведению
                               # несанкционированных публичных мероприятий, а равно создающие угрозу
                               # причинения вреда жизни и (или) здоровью граждан, имуществу, угрозу
                               # массового нарушения общественного порядка и (или) общественной
                               # безопасности либо угрозу создания помех функционированию или прекращения
                               # функционирования объектов жизнеобеспечения, транспортной или социальной
                               # инфраструктуры, кредитных организаций, объектов энергетики, промышленности
                               # или связи, если эти действия не содержат признаков
                               # уголовно наказуемого деяния
                               '20.3.4_'  # Призывы к введению мер ограничительного характера в отношении
                               # Российской Федерации, граждан Российской Федерации
                               # или российских юридических лиц
                               )

    def generate_url(self, court):
        """ Generate url for 'gas pravosudie'
            :param court: Court name (ex: pskov)
            :return: Url string

        """

        try:
            assert court in self.url_court
        except AssertionError as e:
            self.logger_attr_parser.exception(f"{court} not in courts list.")
            raise e

        court_address = self.url_court.get(court)

        attr_address = ''
        for attr_key in self.attrs:

            if attr_key == 'lawbookarticles%5B%5D':
                for value in self.paragraph_part:
                    try:
                        part, chapter = value.split('_')
                    except ValueError as e:
                        self.logger_attr_parser.exception(f"Wrong format for article: 12.1_ exppexted - get {value}")
                        raise e
                    if chapter:
                        attr_address = '&'.join((attr_address, f'lawbookarticles%5B%5D={part}+%F7.{chapter}'))
                    else:
                        attr_address = '&'.join((attr_address, f'lawbookarticles%5B%5D={part}'))
                continue

            attr_address = '&'.join((attr_address, f'{attr_key}={self.attrs.get(attr_key)}'))

        return ''.join((court_address, attr_address[1:]))

    def single_parse_responce(self, court='pskov'):

        browser = webdriver.Firefox()
        # options = Options()
        # options.headless = True
        # browser = webdriver.Chrome("/usr/bin/chromedriver", options=options)

        url_address = self.generate_url(court)
        browser.get(url_address)

        # if it is not error window
        try:
            assert f'{self.title_dict.get(court)}' in browser.title
        except AssertionError as e:
            self.logger_attr_parser.exception(f"Can not get page from address {url_address}. "
                                              f"Page title is {browser.title}")
            raise e
        else:
            page = (browser.page_source).encode('cp1251')
        finally:
            sleep(randint(5, 20))
            browser.close()

        soup = BeautifulSoup(page, from_encoding='cp1251', features='lxml')

        # If no data exist at this page
        text = soup.find('div', id='error')
        if text:
            if 'Данных по запросу не обнаружено' in text.text:
                return []
        else:
            table = soup.find('table', id='tablcont')
            try:
                assert table
            except AssertionError as e:
                self.logger_attr_parser.exception(f"Can not parse page {browser.title} with bs4.")
                raise e

            table_body = table.find("tbody")
            rows = list()
            # table_headers = list(map(lambda x: x.text, table.find_all('th')))
            for index, tr in enumerate(table_body.find_all('tr')[1:]):
                rows.append([])
                for td in tr.find_all('td'):
                    rows[index].append((td.text).strip())

            # rows.extend([table_headers])
            return rows

    def all_parse_response(self):

        result = dict()
        for court in self.url_court:
            result[court] = self.single_parse_responce(court)

        return result

    def set_day_from(self, day_from):
        assert isinstance(day_from, str)
        self.attrs['adm_case__ENTRY_DATE1D'] = day_from

    def set_day_for(self, day_for):
        assert isinstance(day_for, str)
        self.attrs['adm_case__ENTRY_DATE2D'] = day_for


if __name__ == '__main__':
    instance = sudrf_parser()
