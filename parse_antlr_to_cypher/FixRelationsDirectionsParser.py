# Generated from FixRelationsDirections.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,25,136,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,1,0,1,0,5,0,25,8,0,10,0,12,0,
        28,9,0,1,1,1,1,1,1,1,1,5,1,34,8,1,10,1,12,1,37,9,1,1,2,3,2,40,8,
        2,1,2,1,2,1,3,1,3,5,3,46,8,3,10,3,12,3,49,9,3,1,3,1,3,1,4,1,4,1,
        4,1,4,5,4,57,8,4,10,4,12,4,60,9,4,1,5,3,5,63,8,5,1,5,1,5,1,5,1,5,
        3,5,69,8,5,1,6,1,6,3,6,73,8,6,1,6,3,6,76,8,6,1,6,3,6,79,8,6,1,6,
        3,6,82,8,6,1,6,3,6,85,8,6,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,
        7,1,7,1,7,3,7,99,8,7,1,8,1,8,3,8,103,8,8,1,8,1,8,3,8,107,8,8,1,8,
        1,8,1,8,1,8,3,8,113,8,8,1,8,3,8,116,8,8,1,8,3,8,119,8,8,1,9,1,9,
        1,9,1,9,5,9,125,8,9,10,9,12,9,128,9,9,1,9,1,9,1,10,1,10,1,10,1,10,
        1,10,1,47,0,11,0,2,4,6,8,10,12,14,16,18,20,0,0,146,0,26,1,0,0,0,
        2,29,1,0,0,0,4,39,1,0,0,0,6,47,1,0,0,0,8,52,1,0,0,0,10,62,1,0,0,
        0,12,84,1,0,0,0,14,98,1,0,0,0,16,118,1,0,0,0,18,120,1,0,0,0,20,131,
        1,0,0,0,22,23,5,12,0,0,23,25,5,21,0,0,24,22,1,0,0,0,25,28,1,0,0,
        0,26,24,1,0,0,0,26,27,1,0,0,0,27,1,1,0,0,0,28,26,1,0,0,0,29,30,5,
        12,0,0,30,35,3,4,2,0,31,32,5,20,0,0,32,34,3,4,2,0,33,31,1,0,0,0,
        34,37,1,0,0,0,35,33,1,0,0,0,35,36,1,0,0,0,36,3,1,0,0,0,37,35,1,0,
        0,0,38,40,5,19,0,0,39,38,1,0,0,0,39,40,1,0,0,0,40,41,1,0,0,0,41,
        42,5,21,0,0,42,5,1,0,0,0,43,46,3,8,4,0,44,46,9,0,0,0,45,43,1,0,0,
        0,45,44,1,0,0,0,46,49,1,0,0,0,47,48,1,0,0,0,47,45,1,0,0,0,48,50,
        1,0,0,0,49,47,1,0,0,0,50,51,5,0,0,1,51,7,1,0,0,0,52,58,3,16,8,0,
        53,54,3,10,5,0,54,55,3,16,8,0,55,57,1,0,0,0,56,53,1,0,0,0,57,60,
        1,0,0,0,58,56,1,0,0,0,58,59,1,0,0,0,59,9,1,0,0,0,60,58,1,0,0,0,61,
        63,5,11,0,0,62,61,1,0,0,0,62,63,1,0,0,0,63,64,1,0,0,0,64,65,5,13,
        0,0,65,66,3,12,6,0,66,68,5,13,0,0,67,69,5,10,0,0,68,67,1,0,0,0,68,
        69,1,0,0,0,69,11,1,0,0,0,70,72,5,6,0,0,71,73,5,21,0,0,72,71,1,0,
        0,0,72,73,1,0,0,0,73,75,1,0,0,0,74,76,3,2,1,0,75,74,1,0,0,0,75,76,
        1,0,0,0,76,78,1,0,0,0,77,79,3,14,7,0,78,77,1,0,0,0,78,79,1,0,0,0,
        79,81,1,0,0,0,80,82,3,18,9,0,81,80,1,0,0,0,81,82,1,0,0,0,82,83,1,
        0,0,0,83,85,5,7,0,0,84,70,1,0,0,0,84,85,1,0,0,0,85,13,1,0,0,0,86,
        99,5,18,0,0,87,88,5,18,0,0,88,99,5,24,0,0,89,90,5,18,0,0,90,91,5,
        24,0,0,91,92,5,14,0,0,92,99,5,14,0,0,93,94,5,18,0,0,94,95,5,24,0,
        0,95,96,5,14,0,0,96,97,5,14,0,0,97,99,5,24,0,0,98,86,1,0,0,0,98,
        87,1,0,0,0,98,89,1,0,0,0,98,93,1,0,0,0,99,15,1,0,0,0,100,102,5,4,
        0,0,101,103,5,21,0,0,102,101,1,0,0,0,102,103,1,0,0,0,103,104,1,0,
        0,0,104,106,3,0,0,0,105,107,3,18,9,0,106,105,1,0,0,0,106,107,1,0,
        0,0,107,108,1,0,0,0,108,109,5,5,0,0,109,119,1,0,0,0,110,112,5,4,
        0,0,111,113,5,21,0,0,112,111,1,0,0,0,112,113,1,0,0,0,113,115,1,0,
        0,0,114,116,3,18,9,0,115,114,1,0,0,0,115,116,1,0,0,0,116,117,1,0,
        0,0,117,119,5,5,0,0,118,100,1,0,0,0,118,110,1,0,0,0,119,17,1,0,0,
        0,120,121,5,8,0,0,121,126,3,20,10,0,122,123,5,15,0,0,123,125,3,20,
        10,0,124,122,1,0,0,0,125,128,1,0,0,0,126,124,1,0,0,0,126,127,1,0,
        0,0,127,129,1,0,0,0,128,126,1,0,0,0,129,130,5,9,0,0,130,19,1,0,0,
        0,131,132,5,21,0,0,132,133,5,12,0,0,133,134,5,22,0,0,134,21,1,0,
        0,0,20,26,35,39,45,47,58,62,68,72,75,78,81,84,98,102,106,112,115,
        118,126
    ]

class FixRelationsDirectionsParser ( Parser ):

    grammarFileName = "FixRelationsDirections.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'('", "')'", "'['", "']'", "'{'", "'}'", "'>'", "'<'", 
                     "':'", "'-'", "'.'", "','", "'+'", "'/'", "'*'", "'!'", 
                     "'|'" ]

    symbolicNames = [ "<INVALID>", "WS", "COMMENT", "LINE_COMMENT", "LPAREN", 
                      "RPAREN", "LBRACK", "RBRACK", "LBRACE", "RBRACE", 
                      "GT", "LT", "COLON", "SUB", "DOT", "COMMA", "PLUS", 
                      "DIV", "MULT", "NEGATION", "STICK", "NAME", "STRING", 
                      "BACKTICK_STRING", "VARIABLE_LENGTH_DIGITS", "Letter" ]

    RULE_label_expression = 0
    RULE_type_expression = 1
    RULE_type_name = 2
    RULE_start = 3
    RULE_cypher_body = 4
    RULE_relation = 5
    RULE_relation_body = 6
    RULE_variable_length = 7
    RULE_node = 8
    RULE_props = 9
    RULE_prop = 10

    ruleNames =  [ "label_expression", "type_expression", "type_name", "start", 
                   "cypher_body", "relation", "relation_body", "variable_length", 
                   "node", "props", "prop" ]

    EOF = Token.EOF
    WS=1
    COMMENT=2
    LINE_COMMENT=3
    LPAREN=4
    RPAREN=5
    LBRACK=6
    RBRACK=7
    LBRACE=8
    RBRACE=9
    GT=10
    LT=11
    COLON=12
    SUB=13
    DOT=14
    COMMA=15
    PLUS=16
    DIV=17
    MULT=18
    NEGATION=19
    STICK=20
    NAME=21
    STRING=22
    BACKTICK_STRING=23
    VARIABLE_LENGTH_DIGITS=24
    Letter=25

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Label_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(FixRelationsDirectionsParser.COLON)
            else:
                return self.getToken(FixRelationsDirectionsParser.COLON, i)

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(FixRelationsDirectionsParser.NAME)
            else:
                return self.getToken(FixRelationsDirectionsParser.NAME, i)

        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_label_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLabel_expression" ):
                listener.enterLabel_expression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLabel_expression" ):
                listener.exitLabel_expression(self)




    def label_expression(self):

        localctx = FixRelationsDirectionsParser.Label_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_label_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 26
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==12:
                self.state = 22
                self.match(FixRelationsDirectionsParser.COLON)
                self.state = 23
                self.match(FixRelationsDirectionsParser.NAME)
                self.state = 28
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Type_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self):
            return self.getToken(FixRelationsDirectionsParser.COLON, 0)

        def type_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FixRelationsDirectionsParser.Type_nameContext)
            else:
                return self.getTypedRuleContext(FixRelationsDirectionsParser.Type_nameContext,i)


        def STICK(self, i:int=None):
            if i is None:
                return self.getTokens(FixRelationsDirectionsParser.STICK)
            else:
                return self.getToken(FixRelationsDirectionsParser.STICK, i)

        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_type_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType_expression" ):
                listener.enterType_expression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType_expression" ):
                listener.exitType_expression(self)




    def type_expression(self):

        localctx = FixRelationsDirectionsParser.Type_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_type_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self.match(FixRelationsDirectionsParser.COLON)
            self.state = 30
            self.type_name()
            self.state = 35
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==20:
                self.state = 31
                self.match(FixRelationsDirectionsParser.STICK)
                self.state = 32
                self.type_name()
                self.state = 37
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Type_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(FixRelationsDirectionsParser.NAME, 0)

        def NEGATION(self):
            return self.getToken(FixRelationsDirectionsParser.NEGATION, 0)

        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_type_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType_name" ):
                listener.enterType_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType_name" ):
                listener.exitType_name(self)




    def type_name(self):

        localctx = FixRelationsDirectionsParser.Type_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_type_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==19:
                self.state = 38
                self.match(FixRelationsDirectionsParser.NEGATION)


            self.state = 41
            self.match(FixRelationsDirectionsParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(FixRelationsDirectionsParser.EOF, 0)

        def cypher_body(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FixRelationsDirectionsParser.Cypher_bodyContext)
            else:
                return self.getTypedRuleContext(FixRelationsDirectionsParser.Cypher_bodyContext,i)


        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)




    def start(self):

        localctx = FixRelationsDirectionsParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1+1:
                    self.state = 45
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        self.state = 43
                        self.cypher_body()
                        pass

                    elif la_ == 2:
                        self.state = 44
                        self.matchWildcard()
                        pass

             
                self.state = 49
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

            self.state = 50
            self.match(FixRelationsDirectionsParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cypher_bodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_cypher_body

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TripleContext(Cypher_bodyContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FixRelationsDirectionsParser.Cypher_bodyContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def node(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FixRelationsDirectionsParser.NodeContext)
            else:
                return self.getTypedRuleContext(FixRelationsDirectionsParser.NodeContext,i)

        def relation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FixRelationsDirectionsParser.RelationContext)
            else:
                return self.getTypedRuleContext(FixRelationsDirectionsParser.RelationContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTriple" ):
                listener.enterTriple(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTriple" ):
                listener.exitTriple(self)



    def cypher_body(self):

        localctx = FixRelationsDirectionsParser.Cypher_bodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_cypher_body)
        try:
            localctx = FixRelationsDirectionsParser.TripleContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.node()
            self.state = 58
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 53
                    self.relation()
                    self.state = 54
                    self.node() 
                self.state = 60
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SUB(self, i:int=None):
            if i is None:
                return self.getTokens(FixRelationsDirectionsParser.SUB)
            else:
                return self.getToken(FixRelationsDirectionsParser.SUB, i)

        def relation_body(self):
            return self.getTypedRuleContext(FixRelationsDirectionsParser.Relation_bodyContext,0)


        def LT(self):
            return self.getToken(FixRelationsDirectionsParser.LT, 0)

        def GT(self):
            return self.getToken(FixRelationsDirectionsParser.GT, 0)

        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_relation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelation" ):
                listener.enterRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelation" ):
                listener.exitRelation(self)




    def relation(self):

        localctx = FixRelationsDirectionsParser.RelationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_relation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 61
                self.match(FixRelationsDirectionsParser.LT)


            self.state = 64
            self.match(FixRelationsDirectionsParser.SUB)
            self.state = 65
            self.relation_body()
            self.state = 66
            self.match(FixRelationsDirectionsParser.SUB)
            self.state = 68
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 67
                self.match(FixRelationsDirectionsParser.GT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Relation_bodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACK(self):
            return self.getToken(FixRelationsDirectionsParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(FixRelationsDirectionsParser.RBRACK, 0)

        def NAME(self):
            return self.getToken(FixRelationsDirectionsParser.NAME, 0)

        def type_expression(self):
            return self.getTypedRuleContext(FixRelationsDirectionsParser.Type_expressionContext,0)


        def variable_length(self):
            return self.getTypedRuleContext(FixRelationsDirectionsParser.Variable_lengthContext,0)


        def props(self):
            return self.getTypedRuleContext(FixRelationsDirectionsParser.PropsContext,0)


        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_relation_body

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelation_body" ):
                listener.enterRelation_body(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelation_body" ):
                listener.exitRelation_body(self)




    def relation_body(self):

        localctx = FixRelationsDirectionsParser.Relation_bodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_relation_body)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 70
                self.match(FixRelationsDirectionsParser.LBRACK)
                self.state = 72
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==21:
                    self.state = 71
                    self.match(FixRelationsDirectionsParser.NAME)


                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 74
                    self.type_expression()


                self.state = 78
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==18:
                    self.state = 77
                    self.variable_length()


                self.state = 81
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==8:
                    self.state = 80
                    self.props()


                self.state = 83
                self.match(FixRelationsDirectionsParser.RBRACK)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Variable_lengthContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MULT(self):
            return self.getToken(FixRelationsDirectionsParser.MULT, 0)

        def VARIABLE_LENGTH_DIGITS(self, i:int=None):
            if i is None:
                return self.getTokens(FixRelationsDirectionsParser.VARIABLE_LENGTH_DIGITS)
            else:
                return self.getToken(FixRelationsDirectionsParser.VARIABLE_LENGTH_DIGITS, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(FixRelationsDirectionsParser.DOT)
            else:
                return self.getToken(FixRelationsDirectionsParser.DOT, i)

        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_variable_length

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariable_length" ):
                listener.enterVariable_length(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariable_length" ):
                listener.exitVariable_length(self)




    def variable_length(self):

        localctx = FixRelationsDirectionsParser.Variable_lengthContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_variable_length)
        try:
            self.state = 98
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 86
                self.match(FixRelationsDirectionsParser.MULT)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 87
                self.match(FixRelationsDirectionsParser.MULT)
                self.state = 88
                self.match(FixRelationsDirectionsParser.VARIABLE_LENGTH_DIGITS)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 89
                self.match(FixRelationsDirectionsParser.MULT)
                self.state = 90
                self.match(FixRelationsDirectionsParser.VARIABLE_LENGTH_DIGITS)
                self.state = 91
                self.match(FixRelationsDirectionsParser.DOT)
                self.state = 92
                self.match(FixRelationsDirectionsParser.DOT)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 93
                self.match(FixRelationsDirectionsParser.MULT)
                self.state = 94
                self.match(FixRelationsDirectionsParser.VARIABLE_LENGTH_DIGITS)
                self.state = 95
                self.match(FixRelationsDirectionsParser.DOT)
                self.state = 96
                self.match(FixRelationsDirectionsParser.DOT)
                self.state = 97
                self.match(FixRelationsDirectionsParser.VARIABLE_LENGTH_DIGITS)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NodeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_node

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class NodeWithVariableContext(NodeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FixRelationsDirectionsParser.NodeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(FixRelationsDirectionsParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(FixRelationsDirectionsParser.RPAREN, 0)
        def NAME(self):
            return self.getToken(FixRelationsDirectionsParser.NAME, 0)
        def props(self):
            return self.getTypedRuleContext(FixRelationsDirectionsParser.PropsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNodeWithVariable" ):
                listener.enterNodeWithVariable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNodeWithVariable" ):
                listener.exitNodeWithVariable(self)


    class NodeWithVariableAndLabelContext(NodeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FixRelationsDirectionsParser.NodeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(FixRelationsDirectionsParser.LPAREN, 0)
        def label_expression(self):
            return self.getTypedRuleContext(FixRelationsDirectionsParser.Label_expressionContext,0)

        def RPAREN(self):
            return self.getToken(FixRelationsDirectionsParser.RPAREN, 0)
        def NAME(self):
            return self.getToken(FixRelationsDirectionsParser.NAME, 0)
        def props(self):
            return self.getTypedRuleContext(FixRelationsDirectionsParser.PropsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNodeWithVariableAndLabel" ):
                listener.enterNodeWithVariableAndLabel(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNodeWithVariableAndLabel" ):
                listener.exitNodeWithVariableAndLabel(self)



    def node(self):

        localctx = FixRelationsDirectionsParser.NodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_node)
        self._la = 0 # Token type
        try:
            self.state = 118
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                localctx = FixRelationsDirectionsParser.NodeWithVariableAndLabelContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 100
                self.match(FixRelationsDirectionsParser.LPAREN)
                self.state = 102
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==21:
                    self.state = 101
                    self.match(FixRelationsDirectionsParser.NAME)


                self.state = 104
                self.label_expression()
                self.state = 106
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==8:
                    self.state = 105
                    self.props()


                self.state = 108
                self.match(FixRelationsDirectionsParser.RPAREN)
                pass

            elif la_ == 2:
                localctx = FixRelationsDirectionsParser.NodeWithVariableContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 110
                self.match(FixRelationsDirectionsParser.LPAREN)
                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==21:
                    self.state = 111
                    self.match(FixRelationsDirectionsParser.NAME)


                self.state = 115
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==8:
                    self.state = 114
                    self.props()


                self.state = 117
                self.match(FixRelationsDirectionsParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_props

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class PropertiesContext(PropsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FixRelationsDirectionsParser.PropsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LBRACE(self):
            return self.getToken(FixRelationsDirectionsParser.LBRACE, 0)
        def prop(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FixRelationsDirectionsParser.PropContext)
            else:
                return self.getTypedRuleContext(FixRelationsDirectionsParser.PropContext,i)

        def RBRACE(self):
            return self.getToken(FixRelationsDirectionsParser.RBRACE, 0)
        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(FixRelationsDirectionsParser.COMMA)
            else:
                return self.getToken(FixRelationsDirectionsParser.COMMA, i)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProperties" ):
                listener.enterProperties(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProperties" ):
                listener.exitProperties(self)



    def props(self):

        localctx = FixRelationsDirectionsParser.PropsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_props)
        self._la = 0 # Token type
        try:
            localctx = FixRelationsDirectionsParser.PropertiesContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self.match(FixRelationsDirectionsParser.LBRACE)
            self.state = 121
            self.prop()
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==15:
                self.state = 122
                self.match(FixRelationsDirectionsParser.COMMA)
                self.state = 123
                self.prop()
                self.state = 128
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 129
            self.match(FixRelationsDirectionsParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(FixRelationsDirectionsParser.NAME, 0)

        def COLON(self):
            return self.getToken(FixRelationsDirectionsParser.COLON, 0)

        def STRING(self):
            return self.getToken(FixRelationsDirectionsParser.STRING, 0)

        def getRuleIndex(self):
            return FixRelationsDirectionsParser.RULE_prop

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProp" ):
                listener.enterProp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProp" ):
                listener.exitProp(self)




    def prop(self):

        localctx = FixRelationsDirectionsParser.PropContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_prop)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.match(FixRelationsDirectionsParser.NAME)
            self.state = 132
            self.match(FixRelationsDirectionsParser.COLON)
            self.state = 133
            self.match(FixRelationsDirectionsParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





