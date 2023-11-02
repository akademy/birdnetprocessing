
import csv
import os
from ..util import get_logger


class Combiner:

	def __init__(self, debug):
		self.log = get_logger(__name__, debug)
		self.original_headers = ['Start (s)', 'End (s)', 'Scientific name', 'Common name', 'Confidence']
		self.new_headers = ['Filename', 'Date', 'Time'] + self.original_headers

	def combine(self, filepath_list, output_filepath ):

		filepath_list = self.check_filepath_list(filepath_list)

		filepath_list_len = len( filepath_list )

		self.log.info( f"Processing {filepath_list_len} csv files" )
		self.log.debug( f"csv files: {filepath_list}" )
		
		if filepath_list_len > 0:

			row_count = 0
			with open(output_filepath, 'w') as wf:

				wf.write( ",".join(self.new_headers) + os.linesep )

				for filepath in filepath_list:
					with open(filepath) as rf:
		
						csv_file = csv.DictReader( rf )
						info = self.get_info_from_filename(filepath)

						for row in csv_file:
							data = [
								info["filename"],
								info["date"],
								info["time"],
							]
							for head in self.original_headers:
								data.append(row[head])
						
							wf.write( ",".join(data) + os.linesep)
							row_count += 1
			
			self.log.info(f"Combined file saved to {output_filepath} with {row_count} rows.")
						

	def get_info_from_filename(self, filename: str) -> dict:
		"""
		Extract date and time from filename
			e.g. "EARTH_20220809_025600.BirdNET.results.csv"
		:param filename: filename or filepath
		:return: dict {'filename': filename, 'date': date, 'time': time}
		:raise: ValueError if can't read data from name
		"""
		filename = os.path.basename(filename).replace(",", "-")
		date_and_time = filename.split("_")
		date = date_and_time[1]
		time = date_and_time[2].split(".")[0]
		
		# test are numbers
		_ = int(date)
		_ = int(time)
		
		return {'filename': filename, 'date': date, 'time': time}
		
	def check_filepath_list(self, filepath_list):
		"""
		Test the csvs are in a good condition
		:param filepath_list: list of filepaths
		:return: any good filepaths
		"""
		clean_list = []
		good_headers = set(self.original_headers)
		
		for filepath in filepath_list:
			
			# Check csv has the right filename
			try:
				self.get_info_from_filename(filepath)
			except ValueError:
				self.log.debug(f"Skipped {filepath}, it is called the wrong name.")
				continue
				
			with open(filepath) as rf:

				csv_file = csv.DictReader( rf )

				# Check csv has the right headers
				if set(csv_file.fieldnames) != good_headers :
					self.log.debug(f"Skipped {filepath}, it contains the wrong headers: {csv_file.fieldnames}.")
					continue

				# Check csv has some entries
				try:
					next(csv_file)
				except StopIteration:
					self.log.debug(f"Skipped {filepath}, it doesn't contain any entries.")
					continue
					
				clean_list.append( filepath )
		
		return clean_list


