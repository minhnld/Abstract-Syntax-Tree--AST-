
grammar MC;
// 1712177
@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options {
	language = Python3;
}

program: manydecl EOF;

manydecl: decl manydecl | decl;

decl: varDecla | func_decl ;

varDecla: primitive_type varlist SEMI;
var: ID | arrayVar;
arrayVar: ID L_SQUARE NUM_INT R_SQUARE;
varlist: var (COMMA var)*;

/* var_decl: varlist;
varlist: var SEMI varlist | var SEMI;
var: primitive_type idenlist |  primitive_type ID array_type ;
idenlist: ID COMMA idenlist | ID ; */

var2: primitive_type ID | primitive_type array_pointer_type ;

primitive_type: BOOLEAN | INT | FLOAT | STRING;
array_type: L_SQUARE NUM_INT R_SQUARE;
array_pointer_type: ID L_SQUARE R_SQUARE;

type_plus: VOID | primitive_type | primitive_type L_SQUARE R_SQUARE;

func_decl:
	type_plus ID L_BRAC param_list? R_BRAC block_statement;

param_list:
	  var2 COMMA param_list
	| var2;

expression: expression_lv1 (ASSIGN) expression | expression_lv1;
expression_lv1:
	expression_lv1 (OR) expression_lv2
	| expression_lv2;

expression_lv2:
	expression_lv2 (AND) expression_lv3
	| expression_lv3;

expression_lv3:
	expression_lv4 (EQUAL | NOT_EQUAL) expression_lv4
	| expression_lv4;

expression_lv4:
	expression_lv5 (LESS | GREATER | LESS_EQUAL | GREATER_EQUAL) expression_lv5
	| expression_lv5;
expression_lv5:
	expression_lv5 (PLUS | MINUS) expression_lv6
	| expression_lv6;
expression_lv6:
	expression_lv6 (DIV | MUL | MODUL) expression_lv7
	| expression_lv7;
expression_lv7: (NOT | MINUS) expression_lv7 | expression_lv8;
expression_lv8:
	index_expression (L_SQUARE R_SQUARE)
	| index_expression;
index_expression:
	 L_BRAC expression R_BRAC
	| factor;

invocation_expression: L_BRAC call_param? R_BRAC;
array_index_express: (call_statement|ID) L_SQUARE expression R_SQUARE;

factor:
	L_BRAC expression R_BRAC
	| literal
	| ID
	| ID invocation_expression
	| array_index_express;

literal: number | bool_lit | STRING_LITERAL;
bool_lit: TRUE | FALSE;
number: NUM_INT | NUM_FLOAT;

statement:
	  normal_statement SEMI
	| structured_statement
	| varDecla;

structured_statement:
	if_statement
	| for_statement
	| block_statement
	| while_statement;

normal_statement:
	
 	  break_statement
	| continue_statement
	| return_statement
	| call_statement
	| expression;

/* assignment_statement: assignment_lhs_list expression;

assignment_lhs_list:
	lhs ASSIGN assignment_lhs_list
	| lhs ASSIGN; */
/* 
assignment_statement: expression assignment_lhs_list;
assignment_lhs_list: ASSIGN lhs assignment_lhs_list | ASSIGN lhs ;  */

lhs: index_expression | ID;
if_statement:
	IF L_BRAC expression R_BRAC statement (ELSE statement)?;

while_statement: DO (statement)+ WHILE expression SEMI;

for_statement:
	FOR L_BRAC expression SEMI expression SEMI expression R_BRAC statement;

break_statement: BREAK;

continue_statement: CONTINUE;

return_statement: RETURN expression?;

block_statement: L_PARENT statement* R_PARENT;

call_statement: ID L_BRAC call_param? R_BRAC;

call_param: expression COMMA call_param | expression;

empty:;

BOOLEAN: 'boolean';
BREAK: 'break';
CONTINUE: 'continue';
ELSE: 'else';
FOR: 'for';
FLOAT: 'float';
IF: 'if';
INT: 'int';
RETURN: 'return';
VOID: 'void';
DO: 'do';
WHILE: 'while';
TRUE: 'true';
FALSE: 'false';
STRING: 'string';

PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
NOT: '!';
MODUL: '%';
OR: '||';
AND: '&&';
NOT_EQUAL: '!=';
EQUAL: '==';
LESS: '<';
GREATER: '>';
LESS_EQUAL: '<=';
GREATER_EQUAL: '>=';
ASSIGN: '=';

L_SQUARE: '[';
R_SQUARE: ']';
L_PARENT: '{';
R_PARENT: '}';
L_BRAC: '(';
R_BRAC: ')';
SEMI: ';';
COMMA: ',';


NUM_INT: [0-9]+;
NUM_FLOAT:
	[0-9]+ '.' [0-9]* EXPONENT?
	| '.' [0-9]+ EXPONENT?
	| [0-9]+ EXPONENT;
fragment EXPONENT: ('e' | 'E') '-'? ('0' .. '9')+;


STRING_LITERAL: UNCLOSE_STRING '"' {self.text = self.text[1:-1]};

UNCLOSE_STRING:
	'"' ('\\' [btrnf\\'"] | ~[\b\t\r\n\f\\'"])* {raise UncloseString(self.text[1:])};
ILLEGAL_ESCAPE:
	UNCLOSE_STRING '\\' ~[btnfr"'\\] {raise IllegalEscape(self.text[1:])};

fragment ESCAPE_STRING:
	'\\b'
	| '\\f'
	| '\\r'
	| '\\n'
	| '\\t'
	| '\\\''
	| '\\"'
	| '\\\\';
COMMENT_1: '/*' .*? '*/' -> skip;
COMMENT_2: '//' ~[\r\n]* -> skip;
WS: [ \t\r\n] -> skip;
ID: [a-zA-Z_] [a-zA-Z0-9_]*;
ERROR_CHAR: .{raise ErrorToken(self.text)};