import pytest
import pymysql





def pytest_addoption(parser):
    parser.addoption("--db-host", default="192.168.0.101", help="Database host")
    parser.addoption("--db-port", type=int, default=3306, help="Database port")
    parser.addoption("--db-name", default="bitnami_opencart", help="Database name")
    parser.addoption("--db-user", default="bn_opencart", help="Database user")
    parser.addoption("--db-password", default="", help="Database password")


@pytest.fixture(scope="session")
def connection(request) -> pymysql.Connection:
    """Фикстура для установки соединения с БД"""
    conn = pymysql.connect(
        host=request.config.getoption("--db-host"),
        port=request.config.getoption("--db-port"),
        database=request.config.getoption("--db-name"),
        user=request.config.getoption("--db-user"),
        password=request.config.getoption("--db-password"),
        cursorclass=pymysql.cursors.DictCursor
    )

    yield conn
    conn.close()