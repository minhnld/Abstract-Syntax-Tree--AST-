from MCVisitor import MCVisitor
from MCParser import MCParser
from AST import *
from functools import reduce
from AST import Id
#1712177

def flatten(listOflist):
    return reduce(lambda x, item: x + item, listOflist, [])


class ASTGeneration(MCVisitor):
    def visitProgram(self, ctx: MCParser.ProgramContext):
        """
        return Program(list of Decl)
        where Decl:
            + VarDecl  ==> var_decl
            + FuncDecl ==> func_decl
        """
        return Program(self.visit(ctx.manydecl()))

    def visitManydecl(self, ctx: MCParser.ManydeclContext):
        """
        return list of decl expanded
        """
        decl = self.visit(ctx.decl())
        if ctx.manydecl():
            return decl + self.visit(ctx.manydecl())
        else:
            return decl

    def visitDecl(self, ctx: MCParser.DeclContext):
        """
        return either
            + var_decl
            + func_decl
        """
        decl = self.visit(ctx.getChild(0))
        if ctx.varDecla():
            return decl
        return [decl]

    def visitVarDecla(self,ctx:MCParser.VarDeclaContext):
        self.varType = self.visit(ctx.primitive_type())
        return self.visit(ctx.varlist())

    def visitVar(self,ctx:MCParser.VarContext):
        if ctx.ID():
            return VarDecl(ctx.ID().getText(),self.varType)
        else:
            return self.visit(ctx.arrayVar())    

    def visitArrayVar(self,ctx:MCParser.ArrayVarContext):
        return VarDecl(ctx.ID().getText(),ArrayType(int(ctx.NUM_INT().getText()),self.varType))

    def visitVarlist(self,ctx:MCParser.VarlistContext):
        return [self.visit(x) for x in ctx.var()]

    def visitVar2(self, ctx: MCParser.Var2Context):
        """
        """
        if ctx.ID() :
            pri_type=self.visit(ctx.primitive_type())
            idenlist = ctx.ID().getText()
            return [VarDecl(idenlist, pri_type)]
        else:
            eleType=self.visit(ctx.primitive_type())
            typee  = ArrayPointerType(eleType)
            idenlist = self.visit(ctx.array_pointer_type())
            return [VarDecl(idenlist, typee)]

    def visitPrimitive_type(self, ctx: MCParser.Primitive_typeContext):
        if ctx.INT():
            return IntType()
        elif ctx.BOOLEAN():
            return BoolType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()

    def visitArray_type(self, ctx: MCParser.Array_typeContext):
        """
        return ArrayType(dim, type)
        """
        dim = ctx.getChild(1).getText()
        return dim
    def visitArray_pointer_type(self, ctx: MCParser.Array_pointer_typeContext):
        """
        """
        dim = ctx.getChild(0).getText()
        return dim

    def visitType_plus(self, ctx: MCParser.Type_plusContext):
        if ctx.VOID():
            return VoidType()
        elif ctx.L_SQUARE():
            return ArrayPointerType(self.visit(ctx.primitive_type()))
        else:
            return self.visit(ctx.primitive_type())

    def visitFunc_decl(self, ctx: MCParser.Func_declContext):
        ident = Id(ctx.ID().getText())
        param_list = self.visit(ctx.param_list()) if ctx.param_list() else []
        mctype = self.visit(ctx.type_plus())
        block_statement = self.visit(ctx.block_statement())
        return FuncDecl(
            ident,
            param_list,
            mctype,
            block_statement
        )
    def visitParam_list(self, ctx: MCParser.Param_listContext):
        if ctx.param_list():
            return self.visit(ctx.var2())+self.visit(ctx.param_list())
        else:
            return self.visit(ctx.var2())
        return

    def visitExpression(self, ctx: MCParser.ExpressionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv1())
        else:
            op =ctx.ASSIGN().getText()
            return BinaryOp(
                op,
                self.visit(ctx.expression_lv1()),
                self.visit(ctx.expression())
            )
    def visitExpression_lv1(self, ctx: MCParser.Expression_lv1Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv2())
        else:
            op =ctx.getChild(1).getText()
            return BinaryOp(
                op,
                self.visit(ctx.expression_lv1()),
                self.visit(ctx.expression_lv2())
            )
    def visitExpression_lv2(self, ctx: MCParser.Expression_lv2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv3())
        else:
            op =ctx.getChild(1).getText()
            return BinaryOp(
                op,
                self.visit(ctx.expression_lv2()),
                self.visit(ctx.expression_lv3())
            )
    def visitExpression_lv3(self, ctx: MCParser.Expression_lv3Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv4(0))
        else:
            op =ctx.getChild(1).getText()
            return BinaryOp(
                op,
                self.visit(ctx.expression_lv4(0)),
                self.visit(ctx.expression_lv4(1))
            )
    def visitExpression_lv4(self, ctx: MCParser.Expression_lv4Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv5(0))
        else:
            op =ctx.getChild(1).getText()
            return BinaryOp(
                op,
                self.visit(ctx.expression_lv5(0)),
                self.visit(ctx.expression_lv5(1))
            )
    def visitExpression_lv5(self, ctx: MCParser.Expression_lv5Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv6())
        else:
            op =ctx.getChild(1).getText()
            return BinaryOp(
                op,
                self.visit(ctx.expression_lv5()),
                self.visit(ctx.expression_lv6())
            )
    def visitExpression_lv6(self, ctx: MCParser.Expression_lv6Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv7())
        else:
            op =ctx.getChild(1).getText()
            return BinaryOp(
                op,
                self.visit(ctx.expression_lv6()),
                self.visit(ctx.expression_lv7())
            )
    def visitExpression_lv7(self, ctx: MCParser.Expression_lv7Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv8())
        else:
            op =ctx.getChild(0).getText()
            return UnaryOp(
                op,
                self.visit(ctx.expression_lv7()),
            )
    def visitExpression_lv8(self, ctx: MCParser.Expression_lv8Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.index_expression())
        else:
            op =ctx.getChild(1).getText()+ctx.getChild(2).getText()
            return UnaryOp(
                op,
                self.visit(ctx.index_expression())
            )
    def visitIndex_expression(self, ctx: MCParser.Index_expressionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.factor())
        else:
            return self.visit(ctx.expression())

    def visitInvocation_expression(self, ctx: MCParser.Invocation_expressionContext):
        if ctx.call_param():
            return self.visit(ctx.call_param())
        return []
    def visitArray_index_express(self, ctx: MCParser.Array_index_expressContext):
        if ctx.call_statement():
            a=self.visit(ctx.call_statement())
        elif ctx.ID():
            a=Id(ctx.ID().getText())
        b=self.visit(ctx.expression())
        return ArrayCell(a,b)

    def visitFactor(self,ctx:MCParser.FactorContext):
        if ctx.expression():
            return self.visit(ctx.expression())
        elif ctx.invocation_expression():
            return CallExpr(Id(ctx.ID().getText()),
                            self.visit(ctx.invocation_expression()))
        elif ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.array_index_express():
            return self.visit(ctx.array_index_express())
        return
    def visitLiteral(self, ctx: MCParser.LiteralContext):
        if ctx.number():
            return self.visit(ctx.number())
        elif ctx.bool_lit():
            return self.visit(ctx.bool_lit())
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        return

    def visitBool_lit(self, ctx: MCParser.Bool_litContext):
        if ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
    def visitNumber(self, ctx: MCParser.NumberContext):
        if ctx.NUM_INT():
            return IntLiteral(int(ctx.NUM_INT().getText()))
        elif ctx.NUM_FLOAT():
            return FloatLiteral(float(ctx.NUM_FLOAT().getText()))

    def visitStatement(self, ctx: MCParser.StatementContext):
        return self.visit(ctx.getChild(0))

    def visitStructured_statement(self, ctx: MCParser.Structured_statementContext):
        if ctx.block_statement():
            return [self.visit(ctx.getChild(0))]
        else:
            return [self.visit(ctx.getChild(0))]

    def visitNormal_statement(self, ctx: MCParser.Normal_statementContext):
            return [self.visit(ctx.getChild(0))]


    def visitLhs(self, ctx: MCParser.LhsContext):
        """
        XXXXXXX
        """
        if ctx.ID():
            return Id(ctx.ID().getText())
        else:
            return self.visit(ctx.index_expression())

    def visitIf_statement(self, ctx: MCParser.If_statementContext):
        expression = self.visit(ctx.expression())
        if ctx.ELSE():
            then_statement = self.visit(ctx.statement(0))
            if (type(then_statement)==list):
                 then_statement = then_statement[0] 
            else_statement = self.visit(ctx.statement(1))
            if (type(else_statement)==list):
                 else_statement = else_statement[0]
            return If(expression, then_statement, else_statement)
        else:
            then_statement = self.visit(ctx.statement(0))
            if (type(then_statement)==list):
                 then_statement = then_statement[0] 
            return If(expression, then_statement)

    def visitWhile_statement(self, ctx: MCParser.While_statementContext):
        return Dowhile(flatten(list(map(self.visit, ctx.statement()))), self.visit(ctx.expression()) )

    def visitFor_statement(self, ctx: MCParser.For_statementContext):
        a=self.visit(ctx.statement())
        if (type(a)==list):
             a=a[0]
        return For(
            self.visit(ctx.expression(0)),
            self.visit(ctx.expression(1)),
            self.visit(ctx.expression(2)),
            a
            )

    def visitBreak_statement(self, ctx: MCParser.Break_statementContext):
        return Break()

    def visitContinue_statement(self, ctx: MCParser.Continue_statementContext):
        return Continue()

    def visitReturn_statement(self, ctx: MCParser.Return_statementContext):
        if ctx.expression():
            return Return(self.visit(ctx.expression()))
        else:
            return Return()

    def visitBlock_statement(self, ctx: MCParser.Block_statementContext):
        if ctx.statement():
            return Block(flatten(list(map(self.visit, ctx.statement()))))
        else:
            return Block([])

    def visitCall_statement(self, ctx: MCParser.Call_statementContext):
        param = self.visit(ctx.call_param()) if ctx.call_param() else []
        return CallExpr(Id(ctx.ID().getText()), param)
    
    def visitCall_param(self, ctx: MCParser.Call_paramContext):
        expression = self.visit(ctx.expression())
        if ctx.call_param():
            return [expression] + self.visit(ctx.call_param())
        else:
            return [expression]

    def visitEmpty(self, ctx: MCParser.EmptyContext):
        return



       

 





