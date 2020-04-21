import sqlite3

class DataController:

	db_created = False

	def __init__(self, data=None, db_name="metrics.db"):
		self.connection = sqlite3.connect(db_name) 
		self.cursor = self.connection.cursor()
		self.initialize_queries = ["""
			CREATE TABLE IF NOT EXISTS filesystem( 
				id integer primary key autoincrement,
				hostname text NOT NULL,
				filesystem text NOT NULL,
				type text NOT NULL,
				size text NOT NULL,
				used integer NOT NULL,
				mountpoint integer NOT NULL,
				timeinsertion text NOT NULL)
			""",
			
			# in below query component refers to the table
			"""	
			CREATE TABLE IF NOT EXISTS alerts(
				id integer primary key autoincrement,
				component text NOT NULL,
				timeinsertion text NOT NULL)	
			"""

		]

		if not DataController.db_created:
			for query in self.initialize_queries:
				self.cursor.execute(query)

			self.connection.commit()
			DataController.db_created = True


	def navigate_data(self, data):
		try:

			if "Filesystem" in data.keys():
				print("Oopps under File System entry, time to import it inside the db")
				print("Printing the data")
				print(data)
				record = (data["Hostname"], data["Filesystem"], data["Type"], data["Size"], int(data["Use%"]), data["Mount Point"], data["TimeInsertion"])
				self.insert_record("filesystem", record)
				print("Record is inserted")	
			
		except IndexError:
			print("No data element at index 0")

	def insert_record(self, table, record):
		insert_query = """
		INSERT INTO {0}(hostname, filesystem, type, size, used, mountpoint, timeinsertion) VALUES (?, ?, ?, ?, ?, ?, ?)
		""".format(table)

		self.cursor.execute(insert_query, record)
		self.connection.commit()

	def retrieve_records(self, table, column):
		retrieve_query = """
		SELECT * FROM {0} ORDER BY {1} DESC
		""".format(table, column)

		print("Retrieve query""")
		print(retrieve_query)
		self.cursor.execute(retrieve_query)
		rows = self.cursor.fetchall()
		
		records = []		
		for row in rows:
			records.append(row)

		return records

	

dc = DataController()

data = {
	"Filesystem" : "/dev/sda", 
	"Hostname" : "prod001-eu.sap",
	"Type" : "xfs",
	"Size" : "40GB",
	"Use%" : 20,
	"Mount Point" : "/gosho"
}

#dc.navigate_data(data)


### One more insertion operation in this place




### Fetching operations

#dc.retrieve_records("filesystem")








