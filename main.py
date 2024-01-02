import psycopg2
from tabulate import tabulate

db_params = {
    'host': 'localhost',
    'database': 'jobs_database',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432'
}

query_1 = '''
SELECT
  w.writer_name,
  COUNT(DISTINCT wr.comic_id) AS total_comics_written
FROM
  Writer w
  JOIN Written wr ON w.writer_id = wr.writer_id
GROUP BY
  w.writer_id;
'''

query_2 = '''
SELECT
  EXTRACT(YEAR FROM date) AS comic_year,
  COUNT(DISTINCT comic_id) AS total_comics
FROM
  Written
GROUP BY
  comic_year
ORDER BY
  comic_year;
'''

query_3 = '''
SELECT
  comic_format,
  COUNT(comic_id) AS total_comics
FROM
  Comic
GROUP BY
  comic_format;
'''

def execute_query(cursor, query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def print_query_results(query, result, cursor):
    print(f"\nQuery: {query}\n")
    headers = [desc[0] for desc in cursor.description]
    print(tabulate(result, headers, tablefmt="pretty"))

def main():
    connection = psycopg2.connect(
        user=db_params['user'],
        password=db_params['password'],
        dbname=db_params['database'],
        host=db_params['host'],
        port=db_params['port']
    )

    with connection.cursor() as cursor:
        result_1 = execute_query(cursor, query_1)
        print_query_results(query_1, result_1, cursor)

        result_2 = execute_query(cursor, query_2)
        print_query_results(query_2, result_2, cursor)

        result_3 = execute_query(cursor, query_3)
        print_query_results(query_3, result_3, cursor)

if __name__ == '__main__':
    main()