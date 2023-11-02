
import os, os.path
import shutil

from datetime import datetime, timedelta

from ..util import get_logger


class Redater:

	def __init__(self, debug):
		self.log = get_logger(__name__, debug)

	def redate(self, filepath_list, output_directory, days: int ):

		filepath_list_len = len( filepath_list )

		self.log.info( f"Processing {filepath_list_len} wav files:" )
		self.log.debug( f"wav files: {filepath_list}" )

		if filepath_list_len > 0:

			for filepath in filepath_list:
				
				data = self.split_filename(filepath)
				original_date = datetime.strptime(
					f"{data['date']} {data['time']}",
					"%Y%m%d %H%M%S"
				)
				# Calculate days between two dates
				# https://www.timeanddate.com/date/duration.html
				#
				time_change = timedelta(days=days)
				new_date = original_date + time_change

				new_filename = data['start'] + "_" + new_date.strftime("%Y%m%d_%H%M%S") + "." + data['ext']

				self.log.debug( f"from {original_date} adding {time_change}: to {new_date}" )
				
				self.log.info( f"Copying {data['filename']} to {new_filename}..." )
				shutil.copy2(filepath, os.path.join(output_directory, new_filename ) )
				
			# Create an info file
			with open( os.path.join(output_directory, "info.ini" ), "w" ) as f :

				f.writelines([
					f"files_changed={filepath_list_len}\n",
					f"days_adjusted={days}\n",
					f"processed={datetime.now()}\n"
				])

	def split_filename(self, filename: str) -> dict:
		"""
		Extract date and time from filename
			e.g. "EARTH_20000129_014428.wav"
		:param filename: filename or filepath
		:return: dict {'filename': filename, 'date': date, 'time': time}
			e.g. {'filename': "EARTH", 'date': "20220809", 'time': "025600"}
		:raise: ValueError if can't read data from name
		"""
		filename = os.path.basename(filename)
		start, date, time_and_ext = filename.split("_")
		time, ext = time_and_ext.split(".")
		
		# test are numbers
		_ = int(date)
		_ = int(time)
		
		return { 'filename': filename, 'start': start, 'ext': ext, 'date': date, 'time': time }




