class A(object):
	words = [
			'whatever',
			'you',
			'say',
			'boss'
			]

	def __init__(self):
		self._name = "Michael"
		self._age = 42
		print self.words[2]

	@property
	def name(self):
		return self._name

	@property
	def age(self):
		return self._age

	def printMe(self):
		print "My name is {0}, and I am {1} years old.".format(self.name, self.age)

me = A()
print me.name
me.printMe()
me._name = 'Mike'
print me.name

def func(name, *args, **kwargs):
	print name
	print args[:]

def otherFunc():
	return "michael",

func(*(otherFunc()))
