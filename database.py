import sqlite3
from itertools import islice
import json

class Database:

	READ_IN_SIZE = 1000000

		#Open a database for work
	def _init_(self):
		self.startPos = 0
		self.endPos = Database.READ_IN_SIZE
		self.conn =  sqlite3.connect('workDB.sqlite')
		print "Connection To The DB Has Been Established..."


	def get_state(self,block_id):
		self.temp = []
		result = self.conn.execute("""SELECT DISTINCT oneK,twoK,threeK,fourK,fiveK FROM blockmanagement WHERE blockid=1 =?""",(block_id,))
		for row in result:
			self.temp=row
		
		if not self.temp:
			print "Nothing has left the block!"
			return -1
		
		else:
			i=0
			count=0;
			while i<len(self.temp):
				if self.temp[i]==1:
					count=count+1
				else:
					break;
				i=i+1
		
		if count*1000==0:
			return -1
		else:
			return count*1000


	
	def update_state(self,block_id,pos):
		if pos==1000:
			self.conn.execute("""UPDATE blockmanagement SET oneK = ? WHERE blockid= ? """,(True,block_id))
		elif pos==2000:
			self.conn.execute("""UPDATE blockmanagement SET twoK = ? WHERE blockid= ? """,(True,block_id))
		elif pos==3000:
			self.conn.execute("""UPDATE blockmanagement SET threeK = ? WHERE blockid= ? """,(True,block_id))
		elif pos==4000:
			self.conn.execute("""UPDATE blockmanagement SET fourK = ? WHERE blockid= ? """,(True,block_id))
		elif pos==5000:
			self.conn.execute("""UPDATE blockmanagement SET fiveK = ? WHERE blockid= ? """,(True,block_id))
		self.conn.commit()

	

	def get_data(self,block_id):
		#I need to figure out what needs to be sent
		self.dataStore = []
		self.dataObject = []
		cursor = self.conn.execute('''SELECT data from datapool where blockid=(?)''', (block_id,))
		for row in cursor:
			data = row[0]
			self.dataStore.append(data)
		
		self.dataObject.append({'id':block_id})
		self.dataObject.append({'data':self.dataStore})

		return json.dumps(self.dataObject, sort_keys=True, indent=4,
                          separators=(',', ': '))


		self.conn.commit()

	def data_available(self):
		print "is data data available"
	
	

	def read_into_db(self,filename):
		block=0
		j=0
		with open(filename, 'r') as myfile:
			lines_gen = islice(myfile,self.startPos,self.endPos)
    			for line in lines_gen:
    				self.conn.execute('''INSERT INTO datapool(num, blockid, data) VALUES(?,?,?)''', (j, block, line))
    				j=j+1
    				if j==5000:
    					block=block+1 
    					self.conn.execute('''INSERT INTO blockmanagement(blockid) VALUES(?)''', (block,))
    					j=0
    					
        	self.conn.commit()
        	self.startPos=self.endPos
        	self.endPos=self.endPos+Database.READ_IN_SIZE
	

	def delete_data(self):
		self.conn.execute('DELETE FROM datapool')
		self.conn.commit()
		print "<< Database Table Cleaned >>"

	def delete_management_info(self):
		self.conn.execute('DELETE FROM blockmanagement')
		self.conn.commit()
		print "<< Management Table Cleaned >>"

		#Close the Database connection
	def close_connection(self):
		self.conn.close()
		print "DB Connection Terminated..."



def main():
	#The Following are Tests for the database
	print "Testing DB Class"
	db = Database()
	db._init_()
	filename = "names.txt"
	db.read_into_db(filename)
	db.update_state(1,5000)
	db.update_state(1,4000)
	db.update_state(1,2000)
	db.update_state(1,1000)
	db.update_state(1,3000)
	db.get_state(1)
	db.get_data(1)
	db.delete_data()
	db.delete_management_info()
	db.close_connection()

if __name__ == "__main__":
	main()