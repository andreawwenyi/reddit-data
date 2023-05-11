import duckdb
# Read JSON from **filename**, where **filename** can be list of files, or a glob pattern
duckdb.sql("""
select * from read_ndjson(
['../data_in/RC_2018-10.zst', '../data_in/RC_2023-01.zst'], 
columns={'author': 'STRING', 'body': 'STRING'})
""").show()