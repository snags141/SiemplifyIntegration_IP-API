import os
from datetime import datetime

# =====================================
#              IMPORTS                #
# =====================================
import requests

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    
# =====================================
#             CONSTANTS               #
# =====================================
HTTP_ERRORS = {
    401 : "Unauthorized - is set if the authentication failed for the request (e.g. the API key is incorrect or missing)",
    403 : "Forbidden - is set if the request is not authorized to consume the desired functionality (e.g. the API is not enabled for the used API key)",
    405 : "Method not allowed - The HTTP method is other than POST",
    429 : "Too many requests - More than 10 requests per second have been issued from the same IP address"
}
URL_TYPE = u'url'
DUMMY_IP_FOR_TEST = u'google.com'

API_ROOT = u'http://ip-api.com/json/{}'

# Scan IP messages indicators.
NO_DATA_FOUND_MESSAGE = u'No Data Found'
RESOURCE_COULD_NOT_BE_FOUND_MESSAGE = u'resource could not be found'
INVALID_MESSAGE = u'Invalid'
TIME_FORMAT = u"%Y-%m-%d %H:%M:%S"


# =====================================
#              CLASSES                #
# =====================================
class IP_APIManagerError(Exception):
    """
    General Exception for IP-API manager
    """
    pass


class IPAPILimitManagerError(Exception):
    """
    Limit Reached for IP-API manager
    """
    pass


class IPAPIInvalidAPIKeyManagerError(Exception):
    """
    Invalid API key exception for IP-API manager
    """
    pass

class IP_APIManager(object):
    def __init__(self, api_key, verify_ssl=False):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.verify = verify_ssl

    #
    def validate_response(self, response, error_msg=u"An error occurred"):
        """
        Retrieve a report on a given url/file
        :param response: {dict} response from api call,
        :param error_msg: {string} message if response is not valid
        :return: {bool}
        """
        try:
            response.raise_for_status()

            if response.status_code == 429:
                # API limit reached
                raise IPAPILimitManagerError(u"Request rate limit exceeded")

        except requests.HTTPError as error:
            if response.status_code == 403:
                # Forbidden - no permission to resource.
                # You don't have enough privileges to make the request. You may be doing a request without providing
                # an API key or you may be making a request to a Private API without having the appropriate privileges.
                raise IPAPIInvalidAPIKeyManagerError(
                    u"Forbidden. You don't have enough privileges to make the request. You may be doing a request "
                        u"without providing an API key or you may be making a request to a Private API without having "
                        u"the appropriate privileges"
                )

            # Not a JSON - return content
            raise IP_APIManagerError(
                u"{error_msg}: {error} - {text}".format(
                        error_msg=error_msg,
                        error=error,
                        text=error.response.content)
            )

        return True

    def test_connectivity(self):
        """
        Ping to server to be sure that connected
        :return: {bool}
        """
        return True if self.check_ip(DUMMY_IP_FOR_TEST) else False

    def check_ip(self, resource):
        """
        Retrieve a report on a given IP
        :param resource: {string} The IP/domain,
        :return: {dict}
        """
        check_url = API_ROOT.format(resource)
        response = self.session.get(url=check_url)
        self.validate_response(response)
        
        
        json_object = response.json()
        
        return json_object
        
    
