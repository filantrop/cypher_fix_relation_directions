"""
This module contains a function to fix directions of the arrows
in cyphers e.g. (:Person)-[]->(:Car) could be changed to (:Person)<-[]-(:Car)

"""
#from sys import *
#from io import FileIO
from antlr4 import InputStream,CommonTokenStream,ParseTreeWalker
#from antlr4.tree.Trees import Trees
# from antlr4.error.ErrorListener import ErrorListener
from fixcypher_ast_method.fix_relations_directions  import MyErrorListener,CypherParserListener
from core.core_classes import SchemaParser
from core.schema_rules import SchemaRules

# from parse_antlr_to_neo4j.language.hello.FixRelationsDirectionsListener import FixRelationsDirectionsListener
from parse_antlr_to_cypher.FixRelationsDirectionsParser import FixRelationsDirectionsParser
from parse_antlr_to_cypher.FixRelationsDirectionsLexer import FixRelationsDirectionsLexer


class FixDirections():

    @staticmethod
    def fix_cypher_relations_directions(cypher, schema)->str:
        """Validates the relations directions in the cypher with the schema and outputs a fixed cypher


        Args:
            cypher (str): the cypher to be fixed
            schema (str): the schema to validate against

        Returns:
            str: the cypher with fixed relations directions
        """

        cypher_text_stream = InputStream(cypher)
        lexer = FixRelationsDirectionsLexer(cypher_text_stream)
        lexer.removeErrorListeners()
        tokens = CommonTokenStream(lexer)

        parser = FixRelationsDirectionsParser(tokens)
        parser.removeErrorListeners() # Removes the default error listener
        parser.addErrorListener(MyErrorListener()) # Adds our custom error listener
        tree = parser.start()

        walker = ParseTreeWalker()

        # Walk the cypher and find triples
        listener = CypherParserListener()

        walker.walk(listener, tree)

        # Prepare all triples and directions
        listener.triples_repository.validate_all_triples()

        # Extract schema and variables
        schema_parser = SchemaParser()
        schema_list =  schema_parser.extract_schemas(schema)


        # Iterate all triples and validate direction changes
        for triple in listener.triples_repository.triples:
            SchemaRules.validate_direction_change(triple, schema_list)

        query_fixed = SchemaRules.fix_all_arrow_directions_from_triples(cypher, listener.triples_repository.triples)

        return query_fixed

