""" Test example showing how to use the fix_cypher_relations_directions"""

cypher = """
MATCH (p:Person)<-[:ACTED_IN]-(m:Movie)
WHERE p.name <> 'Tom Hanks'
AND m.title = 'Captain Phillips'
AND m.year > 2019
AND m.year < 2030
RETURN p.name
"""
true_cypher ="""
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE p.name <> 'Tom Hanks'
AND m.title = 'Captain Phillips'
AND m.year > 2019
AND m.year < 2030
RETURN p.name
"""

schema = "(Person, FOLLOWS, Person), (Person, ACTED_IN, Movie), (Person, REVIEWED, Movie), (Person, WROTE, Movie), (Person, DIRECTED, Movie), (Movie, IN_GENRE, Genre), (Person, RATED, Movie)"

from fixcypher_ast_method.fixdirections_astmethod import FixDirections as fix_ast
from fixcypher_stream_method.fixdirections_streammethod import FixDirections as fix_stream


fixed_with_ast =fix_ast.fix_cypher_relations_directions(cypher,schema)
assert fixed_with_ast==true_cypher
fixed_with_stream = fix_stream.fix_cypher_relations_directions(cypher,schema)
assert fixed_with_stream==true_cypher

print("Origanal cypher:")
print(cypher)
print()

print("Fixed directions with Antlr:")
print(fixed_with_ast)

print()

print("Fixed relations directions with Native parser:")
print(fixed_with_stream)

