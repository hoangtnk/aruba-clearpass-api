#!/usr/bin/env python3
#
# Use ClearPass API to delete all endpoints of a specific user

from apis import get_token, get_user_endpoints, delete_user_endpoints


if __name__ == "__main__":
    access_token = get_token()
    headers = {"Authorization": "Bearer {0}".format(access_token)}
    user_endpoints = get_user_endpoints(headers, "username@example.com")
    delete_user_endpoints(headers, user_endpoints)
