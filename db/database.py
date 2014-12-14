import sqlite3
from itertools import islice
from Queue import Queue
import json
import os
import time

class Database():

    READ_IN_SIZE = 1000000
    block = 0
    read_complete = False;

        #Open a database for work
    def _init_(self,filename):
        self.filename = filename
        self.blockid_queue = Queue()
        self.start_pos = 0
        self.end_pos = Database.READ_IN_SIZE
        self.conn =  sqlite3.connect('database.sqlite')
        for line in open('query.sql','r'):
            self.conn.execute(line)
        print "Connection To The DB Has Been Established..."
        


    def get_state(self, block_id):
        self.temp = []
        result = self.conn.execute("""SELECT DISTINCT oneK,twoK,threeK,fourK,fiveK FROM blockmanagement WHERE blockid=?""",(block_id,))
        for row in result:
            self.temp = row
        
        if not self.temp:
            print "Nothing has left the block!"
            return -1
        
        count = self.temp.count(1)
        
        if count * 1000 == 0:
            return -1
        else:
            return count*1000



    def update_state(self, block_id, pos):
        if pos==1000:
            self.conn.execute("""UPDATE blockmanagement SET oneK = ? WHERE blockid= ? """,(True,block_id))
        elif pos==2000:
            self.conn.execute("""UPDATE blockmanagement SET twoK = ? WHERE blockid= ? """,(True,block_id))
        elif pos==3000:
            self.conn.execute("""UPDATE blockmanagement SET threeK = ? WHERE blockid= ? """,(True,block_id))
        elif pos==4000:
            self.conn.execute("""UPDATE blockmanagement SET fourK = ? WHERE blockid= ? """,(True,block_id))
        elif pos==5000:
            self.conn.execute("""UPDATE blockmanagement SET fiveK = ?,processed = ? WHERE blockid= ? """,(True,True,block_id))
        self.conn.commit()

    

    def get_data(self):
        if not self.blockid_queue.empty():
            block_id = self.blockid_queue.get()
            self.dataStore = []
            self.dataObject = []
            position = self.get_state(block_id)

            if position != -1:
                cursor = self.conn.execute('''SELECT data from datapool where blockid=(?) AND num BETWEEN (?) AND 4999''', (block_id,position))
            else:
                cursor = self.conn.execute('''SELECT data from datapool where blockid=(?)''', (block_id,))

            for row in cursor:
                data = row[0]
                self.dataStore.append(data.replace('\n', ''))
            
            self.dataObject.append({'id':block_id})
            self.dataObject.append({'data':self.dataStore})

            return json.dumps(self.dataObject, sort_keys = True, indent = 4,
                              separators=(',', ': '))

            self.conn.commit()
    
    

    def read_into_db(self, filename):
        j=0
        block_size = 5000
        with open(filename, 'r') as f:
            lines = list(islice(f, self.start_pos, self.end_pos))
            number_of_elements = len(lines)
            if number_of_elements == 0:
                return False

            if number_of_elements < block_size:
                block_size = number_of_elements

            for line in lines:
                    self.conn.execute('''INSERT INTO datapool(num, blockid, data) VALUES(?,?,?)''', (j, Database.block, line))
                    j = j + 1
                    if j == block_size:
                        self.blockid_queue.put(Database.block)
                        self.conn.execute('''INSERT INTO blockmanagement(blockid) VALUES(?)''', (Database.block,))
                        self.conn.commit()
                        Database.block=Database.block+1 
                        j = 0
                        
            self.conn.commit()
            self.start_pos = self.end_pos
            self.end_pos = self.end_pos + Database.READ_IN_SIZE
            return True
        
    
    def requeue_blockid(self,blockid):
        self.blockid_queue.put(blockid)

    def data_available(self):
        return self.blockid_queue.qsize() > 0

    def blocks_to_process(self):
        return self.blockid_queue.qsize()

    def delete_data(self):
        self.conn.execute('DELETE FROM datapool')
        self.conn.commit()
        print "<< Database Table Cleaned >>"

    def delete_management_info(self):
        self.conn.execute('DELETE FROM blockmanagement')
        self.conn.commit()
        print "<< Management Table Cleaned >>"

    def close_connection(self):
        self.conn.close()
        print "DB Connection Terminated..."
        
        ## try to delete database file ##
        try:
            os.remove('database.sqlite')
        except OSError, e:  ## if failed, report it back to the user ##
            print ("Error: %s - %s." % (e.filename,e.strerror))

