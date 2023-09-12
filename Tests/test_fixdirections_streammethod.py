"""
All parsing rules tests

"""
#from context import
from core.core_classes import NodeFlag, Node, Relation, Triple, DirectionFlag,RelationFlag
from core.schema_rules import SchemaRules
from fixcypher_stream_method.cypher_parser_streammethod import CypherParser
from fixcypher_stream_method.fixdirections_streammethod import FixDirections



# Cypher empty Node
def test_EmptyNode_ShouldReturnNothingEndWithCharacterEnd():
    cypher = "()*"
    variable = ""

    cp = CypherParser(cypher)

    cp.next_character()
    n = cp.find_node()

    assert n.variable==variable
    assert len(n.labels)==0
    assert cp.current_character == '*'
    assert n.status & NodeFlag.NODE_FOUND

# Cypher Node with variable
def test_NodeWithVariable_ShouldReturnNothingEndWithCharacterEnd():
    cypher = """(n)*"""
    variable = "n"

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert len(n.labels)==0
    assert cp.current_character == '*'
    assert n.status & NodeFlag.NODE_FOUND


# Cypher Node with label
def test_ParseSimpleLabelShouldReturnLabel():
    cypher = "(:Road)"
    variable = ""
    label = "Road"

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert label==n.labels[0]
    assert n.status & NodeFlag.NODE_FOUND

# Cypher Node with label
def test_ParseMultipleLabels_ShouldReturnLabel():
    cypher = "(:Person:Employee)"
    variable = ""

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert n.labels[0]=='Person'
    assert n.labels[1]=='Employee'
    assert n.status & NodeFlag.NODE_FOUND

# Cypher Node with label
def test_ParseMultipleLabelsWithVariable_ShouldReturnLabel():
    cypher = "(`person`:Person:Employee)"

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert n.variable=="person"
    assert n.labels[0]=='Person'
    assert n.labels[1]=='Employee'
    assert n.status & NodeFlag.NODE_FOUND

# Cypher node with variable and label
def test_ParseSimpleNodeWithVariableAndLabel_ShouldExtractVariableAndLabel():
    cypher = "(r:Road)"
    variable = "r"
    label = "Road"

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert label==n.labels[0]
    assert n.status & NodeFlag.NODE_FOUND
# Cypher node with double parenthesis and variable and label
def test_DoubleParenthesis_and_NodeWithVariableAndLabel_ShouldExtractVariableAndLabel():
    cypher = "((person:Person)-[:DIRECTED*]->(:Person))"
    variable = "person"
    label = "Person"

    cyp = CypherParser(cypher)
    cyp.find_triples()

    triple = cyp.triples_repository.triples[0]

    assert triple.first_node.variable == 'person'


# MATCH p = ((person:Person)-[:DIRECTED*]->(:Person))
# WHERE person.name = 'Walt Disney'
# RETURN p

# Cypher node with spaces and variable and label
def test_Spaces_ParseNodeWithVariableAndLabel_ShouldExtractVariableAndLabel():
    cypher = "( r : Road )"
    variable = "r"
    label = "Road"

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert label==n.labels[0]
    assert n.status & NodeFlag.NODE_FOUND


# Cypher node with spaces, tabs and returns and variable and label
def test_MultipleSpaceTypes_ParseNodeWithVariableAndLabelAnd_ShouldExtractVariableAndLabel():
    cypher = """( r :

    Road )"""
    variable = "r"
    label = "Road"

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert label==n.labels[0]
    assert n.status & NodeFlag.NODE_FOUND


# False Cypher node with escapesigns variable and label
def test_SkipEscapeSigns_ParseNodeWithVariableAndLabelAnd_ShouldReturnNoNodeFound():
    cypher = "(r:Road \)"
    variable = ""


    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert len(n.labels)==0
    assert n.status & NodeFlag.NODE_NOT_FOUND

# Cypher node with escapesigns variable and label
def test_SkipEscapeSigns_ParseNodeWithVariableAndLabelAnd_ShouldReturnValidNode():
    cypher = "(r:Road \))"
    label = "Road"
    variable = "r"

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert label == n.labels[0]
    assert n.status & NodeFlag.NODE_FOUND


# Cypher node with propertyblock, and end character )
def test_SkipPropertyBlock_ShouldReturnEndCharacter():
    cypher = """{Name: "Test"})"""

    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_property_block()

    assert cp.current_character == CypherParser.RPARENTHESIS



# Cypher node with propertyblock, and escapesigns until end of propertyblock and return end character )
def test_SkipPropertyBlockWithEscapeSigns_ShouldReturnEndCharacter():
    cypher = """{`Name`: "Test\)

    " }) """

    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_property_block()

    assert cp.current_character == CypherParser.RPARENTHESIS

# Cypher node with propertyblock, and escapesigns until end of propertyblock and return end character )
def test_SkipPropertyBlockWithBackTicksInName_ShouldReturnEndCharacter():
    cypher = """{`Name}`: "Test"})"""

    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_property_block()

    assert cp.current_character == CypherParser.RPARENTHESIS

# Cypher node with propertyblock  variable and label
def test_SkipPropertyBlock_ParseNodeWithVariableAndLabelAnd_ShouldReturnValidNode():
    cypher = "(r:Road {`Rudimentär`: 'Test'})"
    label = "Road"
    variable = "r"

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert label == n.labels[0]
    assert n.status & NodeFlag.NODE_FOUND

# Cypher node with propertyblock  variable and label
def test_SkipPropertyBlockWithMultipleProperties_ParseNodeWithVariableAndLabelAnd_ShouldReturnValidNode():
    cypher = """(r:Road {`Rudimentär`: 'Test}', Namn: "Mitt namn"})"""
    label = "Road"
    variable = "r"

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert label == n.labels[0]
    assert n.status & NodeFlag.NODE_FOUND

# Skip propertyname
def test_SkipPropertyNameWithBackTick_ShouldReturnEndCharacter():
    cypher = "`test\``*"

    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_property_name()

    assert cp.current_character == '*'

def test_SkipPropertyName_ShouldReturnEndCharacter():
    cypher = "Name*"

    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_property_name()

    assert cp.current_character == '*'

# Skip propertyvalue
def test_SkipPropertyValueWithQuotation_ShouldReturnEndCharacter():
    cypher = "'Test\"'*"

    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_property_value()

    assert cp.current_character == '*'

# Skip propertyvalue with multiple rows
def test_SkipPropertyValueWithQuotationAndMultipleRows_ShouldReturnEndCharacter():
    cypher = """'Te


    st\"'*"""

    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_property_value()

    assert cp.current_character == '*'

# Skip propertyvalue
def test_SkipProperty_ShouldReturnEndCharacter():
    cypher = "`Test` : 'Test'*"

    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_property()

    assert cp.current_character == '*'


# Cypher node with propertyblock  variable and label
def test_SkipPropertyBlockWithMultipleProperties_ShouldReturnEndCharacter():
    cypher = """{`Rudimentär`: 'Test}',


    Namn: "Mitt namn\}"}*"""


    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_property_block()

    assert cp.current_character == '*'


# Cypher node with properties and  variable and label
def test_SkipPropertyBlockWithMultipleProperties_ParseNodeWithVariableAndLabelAnd_ShouldReturnValidNodeAndEndCharacter():
    cypher = """(r:Road {`Rudimentär`: 'Test}', Namn: "Mitt namn\}"})*"""
    label = "Road"
    variable = "r"

    cp = CypherParser(cypher)
    cp.next_character()
    n = cp.find_node()

    assert variable==n.variable
    assert label == n.labels[0]
    assert cp.current_character == '*'


# --------------------------------------------------------------------------
#  Find relations
# --------------------------------------------------------------------------
# Simple Cypher relation
def test_OnlyRelationWithoutDirection_ShouldReturnValidRelation():
    cypher = "--"

    cp = CypherParser(cypher)
    cp.next_character()
    r = cp.find_relation()

    assert r.left==CypherParser.HYPHEN
    assert r.right==CypherParser.HYPHEN
    assert r.left_position1==-1
    assert r.left_position2==0
    assert r.right_position1==1
    assert r.right_position2==-1
    assert len(r.types)==0
    assert len(r.negative_types)==0
    assert r.variable_length is False
    assert r.status&RelationFlag.RELATION_FOUND

# Simple Cypher relation with left arrow
def test_OnlyRelationWitLeftDirection_ShouldReturnValidRelation():
    cypher = "<--"
    type = ""

    cp = CypherParser(cypher)
    cp.next_character()
    r = cp.find_relation()

    assert r.left=="<-"
    assert r.right=="-"
    assert r.left_position1==0
    assert r.left_position2==1
    assert r.right_position1==2
    assert r.right_position2==-1
    assert len(r.types)==0
    assert len(r.negative_types)==0
    assert r.variable_length is False
    assert r.status&RelationFlag.RELATION_FOUND


# Simple Cypher relation with left arrow
def test_OnlyRelationWithRightDirection_ShouldReturnValidRelation():
    cypher = "-->"
    type = ""

    cp = CypherParser(cypher)
    cp.next_character()
    r = cp.find_relation()

    assert r.left=="-"
    assert r.right=="->"
    assert r.left_position1==-1
    assert r.left_position2==0
    assert r.right_position1==1
    assert r.right_position2==2
    assert len(r.types)==0
    assert len(r.negative_types)==0
    assert r.variable_length is False
    assert r.status&RelationFlag.RELATION_FOUND

# Cypher relation with arrow and relation body
def test_RelationWithDirectionAndRelationVariable_ShouldReturnValidRelation():
    cypher = "-[r]->"
    type = ""

    cp = CypherParser(cypher)
    cp.next_character()
    r = cp.find_relation()

    assert r.left=="-"
    assert r.right=="->"
    assert r.left_position1==-1
    assert r.left_position2==0
    assert r.right_position1==4
    assert r.right_position2==5
    assert len(r.types)==0
    assert len(r.negative_types)==0
    assert r.variable_length is False
    assert r.variable == 'r'
    assert r.status&RelationFlag.RELATION_FOUND

# Cypher relation with arrow and full relation body
def test_FullRelationWithBody_ShouldReturnValidRelation():
    cypher = "<-[r:`MyRel Type`|!Relation|!Rel*1..2 {Name: \"Andy\" , `Other()))Name` : 'Malle'} ]-"
    type = ""

    cp = CypherParser(cypher)
    cp.next_character()
    r = cp.find_relation()

    assert r.left=="<-"
    assert r.right=="-"
    assert r.left_position1==0
    assert r.left_position2==1
    assert r.right_position1==82
    assert r.right_position2==-1
    assert r.types[0]=='MyRel Type'
    assert r.negative_types[0] == 'Relation'
    assert r.negative_types[1] == 'Rel'
    assert r.variable_length is True
    assert r.variable == 'r'
    assert r.status&RelationFlag.RELATION_FOUND

# Cypher relation with arrow and full relation body and more escape signs
def test_FullRelationWithBodyWithMultipleRows_ShouldReturnValidRelation():
    cypher = """<   -   [r:`MyRel Type`

    |!Relation|!Rel

    *

    1 ..
    2

    {Name: \"Andy\" ,

    `Other()))Name` : 'Malle'} ]-"""

    cyp = CypherParser(cypher)
    cyp.next_character()
    rel = cyp.find_relation()

    assert rel.left=="<-"
    assert rel.right=="-"
    assert rel.left_position1==0
    assert rel.left_position2==4
    assert rel.right_position1==122
    assert rel.right_position2==-1
    assert rel.types[0]=='MyRel Type'
    assert rel.negative_types[0] == 'Relation'
    assert rel.negative_types[1] == 'Rel'
    assert rel.variable_length is True
    assert rel.variable == 'r'
    assert rel.status&RelationFlag.RELATION_FOUND

# Simple Cypher relation body
def test_RelationBodyWithOnlyVariable_ShouldReturnValidVariable():
    cypher = "[r]*"

    cp = CypherParser(cypher)
    cp.next_character()

    types, negative_types,variable_length,variable = cp.get_relation_body_inside_bracket()

    assert len(types)==0
    assert len(negative_types)==0
    assert variable_length is False
    assert variable == 'r'

# Simple Cypher relation body with variable and labels
def test_RelationBodyWithVariableAndLabel_ShouldReturnValidVariable():
    cypher = "[r:Relation]*"

    cp = CypherParser(cypher)
    cp.next_character()

    types, negative_types,variable_length,variable = cp.get_relation_body_inside_bracket()

    assert types[0]=='Relation'
    assert len(negative_types)==0
    assert variable_length is False
    assert variable == 'r'

# Cypher relation with full body
def test_RelationWithFullBody_ShouldReturnValidVariable():
    cypher = "[r:`MyRel Type`|!Relation|!Rel *1..2 {Name: \"Andy\" , `Other()))Name` : 'Malle'} ]*"

    cp = CypherParser(cypher)
    cp.next_character()

    types, negative_types,variable_length,variable = cp.get_relation_body_inside_bracket()

    assert types[0]=='MyRel Type'
    assert negative_types[0] == 'Relation'
    assert negative_types[1] == 'Rel'
    assert variable_length is True
    assert variable == 'r'


# Find cypher relation types
def test_RelationTypes_FindOneType():
    cypher = ":Relation"

    cp = CypherParser(cypher)
    cp.next_character()
    types, negative_types = cp.find_types()

    assert types[0] == 'Relation'

# Find multiple cypher relation types in back tick
def test_MultipleRelationTypesWithBackTicket_FindOneType():
    cypher = ":   `Relation\r\()}}-` | Name "

    cp = CypherParser(cypher)
    cp.next_character()
    types, negative_types = cp.find_types()

    assert types[0] == "Relation\r\()}}-"
    assert types[1] == "Name"

# Find multiple cypher with negative relation types in back tick
def test_MultipleRelationTypesWithBackTicketAndNegative_FindOneType():
    cypher = ":!`Relation\r\()}}-` | Name "

    cp = CypherParser(cypher)
    cp.next_character()
    types, negative_types = cp.find_types()

    assert negative_types[0] == "Relation\r\()}}-"
    assert types[0] == "Name"

# Find cypher relation types in back tick
def test_RelationTypesWithBackTicket_FindOneType():
    cypher = """:

    `Relation\r\()}}-`"""

    cp = CypherParser(cypher)
    cp.next_character()
    types, negative_types = cp.find_types()

    assert types[0] == "Relation\r\()}}-"

# Skip variable length and check position
def test_SkipVariableLength_ShouldReturnRightPosition():
    cypher = '* ..'
    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_variable_length()

    assert cp.position == 4

# Skip variable length and check position
def test_SkipVariableLengthWithNumbers_ShouldReturnRightPosition():
    cypher = '* 1 ..    2'
    cp = CypherParser(cypher)
    cp.next_character()
    cp.skip_variable_length()

    assert cp.position == 11





#----------------------------------------------------------------
# Adding node variable and labels for checing existance
def test_SaveNodeLabelAndVariabelToDictionary():

    cp = CypherParser("")
    n1 = Node("d",["Person", "Aktör"],NodeFlag.NODE_FOUND|NodeFlag.HAS_LABELS|NodeFlag.HAS_VARIABLE)
    n1.position = 10
    cp.triples_repository.save_node_variable_and_label(n1)
    n2 = Node("d",[ "Aktör"],NodeFlag.NODE_FOUND|NodeFlag.HAS_LABELS|NodeFlag.HAS_VARIABLE)
    n2.position = 15
    cp.triples_repository.save_node_variable_and_label(n2)
    node_variables = cp.triples_repository.node_variables
    assert node_variables["d"][0]["Person"] == 10
    assert node_variables["d"][0]["Aktör"] == 10
    assert node_variables["d"][1]["Aktör"] == 15
    assert node_variables["d"][-1]["Aktör"] == 15
    assert node_variables["d"][-1].get("Person") is None

    #assert cp.NodeVariabels["d"]["Kalle"]


# Pattern of two triples
def test_GetSecondNodeLabelFromFirstNodeByVariable_ShouldReturnTriples():
    cypher = """
    match (d:Person)-[:Has]->(:Car) match (d)-[`h`:!Owns|Has]->(s:`Person`)
    return d
    """
    cp = CypherParser()
    cp.find_and_prepare_all_triples(cypher)

    triple1 = cp.triples_repository.triples[0]
    triple2 = cp.triples_repository.triples[1]

    assert triple2.first_node.variable == 'd'
    assert triple1.first_node.labels[0] in triple2.first_node.labels
    assert triple2.first_node.label_is_looked_up is True

# Pattern of node, relation, node
def test_FullPatternOfNodeRelationNode_ShouldReturnTriple():
    cypher = '(d)--() '
    cp = CypherParser()

    cp.find_and_prepare_all_triples(cypher)

    triple = cp.triples_repository.triples[0]

    assert cp.current_character == ''
    assert triple.first_node.variable == 'd'

# Pattern of node, relation, node with labels and types
def test_FullPatternOfNodeRelationNodeWithLabelsAndTypes_ShouldReturnTriple():
    cypher = '(d:Person)-[:Has]->(:Car) '
    cp = CypherParser()

    cp.find_and_prepare_all_triples(cypher)

    triple = cp.triples_repository.triples[0]

    assert cp.current_character == ''
    assert triple.first_node.variable == 'd'
    assert triple.first_node.labels[0] == 'Person'
    assert triple.relation.variable == ''
    assert triple.relation.types[0] == 'Has'
    assert triple.second_node.variable == ''
    assert triple.second_node.labels[0] == 'Car'

# Pattern of two triples
def test_TwoTripples_ShouldReturnTriples():
    cypher = '(d:Person)-[:Has]->(:Car)<-[`h`:!Owns|Has]-(s:`Person`) '
    cp = CypherParser()
    cp.find_and_prepare_all_triples(cypher)

    triple1 = cp.triples_repository.triples[0]
    triple2 = cp.triples_repository.triples[1]

    assert cp.current_character == ''
    assert triple1.first_node.variable == 'd'
    assert triple1.first_node.labels[0] == 'Person'
    assert triple1.relation.variable == ''
    assert triple1.relation.types[0] == 'Has'
    assert triple1.second_node.variable == ''
    assert triple1.second_node.labels[0] == 'Car'
    assert triple2.first_node.variable == ''
    assert triple2.first_node.labels[0] == 'Car'
    assert triple2.relation.variable == 'h'
    assert triple2.relation.types[0] == 'Has'
    assert triple2.relation.negative_types[0] == 'Owns'
    assert triple2.second_node.variable == 's'
    assert triple2.second_node.labels[0] == 'Person'


# Pattern of two triples
def test_TwoTripplesWithMatchAndReturn_ShouldReturnTriples():
    cypher = """
    match (d:Person)-[:Has]->(:Car)<-[`h`:!Owns|Has]-(s:`Person`)
    return d
    """
    cp = CypherParser()
    cp.find_and_prepare_all_triples(cypher)

    triple1 = cp.triples_repository.triples[0]
    triple2 = cp.triples_repository.triples[1]

    assert cp.current_character == ''
    assert triple1.first_node.variable == 'd'
    assert triple1.first_node.labels[0] == 'Person'
    assert triple1.relation.variable == ''
    assert triple1.relation.types[0] == 'Has'
    assert triple1.second_node.variable == ''
    assert triple1.second_node.labels[0] == 'Car'
    assert triple2.first_node.variable == ''
    assert triple2.first_node.labels[0] == 'Car'
    assert triple2.relation.variable == 'h'
    assert triple2.relation.types[0] == 'Has'
    assert triple2.relation.negative_types[0] == 'Owns'
    assert triple2.second_node.variable == 's'
    assert triple2.second_node.labels[0] == 'Person'


# Validate right direction
def test_validate_direction_of_triple_should_return_right_flag():

    cp = CypherParser("")
    first_node = Node("",["Person"],NodeFlag.HAS_LABELS)
    rel = Relation()
    rel.left = '-'
    rel.right = '->'
    second_node = Node("",["Person"],NodeFlag.HAS_LABELS)
    triple = Triple(first_node,rel,second_node)

    cp.triples_repository.validate_direction_of_triple(triple)

    assert triple.direction & DirectionFlag.SOURCE_TO_DESTINATION

# Validate right direction
def test_validate_direction_of_triple_should_return_left_flag():

    cp = CypherParser("")
    first_node = Node("",["Person"],NodeFlag.HAS_LABELS)
    rel = Relation()
    rel.left = '<-'
    rel.right = '-'
    second_node = Node("",["Person"],NodeFlag.HAS_LABELS)
    triple = Triple(first_node,rel,second_node)

    cp.triples_repository.validate_direction_of_triple(triple)

    assert triple.direction & DirectionFlag.DESTINATION_TO_SOURCE

# Validate no direction
def test_validate_direction_of_triple_should_return_no_direction_flag():

    cp = CypherParser("")
    first_node = Node("",["Person"],NodeFlag.HAS_LABELS)
    rel = Relation()
    rel.left = '-'
    rel.right = '-'
    second_node = Node("",["Person"],NodeFlag.HAS_LABELS)
    triple = Triple(first_node,rel,second_node)

    cp.triples_repository.validate_direction_of_triple(triple)

    assert triple.direction & DirectionFlag.UNDIRECTED

# Validate  both directions
def test_validate_direction_of_triple_should_return_both_direction_flag():

    cp = CypherParser("")
    first_node = Node("",["Person"],NodeFlag.HAS_LABELS)
    rel = Relation()
    rel.left = '-'
    rel.right = '-'
    second_node = Node("",["Person"],NodeFlag.HAS_LABELS)
    triple = Triple(first_node,rel,second_node)

    cp.triples_repository.validate_direction_of_triple(triple)

    assert triple.direction & DirectionFlag.UNDIRECTED


# Add left direction
def test_add_left_direction_should_match_result_cypher():

    cp = CypherParser("")
    cypher = "(:Person)-[:WORKS_AT]->(:Organization)"
    fixed_cypher_test ="(:Person)<-[:WORKS_AT]-(:Organization)"
    left1 = 9
    right1 = 21
    right2 = 22

    fixed_cypher = SchemaRules.add_left_arrow(cypher,left1,right2)

    assert fixed_cypher == fixed_cypher_test

# Add left direction to triple
def test_add_left_direction_to_triple_should_match_result_cypher():

    cp = CypherParser("")
    cypher = "(:Person)-[:WORKS_AT]->(:Organization)"
    fixed_cypher_test ="(:Person)<-[:WORKS_AT]-(:Organization)"
    triple = Triple(Node('',[],NodeFlag.NONE),Relation(),Node('',[],NodeFlag.NONE))
    triple.direction = DirectionFlag.SOURCE_TO_DESTINATION
    triple.relation.left_position1 = -1
    triple.relation.left_position2 = 9
    triple.relation.right_position2 = 22
    triple.schema_validated_direction = DirectionFlag.DESTINATION_TO_SOURCE

    fixed_cypher = SchemaRules.fix_arrow_direction_if_needed(triple,cypher)

    assert fixed_cypher == fixed_cypher_test


# Add right direction
def test_add_right_direction_should_match_result_cypher():

    cp = CypherParser("")
    cypher = "(:Person)<-[:WORKS_AT]-(:Organization)"
    fixed_cypher_test ="(:Person)-[:WORKS_AT]->(:Organization)"
    left1 = 9
    left2 = 10
    right1 = 22


    fixed_cypher = SchemaRules.add_right_arrow(cypher,left1,right1)

    assert fixed_cypher == fixed_cypher_test

# Add right direction to triple
def test_add_right_direction_to_triple_should_match_result_cypher():

    cp = CypherParser("")
    cypher = "(:Person)<-[:WORKS_AT]-(:Organization)"
    fixed_cypher_test ="(:Person)-[:WORKS_AT]->(:Organization)"
    triple = Triple(Node('',[],NodeFlag.NONE),Relation(),Node('',[],NodeFlag.NONE))
    triple.direction = DirectionFlag.DESTINATION_TO_SOURCE
    triple.relation.left_position1 = 9
    triple.relation.right_position1 = 22
    triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION

    fixed_cypher = SchemaRules.fix_arrow_direction_if_needed(triple,cypher)

    assert fixed_cypher == fixed_cypher_test


def test_1_cypher_should_change_direction():
    orginal_query = """
    MATCH (o:`Organization` {name:"Foo"})-[:WORKS_AT]->(p:Person {id:"Foo"})-[:WORKS_AT]-(o1:Organization {name:"b"})
    WHERE id(o) > id(o1)
    RETURN o.name AS name
    """

    fixed_query="""
    MATCH (o:`Organization` {name:"Foo"})-<[:WORKS_AT]->p:Person {id:"Foo"})-[:WORKS_AT]-(o1:Organization {name:"b"})
    WHERE id(o) > id(o1)
    RETURN o.name AS name
    """

    correct_query = """
    MATCH (o:`Organization` {name:"Foo"})<-[:WORKS_AT]-(p:Person {id:"Foo"})-[:WORKS_AT]-(o1:Organization {name:"b"})
    WHERE id(o) > id(o1)
    RETURN o.name AS name
    """

    schema = "(Person,KNOWS,Person),(Person,WORKS_AT,Organization)"

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

def test_2_cypher_should_change_direction():
    #schema = '(Person,KNOWS,Person),(Person,WORKS_AT,Organization)'
    schema = '(Person,WORKS_AT,Organization)'

    orginal_query = """
    MATCH (p:Person)<--(:Organization)--(p1:Person)
    RETURN p1
    """
    fixed_query = """
    MATCH (p:Person)<--(:Organization)--(p1:Person)
    RETURN p1
    """
    correct_query = """
    MATCH (p:Person)-->(:Organization)--(p1:Person)
    RETURN p1
    """
    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query


def test_3_cypher_should_change_directions():

    #schema = '(Person,FOLLOWS,Person),(Person,ACTED_IN,Movie),(Person,REVIEWED,Movie),(Person,WROTE,Movie),(Person,DIRECTED,Movie),(Movie,IN_GENRE,Genre),(Person,RATED,Movie)'
    schema = '(Person,ACTED_IN,Movie)'

    orginal_query = """
MATCH (p:Person)<-[:ACTED_IN]-(m:Movie),
(coActors:Person)-[:ACTED_IN]->(m)
WHERE p.name = 'Eminem'
RETURN m.title AS movie ,collect(coActors.name) AS coActors
"""
    fixed_query = """
MATCH (p:Person)<-[:ACTED_IN]-(m:Movie),
(coActors:Person)-[:ACTED_IN]->(m)
WHERE p.name = 'Eminem'
RETURN m.title AS movie ,collect(coActors.name) AS coActors
"""
    correct_query = """
MATCH (p:Person)-[:ACTED_IN]->(m:Movie),
(coActors:Person)-[:ACTED_IN]->(m)
WHERE p.name = 'Eminem'
RETURN m.title AS movie ,collect(coActors.name) AS coActors
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

def test_4_cypher_should_change_direction():
    schema = '(Person,KNOWS,Person),(Person,WORKS_AT,Organization)'

    orginal_query = """
MATCH (person:Person)
CALL {
   WITH person
   MATCH (person)-[:KNOWS]->(o:Organization)
   RETURN o LIMIT 3
}
RETURN person, o
"""
    fixed_query = """
MATCH (person:Person)
CALL {
   WITH person
   MATCH (person)-[:KNOWS]->(o:Organization)
   RETURN o LIMIT 3
}
RETURN person, o
"""
    correct_query = """"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query


def test_5_cypher_should_change_direction():
    schema = '(Person,FOLLOWS,Person),(Person,ACTED_IN,Movie),(Person,REVIEWED,Movie),(Person,WROTE,Movie),(Person,DIRECTED,Movie),(Movie,IN_GENRE,Genre),(Person,RATED,Movie)'

    orginal_query = """
MATCH (p:Person)
WITH p LIMIT 100
CALL {
  WITH p
  OPTIONAL MATCH (p)<-[:ACTED_IN]-(m)
  RETURN m.title + ": " + "Actor" AS work
UNION
  WITH p
  OPTIONAL MATCH (p)-[:DIRECTED]->(m:Movie)
  RETURN m.title+ ": " +  "Director" AS work
}
RETURN p.name, collect(work)
"""
    fixed_query = """

"""
    correct_query = """
MATCH (p:Person)
WITH p LIMIT 100
CALL {
  WITH p
  OPTIONAL MATCH (p)-[:ACTED_IN]->(m)
  RETURN m.title + ": " + "Actor" AS work
UNION
  WITH p
  OPTIONAL MATCH (p)-[:DIRECTED]->(m:Movie)
  RETURN m.title+ ": " +  "Director" AS work
}
RETURN p.name, collect(work)
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

def test_6_cypher_should_change_direction():
    schema = '(Person,KNOWS,Person),(Person,WORKS_AT,Organization)'

    orginal_query = """
MATCH (o:Organization)-[:WORKS_AT]-(p:Person {id:"Foo"})-[:WORKS_AT]-(o1:Organization)
WHERE id(o) < id(o1) RETURN o.name AS name
"""
    fixed_query = """

"""
    correct_query = """
MATCH (o:Organization)-[:WORKS_AT]-(p:Person {id:"Foo"})-[:WORKS_AT]-(o1:Organization)
WHERE id(o) < id(o1) RETURN o.name AS name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

def test_7_cypher_should_change_direction():
    schema = '(Person,KNOWS,Person),(Person,WORKS_AT,Organization)'

    orginal_query = """
MATCH (p:Person)
WHERE EXISTS { (p)<-[:KNOWS]-()}
RETURN p
"""
    fixed_query = """
MATCH (p:Person)
WHERE EXISTS { (p)-[:KNOWS]->()}
RETURN p
"""
    correct_query = """
MATCH (p:Person)
WHERE EXISTS { (p)<-[:KNOWS]-()}
RETURN p
"""
    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

def test_8_validate_test_cypher():
    schema = '(Person,FOLLOWS,Person),(Person,ACTED_IN,Movie),(Person,REVIEWED,Movie),(Person,WROTE,Movie),(Person,DIRECTED,Movie),(Movie,IN_GENRE,Genre),(Person,RATED,Movie)'

    orginal_query = """
MATCH (p:Person)-[:ACTED_IN]-(m:Movie)-[:DIRECTED]->(p)
WHERE  p.born.year > 1960
RETURN p.name, p.born, labels(p), m.title
"""
    fixed_query = """
MATCH (p:Person)-[:ACTED_IN]-(m:Movie)-[:DIRECTED]->(p)
WHERE  p.born.year > 1960
RETURN p.name, p.born, labels(p), m.title
"""
    correct_query = """
MATCH (p:Person)-[:ACTED_IN]-(m:Movie)<-[:DIRECTED]-(p)
WHERE  p.born.year > 1960
RETURN p.name, p.born, labels(p), m.title
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

def test_9_validate_test_cypher():
    schema = '(Person,FOLLOWS,Person),(Person,ACTED_IN,Movie),(Person,REVIEWED,Movie),(Person,WROTE,Movie),(Person,DIRECTED,Movie),(Movie,IN_GENRE,Genre),(Person,RATED,Movie)'

    orginal_query = """
MATCH (d:Person)-[:DIRECTED]->(m:Movie)<--(g:Genre)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""
    fixed_query = """
MATCH (d:Person)-[:DIRECTED]->(m:Movie)<--(g:Genre)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""
    correct_query = """
MATCH (d:Person)-[:DIRECTED]->(m:Movie)-->(g:Genre)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query



    #(:Person)-[:WORKS_AT*]->(:Person), (:Person)-[:WORKS_AT*1..4]->(:Person)

# Check variable length
def test_10_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)<-[:DIRECTED*]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)<-[:DIRECTED*]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query


# Check variable length
def test_11_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)<-[:DIRECTED *1 ..]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)<-[:DIRECTED *1 ..]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

# Check variable length
def test_13_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)<-[:DIRECTED *1 .. 4]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)<-[:DIRECTED *1 .. 4]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

# Check variable length
def test_13B_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)<-[:DIRECTED*2]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)<-[:DIRECTED*2]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query


# Check variable length
def test_13C_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)<-[:DIRECTED*2..]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)<-[:DIRECTED*2..]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

# Check variable length
def test_13D_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)<-[:DIRECTED*2..4]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)<-[:DIRECTED*2..4]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

# Check undirected relation
def test_14_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)-[:DIRECTED]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)-[:DIRECTED]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query














