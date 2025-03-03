import sys
import requests

base_url = "http://127.0.0.1:8000"
session = requests.Session()

def parse_register(*args):
    if args:
        print("Usage: register")
        return

    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    resp = requests.post(f"{base_url}/register/", data={"username": username, "email": email, "password": password})

    try:
        data = resp.json()
        if resp.status_code == 201:
            print(f"Registration successful! Your student ID is {data['student_id']}.")
        else:
            print(f"{resp.status_code} {data.get('error', 'Unknown error')}")
    except ValueError:
        print("Invalid response from server.")

def parse_login(*args):
    if len(args) != 1:
        print("Usage: login <url>")
        return

    url = args[0]
    username = input("Enter username: ")
    password = input("Enter password: ")

    resp = session.post(f"{url}/login/", data={"username": username, "password": password})

    try:
        data = resp.json()
        if resp.status_code == 200:
            print(f"Login successful! Welcome, {username}.")
        else:
            print(f"{resp.status_code} {data.get('error', 'Unknown error')}")
    except ValueError:
        print("Unexpected response format. No JSON returned.")

def parse_logout(*args):
    if args:
        print("Usage: logout")
        return

    resp = requests.post(f"{base_url}/logout/")

    try:
        data = resp.json()
        if resp.status_code == 200:
            print("Logout successful.")
        else:
            print(f"{resp.status_code} {data.get('error', 'Unknown error')}")
    except ValueError:
        print("Unexpected response format. No JSON returned.")

def parse_list(*args):
    if args:
        print("Usage: list")
        return

    resp = requests.get(f"{base_url}/list/")
    
    if resp.status_code == 200:
        try:
            data = resp.json()
            if data:
                for item in data:
                    professors = ", ".join([f"{prof['name']} ({prof['id']})" for prof in item['professors']])
                    print(f"Module {item['module_code']} - {item['module_name']} ({item['year']} - {item['semester']}):")
                    print(f"  Professors: {professors}")
                    print()
            else:
                print("No data available.")
        except ValueError:
            print(f"{resp.status_code} Invalid JSON")
    else:
        print(f"{resp.status_code} {resp.text}")

def parse_view(*args):
    if args:
        print("Usage: view")
        return

    resp = requests.get(f"{base_url}/view/")
    if resp.status_code == 200:
        try:
            data = resp.json()
            for professor in data:
                print(f"{professor['professor']} ({professor['id']}) has a rating of {professor['rating']} ({professor['avg_rating']})")
        except ValueError:
            print(f"{resp.status_code} Invalid JSON")
    else:
        print(f"{resp.status_code} {resp.text}")

def parse_average(*args):
    if len(args) != 2:
        print("Usage: average <professor_id> <module_code>")
        return

    prof_id, mod_code = args[0].upper(), args[1].upper()
    resp = requests.get(f"{base_url}/average/", params={'professor_id': prof_id, 'module_code': mod_code})

    try:
        data = resp.json()
    except ValueError:
        print(f"{resp.status_code} Invalid JSON response")
        return

    if resp.status_code == 200:
        print(f"The rating of Professor {data['professor']} ({data['id']}) in module {data['module_name']} ({data['module_code']}) is {data['rating']} ({data['avg_rating']})")
    else:
        error_msg = data.get("error", "Unknown error")
        print(f"{resp.status_code} {error_msg}")  

def parse_rate(*args):
    if len(args) != 5:
        print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")
        return

    try:
        payload = {
            "professor_id": args[0].upper(),
            "module_code": args[1].upper(),
            "year": args[2],
            "semester": args[3],
            "rating": float(args[4]),
        }
    except ValueError:
        print("err: rating must be a valid number.")
        return

    resp = session.post(f"{base_url}/rate/", json=payload)

    try:
        data = resp.json()
    except ValueError:
        print(f"{resp.status_code} Unable to validate")
        return

    if resp.status_code == 201:
        print(f"Rating for professor {data['professor_id']} in module {data['module_code']} ({data['year']}, {data['semester']}) submitted successfully with rating {data['rating']}")
    else:
        error_msg = data.get("error", "Unknown error")
        print(f"{resp.status_code} {error_msg}")

def main():
    while True:
        print("\nEnter a command:")
        print("Available commands: register, login, logout, list, view, average, rate, exit")
        command_input = input("Command: ").strip()
        
        if command_input == "exit":
            print("Exiting...")
            break
        
        args = command_input.split()
        func_name = args[0]
        
        func_map = {
            "register": parse_register,
            "login": parse_login,
            "logout": parse_logout,
            "list": parse_list,
            "view": parse_view,
            "average": parse_average,
            "rate": parse_rate,
        }

        func = func_map.get(func_name)

        if func:
            func(*args[1:])
        else:
            print(f"Unknown function: {func_name}")

if __name__ == "__main__":
    main()
