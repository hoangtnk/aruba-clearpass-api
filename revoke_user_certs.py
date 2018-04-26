#!/usr/bin/env python3
#
# Use ClearPass API to revoke all certs of a specific user

from api import get_token, get_user_cert_ids, revoke_user_certs


if __name__ == "__main__":
    access_token = get_token()
    headers = {"Authorization": "Bearer {0}".format(access_token)}
    user_cert_ids = get_user_cert_ids(headers, "username@example.com")
    revoke_user_certs(headers, user_cert_ids)

