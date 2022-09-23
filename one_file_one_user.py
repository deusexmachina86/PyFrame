


from tinydb import TinyDB, Query
import utils
import date_helper

from tinydb import TinyDB,Query
import date_helper

user_db = TinyDB('user_files/test_user_file_paths_2022-08.json')


Files = Query()



user_files = user_db.search(Files.user == 'Car_6262')
list_files_date = []
data_file = []

user_files = user_files[0].get('files')

for file in user_files:
        if date_helper.parse_date_f_filename(file) == '20220808':
                list_files_date.append(file)



list_files_date = sorted(list_files_date)


test = utils.Utilities()
for file in list_files_date:
	data = test.execute(['/home/pamadmin/WICE/2022-08/{file}}'])[0]
	timestamps = []
	print(data[0].get('Time'))
	date_obj = date_helper.clock_datetime_from_filename(f'/home/pamadmin/WICE/2022-08/{file}}')
	for time in data[0].get('Time'):
        timestamps.append(date_helper.add_seconds_to_offset(time,date_obj).strftime("%H:%M:%S"))
		data[0]['Timestamp'] = timestamps
	
	data_file.append(data)


#print(data[0].keys())
#print(data[0].get('Timestamp'))
print(date_file)

