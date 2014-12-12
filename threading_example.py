from threading import * 

class Test(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
	  # Other methods can also be invoked from
	  # within this method. 
		while True:
			print "Hello, from run()"
	def another_method(self):
		while True:
			print "Hello, from another_method()"


if __name__ == "__main__":
	instance = Test()
	instance.start() # Causes the run() method to begin executing
	instance.another_method() # Just some other method of the Threaded class
