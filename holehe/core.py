import time
import random
import importlib
import pkgutil
import string
from termcolor import colored
from bs4 import BeautifulSoup
import hashlib
import re
import sys
import httpx
import trio
from subprocess import Popen, PIPE
import os
import time
import json
from datetime import datetime
try:
    import cookielib
except BaseException:
    import http.cookiejar as cookielib

from holehe.localuseragent import ua


DEBUG = False

__version__ = "1.58.2.3"
checkVersion = httpx.get("https://pypi.org/pypi/holehe/json")

if not DEBUG and checkVersion.json()["info"]["version"] != __version__:
    if os.name != 'nt':
        p = Popen(["pip3",
                   "install",
                   "--upgrade",
                   "git+git://github.com/megadose/holehe@master"],
                  stdout=PIPE,
                  stderr=PIPE)
    else:
        p = Popen(["pip",
                   "install",
                   "--upgrade",
                   "git+git            out.append({"name": name,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return None
            headers['X-Requested-With'] = 'XMLHttpRequest'

            params = {
                'action': 'email_availability',
            }

            data = {
                'email': email,
                'my_post_key': r.text.split('var my_post_key = "')[1].split('"')[0]
            }

            response = await client.post('https://cracked.to/xmlhttp.php', headers=headers, params=params, data=data)
            if "Your request was blocked" not in response.text and response.status_code == 200:
                if "email address that is already in use by another member." in response.text:
                    out.append({"name": name,
                                "rateLimit": False,
                                "exists": True,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
                else:
                    out.append({"name": name,
                                "rateLimit": False,
                                "exists": False,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
            else:
                out.append({"name": name,
                            "rateLimit": True,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
://github.com/megadose/holehe@master"],
                  stdout=PIPE,
                  stderr=PIPE)
    (output, err) = p.communicate()
    p_status = p.wait()
    print("Holehe has just been updated, you can restart it. ")
    exit()


def import_submodules(package, recursive=True):
    """Get all the holehe submodules"""
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def get_functions(modules):
    """Transform the modules objects to functions"""
    websites = []
    for module in modules:
        if len(module.split(".")) > 3:
            modu = modules[module]
            site = module.split(".")[-1]
            websites.append(modu.__dict__[site])
    return websites


def ask_email():
    if len(sys.argv) < 2 or len(sys.argv[1]) < 5:
        exit("[-] Please enter a target email ! \nExample : holehe email@example.com")
    return sys.argv[1]


async def maincore():
    modules = import_submodules("holehe.modules")
    websites = get_functions(modules)

    print('Twitter : @palenath')
    print('Github : https://github.com/megadose/holehe')
    print('For BTC Donations : 1FHDM49QfZX6pJmhjLE5tB2K6CaTLMZpXZ')
    start_time = time.time()

    email = ask_email()
    checkTimeout = httpx.get("https://gravatar.com")
    timeoutValue=int(checkTimeout.elapsed.total_seconds()*6)+5
    #print(timeoutValue)
    client = httpx.AsyncClient(timeout=timeoutValue)
    out = []
    async with trio.open_nursery() as nursery:
        for website in websites:
            nursery.start_soon(website, email, client, out)
    out = sorted(out, key=lambda i: i['name'])  # We sort by modules names
    await client.aclose()

    description = colored("[+] Email used",
                          "green") + "," + colored(" [-] Email not used",
                                                   "magenta") + "," + colored(" [x] Rate limit",
                                                                              "red")
    print("\033[H\033[J")
    print("*" * (len(email)+6))
    print("   "+email)
    print("*" * (len(email)+6))
    for results in out:
        if results["rateLimit"]:
            websiteprint = colored("[x] " + results["name"], "red")
        elif results["exists"] == False:
            websiteprint = colored("[-] " + results["name"], "magenta")
        else:
            toprint = ""
            if results["emailrecovery"] is not None:
                toprint += " " + results["emailrecovery"]
            if results["phoneNumber"] is not None:
                toprint += " / " + results["phoneNumber"]
            if results["others"] is not None and "FullName" in str(results["others"].keys()) :
                toprint += " / FullName " + results["others"]["FullName"]
            if results["others"] is not None and "Date, time of the creation" in str(results["others"].keys()):
                toprint += " / Date, time of the creation " + results["others"]["Date, time of the creation"]

            websiteprint = colored("[+] " + results["name"] + toprint, "green")
        print(websiteprint)

    print("\n" + description)
    print(str(len(websites)) + " websites checked in " +
          str(round(time.time() - start_time, 2)) + " seconds")
    print("\n")
    print('Twitter : @palenath')
    print('Github : https://github.com/megadose/holehe')
    print('For BTC Donations : 1FHDM49QfZX6pJmhjLE5tB2K6CaTLMZpXZ')


def main():
    trio.run(maincore)
