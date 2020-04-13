class all_request:
    def __init__(self, method, data,headers,url,time):
        self.method = method
        self.data = data
        self.header = headers
        self.url = url
        self.time = time
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
