from jsonrpcclient import request, parse
import requests

PORT = 5001

def sendToServer(functionName, params=None):
    response = requests.post(
        f"http://localhost:{PORT}/",
        json=request(functionName, params=params or {})
    )
    parsed = parse(response.json())
    return parsed.result

print("Welcome!")

while True:
    print("please type a menu option")
    print("1. ping")
    print("2. make_folder")
    print("3. delete_folder")
    print("4. whoareyou")
    print("5. get_version")
    print("6. search")
    print("7. startup")
    print("8. shutdown")
    print("9. list_friends")
    print("10. heartbeat")
    print("11. pass")
    print("12. exit")

    option = int(input())

    if option == 12:
        break

    try:
        if option == 1:
            print(sendToServer("ping"))

        elif option == 2:
            print("folder name?")
            name = input()
            print(sendToServer("make_folder", {"name": name}))

        elif option == 3:
            print("folder name?")
            name = input()
            print(sendToServer("delete_folder", {"name": name}))

        elif option == 4:
            print(sendToServer("whoareyou"))

        elif option == 5:
            print(sendToServer("get_version"))

        elif option == 6:
            print("file name?")
            name = input()
            print(sendToServer("search", {"name": name}))

        elif option == 7:
            print("server number to start?")
            x = input()
            print(sendToServer("startup", {"x": x}))

        elif option == 8:
            print("server number to shutdown?")
            x = input()
            print(sendToServer("shutdown", {"x": x}))

        elif option == 9:
            print(sendToServer("list_friends"))

        elif option == 10:
            print(sendToServer("heartbeat"))

        elif option == 11:
            print("message?")
            msg = input()
            print("target server number?")
            x = input()
            print(sendToServer("pass_message", {"msg": msg, "x": x}))

        else:
            print("unknown option")

    except:
        print("error")