# Projeto Lógica da Computação

![git status](http://3.129.230.99/svg/cicerotcv/logcomp/)

## Testes de Unidade

```shell
$ python3.8 -m pytest -v --no-header 
```

## Diagrama Sintático

![diagrama](./diagrama.png)

## EBNF

```
TOP_LEVEL = { FUNCTION_DECLARATION } ;

BLOCK = "{" , { STATEMENT }, "}" ;

TYPE = "int" | "str" ;

TYPE_WITH VOID = TYPE | "void";

IDENTIFIER_DECLARATION = TYPE , IDENTIFIER ;

FUNCTION_DECLARATION = TYPE_WITH_VOID , IDENTIFIER , "(" [ , TYPE, IDENTIFIER [ , { "," , TYPE, IDENTIFIER } ] ] , ")" , FUNCTION_BODY;

FUNCTION_BODY = "{" , { STATEMENT }, [ , FUNCTION_RETURN ] , "}";

FUNCTION_RETURN = "return", EXPRESSION ;

FUNCTION_CALL = IDENTIFIER , "(" [ , IDENTIFIER [ , { "," , IDENTIFIER } ] ] , ")" ;

STATEMENT = ( λ | IDENTIFIER_DECLARATION | FUNCTION_DECLARATION | FUNCTION_CALL | ASSIGNMENT | BLOCK | WHILE_STATEMENT | IF_STATEMENT ), ";";

FACTOR = ( NUMBER | STRING | IDENTIFIER | FUNCTION_CALL | ( UNNARY_OPERATOR , FACTOR ) | "(" , CONDITIONAL , ")" );

TERM = FACTOR, { ("*" | "/" | "&&"), FACTOR } ;

EXPRESSION = TERM, { ("+" | "-" | "||"), TERM } ;

CONDITIONAL = EXPRESSION , { ("<" | "==" | ">" ) , EXPRESSION } ;

WHILE_STATEMENT = "while" , "(" , CONDITIONAL , ")" , BLOCK ;

IF_STATEMENT = "if" , "(" , CONDITIONAL , ")" , BLOCK , [ "else" , BLOCK ] ;

ASSIGNMENT = IDENTIFIER, "=" , EXPRESSION ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

UNNARY_OPERATOR = ( "+" | "-" | "!" ) ;

NUMBER = DIGIT [ { , DIGIT } ] ;

STRING = '"' , { ... } , '"' ;

LETTER = ( "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" |
"K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" |
"W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" |
"i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" |
"u" | "v" | "w" | "x" | "y" | "z" ) ;

DIGIT = ( "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0" ) ;
```

## Figma

[Clique aqui](https://www.figma.com/file/FwgHMDOpuHXPAxmSICtWKg/Diagrama-Lógica-de-Computação) para visualizar o diagrama no Figma.
