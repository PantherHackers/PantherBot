class Response():
    def __init__(self, module_called, status_code=0, messages_to_send=None, special_condition=False):
        self.module_called = module_called
        self.status_code = status_code
        self.messages_to_send = messages_to_send
        self.special_condition = special_condition
        # So... Python is incredibly dumb and smart at the same time, and will remember mutable objects during runtime
        # This is because Python only runs the def statement once, and only evaluates that once, and therefor could remember
        # messages_to_send out of thin air.
        if messages_to_send is None: self.messages_to_send = []