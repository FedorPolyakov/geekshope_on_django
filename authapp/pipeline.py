from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile, ShopUser


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200')),
                                                    access_token=response['access_token'],
                                                    v='5.92')),
                              None
                              ))

        resp = requests.get(api_url)
        print(resp.content)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        print(data)
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.about_me = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
            user.age = age

        if data['photo_200']:
            get_avatar = requests.get(data['photo_200'])
            with open(f'{settings.BASE_DIR}/media/users_avatars/{user.id}.jpg', 'wb') as photo:
                photo.write(get_avatar.content)
            # avatar_url = data['photo_200']
            # user.avatar = avatar_url
            user.avatar = f'users_avatars/{user.id}.jpg'

    elif backend.name == 'google-oauth2':
        # api_url = urlunparse(('https',
        #                       'www.googleapis.com',
        #                       '/auth/user.birthday.read',
        #                       None,
        #                       urlencode(OrderedDict(fields=','.join(('date')),
        #                                             access_token=response['access_token'],
        #                                             v='1')),
        #                       None
        #                       ))
        #
        # resp = requests.get(api_url)
        # data = resp.json()['response']
        # print('resp', '-----',resp)
        # print(data)
        # print(response['openid'])
        print(response)
        # print(response['scope'][0])
        if response['picture']:
            get_avatar = requests.get(response['picture'])
            print(settings.BASE_DIR)
            with open(f'{settings.BASE_DIR}/media/users_avatars/{user.id}.jpg', 'wb') as photo:
                photo.write(get_avatar.content)
            user.avatar = f'users_avatars/{user.id}.jpg'
    elif backend.name == 'github':
        print(response)
    else:
        return

    user.save()