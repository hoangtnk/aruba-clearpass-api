#!/usr/bin/env python3

import requests


LOGIN_URL = "https://clearpass.example.com/api/oauth"
LOGIN_DATA = {
    "grant_type": "password",
    "client_id": "QuickAccess",
    "client_secret": "yoursecret",
    "username": "yourusername",
    "password": "yourpassword"
}
REVOKE_DATA = {
    "ca_id": 2,  # CA no.2 in the list of available CAs. This depends on your environment
    "confirm_revoke": "True"
}


def get_token():
    """Get token to make API call."""

    res = requests.post(LOGIN_URL, LOGIN_DATA)
    if res.status_code == 200:
        return res.json()["access_token"]
    else:
        msg = "Error! Server replied with status code {}".format(res.status_code)
        raise ValueError(msg)
    

def get_user_endpoints(headers, full_username):
    """Get all endpoints of a specific user.

    :param headers: HTTP headers containing access token
    :type headers: dictionary

    :param full_username: username in full format (i.e. username@example.com)
    :type full_username: str

    :return: a list of mac addresses
    """

    username, domain = full_username.split("@")
    user_endpoints_url = "https://clearpass.example.com/api/endpoint?filter=%7B%22social_username%22%3A%20%22" \
                         "{0}%40{1}%22%7D".format(username, domain)
    res = requests.get(user_endpoints_url, headers=headers)
    if res.status_code == 200:
        user_endpoints = []
        for i, endpoint in enumerate(res.json()["_embedded"]["items"]):
            user_endpoints.append(endpoint["mac_address"])
        return user_endpoints
    else:
        msg = "Error! Server replied with status code {}".format(res.status_code)
        raise ValueError(msg)


def get_user_cert_ids(headers, full_username):
    """Get all cert IDs belong a specific user. This is required to revoke user certs later.
    
    :param headers: HTTP headers containing access token
    :type headers: dictionary
    
    :param full_username: username in full format (i.e. username@example.com)
    :type full_username: str
    
    :return: a list of cert IDs
    """

    username, domain = full_username.split("@")
    user_certs_url = "https://clearpass.example.com/api/certificate?filter=%7B%22subject_common_name%22%3A%20%22" \
                     "{0}%40{1}%22%7D".format(username, domain)
    res = requests.get(user_certs_url, headers=headers)
    if res.status_code == 200:
        user_cert_ids = [cert["id"] for i, cert in enumerate(res.json()["_embedded"]["items"])]
        return user_cert_ids
    else:
        msg = "Error! Server replied with status code {}".format(res.status_code)
        raise ValueError(msg)


def delete_user_endpoints(headers, user_endpoints):
    """Delete all endpoints of a specific user.

    :param headers: HTTP headers containing access token
    :type headers: dictionary

    :param user_endpoints: a list of mac addresses
    :type user_endpoints: list

    :return: True if deleted successfully
    """

    for endpoint in user_endpoints:
        delete_endpoint_url = "https://clearpass.example.com/api/endpoint/mac-address/{}".format(endpoint)
        requests.delete(delete_endpoint_url, headers=headers)

    print("Deleted all user endpoints successfully")
    return True


def update_user_endpoints(headers, user_endpoints):
    """Update attributes for all endpoints of a specific user.

    :param headers: HTTP headers containing access token
    :type headers: dictionary

    :param user_endpoints: a list of mac addresses
    :type user_endpoints: list

    :return: True if updated successfully
    """

    update_data = {
        "attributes": {
            "social_department": "New Department",
            "social_jobTitle": "New Job Title",
            "social_vip": ""  # this attribute should not be absent
        }
    }

    for endpoint in user_endpoints:
        update_endpoints_url = "https://clearpass.example.com/api/endpoint/mac-address/{}".format(endpoint)
        requests.patch(update_endpoints_url, headers=headers, json=update_data)

    print("Updated all user endpoints successfully")
    return True


def revoke_user_certs(headers, user_cert_ids):
    """Revoke user certs based on cert IDs.

    :param headers: HTTP headers containing access token
    :type headers: dictionary

    :param user_cert_ids: a list of cert IDs
    :type user_cert_ids: list

    :return: True if revoked successfully
    """

    for cert_id in user_cert_ids:
        revoke_certs_url = "https://clearpass.example.com/api/certificate/{}/revoke".format(cert_id)
        requests.post(revoke_certs_url, headers=headers, json=REVOKE_DATA)
        
    print("Revoked all user certs successfully")
    return True
