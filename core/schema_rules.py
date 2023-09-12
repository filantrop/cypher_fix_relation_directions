"""
schema rules used to test if triples against schemas
"""
from typing import List
from core.core_classes import Node, Relation, Triple, DirectionFlag,Schema,RelationTypeEnum


class SchemaRules:
    """
    Rules to check if triples should change direction

    """
    @staticmethod
    def validate_direction_change(triple:Triple, schemas: List[Schema]):
        """Checks against rules to see that the triple direction is valid

        Args:
            triple (Triple): the triple a it was parsed from the cypher (node,relation,node)
            schemas (List[Schema]): the schemas to use when validating the triple
        """
        first_node = triple.first_node
        second_node = triple.second_node

        has_match = False
        triple.has_schema_match = True
        if  SchemaRules.has_same_labels(triple,schemas):
            has_match = True

        elif  SchemaRules.schema_match_with_both_node_labels(first_node, second_node,triple, schemas):
            has_match = True

        elif  SchemaRules.check_schema_when_one_node_has_missing_labels(first_node, second_node,triple, schemas):
            has_match = True

        elif  SchemaRules.check_schema_when_no_relationship_type_and_at_least_one_label(first_node, second_node,triple,schemas):
            has_match = True

        # If nothing matches above, then the schema does not match the triple
        if not has_match:
            triple.has_schema_match = False
            return

        # Test if undirected or has variable length
        elif has_match and (SchemaRules.has_undirected_relationships(triple,schemas) or SchemaRules.relation_has_variable_length(triple)):
            # Set that the schema validated direction is the same as triple direction
            triple.schema_validated_direction = triple.direction



    # Rule 2
    @staticmethod
    def has_same_labels(triple:Triple,schemas: List[Schema]):

        """ If the relationship is between two nodes of the same labels,
            there is nothing to validate or correct
            (:Person)-->(:Person), (:Person)-[:KNOWS]->(:Person)

        Args:
            triple (Triple): the triple a it was parsed from the cypher (node,relation,node)
        Returns:
            bool: return True if match, else false
        """
        for schema in schemas:
            relation_type = SchemaRules.validate_relation_type(triple.relation,schema)

            if SchemaRules.has_at_least_one_intersection(triple.first_node.labels, triple.second_node.labels):
                if RelationTypeEnum.NOT_VALID != relation_type:
                    return True
        return False

    # Rule 3
    @staticmethod
    def has_undirected_relationships(triple:Triple,schemas: List[Schema]):
        """ If the input query has an undirected relationship in the pattern,
            we do not correct it.
            (:Person)--(:Organization), (:Person)-[:WORKS_AT]-(:Organization)

        Args:
            triple (Triple): the triple a it was parsed from the cypher (node,relation,node)
        Returns:
            bool: return True if match, else false
        """
        for schema in schemas:
            relation_type = SchemaRules.validate_relation_type(triple.relation,schema)
            if triple.direction & DirectionFlag.UNDIRECTED:

                if RelationTypeEnum.NOT_VALID != relation_type:
                    return True
                else:
                    return False
        return False

    # Rule 4
    @staticmethod
    def check_schema_when_one_node_has_missing_labels(source_node: Node, destination_node: Node, triple:Triple, schemas: List[Schema]):
        """ If a node label is missing in the defined pattern,
            we can still validate if it fits the graph schema

            Don't change direction
            (:Person)-[:WORKS_AT]->()
            ()-[:WORKS_AT]->(:Person)

            Change direction
            (:Person)<-[:WORKS_AT]-()
            ()<-[:WORKS_AT]-(:Person)


        Args:
            triple (Triple): the triple a it was parsed from the cypher (node,relation,node)
            schemas (List[Schema]): the schemas to use when validating the triple
        Returns:
            bool: return True if match, else false
        """

        for schema in schemas:
            relation_type = SchemaRules.validate_relation_type(triple.relation,schema)

            change_direction = (schema.source!=schema.destination)
            triple.schema_validated_direction = triple.direction

            if schema.relation in triple.relation.types:
                if schema.source in source_node.labels and \
                    len(destination_node.labels)==0:

                    if change_direction:
                        triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION

                    if RelationTypeEnum.TYPE_IS_VALID == relation_type:
                        return True
                elif schema.source in destination_node.labels and \
                    len(source_node.labels)==0:

                    if change_direction:
                        triple.schema_validated_direction = DirectionFlag.DESTINATION_TO_SOURCE
                    if RelationTypeEnum.TYPE_IS_VALID == relation_type:
                        return True

                elif schema.destination in source_node.labels and \
                    len(destination_node.labels)==0:

                    if change_direction:
                        triple.schema_validated_direction = DirectionFlag.DESTINATION_TO_SOURCE
                    if RelationTypeEnum.TYPE_IS_VALID == relation_type:
                        return True
                elif schema.destination in destination_node.labels and \
                    len(source_node.labels)==0:

                    if change_direction:
                        triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION
                    if RelationTypeEnum.TYPE_IS_VALID == relation_type:
                        return True

        return False

    # Rule 5
    @staticmethod
    def check_schema_when_no_relationship_type_and_at_least_one_label(source_node: Node, destination_node: Node, triple:Triple, schemas: List[Schema])->bool:
        """ If the input query doesn't define the relationship type,
            but at least one node label is given of a pattern,
            we check if any relationship exists that matches the pattern and correct it if needed
            (:Person)-->(), (:Organization)<-[r]-()
        Args:
            triple (Triple): the triple a it was parsed from the cypher (node,relation,node)
            schemas (List[Schema]): the schemas to use when validating the triple
        Returns:
            bool: return True if match, else false
        """

        for schema in schemas:
            relation_type = SchemaRules.validate_relation_type(triple.relation,schema)
            if  RelationTypeEnum.TYPE_IS_EMPTY == relation_type:
                if schema.source in source_node.labels and schema.destination in destination_node.labels:
                    triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION
                    return True
                elif (schema.source in source_node.labels and len(destination_node.labels)==0) or\
                     (len(source_node.labels)==0 and schema.destination in destination_node.labels):
                    triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION
                    return True

                if schema.source in destination_node.labels and schema.destination in source_node.labels:
                    triple.schema_validated_direction = DirectionFlag.DESTINATION_TO_SOURCE
                    return True
                elif (schema.source in destination_node.labels and len(source_node.labels)==0) or\
                     (len(destination_node.labels)==0 and schema.destination in source_node.labels):
                    triple.schema_validated_direction = DirectionFlag.DESTINATION_TO_SOURCE
                    return True


            #return False
        return False

    # Rule 6
    @staticmethod
    def schema_match_with_both_node_labels(source_node: Node, destination_node: Node, triple:Triple, schemas: List[Schema])->bool:
        """ When multiple relationships are given or a negation is used in a pattern,
            make sure that at least one of relationship types of the possible fits the given schema
            (:Person)-[:KNOWS|WORKS_AT]->(:Organization), (:Person)-[:!KNOWS]->(:Organization)
        Args:
            triple (Triple): the triple a it was parsed from the cypher (node,relation,node)
            schemas (List[Schema]): the schemas to use when validating the triple
        Returns:
            bool: return True if match, else false
        """

        # valid_type = SchemaRules.has_a_valid_type(triple.relation,schemas):
            # return False

        for schema in schemas:
            relation_type = SchemaRules.validate_relation_type(triple.relation,schema)
            # Cypher: (:Person) [X] (:Organization), Schema: (:Person)-[:WORKS_AT]->(:Organization)
            if  schema.source in source_node.labels and \
                schema.destination in destination_node.labels:
                triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION
                #(:Person)-[X]->(:Organization)
                if triple.direction & DirectionFlag.SOURCE_TO_DESTINATION:
                    # triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION
                    if  RelationTypeEnum.TYPE_IS_VALID == relation_type:
                        triple.has_schema_match = True
                        return True
                    else:
                        continue
                #(:Person)<-[X]-(:Organization)
                elif triple.direction & DirectionFlag.DESTINATION_TO_SOURCE:
                    #triple.schema_validated_direction = DirectionFlag.DESTINATION_TO_SOURCE
                    # triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION
                    if RelationTypeEnum.TYPE_IS_VALID == relation_type:
                        triple.has_schema_match = True
                        return True
                    else:
                        continue
                elif triple.direction & DirectionFlag.UNDIRECTED:
                    # triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION
                    if RelationTypeEnum.TYPE_IS_VALID == relation_type:
                        triple.has_schema_match = True
                        return True
                    else:
                        continue
                else:
                    return False
            # Cypher: (:Organization) [X] (:Person), Schema: (:Person)-[:WORKS_AT]->(:Organization)
            elif   schema.source in destination_node.labels and\
                   schema.destination in source_node.labels:
                triple.schema_validated_direction = DirectionFlag.DESTINATION_TO_SOURCE
                # (:Organization)-[X]->(:Person)
                if triple.direction & DirectionFlag.SOURCE_TO_DESTINATION:
                    # triple.schema_validated_direction = DirectionFlag.DESTINATION_TO_SOURCE
                    if RelationTypeEnum.TYPE_IS_VALID == relation_type:
                        triple.has_schema_match = True
                        return True
                    else:
                        continue

                # (:Organization)<-[X]-(:Person)
                elif triple.direction & DirectionFlag.DESTINATION_TO_SOURCE:
                    # triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION
                    if RelationTypeEnum.TYPE_IS_VALID == relation_type:
                        triple.has_schema_match = True
                        return True
                    else:
                        continue
                elif triple.direction & DirectionFlag.UNDIRECTED:
                    # triple.schema_validated_direction = DirectionFlag.SOURCE_TO_DESTINATION
                    if RelationTypeEnum.TYPE_IS_VALID == relation_type:
                        triple.has_schema_match = True
                        return True
                    else:
                        continue
                else:
                    return False
        return False

    # Rule 7
    @staticmethod
    def relation_has_variable_length(triple: Triple)->bool:
        """Return true if relation has variable length

        Args:
            triple (Triple): triple that contains relation

        Returns:
            bool: if relation has variable length or not
        """
        # When variable length patten is used, we do not correct the direction or validate the schema
        # (:Person)-[:WORKS_AT*]->(:Person), (:Person)-[:WORKS_AT*1..4]->(:Person)

        if triple.relation.variable_length:
            return True
        return False



    @staticmethod
    def validate_relation_type(relation: Relation, schema: Schema)->RelationTypeEnum:
        """Checks that negative types and types is valid, if any negative type then it is not valid

        Args:
            relation (Relation): relation of triple
            schemas (List[Schema]): valid schemas

        Returns:
            bool: if relation is valid according to schemas
        """
        types_count = len(relation.types)
        negative_types_count = len(relation.negative_types)
        relation.schema_validated_relation_type = RelationTypeEnum.NOT_VALID

        # If both is empty then it is a valid relation pattern
        if types_count==0 and negative_types_count==0:
            relation.valid_schema = schema
            relation.schema_validated_relation_type = RelationTypeEnum.TYPE_IS_EMPTY
            # return RelationTypeFlag.TYPE_IS_EMPTY

        # If any type in negative types, then it is not valid, else valid

        elif negative_types_count>0:
            if schema.relation in relation.negative_types:
                relation.schema_validated_relation_type =  RelationTypeEnum.NOT_VALID
            else:
                relation.valid_schema = schema
                relation.schema_validated_relation_type =  RelationTypeEnum.TYPE_IS_VALID

        # If any type in types, then it is valid
        elif types_count>0:
            if schema.relation in relation.types:
                relation.valid_schema = schema
                relation.schema_validated_relation_type =  RelationTypeEnum.TYPE_IS_VALID

        return relation.schema_validated_relation_type
        # return RelationTypeFlag.NOT_VALID

    @staticmethod
    def has_at_least_one_intersection(list1: List[str], list2: List[str])->bool:
        """Checks that at least one of the string in list1 matches in list2

        Args:
            list1 (List[str]): list of strings
            list2 (List[str]): list of strings

        Returns:
            bool: the list has at least one intersection
        """

        for item1 in list1:
            for item2 in list2:
                if item1 == item2:
                    return True
        return False

    @staticmethod
    def fix_all_arrow_directions_from_triples( cypher,triples: List[Triple]) -> str:
        """Fixes all triples arrow directions that needs to be changed

        Returns:
            str: returns the fixed cypher
        """
        fixed_cypher = cypher
        one_triple_has_schema_match = False

        # The direction is not important, but for future changes it is more lasting
        for triple in reversed(triples):
            fixed_cypher = SchemaRules.fix_arrow_direction_if_needed(triple, fixed_cypher)
            if triple.has_schema_match:
                one_triple_has_schema_match = True

        if one_triple_has_schema_match is False:
            return ""

        return fixed_cypher
    @staticmethod
    def fix_arrow_direction_if_needed( triple: Triple, fixed_cypher: str) -> str:
        """Validates and fixes the arrow directions if necessary

        Args:
            triple (Triple): triple of node, relation, node to fix direction on
            fixed_cypher (str): the input cypher to change direction on based on the position
            on the arrow

        Returns:
            str: returns the fixed cypher
        """
        if triple.change_direction():
            if triple.direction & DirectionFlag.SOURCE_TO_DESTINATION:
                fixed_cypher = SchemaRules.add_left_arrow(
                    fixed_cypher,
                    triple.relation.left_position2,
                    triple.relation.right_position2,
                )
            elif triple.direction & DirectionFlag.DESTINATION_TO_SOURCE:
                fixed_cypher = SchemaRules.add_right_arrow(
                    fixed_cypher,
                    triple.relation.left_position1,
                    triple.relation.right_position1,
                )
        return fixed_cypher
    @staticmethod
    def add_left_arrow(
        cypher, new_left_arrow_position, existing_right_arrow_position
    ):
        """
        Adds an arrow to the left, this means removing the right arrow, then inserting the left

        Args:
            cypher: The original string.
            new_left_arrow_position: The left arrow position to be inserted.
            existing_right_arrow_position: The right arrow position to be removed

        Return:
            The modified string.
        """

        if new_left_arrow_position > 0:
            cypher = SchemaRules.remove_char(
                cypher,
                existing_right_arrow_position,
            )
            cypher = SchemaRules.insert_char(cypher, new_left_arrow_position, "<")

        return cypher
    @staticmethod
    def add_right_arrow(
        cypher, existing_left_arrow_position, new_right_arrow_position
    ):
        """
        Adds an arrow to the left, this means removing the right arrow, then inserting the left

        Args:
             cypher: The original string.
             existing_left_arrow_position: The left arrow position to be removed.
             new_right_arrow_position: The right arrow position to be inserted

        Return:
            The modified string.
        """

        if existing_left_arrow_position > 0:
            cypher = SchemaRules.remove_char(
                cypher,
                existing_left_arrow_position,
            )
            cypher = SchemaRules.insert_char(cypher, new_right_arrow_position, ">")

        return cypher
    @staticmethod
    def insert_char( cypher, index, char):
        """Inserts a character at a specific position in the string.

        :param s: The original string.
        :param index: The position to insert the character.
        :param char: The character to insert.

        :return: The modified string.
        """

        return cypher[:index] + char + cypher[index:]
    @staticmethod
    def remove_char( cypher, index):
        """Removes a character at a specific position in the string.

        :param s: The original string.
        :param index: The position of the character to remove.

        :return: The modified string.
        """

        return cypher[:index] + cypher[index + 1 :]