import sys
import requests

base_url = "http://127.0.0.1:8000"

def parse_register(*args):
    resp = requests.post(f"{base_url}/register/")
    print("Register:", resp.text)

def parse_login(*args):
    resp = requests.post(f"{base_url}/login/")
    print("Login:", resp.text)

def parse_logout(*args):
    resp = requests.post(f"{base_url}/logout/")
    print("Logout:", resp.text)

import requests

def parse_list(*args):
    resp = requests.get(f"{base_url}/list/")
    
    if resp.status_code == 200:  #success code
        try:
            data = resp.json()  # parse
            print("List:", data)  # print
        except ValueError:
            print("Invalid JSON")
    else:
        print(f"Error code {resp.status_code}")

def parse_view(*args):
    resp = requests.get(f"{base_url}/view/")
    print("View:", resp.text)

def parse_average(*args):
    resp = requests.get(f"{base_url}/average/")
    print("Average:", resp.text)

def parse_rate(*args):
    resp = requests.post(f"{base_url}/rate/")
    print("Rate:", resp.text)

def main():
    if len(sys.argv) < 2:
        print("Usage: python request.py <command_name> <command_args*(if required)>")
        return
    
    func_name = sys.argv[1]
    args = sys.argv[2:]  # extra arguments after cmd name

    # dictionary lookup faster than if else block
    func_map = {
        "register": parse_register,
        "login": parse_login,
        "logout": parse_logout,
        "list": parse_list,
        "view": parse_view,
        "average": parse_average,
        "rate": parse_rate,
    }

    # call function got from dictionary
    func = func_map.get(func_name)

    if func:
        func(*args)
    else:
        print(f"Unknown function: {func_name}")

if __name__ == "__main__":
    main()