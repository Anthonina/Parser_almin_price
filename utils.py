import requests


def get_html(url):
	r_html = requests.get(url) 
	# r - response - ответ сервера, который будет получать значение от модуля requests от метода get.
	# Метод get в качестве аргумента получает url
	return r_html.text	# возвращает html-код страницы, которая передана в качестве аргумента (url)
