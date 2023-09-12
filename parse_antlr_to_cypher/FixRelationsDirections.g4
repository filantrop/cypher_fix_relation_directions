/*

*/
grammar FixRelationsDirections;


options { caseInsensitive=true; }

WS: [ \t\r\n] -> skip; // skip spaces, tabs, newlines, \r (Windows)
//ID: [a-z]+ ; // match lower-case identifiers
COMMENT         : '/*' .*? '*/' -> skip;
LINE_COMMENT    : '//' ~[\r\n]* -> skip;
LPAREN          : '(';
RPAREN          : ')';
LBRACK          : '[';
RBRACK          : ']';
LBRACE          : '{';
RBRACE          : '}';
GT              : '>';
LT              : '<';
COLON           : ':';
SUB             : '-';
DOT             : '.';
COMMA           : ',';
PLUS            : '+';
DIV             : '/';
MULT            : '*';
NEGATION        : '!';
STICK           : '|';


NAME
    : BACKTICK_STRING
    | Letter LetterOrDigit*
    ;

STRING
    : '\'' ~('\'')* '\''
    | '"' ~('"')* '"'
    ;

// label
//     : BACKTICK_STRING   #labelValue
//     | Letter LetterOrDigit* #labelValue
//     ;

label_expression
    : (COLON NAME)*
    ;
type_expression
    : COLON  type_name (STICK type_name)*
    ;

type_name
    : NEGATION? NAME
    ;

BACKTICK_STRING
    : '`' ('``'|~'`')* '`' // quote-quote is an escaped quote
    ;

VARIABLE_LENGTH_DIGITS: Digits;

fragment LetterOrDigit  : Letter | [0-9];

fragment Digits: [1-9] ([0-9_]* [0-9])? ;


Letter :
	[a-z_]
	| ~[\u0000-\u007F\uD800-\uDBFF] // covers all characters above 0x7F which are not a surrogate
	| [\uD800-\uDBFF] [\uDC00-\uDFFF]; // covers UTF-16 surrogate pairs encodings for U+10000 to U+10FFFF


start: (cypher_body | .)*? EOF;

cypher_body
    : node (relation node)* #triple
    //| node #singleNode
    ;
relation
    : LT? SUB relation_body SUB GT?
    ;
relation_body
    : ('[' NAME? type_expression? variable_length? props? ']')?
    ;


variable_length
    : MULT //VARIABLE_LENGTH_DIGITS? (DOT DOT)? VARIABLE_LENGTH_DIGITS?
    | MULT VARIABLE_LENGTH_DIGITS
    | MULT VARIABLE_LENGTH_DIGITS DOT DOT
    | MULT VARIABLE_LENGTH_DIGITS DOT DOT VARIABLE_LENGTH_DIGITS
    ;

node
    : LPAREN NAME? label_expression props? RPAREN   #nodeWithVariableAndLabel // match keyword hello followed by an identifier
    | LPAREN NAME? props? RPAREN              #nodeWithVariable
    ;

props
    : LBRACE prop (',' prop)* RBRACE   #properties
    ;
prop
    : NAME COLON STRING
    ;
