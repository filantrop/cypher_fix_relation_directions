"""Contains classes shared among other modules
"""
from enum import IntFlag, auto,Enum
from typing import List
import re
import json
def to_string(data):
    if isinstance(data, list):
        return [str(item) for item in data]
    return str(data)

def json_serializable(cls):
    """
    A class decorator that adds a to_json method to a class,
    assuming all attributes of the class are JSON serializable.
    """
    def to_json(self):
            if isinstance(self, (Enum, IntFlag)):
                return self.name
            result = {}
            for k, v in vars(self).items():
                if not k.startswith('_'):
                    if hasattr(v, 'to_json'):
                        result[k] = v.to_json()
                    else:
                        result[k] = v
            return result

    def to_json_string(self, indent=4):
        return json.dumps(self.to_json(), indent=indent)

    cls.to_json = to_json
    cls.to_json_string = to_json_string
    return cls

@json_serializable
class RelationTypeEnum(Enum):
    """ The status of the relationtype """
    NOT_VALID = 1
    TYPE_IS_VALID = 2
    TYPE_IS_EMPTY = 3
@json_serializable
class NodeFlag(IntFlag):
    """
    A flag enum representing different node states.
    """
    NONE = auto()
    NODE_NOT_FOUND = auto()
    HAS_VARIABLE = auto()
    HAS_LABELS = auto()
    NODE_FOUND = auto()
    DO_LABEL_LOOKUP = HAS_VARIABLE&~HAS_LABELS

@json_serializable
class RelationFlag(IntFlag):
    """
    A flag enum representing different relation status.
    """
    NONE = auto()
    RELATION_FOUND = auto()
    HAS_VARIABLE = auto()
    HAS_NEGATIVE_TYPES = auto()
    HAS_TYPES = auto()
    HAS_ANY_TYPES = HAS_TYPES | HAS_NEGATIVE_TYPES
    HAS_VARIABLE_LENGTH = auto()

@json_serializable
class DirectionFlag(IntFlag):
    """
    A flag enum representing different directions.
    """
    NOT_SET = auto()
    SOURCE_TO_DESTINATION = auto()
    DESTINATION_TO_SOURCE = auto()
    DIRECTION_IN_BOTH_ENDS = auto()
    HAS_DIRECTION_ERROR = auto()
    UNDIRECTED = auto()
@json_serializable
class Node:
    """
    Represents a node in the application.

    This class is used to store information about a specific node,
    including its variable, labels, and status.
    """
    def __init__(self, variable, labels, status: NodeFlag) -> None:
        self.variable = variable
        self.labels = labels
        self.status = status
        self.position = -1
        self.label_is_looked_up = False
    def __str__(self):
        return f"({self.variable}:{':'.join(self.labels)})"

@json_serializable
class Relation:
    """
    This class represents a relationship.
    """
    def __init__(self) -> None:
        self.status = RelationFlag._missing_
        self.types = []
        self.negative_types = []
        self.variable = None
        self.variable_length = None
        self.left = None
        self.left_position1 = None
        self.left_position2 = None
        self.right = None
        self.right_position1 = None
        self.right_position2 = None
        self.valid_schema = None
        self.schema_validated_relation_type = RelationTypeEnum.NOT_VALID

    def __str__(self):
        all_types = []

        if len(self.types)>0:
            all_types.append('|'.join(self.types))
        if len(self.negative_types)>0:
            all_types.append('|!'.join(self.negative_types))
        return f"{self.left}[{self.variable}:{'|!'.join(all_types)}]{self.right}"

@json_serializable
class Schema:
    """
    This class represents a schema.
    """
    def __init__(self, source: str, relation: str, destination: str) -> None:

        self.source = source
        self.relation = relation
        self.destination = destination

    def __str__(self):
        return f"(:{self.source})-[:{self.relation}]->(:{self.destination})"

@json_serializable
class Triple:
    """
    This class represents a triple.
    """
    def __init__(self, first_node: Node, relation: Relation, second_node: Node) -> None:
        self.first_node = first_node
        self.relation = relation
        self.second_node = second_node
        self.direction = DirectionFlag.NOT_SET
        #self.schema_validated_relation_type = False
        #self.change_direction = False
        # When one of the schemas matches source label, relation type and destination label in any order
        self.has_schema_match = False
        self.schema_validated_direction = DirectionFlag.NOT_SET

    def __str__(self):
        """ tostring method """
        return f"{to_string(self.first_node)}{to_string(self.relation)}{to_string(self.second_node)}"


    def change_direction(self)->bool:
        """Checks if direction needs to change
            if the direction on the triple and the schema direction is opposite
            then change
        Returns:
            bool: True for change, False for not change
        """
        if self.direction & DirectionFlag.SOURCE_TO_DESTINATION and \
            self.schema_validated_direction & DirectionFlag.DESTINATION_TO_SOURCE:
            return True
        if self.direction & DirectionFlag.DESTINATION_TO_SOURCE and \
            self.schema_validated_direction & DirectionFlag.SOURCE_TO_DESTINATION:
            return True
        return False

@json_serializable
class SchemaParser:
    """
    Schema parser that parses an string to schemas
    """
    def __init__(self)->None:
        pass

    def extract_schemas(self, schema_string)->List[Schema]:
        """Extracts schema from string

        Args:
            schema_string (string): string in the format "(Source label, Relation type, Destination label),(Source2 label, Relation2 type, Destination2 label)"
            multiple triples can be given

        Returns:
            List[Schema]: returns a list of schema objects
        """
        # Find all matches for tuple-like structures in the string
        matches = re.findall(r"\(([^)]+)\)", schema_string)

        schemas = []
        for match in matches:
            # Split the match by commas and strip whitespace
            elements = [element.strip() for element in match.split(",")]

            # Add a new relationship dictionary to the list
            if len(elements) == 3:
                schemas.append(Schema(elements[0],elements[1],elements[2]))
            else:
                raise Exception(f"Can't extract schemas {schema_string}")

        return schemas

@json_serializable
class TriplesRepository:
    """ Holds the triples and the rules for preparing them"""

    def __init__(self)->None:
        self.reset()

    def reset(self)->None:
        self.triples:List[Triple] = []
        # node variables and labels to use when a node has missing labels
        self.node_variables = {}

    def validate_all_triples(self):
        """ Fill missing node labels and validate directions"""

        # Fill all node that is missing labels
        for triple in self.triples:
            self.fill_missing_node_labels(triple.first_node)
            self.fill_missing_node_labels(triple.second_node)
            self.validate_direction_of_triple(triple)

    def validate_direction_of_triple(self, triple: Triple):
        """Validates the type of direction in the triple

        Args:
            triple (Triple): _description_
        """

        if triple.relation.left == "<-":
            triple.direction |= DirectionFlag.DESTINATION_TO_SOURCE

        elif triple.relation.left != "-":
            triple.direction |= DirectionFlag.HAS_DIRECTION_ERROR

        if triple.relation.right == "->":
            triple.direction |= DirectionFlag.SOURCE_TO_DESTINATION

        elif triple.relation.right != "-":
            triple.direction |= DirectionFlag.HAS_DIRECTION_ERROR

        if (
            triple.direction & DirectionFlag.DESTINATION_TO_SOURCE
        ) and triple.direction & DirectionFlag.SOURCE_TO_DESTINATION:
            triple.direction |= DirectionFlag.DIRECTION_IN_BOTH_ENDS

        if triple.relation.left == "-" and triple.relation.right == "-":
            triple.direction |= DirectionFlag.UNDIRECTED

    def fill_missing_node_labels(self, node: Node):
        """If the node has varible and is missing the label, then it tries to fix it

        Args:
            node (Node): _description_
        """
        if (node.status & NodeFlag.HAS_VARIABLE) and not (
            node.status & NodeFlag.HAS_LABELS
        ):
            self.find_labels_for_node_variable(node)

    def save_node_variable_and_label(self, node: Node):
        """
        This method saves the given node's variable and label in the node_variables dictionary.

        Args:
            node (Node): The node object containing the variable and label.

        Returns:
            None
        """
        if not (
            (node.status & NodeFlag.HAS_LABELS)
            and (node.status & NodeFlag.HAS_VARIABLE)
        ):
            return

        if self.node_variables.get(node.variable) is None:
            self.node_variables[node.variable] = []
            self.node_variables[node.variable].append({})
        else:
            self.node_variables[node.variable].append({})

        for label in node.labels:
            # Add to last array for variable
            self.node_variables[node.variable][-1][label] = node.position

    def get_node_labels_from_variable(self, variable):
        """Gets labels from variable name

        Args:
            variable (string): variable name

        Returns:
            labels: the labels
        """
        if self.node_variables.get(variable) is None:
            return None
        if self.node_variables[variable][-1] is None:
            return None

        # Gets the last set labels
        return self.node_variables[variable][-1]


    def find_labels_for_node_variable(self, node: Node):
        """Finds any node variable in the global storage of key, values : variable, label

        Args:
            node (Node): The node where the variable is from
        """
        labels = self.get_node_labels_from_variable(node.variable)

        if labels is None:
            return
        node.labels = labels
        node.label_is_looked_up = True