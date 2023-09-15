"""
All parsing rules tests

"""
#from context import
from core.core_classes import NodeFlag, Node, Relation, Triple, DirectionFlag,RelationFlag
from core.schema_rules import SchemaRules
#from fixcypher_streammethod.cypher_parser_streammethod import CypherParser
# from fixcypher_streammethod.fixdirections_streammethod1 import FixDirections
from fixcypher_ast_method.cypher_parser_ast_method import CypherParser
from fixcypher_ast_method.fixdirections_astmethod import FixDirections



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
def test_13A_validate_test_cypher():

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


# Check not valid cypher
def test_15_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)-[:DIRECTED-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)-[:DIRECTED-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == ""


# Check schema does not match
def test_16_validate_test_cypher():

    schema = '(Person,DIRECTED,Director)'

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
    assert fixed_cypher == ""

# Check schema does not match
def test_17_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)-[:DIRECTED]-(m:Movie
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)-[:DIRECTED]-(m:Movie
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == ""

# Check schema does not match
def test_18_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH d:Person)-[:DIRECTED]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == ""

# Check schema does not match
def test_19_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)-[:DIRECTED](m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == ""

# Check schema does not match
def test_20_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)-[:DIRECTED](m:Movie) MATCH (d:Person)<-[:DIRECTED]-(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)-[:DIRECTED](m:Movie) MATCH (d:Person)-[:DIRECTED]->(m:Movie)
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

# Check schema does not match
def test_21_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)-[:DIRECTED](m:Movie) MATCH (d:Person)<-[:DIRECTED]-(m:Movie {Test: 'test'})
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)-[:DIRECTED](m:Movie) MATCH (d:Person)-[:DIRECTED]->(m:Movie {Test: 'test'})
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

# Check a property with not quotes work
def test_22_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)-[:DIRECTED]->(m:Movie) MATCH (d:Person)<-[:DIRECTED]-(m:Movie {Test:   'test'})
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)-[:DIRECTED]->(m:Movie) MATCH (d:Person)-[:DIRECTED]->(m:Movie {Test:   'test'})
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

# Check a property with not quotes work
def test_23_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)<-[:DIRECTED]-(m:Movie {Test: test})
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)-[:DIRECTED]->(m:Movie {Test: test})
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query


# Check a property with not quotes work
def test_24_validate_test_cypher():

    schema = '(Person,DIRECTED,Movie)'

    orginal_query = """
MATCH (d:Person)<-[:DIRECTED]-(m:Movie {Test: [test]})
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    correct_query = """
MATCH (d:Person)-[:DIRECTED]->(m:Movie {Test: [test]})
WHERE m.year = 2000 AND g.name = "Horror"
RETURN d.name
"""

    fixed_cypher = FixDirections.fix_cypher_relations_directions(orginal_query, schema)
    assert fixed_cypher == correct_query

