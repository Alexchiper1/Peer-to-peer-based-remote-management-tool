from jsonrpcserver import Success, method, serve
from jsonrpcclient import request, parse
import requests
import os
import shutil
import platform

serverNumber = "1"
portNumber = "5001"

myFriends = []

def callServer(portToCall, functionName, params=None):
    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request(functionName, params=params or {})
        )
        parsed = parse(response.json())
        return parsed.result
    except:
        return "error"

@method
def ping():
    print("found ping command", flush=True)
    return Success("pong")

@method
def make_folder(name):
    print("found make_folder command", flush=True)
    print("folder name: " + str(name), flush=True)
    os.makedirs(name, exist_ok=True)
    return Success("folder created")

@method
def delete_folder(name):
    print("found delete_folder command", flush=True)
    print("folder name: " + str(name), flush=True)
    if os.path.exists(name):
        shutil.rmtree(name)
        return Success("folder deleted")
    return Success("folder not found")

@method
def whoareyou():
    print("found whoareyou command", flush=True)
    return Success("I am server " + serverNumber + " on port " + portNumber)

@method
def get_version():
    print("found get_version command", flush=True)
    return Success(platform.python_version())

@method
def search(name):
    print("found search command", flush=True)
    print("search name: " + str(name), flush=True)
    files = os.listdir(".")
    if name in files:
        return Success(name + " found")
    return Success(name + " not found")

@method
def startup(x):
    print("found startup command", flush=True)
    print("starting server: " + str(x), flush=True)
    os.system("start python s.py " + str(x))
    online("500" + str(x))
    return Success("started server on port 500" + str(x))

@method
def shutdown(x):
    print("found shutdown command", flush=True)
    print("shutdown server: " + str(x), flush=True)
    result = callServer("500" + str(x), "shutdown_now")
    offline("500" + str(x))
    return Success(result)

@method
def list_friends():
    print("found list_friends command", flush=True)
    return Success(myFriends)

@method
def online(x):
    print("found online command", flush=True)
    print("online port: " + str(x), flush=True)

    if x not in myFriends and x != portNumber:
        myFriends.append(x)

    for friend in myFriends:
        if friend != x:
            callServer(friend, "add_friend", {"x": x})

    return Success("server " + str(x) + " online")

@method
def offline(x):
    print("found offline command", flush=True)
    print("offline port: " + str(x), flush=True)

    if x in myFriends:
        myFriends.remove(x)

    for friend in myFriends:
        callServer(friend, "remove_friend", {"x": x})

    return Success("server " + str(x) + " offline")

@method
def add_friend(x):
    print("found add_friend command", flush=True)
    print("add friend: " + str(x), flush=True)

    if x not in myFriends and x != portNumber:
        myFriends.append(x)

    return Success("friend added")

@method
def remove_friend(x):
    print("found remove_friend command", flush=True)
    print("remove friend: " + str(x), flush=True)

    if x in myFriends:
        myFriends.remove(x)

    return Success("friend removed")

@method
def heartbeat():
    print("found heartbeat command", flush=True)
    results = []

    for friend in myFriends:
        result = callServer(friend, "ping")
        results.append("port " + str(friend) + " : " + str(result))

    return Success(results)

@method
def pass_message(msg, x, visited=None):
    print("found pass_message command", flush=True)
    print("message: " + str(msg), flush=True)
    print("target server: " + str(x), flush=True)

    if visited is None:
        visited = []

    visited.append(portNumber)

    if serverNumber == str(x):
        return Success("message received: " + msg)

    for friend in myFriends:
        if friend not in visited:
            result = callServer(friend, "pass_message", {
                "msg": msg,
                "x": x,
                "visited": visited
            })

            if result != "error":
                return Success(result)

    return Success("target not found")

@method
def shutdown_now():
    print("found shutdown_now command", flush=True)
    quit()

if __name__ == "__main__":
    print("Server running on port 5001...", flush=True)
    serve(port=5001)