JSON Class Designer (JCD)

One of the burdens of JSON is that really, no one wants to deal with 
the JSON itself, instead what one wants to work with is the JSON information
in more practical forms. That is where the JCD lends 
a hand. With the designer, the programmer does not need to worry about validating
the JSON or extracting information from the JSON. The utility produces all of
the necessary code for that. The programmer will be able to work with a clean 
interface to a class that represents the JSON information.

There are two ways to use the designer. One, called dirty, accepts a JSON file
as is. Nothing needs to be cleaned up or changed, as long as the file has valid
JSON, the designer can produce the necessary code files. The other method of using
the tool is to use the json-schema (json-schema.org) formatting in order to produce 
more useful classes (clean). With the formatting, the tool will be able to not 
only verify types, but also restrict the values of types to ranges or specific items.

Out-of-the-box the tool works to create classes in either C# or Python, however,
the tool is easily expandable by simply inheriting from the classMaker class. The file,
classMakerTemplate.py provides a framework for anyone that wants to support a new language. The
language must have its own JSON module for parsing and validating the JSON at runtime.

The tool can also be run using its CLI, the json configuration utility (JCU). For more 
information on how to use the utility, navigate within the src directory and type in 
"python jcu.py -h". 

Hopefully you find the tool useful!! Please email me at jsonclassdesigner@gmail.com
with any suggestions.


Utility Requirements:
Python 3.5.2 (or higher)