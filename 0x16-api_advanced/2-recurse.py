import requests

def recurse(subreddit, hot_list=None, count=0, after=None):
    if hot_list is None:
        hot_list = []

    headers = {"User-Agent": "Your-User-Agent"}

    # Construct the URL with parameters
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"count": count, "after": after}

    try:
        response = requests.get(url, params=params, headers=headers, allow_redirects=False)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        hot_list += [child["data"]["title"] for child in data["data"]["children"]]

        if not data["data"]["after"]:
            return hot_list

        return recurse(subreddit, hot_list, data["data"]["count"], data["data"]["after"])

    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return None
    except KeyError as e:
        print(f"KeyError: {e}")
        return None

if __name__ == "__main__":
    subreddit = "your_subreddit_name"
    hot_posts = recurse(subreddit)
    if hot_posts:
        for i, post in enumerate(hot_posts, 1):
            print(f"{i}. {post}")
    else:
        print("Failed to fetch hot posts.")

