def get_avatar(request, backend, strategy, details, response, user=None, *args, **kwargs):
    url = None
    # if backend.name == 'facebook':
    #     url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
    # if backend.name == 'twitter':
    #     url = response.get('profile_image_url', '').replace('_normal','')
    if backend.name == 'google-oauth2':
        try:
            url = response["picture"]
        except KeyError:
            url = response['image'].get('url')

        get_file = download(url)
        file_name = url.split('/')[-1]
        extension = 'jpeg'

        f = BytesIO(get_file)
        out = BytesIO()

        image = Image.open(f)
        image.save(out, extension)

def download(url):
    try:
        r = requests.get(url)
        if not r.status_code == 200:
            raise Exception('file request failed with status code: ' + str(r.status_code))
        return (r.content)
    except Exception as ex:
        return ('error')