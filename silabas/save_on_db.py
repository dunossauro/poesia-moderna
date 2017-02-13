import pandas.io.sql as pd_sql
from pandas import read_csv
from sqlite3 import connect

con = connect('pt_base.db')
df = read_csv('divisaosilabica.csv')

pd_sql.to_sql(df, 'silabas', con)
con.commit()
con.close()
