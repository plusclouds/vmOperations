import os
import requests


class CallbackAgent:
	def __init__(self, url):
		base_url = os.getenv('LEO_URL', "http://api.plusclouds.com")

		self.url = base_url + "/v2" + url
		print("New Callback Agent formed, with the following url : {}".format(url))

	def __send_message(self, status: str, message: str):
		body = {
			"service_report": message,
			"service_status": status
		}
		print("sending the following message", message)
		requests.put(self.url, data=body)

	def starting(self, message: str):
		self.__send_message("starting", message)

	def downloading(self, message: str):
		self.__send_message("downloading", message)

	def initiating(self, message: str):
		self.__send_message("initiating", message)

	def completed(self, message: str):
		self.__send_message("completed", message)

	def failed(self, message: str):
		self.__send_message("failed", message)