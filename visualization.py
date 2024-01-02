import psycopg2
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt

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
        result_1 = pd.DataFrame(result_1)

        def my_fmt(x):
            return '{:.1f}%\n({:.0f})'.format(x, result_1.shape[0] * x / 100)

        plt.figure(figsize=(14, 6))

        plt.subplot(131)
        plt.title("Number of comics per author")
        plt.pie(x=result_1[1], labels=result_1[0], autopct=my_fmt)

        result_2 = execute_query(cursor, query_2)
        result_2 = pd.DataFrame(result_2)
        plt.subplot(132)
        plt.title("Number of comics per year")
        plt.xticks(result_2[0])
        plt.yticks(list(range(1, 5)))
        plt.plot(result_2[0], result_2[1], linewidth=3)

        plt.subplot(133)
        plt.title("Comics by format")
        result_3 = execute_query(cursor, query_3)
        result_3 = pd.DataFrame(result_3)
        plt.yticks(list(range(1, 5)))
        plt.bar(result_3[0], result_3[1])
 
        plt.tight_layout()

        plt.show()

if __name__ == '__main__':
    main()