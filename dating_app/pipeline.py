# -*- coding: utf-8 -*-
import logging
import requests
from django.core.files.base import ContentFile


def get_profile_image(backend, user, response, is_new=False, *args, **kwargs):
    if user is None:
        return None

    elif backend.name == 'vk-oauth2':
        avatar_url = response['photo']
        print(avatar_url)
    else:
        avatar_url = None

    if avatar_url and is_new:
        print('ok')
        try:
            avatar_resp = requests.get(avatar_url, params={'type': 'large'})
            print(avatar_resp)
            avatar_resp.raise_for_status()
        except requests.HTTPError as e:
            logging.error(e)
        else:
            avatar_file = ContentFile(avatar_resp.content)
            print(avatar_file)
            # full_name = "%s %s" % (response['first_name'],
            #                       response['last_name'])

            user.userprofile.avatar.save("{0}.jpg".format(user.pk), avatar_file)
            # user.full_name = full_name
            user.userprofile.save(update_fields=['avatar', ])
