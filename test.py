import requests


def error():
    print("Error!!")


def url(rest):
    return "http://127.0.0.1:5000" + rest


def print_drivers():
    response = requests.get(url("/drivers/driver/"))
    print(response.json())


def new_driver():
    dr = {'first_name': 'John', 'last_name': 'Smith'}
    response = requests.post(url("/drivers/driver/"), json=dr)
    print(response.json())


if __name__ == "__main__":
    new_driver()
    print_drivers()
