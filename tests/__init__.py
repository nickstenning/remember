import remember

def setup():
    app = remember.create_app()
    remember.drop_db(app)

class TestCase(object):
    def setup(self):
        self.app = remember.create_app()
        remember.create_db(self.app)
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def teardown(self):
        self.ctx.pop()
        remember.drop_db(self.app)
