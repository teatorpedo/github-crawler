"""Functions for Github API points"""

import requests
import yaml
import csv
import time

import link_header

BASE_URL = "https://api.github.com"

keys = yaml.load(open("keys.yaml"))["keys"]
auths = [(k, v) for k, v in keys.items()]

output = "repos_" + str(int(time.time())) + ".txt"

def get_repositories(stop=None, last=None):
    """Get list of repositories"""

    n = 0
    repos, next_link = _get_page(BASE_URL + "/repositories", n)
    _write_out(_parse_repo_data(repos))

    count = len(repos)
    n += 1
    while repos:

        if stop and count >= stop:
            break

        repos, next_link = _get_page(next_link, n)
        _write_out(_parse_repo_data(repos))
        count += len(repos)
        n += 1

        # throttle
        print next_link
        time.sleep(0.18)

def _get_page(url, n):
    """Get a page of the API point with the given key"""

    r = requests.get(url, auth=auths[n%4])

    if r.status_code != 200:
        print auths[n%4][0], "hit rate limit"
        print r.headers.get("X-RateLimit-Remaining")
        return list(), url

    print r.headers.get("X-RateLimit-Remaining")
    repos = r.json()
    links = link_header.parse(r.headers.get("link"))
    next_link = links["next"]

    return repos, next_link

def _parse_repo_data(data):
    """Parse the repo data and extract info"""

    results = list()
    for repo in data:
        if not repo.get("fork"):
            results.append(repo["name"])

    return results

def _write_out(data):
    """Write out to file"""
    with open(output, "a") as f:
        for item in data:
            f.write(item.encode("utf8") + "\n")

