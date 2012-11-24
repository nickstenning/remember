from collections import namedtuple
import re

import requests

API_ROOT = 'https://api.clockworksms.com'

class ClientError(Exception):
    pass

class Clockwork(object):

    def __init__(self, key, root=API_ROOT):
        self._session = requests.Session()

        self.key = key
        self.root = root

    def _req(self, method, url, *args, **kwargs):
        res = self._session.request(method, url, *args, **kwargs)
        return ClockworkResponse(res)

    def _url(self, path):
        return self.root + path

    def send(self, to, content, from_=None, long=False):
        params = {'key': self.key, 'to': to, 'content': content}

        params['long'] = '0' if long else '1'

        if from_ is not None:
            params['from'] = from_

        return self._req('get', self._url('/http/send.aspx'), params=params)


class ClockworkResponse(object):

    def __init__(self, raw):
        self.raw = raw

        self.raw.raise_for_status()

        self.tickets = []
        self.errors = []

        for line in self.raw.content.splitlines():
            tck, err = _parse_response_line(line)
            if tck:
                self.tickets.append(tck)
            if err:
                self.errors.append(err)

    @property
    def ok(self):
        return self.errors == []


ClockworkTicket = namedtuple('ClockworkTicket', 'to id')
ClockworkError = namedtuple('ClockworkError', 'to code message')


def _parse_response_line(line):
    m = re.match(r'Error (\d+): (.+)', line)
    if m:
        return None, ClockworkError(None, *m.groups())

    m = re.match(r'To: (\S+) Error (\d+): (.+)', line)
    if m:
        return None, ClockworkError(*m.groups())

    m = re.match(r'To: (\S+) ID: (\S+)', line)
    if m:
        return ClockworkTicket(*m.groups()), None

    raise ClientError("Couldn't parse Clockwork response line: %s" % line)
