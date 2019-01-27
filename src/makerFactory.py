"""Credit to David Monts, circa 2017

The module for getting the correct maker type based upon the language.
"""

from cppClassMaker import CppClassMaker
from pythonClassMaker import PythonClassMaker
from csharpClassMaker import CsharpClassMaker

class MakerFactory(object):
	"""A simple class to serve as a factory for creating different classMakers
	"""
	
	@staticmethod
	def get_maker(language, class_name):
		"""A static method that allows retrieving the appropriate classMakers
		based upon the language parameter.
		
		Args:
			language - The language of the classMakers
			class_name - The name that will be used when creating the class
			
		Returns:
			A new class object is returned or None if we do not support the language.
		"""
		if language == "python":
			return PythonClassMaker(class_name)
		elif language == "cpp":
			return CppClassMaker(class_name)
		elif language == "csharp":
			return CsharpClassMaker(class_name)
		else:
			return None