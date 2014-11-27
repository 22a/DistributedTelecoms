

class FileExample:
	def run(self):
		self.fname = raw_input("Please enter a file name:")
		
		for line in open(self.fname).xreadlines():
   			print line



def main():
	print "Program Start"
	getFile = FileExample()
	getFile.run()
	print "Program End"

if __name__ == "__main__":
	main()