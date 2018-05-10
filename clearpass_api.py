# API object to interact with ClearPass API

import requests


class ClearPassAPI:
    """API object to interact with ClearPass API."""

    def __init__(self, host, grant_type, client_id, client_secret,
                 username, password, verify=True):
        """Initialize API object.

        :param host: IP address or domain name of ClearPass
        :type host: str

        :param grant_type: the type used to grant access token for API client
        :type grant_type: str

        :param client_id: API client ID
        :type client_id: str

        :param client_secret: API client secret
        :type client_secret: str

        :param username: API client username
        :type username: str

        :param password: API client password
        :type password: str

        :param verify: verify SSL certificate
        :type verify: bool
        """

        self.host = host
        login_url = "https://{}/api/oauth".format(self.host)
        login_data = {
            "grant_type": grant_type,
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
            "password": password
        }
        rsp = requests.post(login_url, login_data, verify=verify)
        if rsp.status_code == 200:
            access_token = rsp.json()["access_token"]
            headers = {"Authorization": "Bearer {}".format(access_token)}
            self.headers = headers
        else:
            msg = "Error! Server replied with status code {}".format(rsp.status_code)
            raise ValueError(msg)

    def get_endpoints(self, full_username):
        """Get all endpoints of a certain user.

        :param full_username: username in full format (i.e. username@example.com)
        :type full_username: str

        :return: a list of mac addresses
        """

        username, domain = full_username.split("@")
        endpoints_url = "https://{host}/api/endpoint?filter=%7B%22social_username%22%3A%20%22" \
                        "{username}%40{domain}%22%7D".format(host=self.host,
                                                             username=username,
                                                             domain=domain)
        rsp = requests.get(endpoints_url, headers=self.headers)
        if rsp.status_code == 200:
            endpoints = []
            for i, endpoint in enumerate(rsp.json()["_embedded"]["items"]):
                endpoints.append(endpoint["mac_address"])
            return endpoints
        else:
            msg = "Error! Server replied with status code {}".format(rsp.status_code)
            raise ValueError(msg)

    def get_cert_ids(self, full_username):
        """Get all cert IDs of a certain user. This is required to revoke user certs.

        :param full_username: username in full format (i.e. username@example.com)
        :type full_username: str

        :return: a list of cert IDs
        """

        username, domain = full_username.split("@")
        certs_url = "https://{host}/api/certificate?filter=%7B%22subject_common_name%22%3A%20%22" \
                    "{username}%40{domain}%22%7D".format(host=self.host,
                                                         username=username,
                                                         domain=domain)
        rsp = requests.get(certs_url, headers=self.headers)
        if rsp.status_code == 200:
            cert_ids = [cert["id"] for i, cert in enumerate(rsp.json()["_embedded"]["items"])]
            return cert_ids
        else:
            msg = "Error! Server replied with status code {}".format(rsp.status_code)
            raise ValueError(msg)

    def delete_endpoints(self, endpoints):
        """Delete all endpoints of a certain user.

        :param endpoints: a list of mac addresses
        :type endpoints: list

        :return: True if deleted successfully
        """

        for endpoint in endpoints:
            delete_endpoint_url = "https://{}/api/endpoint/mac-address/{}".format(self.host, endpoint)
            requests.delete(delete_endpoint_url, headers=self.headers)
        return True

    def update_endpoints(self, endpoints, **kwargs):
        """Update attributes for all endpoints of a certain user.

        :param endpoints: a list of mac addresses
        :type endpoints: list

        :param kwargs: attribute-value pairs
        :type kwargs: dict

        :return: True if updated successfully
        """

        update_data = {"attributes": {}}
        for attr, val in kwargs.items():
            update_data["attributes"][attr] = val
        update_data["attributes"]["social_vip"] = ''  # should not be absent if use SSO onboarding

        for endpoint in endpoints:
            update_endpoint_url = "https://{}/api/endpoint/mac-address/{}".format(self.host, endpoint)
            requests.patch(update_endpoint_url, headers=self.headers, json=update_data)
        return True

    def revoke_certs(self, cert_ids, ca_id, confirm_revoke=True):
        """Revoke user certs based on cert IDs.

        :param cert_ids: a list of cert IDs
        :type cert_ids: list

        :param ca_id: ID of the CA that has issued user certs
        :type ca_id: int

        :param confirm_revoke: confirm the revocation of certs
        :type confirm_revoke: bool

        :return: True if revoked successfully
        """

        revoke_data = {
            "ca_id": ca_id,
            "confirm_revoke": confirm_revoke
        }

        for cert_id in cert_ids:
            revoke_cert_url = "https://{}/api/certificate/{}/revoke".format(self.host, cert_id)
            requests.post(revoke_cert_url, headers=self.headers, json=revoke_data)
        return True
