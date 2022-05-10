from lxml import etree
import xml.etree.ElementTree as ET


def format_validator(root):
    source_file = ET.tostring(root)
    schema_file = 'schema.xsd'
    flag = True

    with open(schema_file) as f_schema:

        schema_doc = etree.parse(f_schema)
        schema = etree.XMLSchema(schema_doc)
        parser = etree.XMLParser(schema = schema)

        
        try:
            doc = etree.fromstring(source_file, parser)
        except etree.XMLSyntaxError as e:
            # this exception is thrown on schema validation error
            #print(e) è solo per eventuale debugging
            print(e)
            flag = False
    print(flag)
    return flag
            
format_validator(ET.parse('jkkbF2020-01-2.xml').getroot())