import warnings
import xml.etree.ElementTree as ET
from xml.dom import minidom
from byteconv import strToText

# TODO:
# 1) Find out whether these patches are necessary
# 2) learn how to write and test patches properly


# I don't want to mess with ANYthing :)
def tostring(elem, enc):
	return ET.tostring(elem, enc)
def SubElement(parent, tag):
	return ET.SubElement(parent, tag)

class Element(ET.Element):

	pass
	# Replacement for ET's 'findtext' function, which has a bug
	# that will return empty string if text field contains integer with
	# value of zero (0); If there is no match, return None
	def findElementText(self, match):
		elt = self.find(match)
		if elt is not None:
			return elt.text
		else:
			return None

	# Searches element and returns list that contains 'Text' attribute
	# of all matching sub-elements. Returns empty list if element
	# does not exist
	def findAllText(self, match):
		try:
			return [result.text for result in self.findall(match)]
		except:
			return []

	# Append childnode with text
	def appendChildTagWithText(self, tag, text):
		el = ET.SubElement(self, tag)
		el.text = text

	# Translate values to human readable, optionally using mappings
	def makeHumanReadable(self, remapTable = {}):
		# Takes element tree object, and returns a modified version in which all
		# non-printable 'text' fields (which may contain numeric data or binary strings)
		# are replaced by printable strings
		#
		# Property values in original tree may be mapped to alternative (more user-friendly)
		# reportable values using a rempapTable, which is a nested dictionary.
		# Destination tree: copy of source (?? think this is just a reference, Johan)
		for elt in self.iter():
			# Text field of this element
			textIn = elt.text
			# Tag name
			tag = elt.tag
			# Step 1: replace property values by values defined in enumerationsMap,
			# if applicable
			try:
				# If tag is in enumerationsMap, replace property values
				parameterMap = remapTable[tag]
				try:
					# Map original property values to values in dictionary
					remappedValue = parameterMap[textIn]
				except KeyError:
					# If value doesn't match any key: use original value instead
					remappedValue = textIn
			except KeyError:
				# If tag doesn't match any key in enumerationsMap, use original value
				remappedValue = textIn
			# Step 2: convert all values to text strings
			if remappedValue != None:
				# Data type
				textType = type(remappedValue)
				# Convert text field, depending on type
				if textType == bytes:
					textOut = strToText(remappedValue)
				else:
					textOut = str(remappedValue)
				# Update output tree
				elt.text = textOut

	def toxml(self, indent = "  "):
		return minidom.parseString(ET.tostring(self, 'ascii')).toprettyxml(indent)
