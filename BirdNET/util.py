import logging


def get_logger( name: str = "", dbg=False, initial=False ):
	"""
	call with get_logger(__name__):
	:param initial: reset file?
	:param dbg: logging.DEBUG or logging.INFO
	:param name: name of logger, (use __name__)
	:return: logger
	"""
	
	log_name = "main"
	#if name != "" :
	#	log_name += "." + name
		
	logger = logging.getLogger( log_name )
	logger.setLevel( logging.DEBUG )
	
	console_handler = logging.StreamHandler()
	console_handler.setLevel( logging.INFO )
	console_handler.setFormatter( logging.Formatter( '%(asctime)s -- %(message)s' ) )

	if dbg :
		file_handler = logging.FileHandler( 'debug.log', mode='w' if initial else "a")
		file_handler.setLevel( logging.DEBUG )
		file_handler.setFormatter( logging.Formatter( '%(asctime)s -- %(message)s -- (%(levelname)s %(name)s)' ) )

		logger.addHandler( file_handler )

	logger.addHandler( console_handler )
	
	return logger

