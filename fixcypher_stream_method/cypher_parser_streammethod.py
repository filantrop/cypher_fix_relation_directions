"""
This module contains a function to fix directions of the arrows
in cyphers e.g. (:Person)-[]->(:Car) could be changed to (:Person)<-[]-(:Car)

"""
import io
from core.core_classes import (
    NodeFlag,
    Node,
    Relation,
    Triple,
    RelationFlag,
    TriplesRepository
)


class CypherParser:
    """
    A class for parsing Cypher queries

    Args:
        cypher (str): The Cypher query to parse
        schema (str): The database schema to use for parsing
    """

    def __init__(self,cypher=None):
        self.triples_repository = TriplesRepository()
        self.current_triple = None
        if cypher is not None:
            self.reset()
            self.set_cypher(cypher)


    def reset(self):
        """ Reset to init"""
        self.input_stream = None
        self.cypher = None
        self.word = ""
        self.current_character = None
        self.position = None
        self.current_triple: Triple = None
        self.triples_repository.reset()


    # Character constants
    LPARENTHESIS = "("
    RPARENTHESIS = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LCURLY = "{"
    RCURLY = "}"
    COLON = ":"
    BACKTICK = "`"
    SINGLE_QUOTATION = "'"
    DOUBLE_QOUTATION = '"'
    COMMA = ","
    LEFT = "<"
    RIGHT = ">"
    HYPHEN = "-"
    TYPE_NEGATION = "!"
    OR_RELATION = "|"
    VARIABLE_LENGTH = "*"

    # Status messages
    STATUS_NO_COMPLETE_NODE_FOUND = "No complete node found"

    def set_cypher(self,cypher):
        """ Sets cypher and set input stream"""

        self.input_stream = io.StringIO(cypher)
        self.cypher = cypher

    def find_and_prepare_all_triples(self, cypher):
        """Finds all triples in the actual Cypher"""
        self.reset()
        self.set_cypher(cypher)

        # Parse cypher and find all triples (n:Person)-[:WORKS_AT]->(:Department)
        self.find_triples()
        self.triples_repository.validate_all_triples()

    def find_triples(self):
        """The starting point to find the triples in the cypher, first step one character in
        the stream the start finding the first node e.g. (p:Person)

        """
        self.next_character()
        self.skip_whitespaces()

        self.validate_if_next_is_a_node()

    def validate_if_next_is_a_node(self):
        """ Find and validate found node. Then add any relation. Otherwise starts over and tries to find the next node
        """
        if self.current_character == "":
            return
        # Look for node
        found_node = self.parse_if_node()

        # if first_node is None and tmp_node.status & NodeFlag.NODE_NOT_FOUND:
        if found_node.status & NodeFlag.NODE_NOT_FOUND:
            self.validate_if_next_is_a_node()

        # If node is found set node
        if found_node.status & NodeFlag.NODE_FOUND:
            if self.current_triple is None:
                self.current_triple = Triple(None, None, None)

            if self.current_triple.first_node is None:
                self.current_triple.first_node = found_node

            elif self.current_triple.second_node is None:
                self.current_triple.second_node = found_node

            # Check if valid triple
            if (
                (self.current_triple.first_node is not None)
                and (self.current_triple.relation is not None)
                and (self.current_triple.second_node is not None)
            ):
                second_node = self.current_triple.second_node
                tmp_triple = self.current_triple
                self.triples_repository.triples.append(tmp_triple)
                self.current_triple = Triple(None, None, None)
                self.current_triple.first_node = second_node

                # Try to find relation
                self.validate_if_next_is_a_relation()

            # Save node value and labels in dictionary if criteria is met
            self.triples_repository.save_node_variable_and_label(found_node)

            self.validate_if_next_is_a_relation()

            self.validate_if_next_is_a_node()

    def validate_if_next_is_a_relation(self):
        """Find and validate any relationship, otherwise continue to find the next node.
        """
        if self.current_character == "":
            return

        relation = self.parse_if_relation()

        self.skip_whitespaces()

        # No relation is found directly after
        if relation.status & RelationFlag.RELATION_FOUND:
            self.current_triple.relation = relation

        else:
            self.current_triple = None

        self.skip_whitespaces()
        self.validate_if_next_is_a_node()


    def parse_if_node(self):
        """
        Check if the next character in the stream is a valid start of a node.
        In this case left parenthesis. Then parses the node from the rules.

        Returns:
            Node: A new object of Node Class
        """

        position = self.position

        variable = ""
        labels = []

        # If another Left Parenthesis, return
        if self.current_character == CypherParser.LPARENTHESIS:
            self.next_character()

            self.skip_whitespaces()

            # If it comes one more time SKIP!
            if self.current_character == CypherParser.LPARENTHESIS:
                node = Node("", [], NodeFlag.NODE_NOT_FOUND)
                return node

        elif self.current_character != CypherParser.LPARENTHESIS:
            self.next_character()
            return Node("", [], NodeFlag.NODE_NOT_FOUND)

        # Find variable of node the p in (p:Person)
        variable = self.get_cypher_word()

        self.skip_whitespaces()

        # Find labels after :
        if self.current_character == CypherParser.COLON:
            labels = self.find_labels()

        self.skip_whitespaces()
        self.skip_escape_signs()

        self.skip_property_block()

        if self.current_character == CypherParser.RPARENTHESIS:
            self.next_character()
            status = NodeFlag.NODE_FOUND
            if variable != "":
                status |= NodeFlag.HAS_VARIABLE
            if len(labels) > 0:
                status |= NodeFlag.HAS_LABELS

            node = Node(variable, labels, status)
            node.position = position

            return node

        node = Node("", [], NodeFlag.NODE_NOT_FOUND)
        node.position = position
        return node



    def parse_if_relation(self):
        """
        Check if the next character in the stream is a valid start of a relation.
        In this case hyphen. Then parses the relation from the rules.

        Returns:
            Node: A new object of Relation Class
        """
        rel = Relation()

        rel.status = RelationFlag.NONE
        rel.types = []
        rel.negative_types = []
        rel.left = ""
        rel.left_position1 = -1
        rel.left_position2 = -1

        rel.right = ""
        rel.right_position1 = -1
        rel.right_position2 = -1

        rel.variable_length = False

        rel.variable = ""

        # Does it start with Hyphen (-)
        if self.current_character == CypherParser.HYPHEN:
            rel.left_position2 = self.position - 1
            rel.left += self.current_character

            self.next_character()
            self.skip_whitespaces()

            # Is next bracket then the relation has a body
            if self.current_character == CypherParser.LBRACKET:

                self.get_relation_body_inside_bracket(rel)
                if rel.status & RelationFlag.NOT_VALID_RELATION:
                    return rel

                if len(rel.types) > 0:
                    rel.status |= RelationFlag.HAS_TYPES
                if len(rel.negative_types) > 0:
                    rel.status |= RelationFlag.HAS_NEGATIVE_TYPES
                if rel.variable != "":
                    rel.status |= RelationFlag.HAS_VARIABLE
                if rel.variable_length is True:
                    rel.status |= RelationFlag.HAS_VARIABLE_LENGTH

            self.skip_whitespaces()

            # Is it an empty arrow
            if self.current_character == CypherParser.HYPHEN:
                rel.status |= RelationFlag.RELATION_FOUND
                rel.right_position1 = self.position - 1
                rel.right += self.current_character

                self.next_character()
                self.skip_whitespaces()

                # Ends with right (>)
                if self.current_character == CypherParser.RIGHT:
                    rel.right_position2 = self.position - 1
                    rel.right += self.current_character
                    self.next_character()

            else:
                rel.status = RelationFlag.NOT_VALID_RELATION
                return rel

            return rel

        # Starts with left (<)
        if self.current_character == CypherParser.LEFT:
            rel.left_position1 = self.position - 1
            rel.left += self.current_character

            self.next_character()
            self.skip_whitespaces()

            # Is it an empty arrow
            if self.current_character == CypherParser.HYPHEN:
                rel.left_position2 = self.position - 1
                rel.left += self.current_character

                self.next_character()
                self.skip_whitespaces()

                # Is next bracket then the relation has a body
                if self.current_character == CypherParser.LBRACKET:
                    self.get_relation_body_inside_bracket(rel)

                    if rel.status & RelationFlag.NOT_VALID_RELATION:
                        return rel

                    if len(rel.types) > 0:
                        rel.status |= RelationFlag.HAS_TYPES
                    if len(rel.negative_types) > 0:
                        rel.status |= RelationFlag.HAS_NEGATIVE_TYPES
                    if rel.variable != "":
                        rel.status |= RelationFlag.HAS_VARIABLE
                    if rel.variable_length is True:
                        rel.status |= RelationFlag.HAS_VARIABLE_LENGTH

                self.skip_whitespaces()

                # Is it an empty arrow
                if self.current_character == CypherParser.HYPHEN:
                    rel.status |= RelationFlag.RELATION_FOUND
                    rel.right_position1 = self.position - 1
                    rel.right += self.current_character

                    self.next_character()
                    self.skip_whitespaces()
                else:
                    rel.status = RelationFlag.NOT_VALID_RELATION
                    return rel

            else:
                rel.status = RelationFlag.NOT_VALID_RELATION
                return rel

        return rel

    def get_relation_body_inside_bracket(self,rel:Relation):
        """Parses the relation information inside bracket [....]

        Returns:
            types: relation types
            negative_types: relation types that is negative
            variable_length: if there is a variable length set
            variable: the name of the variable
        """
        rel.types = []
        rel.negative_types = []
        rel.variable_length = False
        rel.variable = ""

        if self.current_character != CypherParser.LBRACKET:
            rel.status = RelationFlag.NOT_VALID_RELATION
            return

        self.next_character()
        self.skip_whitespaces()

        # Find variable of node
        rel.variable = self.get_cypher_word()

        self.skip_whitespaces()

        rel.types, rel.negative_types = self.find_types()

        self.skip_whitespaces()

        rel.variable_length = self.skip_variable_length()
        self.skip_whitespaces()
        self.skip_property_block()
        self.skip_whitespaces()
        if self.current_character == CypherParser.RBRACKET:
            self.next_character()
        else:
            rel.status = RelationFlag.NOT_VALID_RELATION
            return

        return

    def find_variable(self):
        """Get a variable if there is any

        Returns:
            string: variable string
        """
        variable = self.current_character
        while True:
            self.next_character()

            if self.is_valid_variable_character(self.current_character):
                variable += self.current_character
            else:
                break
        return variable

    def find_labels(self):
        """Get labels if there is any

        Returns:
            labels: string array of labels
        """
        labels = []
        label = ""

        if self.current_character != CypherParser.COLON:
            return [], []
        self.next_character()
        self.skip_whitespaces()
        while True:
            label = self.get_cypher_word()
            labels.append(label)
            self.skip_whitespaces()

            if self.current_character == CypherParser.COLON:
                self.next_character()
                self.skip_whitespaces()
                continue
            break
        return labels

    # Finds types and negative types
    def find_types(self):
        """Get types if there is any

        Returns:
            types: string array of types
            negative_types: string array of negative types
        """
        types = []
        negative_types = []
        # Find labels
        if self.current_character != CypherParser.COLON:
            return [], []
        self.next_character()
        self.skip_whitespaces()

        while True:
            if self.current_character == CypherParser.TYPE_NEGATION:
                self.next_character()
                self.skip_whitespaces()
                word = self.get_cypher_word()
                negative_types.append(word)
                self.skip_whitespaces()

            else:
                word = self.get_cypher_word()
                types.append(word)
                self.skip_whitespaces()

            if self.current_character == CypherParser.OR_RELATION:
                self.next_character()
                self.skip_whitespaces()
                continue

            break

        return types, negative_types

    def skip_variable_length(self):
        """checks and skips over if the next part in stream is a variable length (*  1 .. 2 )

        Returns:
            bool: True for if there is any False if not
        """
        if self.current_character != CypherParser.VARIABLE_LENGTH:
            return False
        self.next_character()
        self.skip_whitespaces()
        self.skip_number()
        self.skip_whitespaces()
        if self.current_character == CypherParser.RBRACKET:
            return True

        if self.current_character == ".":
            self.next_character()
            if self.current_character == ".":
                self.next_character()
                self.skip_whitespaces()
                self.skip_number()
                self.skip_whitespaces()
                return True
        return False

    def skip_number(self):
        """ Skips numbers [0-9]* til no more number"""
        while True:
            if self.current_character.isdigit():
                self.next_character()
            else:
                return

    def skip_escape_signs(self):
        """ Escape escape signs and the character"""
        while True:
            if self.current_character == "\\":
                self.next_character()
                self.next_character()
            else:
                return

    def skip_whitespaces(self):
        """ Skip the next whitespaces"""
        while True:
            if self.current_character.isspace():
                self.next_character()
            else:
                return

    def skip_property_block(self):
        """ Skips the property block with contents { }"""
        if self.current_character != CypherParser.LCURLY:
            return
        while True:
            self.next_character()

            self.skip_property()

            if self.current_character == CypherParser.RCURLY:
                self.next_character()
                return
            if self.current_character is None:
                return

    def skip_property(self):
        """ Skips the properties in the { Name: 'Value'}"""
        self.skip_escape_signs()
        self.skip_whitespaces()
        self.skip_property_name()
        self.skip_whitespaces()
        if self.current_character == CypherParser.COLON:
            self.next_character()
            self.skip_whitespaces()
            self.skip_property_value()
            self.skip_whitespaces()
            if self.current_character == CypherParser.COMMA:
                self.next_character()
                self.skip_property()
            return
        return

    def skip_property_name(self):
        """ Skips property name"""
        self.get_cypher_word()

    def get_cypher_word(self):
        """ Gets valid cypher word, either variable, property, type or label"""

        word = ""
        if self.current_character == CypherParser.BACKTICK:

            self.next_character()
            self.word = self.current_character
            while True:
                self.skip_escape_signs()
                if self.current_character != CypherParser.BACKTICK:
                    word = self.word
                else:
                    self.next_character()
                    self.reset_word()
                    return word

                self.next_character()
        if self.is_valid_start_variable_character(self.current_character):
            self.word = self.current_character
            word = self.word
            self.next_character()
            while True:
                if self.is_valid_variable_character(self.current_character) is False:
                    return word
                word = self.word
                self.next_character()
        return ""

    def skip_property_value(self):
        """ Skips property value, eight single or double quotation"""
        self.skip_quotation()
        self.skip_double_quotation()

    def skip_quotation(self):
        """ Skips quotation with content"""
        if self.current_character == "'":
            self.next_character()
            while True:
                self.skip_escape_signs()
                if self.current_character == "'":
                    self.next_character()
                    return
                self.next_character()
        return

    def skip_double_quotation(self):
        """ Skips double quotation"""
        if self.current_character == '"':
            self.next_character()
            while True:
                self.skip_escape_signs()
                if self.current_character == '"':
                    self.next_character()
                    return
                self.next_character()
        return

    def is_valid_start_variable_character(self, char):
        """ Checks if the character is a start of a valid variable"""
        if not char:
            return False

        if not char.isalpha():
            return False
        return True

    def is_valid_variable_character(self, char):
        """ Check if the character is a valid variable character"""
        if not (char.isalpha() or char.isdigit() or char == "_"):
            return False
        return True

    def is_valid_cypher_label_character(self, char):
        """ Checks if it is a valid cypher label character"""
        if char.isalpha() or char.isdigit() or char == "_":
            return True
        return False

    def next_character(self):
        """ reads the next character in the stream"""
        c = self.input_stream.read(1)

        # Adds character to word
        self.word += c

        # Sets current character
        self.current_character = c

        # Sets the position of the character
        self.position = self.input_stream.tell()

    def reset_word(self):
        """ Resets the global word"""
        word = self.word
        self.word = ""
        return word
