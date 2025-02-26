import psycopg2
import pandas as pd
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED


def safe_query_to_dataframe(query):
    db_config = {
        "host": "localhost",
        "port": 5432,
        "database": "mydb",
        "user": "grisha",
        "password": "aaa"
    }
    result = {
        'data': pd.DataFrame(),
        'warnings': [],
        'errors': [],
        'success': False
    }
    try:
        with psycopg2.connect(**db_config) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
            conn.autocommit = False  # Для ручного управления транзакцией

            with conn.cursor() as cursor:
                try:
                    # Проверка типа запроса
                    explain_query = sql.SQL("EXPLAIN (FORMAT JSON) {}").format(sql.SQL(query))
                    cursor.execute(explain_query)
                    plan = cursor.fetchone()[0][0]
                    
                    if any(op['Plan']['Node Type'] in ['Insert', 'Update', 'Delete'] for op in plan.get('Plans', [plan])):
                        raise psycopg2.DatabaseError("Запрос содержит операции модификации данных")

                    cursor.execute("SET TRANSACTION READ ONLY")
                    cursor.execute(query)
                    
                    if cursor.description:
                        columns = [desc[0] for desc in cursor.description]
                        data = cursor.fetchall()
                        result['data'] = pd.DataFrame(data, columns=columns)
                    
                    result['warnings'] = conn.notices.copy()
                    
                    conn.rollback()
                    result['success'] = True

                except psycopg2.Error as e:
                    conn.rollback()
                    result['errors'].append(str(e))

    except psycopg2.Error as e:
        result['errors'].append(str(e))
    
    if result['warnings']:
        print("Обнаружены предупреждения:")
        for warn in result['warnings']:
            print(f"• {warn}")
    
    if result['errors']:
        print("Обнаружены ошибки:")
        for err in result['errors']:
            print(f"• {err}")

    return result