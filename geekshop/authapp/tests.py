from django.conf import settings
from django.test import TestCase
from django.test.client import Client

# Create your tests here.
from authapp.models import ShopUser


class TestUserManagement(TestCase):
    # исходные данные
    # админ
    ADMIN = 'django'
    EMAIL_ADMIN = 'django@geekshop.local'
    # первый пользователь
    USERNAME_1 = 'STALLONE'
    EMAIL_1 = 'stallone@yandex.local'
    # второй пользователь с именем
    USERNAME_2 = 'Schwarzenegger'
    FIRSTNAME_2 = 'Арнольд'
    EMAIL_2 = 'schwarzenegger@yandex.local'
    # пароль
    PASSWORD = 'geekbrains'

    EXPECTED_SUCCESS_CODE = 200
    EXPECTED_MOVED_TEMP_CODE = 302

    def setUp(self):
        self.client = Client()
        self.superuser = ShopUser.objects.create_superuser(self.ADMIN, self.EMAIL_ADMIN, self.PASSWORD)
        self.user = ShopUser.objects.create_user(self.USERNAME_1, self.EMAIL_1, self.PASSWORD)
        self.user_with_first_name = ShopUser.objects.create_user(self.USERNAME_2, self.EMAIL_2, self.PASSWORD)

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'главная')
        self.assertNotContains(response, 'Пользователь', status_code=self.EXPECTED_SUCCESS_CODE)
        # self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username=self.USERNAME_1, password=self.PASSWORD)

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=self.EXPECTED_SUCCESS_CODE)
        self.assertEqual(response.context['user'], self.user)


    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, self.EXPECTED_MOVED_TEMP_CODE)

        # с логином все должно быть хорошо
        self.client.login(username=self.USERNAME_1, password=self.PASSWORD)

        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('Корзина', response.content.decode())

    def test_user_logout(self):
        # пользователь
        self.client.login(username=self.USERNAME_1, password=self.PASSWORD)

        # заходим в систему
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)
        self.assertFalse(response.context['user'].is_anonymous)

        # выходим из системы
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, self.EXPECTED_MOVED_TEMP_CODE)

        # главная после выхода
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        # переход на регистрацию
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)
        self.assertEqual(response.context['title'], 'регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        # заполняем данные нового пользователя корректно
        new_user_correct_data = {
            'username': 'billmurrey',
            'first_name': 'William',
            'last_name': 'Murrey',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'billmurrey@geekshop.local',
            'age': '70'
        }

        response = self.client.post('/auth/register/', data=new_user_correct_data)
        self.assertEqual(response.status_code, self.EXPECTED_MOVED_TEMP_CODE)

        new_user = ShopUser.objects.get(username=new_user_correct_data['username'])
        activation_url = \
            f'{settings.DOMAIN_NAME}/auth/verify/{new_user_correct_data["email"]}/{new_user.activation_key}/'

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)

        # заходим с данными нового пользователя
        self.client.login(username=new_user_correct_data['username'],
                          password=new_user_correct_data['password1'])

        # заходим в систему
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)
        self.assertFalse(response.context['user'].is_anonymous)

        # переходим на главную страницу
        response = self.client.get('/')
        self.assertContains(response, text=new_user_correct_data['first_name'], status_code=self.EXPECTED_SUCCESS_CODE)

    def test_user_register_failed(self):
        # переход на регистрацию
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)
        self.assertEqual(response.context['title'], 'регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        # заполняем данные нового пользователя некорректно
        new_user_uncorrect_data = {
            'username': 'miketyson',
            'first_name': 'Mike',
            'last_name': 'Tyson',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'miketyson@geekshop.local',
            'age': '10'
        }

        response = self.client.post('/auth/register/', data=new_user_uncorrect_data)
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)
        self.assertFormError(response, 'register_form', 'age', 'Вы слишком молоды')
        # главная после неудачи
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.EXPECTED_SUCCESS_CODE)
        self.assertTrue(response.context['user'].is_anonymous)
