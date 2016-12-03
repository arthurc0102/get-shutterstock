import config
import requests
from parsers import GetPostDataParser, GetTotalPageParser


client = requests.session()
home_url = 'http://www.shutterstock.com'
login_url = 'https://accounts.shutterstock.com/login'
download_history_url = 'http://www.shutterstock.com/download_history.mhtml'


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
    login_resualt = client.post(url=login_url,
                                data=post_data)

    if login_url in login_resualt.url:
        print('Login fail')
        exit()
    else:
        print('Login success with user {0}'.format(config.accounts))
        return


def get_total_page():
    get_total_page_parser = GetTotalPageParser()
    download_history_page = client.get(url=download_history_url)

    get_total_page_parser.feed(download_history_page.text)
    print(get_total_page_parser.total_page)


def get_images_id(total_page):
    for page in total_page:
        get_params = {'license': 'all',
                      'year': 'all_years',
                      'total_pages': total_page,
                      'page': page}

        client.get(url=download_history_url,
                   params=get_params)


def download_test():
    url = 'https://www.shutterstock.com/download/confirm/428018086'
    get_params = {'id': '428018086',
                  'size': 'huge_jpg',
                  'src': 'download_history'}
    r1 = client.get(url=url,
                    params=get_params).text
    t = GetPostDataParser()

    t.feed(r1)

    url = 'https://www.shutterstock.com/download/media/428018086'
    post_data = t.post_data
    r2 = client.post(url=url,
                     data=post_data)

    with open('./test.jpg', 'wb') as i:
        for c in r2:
            i.write(c)


def main():
    print('Testing network......')
    test_network()

    print('\nTrying to login......')
    login()

    # print('\nGetting total page.......')
    # get_total_page()

    print('\nDownloading image......')
    download_test()

if __name__ == '__main__':
    main()
