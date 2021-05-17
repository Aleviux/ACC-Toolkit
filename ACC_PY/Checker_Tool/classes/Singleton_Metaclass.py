from weakref import WeakValueDictionary

########################################
# SINGLETON METACLASS
########################################

class SingletonMetaclass (type):
	'''
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    '''
	_instances = WeakValueDictionary()

	# Call function that creates the Singleton only if it didn't exist previously
	# It takes the default call arguments as params
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super(SingletonMetaclass, cls).__call__(*args, **kwargs)
			cls._instances[cls] = instance

		return cls._instances[cls]

	# Static method that returns the Singleton instance (bound to the class, not the object)
	# It takes the class whose singleton instance we wish to obtain (in case of multiple Singleton Implementations)
	@staticmethod
	def getInstance(cls):
		return (SingletonMetaclass._instances[cls])

# Function to check if a list of objects are the same Singleton instance
def debug_checkSingleton(singletonObjs):
	
	isWorking = False

	# Singleton instances

	print ("")
	print ("------------- SINGLETON INSTANCES -------------")
	print ("")

	for obj in singletonObjs:
		print ("SINGLETON INSTANCE: " + str(obj))

	print ("COMPLETE SINGLETON INSTANCES LIST: " + str(SingletonMetaclass._instances.items()))

	# Singleton uniqueness check

	for i in range (0, len(singletonObjs)):
		if i == 0:
			previous = singletonObjs[i]
		
		assert singletonObjs[i] is previous
		isWorking = singletonObjs[i] is previous

	print ("")
	print ("------------- IS THE SINGLETON WORKING? -------------")
	print ("")

	print ("ARE THEY THE SAME INSTANCE? " + str(isWorking))
	print ("RESULT: " + str(isWorking))

	return isWorking 

# Function with default example values to check if it's working
def debug_checkSingletonDefault():

	# Singleton Implementation test class
	class SingletonImplementation:
		__metaclass__ = SingletonMetaclass

		def __del__(cls):
			print ("--- DESTRUCTOR CALL, DELETING SINGLETON INSTANCE: " + str(cls))

	# Singleton example instances creation

	print ("")
	print ("------------- CREATING SINGLETONS -------------")
	print ("")
	
	mySingleton1 = SingletonImplementation()
	mySingleton2 = SingletonImplementation()
	mySingleton3 = SingletonImplementation()

	print ("SINGLETON 1: " + str(mySingleton1))
	print ("SINGLETON 2: " + str(mySingleton2))
	print ("SINGLETON 3: " + str(mySingleton2))

	# Singleton check

	isWorking = debug_checkSingleton([mySingleton1, mySingleton2, mySingleton3])
	
	# Singleton example instances deletion

	print ("")
	print ("------------- DELETING SINGLETONS -------------")
	
	print ("")
	print ("DELETING SINGLETON 1, NOTHING SHOULD HAPPEN, INSTANCES LIST SHOULD BE SAME")
	del mySingleton1
	print ("SINGLETON INSTANCES LIST: " + str(SingletonImplementation.__metaclass__._instances.items()))

	print ("")
	print ("DELETING SINGLETON 2, NOTHING SHOULD HAPPEN, INSTANCES LIST SHOULD BE SAME")
	del mySingleton2
	print ("SINGLETON INSTANCES LIST: " + str(SingletonImplementation.__metaclass__._instances.items()))

	print ("")
	print ("DELETING LAST SINGLETON, INSTANCES LIST SHOULD NOW BE EMPTY")
	del mySingleton3
	print ("SINGLETON INSTANCES LIST: " + str(SingletonImplementation.__metaclass__._instances.items()))

	print ("")
	print ("------------- TESTING FUNCTION END -------------")
	print ("")

# Function to evaluate the static method getInstance() with two different Singleton Implementations
def debug_checkSingletonInstanceUniqueness():
	
	# Singleton Implementation example classes

	class SingletonImplementation1:
			__metaclass__ = SingletonMetaclass

	class SingletonImplementation2:
			__metaclass__ = SingletonMetaclass
	
	mySingleton1a = SingletonImplementation1()
	mySingleton1b = SingletonImplementation1()

	mySingleton2a = SingletonImplementation2()
	mySingleton2b = SingletonImplementation2()

	# Singleton asserts to check if two implementations are the same Singleton

	assert mySingleton1b is mySingleton1a
	assert mySingleton2a is mySingleton2b

	# Singleton asserts to check if two implementations are different Singletons

	assert not (mySingleton1a is mySingleton2b)
	assert not (mySingleton1b is mySingleton2a)

	print ("Singleton 1 getInstance() result: " + str(SingletonImplementation1.getInstance(SingletonImplementation1)))
	print ("Singleton 2 getInstance() result: " + str(SingletonImplementation2.getInstance(SingletonImplementation2)))

#debug_checkSingletonDefault()
#debug_checkSingletonInstanceUniqueness()
