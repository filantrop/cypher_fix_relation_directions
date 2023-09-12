# cypher_fix_relation_directions
Fixes relations directions for cypher queries

# Start by installing
Install as package in root with:
pip install .

# If windows environment
Run aliassetup.bat to set aliases in windows cmd or powershell



# #################################
# There is two solutions
# ################################
# Native solution
fixcypher_stream_method
This method is about ten times faster than Antlr AST, but not as flexible as the AST
The main class is in the file: fixdirections_astmethod.py
And function fix_cypher_relations_directions should be used

# AST with antlr
fixcypher_ast_method
Easier to change, if you know how antlr works
The main class is in the file: fixdirections_streammethod.py
And function fix_cypher_relations_directions should be used

# To test both methods, examine and try the following file:
test_fix_relations_directions_example.py

# To change antlr ast file:
1. Go into the directory with dir or ls: parse_antlr_to_cypher
2. Change the file: FixRelationsDirections.g4
3. Run this command to rebuild the python files: java -Xmx500M org.antlr.v4.Tool -Dlanguage=Python3 FixRelationsDirections.g4
4. The files in parse_antlr_to_cypher is regenerated


# Tests
The directory Tests contains pytest unit tests and also 2 files to test each method against the testcases
both tests use the following input file that is all tests provided for the task:
datasets/examples_2023-09-11.csv as input file

# Antlr4, AST method:
tests/validate_csv_testfile_with_antrl_ast_method.py

# Native streaming method
tests/validate_csv_testfile_with_streammethod.py




