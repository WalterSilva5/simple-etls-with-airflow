github_url = "https://api.github.com/users/{}"
import requests


def run(user_name):
    gitub_url_user =  github_url.format(user_name)
    print("github  url user: ", gitub_url_user)
    return requests.get(gitub_url_user)