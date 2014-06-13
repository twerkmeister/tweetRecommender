from app import app
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
                        level=logging.DEBUG)

if __name__ == '__main__':
	app.run(debug = True)