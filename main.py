import attr_parser_selenium
import db

parser = attr_parser_selenium.sudrf_parser()
parser_result = parser.all_parse_response()
# Make it rerun once a week and set
# parser.set_day_from('')

with open('temp.txt', 'w') as fp:
    fp.write(str(parser_result))

data_base = db.data_base()
data_base.write_to_database(parser_result)


