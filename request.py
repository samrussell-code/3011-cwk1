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


def parse_list(*args):
    resp = requests.get(f"{base_url}/list/")
    
    if resp.status_code == 200:
        try:
            data = resp.json() 
            if data:
                for item in data:
                    professors = ", ".join([prof['name'] for prof in item['professors']])  
                    print(f"Module {item['module_code']} - {item['module_name']} ({item['year']} - {item['semester']}):")
                    print(f"  Professors: {professors}")
                    print()
            else:
                print("No data available.")
        except ValueError:
            print("Invalid JSON")
    else:
        print(f"Error code {resp.status_code}")



def parse_view(*args):
    resp = requests.get(f"{base_url}/view/") 
    if resp.status_code == 200:
        try:
            data = resp.json()  # parse JSON
            for professor in data:
                print(f"{professor['professor']} ({professor['id']}) has a rating of {professor['rating']} ({professor['avg_rating']})") 
        except ValueError:
            print("Invalid JSON")
    else:
        print(f"Error code {resp.status_code}")



def parse_average(*args):
    if len(args) < 2:
        print("Usage: python request.py average <professor_id> <module_code>")
        return

    prof_id, mod_code = args[0], args[1]
    resp = requests.get(f"{base_url}/average/", params={'professor_id': prof_id, 'module_code': mod_code})  # add params

    if resp.status_code == 200:  # success code
        try:
            data = resp.json()  # parse JSON
            print(f"The rating of Professor {data['professor']} ({data['id']}) in module {data['module_name']} ({data['module_code']}) is {data['rating']} ({data['avg_rating']})")  # output professor, stars and avg rating
        except ValueError:
            print("Invalid JSON")
    else:
        print(f"Error code {resp.status_code}")





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