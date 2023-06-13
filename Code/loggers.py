import logging
import os.path

path_logs = os.path.abspath((os.path.join(os.path.dirname(__file__), os.pardir)))
logging.basicConfig(filename=os.path.join(path_logs,'scrapper_logs.log'),level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
