import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QPixmap
from map_design import Ui_MainWindow
import requests
from delta import delta_find
from PIL import Image
from io import BytesIO


class Map_window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_7.clicked.connect(self.search)

    def initUI(self):
        self.setGeometry(200, 200, 800, 800)
        self.setWindowTitle('Event handler')
        self.show()

    def search(self):
        try:
            toponym_to_find = self.lineEdit.text()
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": toponym_to_find,
                "format": "json"}

            response = requests.get(geocoder_api_server, params=geocoder_params)
            if not response:
                # обработка ошибочной ситуации
                pass
            json_response = response.json()
            # Получаем первый топоним из ответа геокодера.
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # Координаты центра топонима:
            toponym_coodrinates = toponym["Point"]["pos"]
            # Долгота и широта:
            toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

            delta = delta_find(toponym_to_find, geocoder_params, geocoder_api_server)
            # Собираем параметры для запроса к StaticMapsAPI:
            map_params = {
                "ll": ",".join([toponym_longitude, toponym_lattitude]),
                "spn": ",".join([str(delta[0]), str(delta[1])]),
                "l": "map",
                "pt": "{},pm2dgl".format(",".join([toponym_longitude, toponym_lattitude]))}

            map_api_server = "http://static-maps.yandex.ru/1.x/"
            # ... и выполняем запрос
            response = requests.get(map_api_server, params=map_params)
            self.im = Image.open(BytesIO(response.content))
            self.im.save('map.png')
            self.im.resize((300, 300))
            self.pixmap = QPixmap('map.png')
            self.label_2.setPixmap(self.pixmap)
        except Exception:
            pass



app = QApplication(sys.argv)
ex = Map_window()
ex.show()
sys.exit(app.exec_())
