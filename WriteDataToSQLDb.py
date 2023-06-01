from Utilities.DB_Utils import DatabaseUtility

db_util = DatabaseUtility('db_config.json')
# db_util.create_schema('TEST')
# db_util.create_course_record_table()
db_util.select_course_record()
db_util.close_connection()
