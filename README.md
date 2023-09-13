# cypher_fix_relation_directions Repository
Fixes relations directions for cypher queries

### Start by installing
Install as package in root with:</br>
<code> pip install . </code>

### If windows environment
Run <code>aliassetup.bat</code> to set aliases in windows cmd or powershell


## There is two solutions, Native and AST

### Native solution
Directory <code>fixcypher_stream_method</code>
this method is about ten times faster than Antlr AST, but not as flexible as the AST.
The main class is in the file: <code>fixdirections_astmethod.py</code>
And function <code>fix_cypher_relations_directions</code> should be used.

### AST with antlr
Directory <code>fixcypher_ast_method</code> is
easier to change. If you know how antlr works.
The main class is in the file: <code>fixdirections_streammethod.py</code>
And function <code>fix_cypher_relations_directions</code> should be used.



### To change antlr ast file:
1. Go into the directory with dir or ls: <code>parse_antlr_to_cypher</code>
2. Change the file: <code>FixRelationsDirections.g4</code>
3. Run this command to rebuild the python files: <code>java -Xmx500M org.antlr.v4.Tool -Dlanguage=Python3 FixRelationsDirections.g4</code>
4. The files in <code>parse_antlr_to_cypher</code> is regenerated


## Tests
The directory Tests contains pytest unit tests and also 2 files to test each method against the testcases
both tests use the following input file that is all tests provided for the task:
<code>datasets/examples_2023-09-11.csv</code> as input file

### To test both Native and Antlr , examine and try the following file:
<code>test_fix_relations_directions_example.py</code>

### Antlr4, AST method:
<code>tests/validate_csv_testfile_with_antrl_ast_method.py</code>

### Native streaming method
<code>tests/validate_csv_testfile_with_streammethod.py</code>




