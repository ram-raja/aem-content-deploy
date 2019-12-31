import json
import requests
from requests.auth import HTTPBasicAuth


def read_config():
    try:
        with open('config.json') as config_file:
            data = json.load(config_file)
    except IOError:
        print("File not found")

    return data


def get_package_name():
    TWEED = 'redwood'
    SPECTRUM = 'solace'
    BRANDS = 'brands'
    print("1) Tweed")
    print("2) Spectrum")
    print("3) Brands\n")
    package = int(input("Enter content package to deploy >> "))
    print(package)

    if package == 1:
        return TWEED
    elif package == 2:
        return SPECTRUM
    elif package == 3:
        return BRANDS
    else:
        print("WRONG INPUT")


def get_version(username, password, host, content_package, headers):
    url = "http://{0}/etc/packages/com.canopygrowth.{1}/{1}-content.zip/jcr%3acontent/vlt%3adefinition.json".format(host, content_package)
    r = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
    resp_json = json.loads(r.text)
    version = int(resp_json['version'])
    return version


def update_version(username, password, host, content_package, version, headers):
    url = "http://{}/crx/packmgr/update.jsp".format(host)
    payload = {
        'packageName': '{}-content'.format(content_package),
        'groupName': 'com.canopygrowth.{}'.format(content_package),
        'version': version+1,
        'path': '/etc/packages/com.canopygrowth.{0}/{0}-content.zip'.format(content_package)
    }
    r = requests.post(url=url, auth=HTTPBasicAuth(username, password), params=payload, verify=False)
    if r.status_code == 200:
        print("Version bumped")


def main():
    data = read_config()
    username = data['username']
    password = data['password']
    staging = data['staging']
    prod = data['prod']
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}
    content_package = get_package_name()
    content_package = 'brands'
    version = get_version(username, password, staging, content_package, headers)
    update_version(username, password, staging, content_package, version, headers)
    print(version)


if __name__ == '__main__':
    main()
