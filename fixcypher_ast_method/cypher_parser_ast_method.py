from sys import *
#from io import FileIO
from antlr4 import InputStream,CommonTokenStream,ParseTreeWalker
from antlr4.error.ErrorListener import ConsoleErrorListener,ErrorListener

from fixcypher_ast_method.fixdirections_astmethod import (
    FixRelationsDirectionsLexer,
    FixRelationsDirectionsParser,
    CypherParserListener
)
from core.core_classes import (Node,Relation,Triple,NodeFlag,TriplesRepository)


class CypherParser:
    """
    A class for parsing Cypher queries

    Args:
        cypher (str): The Cypher query to parse
        schema (str): The database schema to use for parsing
    """

    def __init__(self):
        self.antlr_listener = CypherParserListener()
        self.triples_repository = self.antlr_listener.triples_repository

    def reset(self):
        self.triples_repository.reset()

    def find_and_prepare_all_triples(self, cypher):
        self.reset()
        """Finds all triples in the actual Cypher"""
        self.cypher = cypher
        # Parse cypher and find all triples (n:Person)-[:WORKS_AT]->(:Department)
        self.find_triples()
        #self.triples_repository.prepare_all_triples()

    def find_triples(self):
        """ Find all triples in the cypher"""

        #my_parser_error_listener = MyErrorListener()
        inputStream = InputStream(self.cypher)

        lexer = FixRelationsDirectionsLexer(inputStream)
        lexer.removeErrorListener(ConsoleErrorListener.INSTANCE)
        #lexer.addErrorListener(my_parser_error_listener)
        tokens = CommonTokenStream(lexer)

        parser = FixRelationsDirectionsParser(tokens)

        parser.removeErrorListeners() # Removes the default error listener
        #parser.addErrorListener(my_parser_error_listener) # Adds our custom error listener

        tree = parser.start()

        walker = ParseTreeWalker()
        walker.walk(self.antlr_listener, tree)

        # Validates all triples
        self.antlr_listener.triples_repository.validate_all_triples()



