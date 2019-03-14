class Farm:
    def __init__(self, param):
        self.param = param

    def signUp(self):
        first_name = self.param['first_name']
        last_name = self.param['last_name']
        email = self.param['email']
        phone = self.param['phone']
        password = self.param['password']
