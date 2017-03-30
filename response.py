class Response():
    def __init__(self, module_called, status_code=None, messages_to_send=None, special_condition=None):
        self.module_called = module_called
        # So... Python is incredibly dumb and smart at the same time, and will remember mutable objects during runtime
        # This is because Python only runs the def statement once, and only evaluates that once, and therefor could remember
        # messages_to_send out of thin air. 
        if status_code is None:
            self.status_code = 0
        if messages_to_send is None:
            self.messages_to_send = []
        if special_condition is None:
            self.special_condition = False
