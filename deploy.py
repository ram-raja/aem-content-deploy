import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
    print("3) Brands")
    print("4) Exit")

    while True:
        try:
            package = int(input("Enter content package to deploy >> "))
            break
        except ValueError:
            print("Please enter a valid number")

    if package == 1:
        return TWEED
    elif package == 2:
        return SPECTRUM
    elif package == 3:
        return BRANDS
    elif package == 4:
        return "EXIT"
    else:
        print("WRONG INPUT")


def get_version(username, password, host, content_package, headers):
    url = "https://{0}/etc/packages/com.canopygrowth.{1}/{1}-content.zip/jcr%3acontent/vlt%3adefinition.json".format(host, content_package)
    r = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
    version = None
    if r.status_code == 200:
        resp_json = json.loads(r.text)
        version = int(resp_json['version'])
    return version


def update_version(username, password, host, content_package, version, headers):
    url = "https://{}/crx/packmgr/update.jsp".format(host)
    payload = {
        'packageName': '{}-content'.format(content_package),
        'groupName': 'com.canopygrowth.{}'.format(content_package),
        'version': version+1,
        'path': '/etc/packages/com.canopygrowth.{0}/{0}-content.zip'.format(content_package)
    }
    r = requests.post(url=url, auth=HTTPBasicAuth(username, password), params=payload, verify=False)
    if r.status_code == 200:
        print("Version bumped")


def rename_package(username, password, host, content_package, version, headers):
    url = "https://{0}/etc/packages/com.canopygrowth.{1}/{1}-content-{2}.zip".format(host, content_package, version+1)
    print(url)
    payload = {
        ':operation': 'move',
        ':dest': '/etc/packages/com.canopygrowth.{0}/{0}-content.zip'.format(content_package)
    }
    r = requests.post(url=url, auth=HTTPBasicAuth(username, password), params=payload, verify=False)
    if r.status_code == 201:
        print("Package Moved")


def build_package(username, password, host, content_package, headers):
    url = "https://{0}/crx/packmgr/service/.json/etc/packages/com.canopygrowth.{1}/{1}-content.zip?cmd=build".format(host, content_package)
    r = requests.post(url=url, auth=HTTPBasicAuth(username, password), verify=False)
    if r.status_code == 200:
        print("Package built")


def download_package(username, password, host, content_package, headers):
    url = "https://{0}/etc/packages/com.canopygrowth.{1}/{1}-content.zip".format(host, content_package)
    r = requests.get(url=url, auth=HTTPBasicAuth(username, password), verify=False)
    if r.status_code == 200:
        with open('./pkg/content.zip', 'wb') as f:
            f.write(r.content)
        print("Package downloaded")


def install_package(username, password, host, headers):
    url = "https://{0}/crx/packmgr/service.jsp".format(host)
    files = {'file': ('content.zip', open('./pkg/content.zip', 'rb'), 'application/zip')}

    payload = {
        'force': 'true',
        'install': 'true'
    }

    print("Installing package to production....")
    r = requests.post(url, auth=HTTPBasicAuth(username, password), params=payload, files=files, verify=False)
    print(r.text)

    if r.status_code == 200:
        print("Package uploaded & installed to production")


def main():
    data = read_config()
    username = data['username']
    password = data['password']
    staging = data['staging']
    prod = data['prod']
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}

    content_package = get_package_name()
    while content_package != 'EXIT':
        version = get_version(username, password, staging, content_package, headers)
        print("Updating {0} version {1}".format(content_package, version))
        update_version(username, password, staging, content_package, version, headers)
        rename_package(username, password, staging, content_package, version, headers)
        build_package(username, password, staging, content_package, headers)
        download_package(username, password, staging, content_package, headers)
        install_package(username, password, prod, headers)
        content_package = get_package_name()


if __name__ == '__main__':
    main()
