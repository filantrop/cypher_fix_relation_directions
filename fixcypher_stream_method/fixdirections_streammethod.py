
from core.core_classes import SchemaParser
from fixcypher_stream_method.cypher_parser_streammethod import CypherParser
from core.schema_rules import SchemaRules

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

        # Extract schema and variables
        schema_parser = SchemaParser()
        schema_list =  schema_parser.extract_schemas(schema)
        cypher_parser = CypherParser()
        cypher_parser.find_and_prepare_all_triples(cypher)

        for triple in cypher_parser.triples_repository.triples:
            SchemaRules.validate_direction_change(triple, schema_list)

        query_fixed = SchemaRules.fix_all_arrow_directions_from_triples(cypher, cypher_parser.triples_repository.triples)

        return query_fixed

