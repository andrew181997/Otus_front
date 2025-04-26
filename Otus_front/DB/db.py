
import pymysql
from typing import Optional, Dict, Union, Any, List
from datetime import datetime

def create_user(
        conn: pymysql.Connection,
        firstname: str,
        lastname: str,
        email: str,
        telephone: str,
        customer_group_id: int = 1,
        language_id: int = 1,
        password: str = "testpassword123",
        newsletter: int = 0,
        status: int = 1,
        ip: str = "127.0.0.1",
        custom_field: str = "{}"
) -> Optional[Dict]:

    try:
        with conn.cursor() as cursor:
            # Создание пользователя
            cursor.execute(
                """INSERT INTO oc_customer (
                    customer_group_id, store_id, language_id, 
                    firstname, lastname, email, telephone, 
                    password, custom_field, 
                    newsletter, ip, status, 
                    safe, token, code, date_added
                ) VALUES (
                    %s, %s, %s, 
                    %s, %s, %s, %s, 
                    %s, %s, 
                    %s, %s, %s, 
                    %s, %s, %s, %s
                )""",
                (
                    customer_group_id, 0, language_id,
                    firstname, lastname, email, telephone,
                    password, custom_field,
                    newsletter, ip, status,
                    0, '', '', datetime.now()
                )
            )
            user_id = cursor.lastrowid
            conn.commit()

            return {
                'customer_id': user_id,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'telephone': telephone,
                'customer_group_id': customer_group_id,
                'status': status
            }

    except pymysql.Error as e:
        conn.rollback()
        print(f"Ошибка при создании пользователя: {e}")
        return None


def get_customer(connection: pymysql.Connection, customer_id: int) -> Dict[str, Any]:
    """Получение данных клиента по ID"""
    with connection.cursor() as cursor:
        sql = "SELECT * FROM oc_customer WHERE customer_id = %s"
        cursor.execute(sql, (customer_id,))
        return cursor.fetchone()


def execute_query(
        connection: pymysql.Connection,
        query: str,
        params: Union[Dict[str, Any], List[Any], None] = None
) -> List[Dict[str, Any]]:
    """Универсальная функция для выполнения SQL-запросов"""
    with connection.cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.fetchall()


def execute_update(
        connection: pymysql.Connection,
        query: str,
        params: Union[Dict[str, Any], List[Any], None] = None
) -> int:
    """Функция для выполнения UPDATE/INSERT запросов"""
    with connection.cursor() as cursor:
        cursor.execute(query, params or ())
        connection.commit()
        return cursor.rowcount