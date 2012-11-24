from nose.tools import *
from mock import patch

from remember.clockwork import Clockwork, ClientError

class TestClockwork(object):

    def setup(self):
        self.patcher = patch('remember.clockwork.requests.Session')
        self.session = self.patcher.start()

    def teardown(self):
        self.patcher.stop()

    def set_response(self, txt):
        self.session.return_value.request.return_value.content = txt

    def test_error(self):
        self.set_response('Error 58: Invalid API Key\r\n')

        c = Clockwork('api_key')
        res = c.send('441234567890', "A message")

        assert_false(res.ok)
        assert_equal(len(res.errors), 1)
        assert_equal(res.errors[0].code, '58')
        assert_equal(res.errors[0].message, 'Invalid API Key')

    def test_ok(self):
        self.set_response('To: 441234567890 ID: AB_12345\r\n')

        c = Clockwork('api_key')
        res = c.send('447811555785', "A message")

        assert_true(res.ok)
        assert_equal(res.tickets[0].to, '441234567890')
        assert_equal(res.tickets[0].id, 'AB_12345')

    def test_ok_multiple(self):
        self.set_response('To: 441234567890 ID: AB_12345\r\nTo: 440987654321 ID: AB_54321\r\n')

        c = Clockwork('api_key')
        res = c.send('441234567890,440987654321', "A message")

        assert_true(res.ok)
        assert_equal(len(res.tickets), 2)
        assert_equal(res.tickets[0].id, 'AB_12345')
        assert_equal(res.tickets[1].id, 'AB_54321')

    def test_mixed_multiple(self):
        self.set_response("To: 441234567890 Error 10: Invalid 'To' Parameter\r\nTo: 440987654321 ID: AB_54321\r\n")

        c = Clockwork('api_key')
        res = c.send('441234567890,440987654321', "A message")

        assert_false(res.ok)
        assert_equal(len(res.tickets), 1)
        assert_equal(len(res.errors), 1)
        assert_equal(res.tickets[0].id, 'AB_54321')
        assert_equal(res.errors[0].code, '10')
        assert_equal(res.errors[0].message, "Invalid 'To' Parameter")

    @raises(ClientError)
    def test_unparseable(self):
        self.set_response("Wibble bang boof!")

        c = Clockwork('api_key')
        res = c.send('441234567890,440987654321', "A message")
