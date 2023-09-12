"""
All schema rules tests
"""
from core.core_classes import NodeFlag, Node, Relation, Triple, DirectionFlag,Schema,SchemaParser,RelationTypeEnum
from core.schema_rules import SchemaRules

def test_extract_schema_should_return_schema_object():
    schema_parser = SchemaParser()
    schemas = schema_parser.extract_schemas("(Person,KNOWS,Person)")

    assert schemas[0].source == 'Person'
    assert schemas[0].relation == 'KNOWS'
    assert schemas[0].destination == 'Person'

#-------------------------------------------------------------------------
# Schema validation rules
#-------------------------------------------------------------------------
# Rule 1
def test_if_no_matching_rule_return_false():
    """If the given pattern doesn't fit the graph schema, simply return an empty string
    Covers all Rules from 2-6. If nothing is match, then return string
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Organization"], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.types = ["WORKS_AT"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION

    schema = Schema("Person","WORKS_AT","Department")

    SchemaRules.validate_direction_change(triple, [schema])

    assert triple.has_schema_match is False


# Rule 2
def test_has_same_labels_should_return_true():
    """
    If the relationship is between two nodes of the same labels, there is nothing to validate or correct
    (:Person)-->(:Person), (:Person)-[:KNOWS]->(:Person)
    """

    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Person"], NodeFlag.NODE_FOUND)
    rel = Relation()

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION

    schemas = [Schema('Person','','Person')]
    result = SchemaRules.has_same_labels(triple,schemas)

    assert result is True


# Rule 3
def test_has_undirected_relationsships_should_return_true():
    """
    If the relationship is between two nodes of the same labels,
    there is nothing to validate or correct
    (:Person)-->(:Person), (:Person)-[:KNOWS]->(:Person)
    """

    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Person"], NodeFlag.NODE_FOUND)
    rel = Relation()

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.UNDIRECTED
    schemas = [Schema('Person','','Person')]
    result = SchemaRules.has_same_labels(triple,schemas)

    assert result is True

# Rule 4.1.1
def test_schema_match_one_node_has_missing_labels_should_return_true():
    """
    If a node label is missing in the defined pattern,
    we can still validate if it fits the graph schema
    (:Person)-[:WORKS_AT]->()
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',[], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.types = ["WORKS_AT"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION

    schema = Schema("Person","WORKS_AT","Department")
    relation_type = SchemaRules.validate_relation_type(rel, schema)
    result = SchemaRules.check_schema_when_one_node_has_missing_labels(first_node,second_node,triple,[schema])


    assert relation_type  == RelationTypeEnum.TYPE_IS_VALID
    assert result is True

# Rule 4.1.2
def test_4_1_2_schema_match_one_node_has_missing_labels_should_return_true():
    """
    If a node label is missing in the defined pattern,
    we can still validate if it fits the graph schema
    (:Person)-[:WORKS_AT]->()
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',[], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.types = ["WORKS_AT"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION


    schema = Schema("Department","WORKS_AT","Person")
    result = SchemaRules.check_schema_when_one_node_has_missing_labels(first_node,second_node,triple,[schema])

    assert triple.relation.schema_validated_relation_type == RelationTypeEnum.TYPE_IS_VALID
    assert result is True

# Rule 4.2, Reverse direction
def test_check_schema_when_one_node_has_missing_labels_should_return_true_2():
    """
    If a node label is missing in the defined pattern,
    we can still validate if it fits the graph schema
    (:Person)<-[:WORKS_AT]-()
    """
    second_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    first_node = Node('',[], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.types = ["WORKS_AT"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.DESTINATION_TO_SOURCE

    schema = Schema("Person","WORKS_AT","Department")
    result = SchemaRules.check_schema_when_one_node_has_missing_labels(first_node, second_node, triple,[schema])

    assert result is True


# Rule 5.1 criteria: no relationship, one label
def test_valid_schema_no_relationship_one_label_should_return_true():
    """
    If the input query doesn't define the relationship type,
    but at least one node label is given of a pattern,
    we check if any relationship exists that matches the pattern and correct it if needed
    (:Person)-->(), (:Organization)<-[r]-()
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',[], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.types = []

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION

    schema = Schema("Person","WORKS_AT","Department")
    relation_type = SchemaRules.validate_relation_type(rel,[schema])
    result = SchemaRules.check_schema_when_no_relationship_type_and_at_least_one_label(first_node, second_node, triple, [schema])

    assert result is True

# Rule 5.2 criteria: no relationship, one label, reverse relation direction
def test_valid_schema_no_relationship_one_label_should_return_true_2():
    """
    If the input query doesn't define the relationship type,
    but at least one node label is given of a pattern,
    we check if any relationship exists that matches the pattern and correct it if needed
    (:Person)-->(), (:Organization)<-[r]-()
    """
    second_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    first_node = Node('',[], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.types = []

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.DESTINATION_TO_SOURCE

    schema = Schema("Person","WORKS_AT","Department")
    relation_type = SchemaRules.validate_relation_type(rel,[schema])
    result = SchemaRules.check_schema_when_no_relationship_type_and_at_least_one_label(first_node, second_node, triple, [schema])

    assert result is True
# Rule 6
# When multiple relationships are given or a negation is used in a pattern,
# make sure that at least one of relationship types of the possible fits the given schema
# (:Person)-[:KNOWS|WORKS_AT]->(:Organization), (:Person)-[:!KNOWS]->(:Organization)

# Rule 6.1.1
def test_valid_schema_match_both_nodes_labels_and_relation_should_return_true_1():
    """
    Relation types contains WORK_AT and Schema is correct
    Triple: (:Person)-[:KNOWS|WORKS_AT]->(:Organization), Schema: Person, WORKS_AT, Organization
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Organization"], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.types = ["KNOWS","WORKS_AT"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION

    schema = Schema("Person","WORKS_AT","Organization")
    result = SchemaRules.schema_match_with_both_node_labels(first_node, second_node, triple,[schema])

    assert triple.has_schema_match is True
    assert triple.change_direction() is False
    assert result is True

# Rule 6.1.2
def test_valid_schema_match_both_nodes_labels_and_relation_should_return_change_direction_1():
    """
    Relation types contains WORK_AT and Schema is correct
    Triple: (:Person)-[:KNOWS|WORKS_AT]->(:Organization), Schema: Person, WORKS_AT, Organization
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Organization"], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.types = ["KNOWS","WORKS_AT"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION


    schema = Schema("Organization","WORKS_AT","Person")
    result = SchemaRules.schema_match_with_both_node_labels(first_node, second_node, triple,[schema])

    assert triple.has_schema_match is True
    assert triple.change_direction() is True
    assert result is True

# Rule 6.2.1, check against negative type
def test_valid_schema_match_both_nodes_labels_and_relation_should_return_true_2():
    """
    Relation has negative type KNOWS and Schema has relation that is WORKS_AT wich is not KNOWS
    Triple: (:Person)-[:!KNOWS]->(:Organization), Schema: Person, WORKS_AT, Organization
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Organization"], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.negative_types = ["KNOWS"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION

    schema = Schema("Person","WORKS_AT","Organization")
    result = SchemaRules.schema_match_with_both_node_labels(first_node, second_node, triple,[schema])

    assert triple.has_schema_match is True
    assert triple.change_direction() is False
    assert result is True

# Rule 6.2.2, check against negative type
def test_valid_schema_match_both_nodes_labels_and_relation_should_return_change_direction_2():
    """
    Relation has negative type KNOWS and Schema has relation that is WORKS_AT wich is not KNOWS
    Triple: (:Person)-[:!KNOWS]->(:Organization), Schema: Person, WORKS_AT, Organization
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Organization"], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.negative_types = ["KNOWS"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION
    triple.relation.schema_validated_relation_type = True

    #has_one_way_direction,source_node, destination_node = SchemaRules.get_true_source_destination(triple)

    schema = Schema("Organization","WORKS_AT","Person")
    result = SchemaRules.schema_match_with_both_node_labels(first_node, second_node, triple,[schema])

    assert triple.has_schema_match is True
    assert triple.change_direction() is True
    assert result is True

# Rule 6.3.1, check against negative type, it should override the types
def test_valid_schema_match_both_nodes_labels_and_relation_should_return_true_3():
    """
    Relation has negative type WORKS_AT and type WORKS_AT and Schema has relation that is WORKS_AT.
    The negative type WORKS_AT override the type WORKS_AT
    Triple: (:Person)-[:!WORKS_AT|WORKS_AT]->(:Organization), Schema: Person, WORKS_AT, Organization
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Organization"], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.negative_types = ["WORKS_AT"]
    rel.types = ["WORKS_AT"]

    triple = Triple(first_node,rel,second_node)


    schema = Schema("Person","WORKS_AT","Organization")
    valid_type = triple.relation.schema_validated_relation_type
    result = SchemaRules.schema_match_with_both_node_labels(first_node, second_node, triple,[schema])

    assert valid_type == RelationTypeEnum.NOT_VALID
    assert triple.has_schema_match is False
    assert triple.change_direction() is False
    assert result is False

# Rule 6.3.2, check against negative type, it should override the types
def test_valid_schema_match_both_nodes_labels_and_relation_should_return_change_direction_3():
    """
    Relation has negative type WORKS_AT and type WORKS_AT and Schema has relation that is WORKS_AT.
    The negative type WORKS_AT override the type WORKS_AT
    Triple: (:Person)-[:!WORKS_AT|WORKS_AT]->(:Organization), Schema: Person, WORKS_AT, Organization
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Organization"], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.negative_types = ["WORKS_AT"]
    rel.types = ["WORKS_AT"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION

    # has_one_way_direction,source_node, destination_node = SchemaRules.get_true_source_destination(triple)

    schema = Schema("Person","WORKS_AT","Organization")
    result = SchemaRules.schema_match_with_both_node_labels(first_node, second_node, triple,[schema])

    assert triple.has_schema_match is False
    assert triple.change_direction() is False
    assert result is False

# Rule 6.4.1, check against negative type, it should override the types
def test_valid_schema_match_both_nodes_labels_and_relation_should_return_true_4():
    """
    Relation has negative type KNOWS and type WORKS_AT and Schema has relation that is WORKS_AT.
    The negative type KNOWS is not LEADER_OF in schema and overrides that schema type is not WORKS_AT
    Triple: (:Person)-[:!KNOWS|IS_AT]->(:Organization), Schema: Person, LEADER_OF, Organization
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Organization"], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.negative_types = ["KNOWS"]
    rel.types = ["WORKS_AT"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION

    schema = Schema("Person","LEADER_OF","Organization")
    result = SchemaRules.schema_match_with_both_node_labels(first_node, second_node, triple,[schema])

    assert triple.has_schema_match is True
    assert triple.change_direction() is False
    assert result is True

# Rule 6.4.2, check against negative type, it should override the types
def test_valid_schema_match_both_nodes_labels_and_relation_should_return_change_direction_4():
    """
    Relation has negative type KNOWS and type WORKS_AT and Schema has relation that is WORKS_AT.
    The negative type KNOWS is not LEADER_OF in schema and overrides that schema type is not WORKS_AT
    Triple: (:Person)-[:!KNOWS|IS_AT]->(:Organization), Schema: Person, LEADER_OF, Organization
    """
    first_node = Node('',["Person"],NodeFlag.NODE_FOUND)
    second_node = Node('',["Organization"], NodeFlag.NODE_FOUND)
    rel = Relation()
    rel.negative_types = ["KNOWS"]
    rel.types = ["WORKS_AT"]

    triple = Triple(first_node,rel,second_node)
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION
    #has_one_way_direction,source_node, destination_node = SchemaRules.get_true_source_destination(triple)

    schema = Schema("Organization","LEADER_OF","Person")
    result = SchemaRules.schema_match_with_both_node_labels(first_node, second_node, triple,[schema])

    assert triple.has_schema_match is True
    assert triple.change_direction() is True
    assert result is True


def test_valid_negative_type_should_return_false():
    """ Check that negative_types override types
    """
    rel = Relation()
    rel.negative_types = ['LIVE_IN','WORKS_AT']
    rel.types = ['WORKS_AT']
    schema = Schema('Person','WORKS_AT','Department')
    result = rel.schema_validated_relation_type

    assert result is RelationTypeEnum.NOT_VALID
