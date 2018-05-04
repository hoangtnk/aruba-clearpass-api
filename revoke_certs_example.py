#!/usr/bin/env python3
#
# Example usage of using ClearPass API to revoke user certificates

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
    cert_ids = clearpass_api.get_cert_ids("username@example.com")
    if clearpass_api.revoke_certs(cert_ids, ca_id=2):  # CA no.2 in the list of available CAs
        print("Revoked all user certificates.")


if __name__ == "__main__":
    main()
