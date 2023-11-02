import glob
import sys
from os import path
import argparse

from BirdNET.Combiner import Combiner
from BirdNET.Redater import Redater
from BirdNET.util import get_logger


def get_csv_filepath_list(directory):
	glob_path = path.normpath(directory) + '/*.csv'
	csv_file_list = glob.glob( glob_path )
	return csv_file_list


def get_wav_filepath_list(directory):
	glob_path = path.normpath(directory) + '/*.wav'
	csv_file_list = glob.glob( glob_path )
	return csv_file_list


def run_combiner( args ):

	filepath_list = get_csv_filepath_list( args.directory )
		
	combiner = Combiner.Combiner(args.debug)
	combiner.combine( filepath_list, args.output_csv )


def run_redater( args ):

	filepath_list = get_wav_filepath_list( args.directory )
		
	redater = Redater.Redater(args.debug)
	redater.redate( filepath_list, args.output_directory, args.days )


def run():

	parser = argparse.ArgumentParser(description='Manipulate data from monitor station')
	parser.add_argument( "-d", "--debug", action="store_true", required=False, help='' )
	
	sub_parser = parser.add_subparsers(required=True, help='sub-command help')
	
	# Combine csvs
	#  e.g. python3 main.py -d combine "BirdNET/test_csvs/" "combined.csv"
	parser_combine = sub_parser.add_parser("combine", help='Combine csvs')
	parser_combine.add_argument( "directory", help='The directory with the csvs in.' )
	parser_combine.add_argument( "output_csv", help='The csv file to combine into.' )
	parser_combine.set_defaults( name="Combiner", func=run_combiner)
	
	
	# redate (rename) wavs
	#  e.g. python3 main.py -d redate "/media/matthew/TOSHIBA EXT/Earth Trust/Wildlife Monitor/temp/bto-input/" "/media/matthew/TOSHIBA EXT/Earth Trust/Wildlife Monitor/temp/bto-input/output/" 8303
	parser_redate = sub_parser.add_parser("redate",   help='Rename files with new date')
	parser_redate.add_argument( "directory", help='The directory with the wavs in.'  )
	parser_redate.add_argument( "output_directory", help='The directory to copy the renamed files to' )
	parser_redate.add_argument( "days", type=int, help='The number of days to change. (see e.g. https://www.timeanddate.com/date/duration.html)' )
	parser_redate.set_defaults( name="Redater", func=run_redater)


	# args = parser.parse_args(["-d"])
	# logger = get_logger("main", args.debug, True )

	args = parser.parse_args()
	
	logger = get_logger("", args.debug, True )
	
	logger.info( f"------- Starting {args.name} -------" )
	args.func(args)
	logger.info( f"------- Done {args.name} -------" )
	

if __name__ == "__main__":
	run()


