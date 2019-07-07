import sqlite3

conn = sqlite3.connect('SavedResults.db')
c = conn.cursor()


c.execute('CREATE TABLE IF NOT EXISTS results(date_time TEXT, test_name TEXT, pass_fail TEXT, results_name TEXT)')
conn.commit()
c.close()
conn.close()