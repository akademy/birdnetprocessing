import logging


def get_logger(name: str, dbg=False):
	"""
	call with get_logger(__name__):
	:param dbg: logging.DEBUG or logging.INFO
	:param name: name of logger, (use __name__)
	:return: logger
	"""
	logger = logging.getLogger( name )
	logger.setLevel( logging.DEBUG )
	
	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.INFO)
	console_handler.setFormatter(logging.Formatter('%(asctime)s -- %(message)s'))

	file_handler = logging.FileHandler('debug.log')
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(logging.Formatter('%(asctime)s -- %(message)s -- (%(levelname)s %(name)s)'))
	
	logger.addHandler(console_handler)
	logger.addHandler(file_handler)
	
	return logger

