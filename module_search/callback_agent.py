import requests

class CallbackAgent:

    def __init__(self, url):
        self.url = url

    def __send_message(self, status: str, message: str):
        body = {
            "service_report": message,
            "service_status": status
        }

        requests.put(self.url, data=body)


    def starting(self, message):
        self.__send_message("starting", message)

    def downloading(self, message):
        self.__send_message("downloading", message)

    def initiating(self, message):
        self.__send_message("initiating", message)

    def completed(self, message):
        self.__send_message("completed", message)

    def failed(self, message):
        self.__send_message("failed", message)
