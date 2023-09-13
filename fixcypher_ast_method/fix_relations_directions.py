
import textwrap
from antlr4 import Lexer
from antlr4.error.ErrorListener import ErrorListener
from parse_antlr_to_cypher.FixRelationsDirectionsListener import FixRelationsDirectionsListener
from parse_antlr_to_cypher.FixRelationsDirectionsParser import FixRelationsDirectionsParser
from core.core_classes import (Node,Relation,Triple,NodeFlag,TriplesRepository,RelationFlag)

class CypherParserListener(FixRelationsDirectionsListener):
    """ The overide for the g4 listener FixRelationsDirectionsListener"""

    def __init__(self)->None:
        self.triples_repository = TriplesRepository()

    # def exitMyr(self, ctx: HelloParser.MyrContext):
    def is_callable_function(self,obj:object, name: str)->bool:
        """ Checks if it is a callable function

        Returns:
            bool: if callable function
        """
        # Don't return if not type_expression
        if hasattr(obj, name) and \
            callable(getattr(obj, name)):
            return True
        return False


    def enterTriple(self, ctx: FixRelationsDirectionsParser.TripleContext):
        """ Enters triple from ANTLR framework.
            DO NOT CHANGE FUNCTION NAME

        Args:
            ctx (HelloParser.TripleContext): _description_
        """
        extracted_nodes = []
        nodes = []
        ctx_node = ctx.node()
        ctx_relation = ctx.relation()
        extracted_relations = []

        if isinstance(ctx_relation, list):
            extracted_relations = ctx_relation

        elif ctx_relation is not None:
            extracted_relations.append(ctx_relation)

        if isinstance(ctx_node,list):
            extracted_nodes = ctx_node
        elif ctx_node is not None:
            extracted_nodes.append(ctx_node)

        # Add all nodes with variables and label to dictionary for
        # later usage when solving nodes that misses labels
        for extracted_node in extracted_nodes:
            node = self.create_node(extracted_node)
            nodes.append(node)
            self.triples_repository.save_node_variable_and_label(node)

        node_count = len(extracted_nodes)
        previous_node = 0

        # Add all triples to repository
        for node_index in range(1,node_count):
            source = nodes[previous_node]
            destination = nodes[node_index]
            relation = self.set_relation(extracted_relations[previous_node])

            previous_node = node_index

            triple = Triple(source,relation,destination)
            self.triples_repository.triples.append(triple)

    def set_relation(self, relation_context: FixRelationsDirectionsParser.RelationContext)->Relation:
        """Matches relation and sets the attributes

        Args:
            relation_context (HelloParser.RelationContext): _description_

        Returns:
            Relation: _description_
        """

        # Setup default values
        relation = Relation()
        relation.types = []
        relation.negative_types = []
        relation.left = ""
        relation.left_position1 = -1
        relation.left_position2 = -1
        relation.right = ""
        relation.right_position1 = -1
        relation.right_position2 = -1
        relation.variable_length = False
        relation.status = RelationFlag.NONE
        relation.variable = ''

        # Validate and set arrow positions
        self.set_arrow_positions(relation_context,relation)


        # Check if relation body exists
        if self.is_callable_function(relation_context, "relation_body"):

            relation_body = relation_context.relation_body()
            self.set_relation_attributes(relation_body,relation)

        return relation


    def set_relation_attributes(self, relation_body: FixRelationsDirectionsParser.Relation_bodyContext\
                                ,relation: Relation):
        """Sets relation attributes as types
        """

        # Is variable length set
        if relation_body.variable_length() is not None:
            relation.variable_length = True


        if not self.is_callable_function(relation_body,"type_expression"):
            return

        type_expression: FixRelationsDirectionsParser.Type_expressionContext = relation_body.type_expression()

        # Check if type_expression
        if type_expression is None or\
            not isinstance(type_expression.type_name(),list):
            return

        # Get type names
        type_names = type_expression.type_name()

        for type_name_item in type_names:
            type_name: FixRelationsDirectionsParser.Type_nameContext = type_name_item

            t = type_name.NAME().getText()
            t = self.replace_first_and_last_backtick(t)
            if type_name.NEGATION() is not None:
                relation.negative_types.append(t)
            else:
                relation.types.append(t)


    def set_arrow_positions(self, relation_context: FixRelationsDirectionsParser.RelationContext, relation: Relation):
        """ Sets arrow positions for the relation"""

        left_arrow_token = relation_context.LT()
        right_arrow_token = relation_context.GT()
        left_arrow_sub_token = relation_context.SUB()[0]
        right_arrow_sub_token = relation_context.SUB()[1]

        # Check if arrow tokens exists < >
        if left_arrow_token is not None:
            relation.left_position1 = left_arrow_token.symbol.start
            relation.left = left_arrow_token.getText()

        # Set hyphens
        relation.left += left_arrow_sub_token.getText()
        relation.left_position2 = left_arrow_sub_token.symbol.start
        relation.right = right_arrow_sub_token.getText()
        relation.right_position1 = right_arrow_sub_token.symbol.start

        if right_arrow_token is not None:
            relation.right_position2 = right_arrow_token.symbol.start
            relation.right += right_arrow_token.getText()



    def create_node(self, node) -> Node:
        """ Creates node with labels and variables"""
        node_flag = NodeFlag.NONE
        node_position = node.LPAREN().symbol.start
        variable = None
        labels = []
        if hasattr(node,"label_expression"):

            if node.label_expression().NAME():
                name = node.label_expression().NAME()
                labels = [self.replace_first_and_last_backtick(n.getText()) for n in name]

                node_flag = node_flag|NodeFlag.HAS_LABELS
        if hasattr(node,"NAME") and node.NAME() is not None:
            variable = node.NAME().getText()
            variable = self.replace_first_and_last_backtick(variable)
            node_flag = node_flag|NodeFlag.HAS_VARIABLE

        new_node = Node(variable,labels,node_flag)
        new_node.position = node_position

        return new_node

    def replace_first_and_last_backtick(self, text:str)->str:
        """ Removes first and last backticks """
        if text.startswith('`'):
            text = text[1:]

        if text.endswith('`'):
            text = text[:-1]
        return text

class MyErrorListener(ErrorListener):
    """ Custom error listener"""


    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):

        lexer:Lexer = recognizer
        lines = lexer.inputStream.strdata.split('\n')
        error_line = lines[line - 1]  # -1 because lines are 0-based indexed

        # Create a pointer towards the error in the input
        pointer = '~' * column + '^'

        # Suggestion can be based on the type of error or the offending symbol
        suggestion = self.suggest_fix(offendingSymbol, msg)

        # Assemble the error message
        error_msg = f"""
Lexer Error at line {line}:{column}:
{textwrap.indent(error_line, '  ')}
{textwrap.indent(pointer, '  ')}
Message: {msg}
Suggestion: {suggestion}
"""
        print(error_msg)

    def suggest_fix(self, offendingSymbol, msg):
        """ This is a rudimentary example. In a real-world scenario, you might analyze the message or offendingSymbol
         to give more specific advice."""
        if "mismatched input" in msg:
            return "Suggestion: Check the token preceding this location."
        return ""
