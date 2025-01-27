from opencart.admin_page_elements import AdminPage


admin_url = "http://192.168.0.101:8081/administration/"
username = "user"
password = "bitnami"


def test_login_logout(browser):
    admin_page = AdminPage(browser)  # Передаем браузер в объект класса
    admin_page.open_admin_page("http://192.168.0.101:8081/administration/")
    admin_page.login(username, password)
    assert admin_page.is_logged_in(), "Логин не выполнен!"
    admin_page.logout()
    assert admin_page.is_logged_out(), "Разлогин не выполнен!"