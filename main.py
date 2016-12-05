import os
import config
import requests
from time import sleep
from parsers import GetPostDataParser, GetTotalPageParser, GetImageUrlParser, \
    GetImageDownloadUrlParser


client = requests.session()
home_url = 'http://www.shutterstock.com'
login_url = 'https://accounts.shutterstock.com/login'
download_history_url = 'http://www.shutterstock.com/download_history.mhtml'
download_image_url = 'https://www.shutterstock.com/download/media/{0}'


def test_network():
    try:
        requests.get('https://www.google.com.tw/')
    except Exception:
        print('No network')
        exit()
    else:
        print('Network is ok')


def login():
    login_parser = GetPostDataParser()
    login_page = client.get(login_url).text
    login_parser.feed(login_page)
    post_data = login_parser.post_data
    post_data['username'] = config.accounts
    post_data['password'] = config.password
    login_result = client.post(url=login_url,
                               data=post_data)
    if login_url in login_result.url:
        print('Login fail')
        exit()
    else:
        print('Login success with user {0}'.format(config.accounts))
        return


def get_total_page():
    get_total_page_parser = GetTotalPageParser()
    download_history_page = client.get(url=download_history_url)
    get_total_page_parser.feed(download_history_page.text)
    print('\nTotal page:', get_total_page_parser.total_page)
    return get_total_page_parser.total_page


def get_images_download_url(total_page, start_page=1):
    for page in range(int(start_page), int(total_page)+1):
        print('\nDownloading page: {0}'.format(page))
        os.system('mkdir \"./download_images/page_{0}\"'.format(page))
        get_params = {'license': 'all',
                      'year': 'all_years',
                      'total_pages': total_page,
                      'page': page}
        download_history_page = client.get(url=download_history_url,
                                           params=get_params)
        get_images_download_url_parser = GetImageDownloadUrlParser()
        get_images_download_url_parser.feed(download_history_page.text)
        download_url_list = get_images_download_url_parser.images_download_url
        download_images(page, download_url_list)


def download_images(page, download_url_list):
    download_count = 0
    for image_url in download_url_list:
        download_count += 1
        download_confirm_page = client.get('{0}{1}'.format(home_url,
                                                           image_url))
        image_id = download_confirm_page.url.split('?')[0].split('/')[-1]
        print('Downloading image\'s id is {0}'.format(image_id))
        get_image_infor = GetPostDataParser()
        get_image_infor.feed(download_confirm_page.text)
        download_page = client.post(url=download_image_url.format(image_id),
                                    data=get_image_infor.post_data)
        get_image_url_parser = GetImageUrlParser()
        get_image_url_parser.feed(download_page.text)
        image = client.get(url=get_image_url_parser.image_url,
                           stream=True)
        image_filename = get_image_url_parser.image_url.split('/')[-1]
        image_fullpath = './download_images/page_{0}/{1}' \
                         .format(page, image_filename)
        print('Downloading image <{0}>...... '.format(image_filename))
        with open(image_fullpath, 'wb')as image_file:
            for chunk in image:
                print('size(kb):', os.path.getsize(image_fullpath)/1024,
                      end='\r')
                image_file.write(chunk)
        print('\n\nSleeping ......')
        if download_count % 50 == 0:
            sleep(60)
        else:
            sleep(3)
        print('Wake up')


def main():
    print('Testing network......')
    test_network()
    print('\nTrying to login......')
    login()
    total_page = int(get_total_page())
    try:
        start_page = int(input('Start download at page: '))
        if start_page > total_page:
            print('start page can\'t bigger than total page, cancal download')
            exit()
    except Exception:
        print('Not a number, cancal download')
        exit()
    else:
        get_images_download_url(total_page, start_page)


if __name__ == '__main__':
    main()
