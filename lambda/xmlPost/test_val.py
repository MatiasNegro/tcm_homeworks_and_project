from lxml import etree
import xml.etree.ElementTree as ET


def format_validator(root):
    source_file = ET.tostring(root)
    schema_file = 'schema.xsd'
    schema_file_type = 'schema_type.xsd'
    flag = True
    flag_type = True

    with open(schema_file) as f_schema, open(schema_file_type) as f_schema_type:

        schema_doc = etree.parse(f_schema)
        schema_type_doc = etree.parse(f_schema_type)
        schema = etree.XMLSchema(schema_doc)
        schema_type = etree.XMLSchema(schema_type_doc)
        parser = etree.XMLParser(schema=schema)
        parser_type = etree.XMLParser(schema = schema_type)

        try:
            doc = etree.fromstring(source_file, parser)
        except etree.XMLSyntaxError as e:
            # this exception is thrown on schema validation error
            # print(e) è solo per eventuale debugging
            #print(e)
            flag = False
        
        try:
            doc = etree.fromstring(source_file, parser_type)
        except etree.XMLSyntaxError as e:
            #print(e)
            flag_type = False

    print(flag)
    return (flag or flag_type)

format_validator(ET.parse('ResultList1.xml').getroot())