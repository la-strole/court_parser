from datetime import datetime
import os
import logging
import sqlite3
from sqlite3 import Error


class data_base:
    def __init__(self):

        # Logging
        self.logger_db = logging.getLogger('db.py')
        f_handler = logging.FileHandler('file.log')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        self.logger_db.addHandler(f_handler)

        # create db if it is not exist
        self.db_name = 'court.db'
        if not os.path.isfile(f'{self.db_name}'):
            self.create_db()

    def create_db(self):
        """ Create database at ./court.db

        """
        if os.path.isfile(f'{self.db_name}'):
            self.logger_db.error(f"Can not create new database. File with db court.db already exist.")
            raise RuntimeError(f"file with db court.db already exist")
        else:
            with open('schema.sql') as fp:
                with sqlite3.connect(f'{self.db_name}') as con:
                    try:
                        con.executescript(fp.read())
                        con.commit()
                    except Error as e:
                        self.logger_db.error(f'{e}')

    def write_to_database(self, result):
        """ Write to database table courts data from result
        :param result: dictionary from attr_parser.all_parse_response()
        :return: None

        """

        for court_name in result:
            if result[court_name]:
                for row in result[court_name]:

                    id = row[0]
                    date_adoption = row[1]
                    full_name, article = row[2].split('-')
                    judge_full_name = row[3]
                    descision_date = row[4]
                    effective_date = row[6]
                    judicial_act = row[7]
                    date_update = datetime.today().isoformat()

                    with sqlite3.connect(f'{self.db_name}') as con:
                        con.row_factory = sqlite3.Row
                        try:
                            con.execute(
                                "insert into courts(court_name, id, full_name, article, judge_full_name, "
                                "date_adoption, decision_date, effective_date, judicial_act, date_update) "
                                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (court_name,
                                                                          id,
                                                                          full_name.strip(),
                                                                          article.strip(),
                                                                          judge_full_name,
                                                                          date_adoption,
                                                                          descision_date,
                                                                          effective_date,
                                                                          judicial_act,
                                                                          date_update))
                            con.commit()
                        except Error as e:
                            self.logger_db.exception(f"Error inserting data for {court_name}. {e}")

            else:
                continue

