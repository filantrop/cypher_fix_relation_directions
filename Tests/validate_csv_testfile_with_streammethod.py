"""_summary_

Returns:
    _type_: _description_
"""
import os,timeit
import pandas as pd
from core.core_classes import SchemaParser
from core.schema_rules import SchemaRules
from fixcypher_stream_method.cypher_parser_streammethod import CypherParser

schema_parser = SchemaParser()
cypher_parser = CypherParser()

def do_work_on_testdata(df,verbose=0):

    errors = []

    for index, row in df.iterrows():

        # Debugging row
        # if(index+1!=60):
        #     continue

        #statement,schema,correct_query
        query = df['statement'][index]
        schema = df['schema'][index]
        correct_query = df["correct_query"][index]
        if correct_query is None or pd.isna(correct_query):
            correct_query = ''


        # Extract schema and variables
        schema_list =  schema_parser.extract_schemas(schema)

        # Find all triples and validate them before fixing relations
        cypher_parser.find_and_prepare_all_triples(query)


        for triple in cypher_parser.triples_repository.triples:
              SchemaRules.validate_direction_change(triple, schema_list)

        query_fixed = SchemaRules.fix_all_arrow_directions_from_triples(query, cypher_parser.triples_repository.triples )



        schema_array = []
        for schema in schema_list:
            schema_array.append(f"({schema.source},{schema.relation},{schema.destination})")

        # Verbose: 0 (Nothing), 1 (Only errors), 2 (Everything)
        if (verbose == 1 and query_fixed != correct_query) or\
            verbose == 2:
            row_index = index+2
            p("--------------------------------------")
            p(f"---- Row {row_index}:",1)
            p("--------------------------------------")

            p(f"Triples: {to_string(cypher_parser.triples_repository.triples)}")

            p(f"Schemas: {to_string(schema_list)}")
            p(f"    schema = '{','.join(schema_array)}'")

            p()
            p('    orginal_query = """')
            p(query)
            p('"""')

            p('    fixed_query = """', 1)
            p(query_fixed, 1)
            p('"""', 1)

            p('    correct_query = """',1)
            p(correct_query,1)
            p('"""',1)

        if(query_fixed != correct_query):
            errors.append(row_index)

            p("--Test not valid Fixed query != Correct query--",1)

            p("\n")

    if len(errors)>0:
        p(f"The following rows has errors: {errors}",1)
    else:
        p("All testcases has passed")


def to_string(data):
    if isinstance(data, list):
        return [str(item) for item in data]
    return str(data)

def p(text="",verbose=0):
    if(verbose>=0):
        print(text)

def read_test_dataset_file(filename):

    if not os.path.isfile(filename):
        p(f"Not a valid file {filename}")
        return None
    df = pd.read_csv(filename)

    #statement,schema,correct_query
    if set(["statement","schema","correct_query"]).issubset(df.columns):
        return df
    else:
        return "The required columns are missing in the CSV file"

# usage
def test_main():
    p()

    dataframe = read_test_dataset_file('datasets/examples_2023-09-11.csv')
    #dataframe = read_test_dataset_file('datasets/examples.csv')

    if isinstance(dataframe, pd.DataFrame):

        # Verbose: 0 (Nothing), 1 (Only errors), 2 (Everything)
        verbose = 0
        do_work_on_testdata(dataframe,verbose)

execution_time = timeit.timeit(test_main, number=1)
print(f"Execution time: {execution_time} seconds")

