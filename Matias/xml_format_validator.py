from lxml import etree

def format_validator(root):
    source_file = root
    schema_file = 'schema.xsd'
    flag = True

    with open(schema_file) as f_schema:

        schema_doc = etree.parse(f_schema)
        schema = etree.XMLSchema(schema_doc)
        parser = etree.XMLParser(schema = schema)

        with root as f_source:
            try:
                doc = etree.parse(f_source, parser)
            except etree.XMLSyntaxError as e:
                # this exception is thrown on schema validation error
                print(e)
                flag = False
    
    return flag
            
    