import glob
from os import path

from BirdNET.Combiner import Combiner
from BirdNET.util import get_logger


def get_csv_filepath_list(directory):
	glob_path = path.normpath(directory) + '/*.csv'
	csv_file_list = glob.glob( glob_path )
	return csv_file_list


def run(config):

	logger.info("------- Starting -------")
	
	filepath_list = get_csv_filepath_list( config['directory'] )
	
	logger.info( f"Found {len(filepath_list)} csv files")
	logger.debug(f"csv files: {filepath_list}")
	
	if len( filepath_list ) > 0 :
		
		combiner = Combiner.Combiner()
		combiner.combine( filepath_list, config['output_csv'])


	logger.info("-------  Done  --------")


if __name__ == "__main__":

	logger = get_logger("main")

	_directory = "/media/matthew/BackupMain/earth-trust/results/normalsound/"
	# _directory = "BirdNET/test_csvs/"
	_output_csv = "combined.csv"  # csvpath.join( _directory, "combined.csv")
	
	_config = {
		'debug': True,
		'directory': _directory,
		'output_csv': _output_csv,
	}
	
	run(_config)
