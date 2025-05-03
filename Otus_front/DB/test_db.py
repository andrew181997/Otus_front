import pymysql

from db import create_user, get_customer, execute_update, execute_query
import pytest
from typing import Dict


TEST_USERS = [
    {
        "firstname": "Иван",
        "lastname": "Петров",
        "email": "ivan.petrov@example.com",
        "customer_group_id": 1,
        "language_id": 1,
        "telephone": "+79161234567"
    },
    {
        "firstname": "Мария",
        "lastname": "Сидорова",
        "email": "maria.sidorova@example.com",
        "customer_group_id": 2,
        "language_id": 2,
        "telephone": "+79035551234"
    },
    {
        "firstname": "Андрейй",
        "lastname": "Демидов",
        "email": "andrey.demidov@example.com",
        "customer_group_id": 1,
        "language_id": 1,
        "telephone": "89065512902"
    }
]
CREATE_CUSTOMER_DATA = {
        'firstname': 'Иван',
        'lastname': 'Петров',
        'email': 'ivan.petrov@example.com',
        'telephone': '+79161234567',
        'customer_group_id': 1,
        'language_id': 1
    }
UPDATE_CUSTOMER_DATA = {
    'firstname': 'НовоеИмя',
    'lastname': 'НоваяФамилия',
    'email': 'new.email@example.com',
    'telephone': '+79005553535'
}


@pytest.mark.parametrize("user_data", TEST_USERS, ids=[user["email"] for user in TEST_USERS])
def test_user_creation(connection, user_data: Dict):
    """Параметризированный тест создания пользователя"""
    # Создаем пользователя
    result = create_user(
        conn=connection,
        firstname=user_data["firstname"],
        lastname=user_data["lastname"],
        email=user_data["email"],
        customer_group_id=user_data["customer_group_id"],
        language_id=user_data["language_id"],
        telephone=user_data["telephone"]
    )

    # Проверяем что пользователь создан
    assert result is not None, "Пользователь не был создан"
    assert isinstance(result["customer_id"], int), "ID пользователя должен быть целым числом"

    # Получаем данные созданного пользователя
    created_user = get_customer(connection, result["customer_id"])
    print(created_user)


def test_customer_lifecycle(connection: pymysql.Connection):
    """Полный цикл тестирования: создание -> обновление -> проверка"""
    # 1. Шаг создания пользователя
    test_data = CREATE_CUSTOMER_DATA

    # Создаем пользователя
    created_user = create_user(connection, **test_data)
    assert created_user is not None, "Не удалось создать пользователя"
    customer_id = created_user['customer_id']
    print(f"\nСоздан пользователь ID {customer_id}")

    try:
        # 2. Шаг обновления данных
        update_data = UPDATE_CUSTOMER_DATA

        # Формируем UPDATE запрос
        set_clause = ", ".join([f"{k} = %s" for k in update_data.keys()])
        update_query = f"""
            UPDATE oc_customer 
            SET {set_clause}
            WHERE customer_id = %s
        """
        update_params = list(update_data.values()) + [customer_id]

        # Выполняем обновление
        affected_rows = execute_update(connection, update_query, update_params)
        assert affected_rows == 1, "Должна обновиться ровно одна запись"
        print("Данные пользователя обновлены")

        # 3. Шаг проверки изменений
        updated_user = get_customer(connection, customer_id)
        assert updated_user is not None, "Пользователь не найден после обновления"

        # Проверяем, что все поля обновились
        for field, new_value in update_data.items():
            assert updated_user[field] == new_value, (
                f"Поле {field} не обновилось. "
                f"Ожидалось: {new_value}, Получено: {updated_user[field]}"
            )

        print("\nПроверка изменений:")
        for field in update_data:
            print(f"{field}: {test_data[field]} -> {updated_user[field]}")

    finally:
        # Очистка - удаляем тестового пользователя
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM oc_customer WHERE customer_id = %s", (customer_id,))
            connection.commit()
        print(f"\nТестовый пользователь ID {customer_id} удален")


def test_update_customer_negative(connection: pymysql.Connection):
    """Тест проверяет, что обновление несуществующего клиента не происходит"""
    # 1. Генерируем несуществующий ID
    nonexistent_id = 999999

    # 2. Проверяем, что такого пользователя действительно нет
    nonexistent_user = get_customer(connection, nonexistent_id)
    assert nonexistent_user is None, "Тест невалиден: пользователь с таким ID существует"

    # 3. Шаг обновления данных
    update_data = UPDATE_CUSTOMER_DATA

    # 4. Формируем UPDATE запрос
    set_clause = ", ".join([f"{k} = %s" for k in update_data.keys()])
    update_query = f"""
        UPDATE oc_customer 
        SET {set_clause}
        WHERE customer_id = %s
    """
    update_params = list(update_data.values()) + [nonexistent_id]

    # 5. Выполняем обновление и проверяем, что ни одна запись не обновилась
    affected_rows = execute_update(connection, update_query, update_params)
    assert affected_rows == 0, "При обновлении несуществующего пользователя должно быть 0 обновленных записей"

def test_create_and_delete_customer(connection: pymysql.Connection):
    """Тест создания и удаления клиента с проверкой через get_customer"""
    # 1. Создание пользователя
    test_data = CREATE_CUSTOMER_DATA

    created_user = create_user(connection, **test_data)
    assert created_user is not None, "Не удалось создать пользователя"
    customer_id = created_user['customer_id']

    # 2. Удаление пользователя
    delete_query = "DELETE FROM oc_customer WHERE customer_id = %s"
    execute_query(connection, delete_query, [customer_id])
    connection.commit()  # Не забываем сделать коммит
    print(f"Пользователь ID {customer_id} удален")

    # 3. Проверка через get_customer
    deleted_user = get_customer(connection, customer_id)
    assert deleted_user is None, f"Пользователь с ID {customer_id} не был удален"


def test_delete_nonexistent_customer(connection: pymysql.Connection):
    """Тест проверяет, что попытка удаления несуществующего пользователя не приводит к ошибке"""
    # 1. Генерируем заведомо несуществующий ID
    nonexistent_id = 999999

    # 2. Проверяем, что пользователя действительно нет в БД
    check_query = "SELECT 1 FROM oc_customer WHERE customer_id = %s"
    result = execute_query(connection, check_query, [nonexistent_id])
    assert len(result) == 0, "Тест невалиден: пользователь с таким ID существует"

    # 3. Пытаемся удалить несуществующего пользователя
    delete_query = "DELETE FROM oc_customer WHERE customer_id = %s"
    try:
        # Выполняем запрос на удаление
        execute_query(connection, delete_query, [nonexistent_id])
        connection.commit()  # Явный коммит

        # Проверяем, что ни одна запись не была удалена
        with connection.cursor() as cursor:
            cursor.execute(delete_query, (nonexistent_id,))
            assert cursor.rowcount == 0, "При удалении несуществующего пользователя должно быть 0 удаленных записей"


    except pymysql.Error as e:
        pytest.fail(f"Удаление несуществующего пользователя вызвало ошибку: {e}")

