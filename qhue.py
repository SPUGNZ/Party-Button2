# Qhue is (c) Quentin Stafford-Fraser 2017
# but distributed under the GPL v2.

import urequests as requests
import json
import ure
import sys

# default timeout in seconds
_DEFAULT_TIMEOUT = 5


class Resource(object):

    def __init__(self, url, timeout=_DEFAULT_TIMEOUT):
        self.url = url
        self.address = url[url.find('/api'):]
        # Also find the bit after the username, if there is one
        self.short_address = None
        #post_username_match = ure.search(r'/api/[^/]*(.*)', url)
        #if post_username_match is not None:
        #    self.short_address = post_username_match.group(1)
        self.timeout = timeout

    def __call__(self, *args, **kwargs):
        url = self.url
        for a in args:
            url += "/" + str(a)
        http_method = kwargs.pop('http_method',
            'get' if not kwargs else 'put').lower()
        if http_method == 'put':
            r = requests.put(url, data=json.dumps(kwargs))
        elif http_method == 'post':
            r = requests.post(url, data=json.dumps(kwargs))
        elif http_method == 'delete':
            r = requests.delete(url)
        else:
            r = requests.get(url)
        if r.status_code != 200:
            raise QhueException("Received response {c} from {u}".format(c=r.status_code, u=url))
        resp = r.json()
        if type(resp) == list:
            errors = [m['error']['description'] for m in resp if 'error' in m]
            if errors:
                raise QhueException("\n".join(errors))
        return resp

    def __getattr__(self, name):
        return Resource(self.url + "/" + str(name), timeout=self.timeout)

    __getitem__ = __getattr__


def _api_url(ip, username):
    return "http://{}/api/{}".format(ip, username)

class Bridge(Resource):

    def __init__(self, ip, username, timeout=_DEFAULT_TIMEOUT):
        """Create a new connection to a hue bridge.

        If a whitelisted username has not been generated yet, use
        create_new_username to have the bridge interactively generate
        a random username and then pass it to this function.

        Args:
            ip: ip address of the bridge
            username: valid username for the bridge
            timeout (optional, default=5): request timeout in seconds
        """
        self.ip = ip
        self.username = username
        url = _api_url(ip, username)
        super(Bridge, self).__init__(url, timeout=timeout)


class QhueException(Exception):
    pass
