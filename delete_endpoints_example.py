#!/usr/bin/env python3
#
# Example usage of using ClearPass API to delete user endpoints

from clearpass_api import ClearPassAPI


def main():

    data = {
        "host": "clearpass.example.com",
        "grant_type": "password",
        "client_id": "yourid",  # e.g. QuickAccess
        "client_secret": "yoursecret",
        "username": "youruser",
        "password": "yourpass"
    }

    clearpass_api = ClearPassAPI(**data)
    endpoints = clearpass_api.get_endpoints("username@example.com")
    if clearpass_api.delete_endpoints(endpoints):
        print("Deleted all user endpoints.")


if __name__ == "__main__":
    main()
