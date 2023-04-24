import xml.etree.ElementTree as ET

parser = ET.XMLParser(encoding='utf-8')
tree = ET.parse('amazon_stokens.xml', parser = parser)
root = tree.getroot()

'''
This is how you get the text of the xml file
This is how you get the text of the title tag and the abstract tag
'''
#for child in root:
#    print(child.text)
#import io

#amazon = 'amazon_stokens.xml'
#with io.open(amazon, 'r', encoding='utf-8-sig') as f:
#    contents = f.read()
#    tree = ET.fromstring(contents)
