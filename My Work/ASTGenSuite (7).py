import unittest
from TestUtils import TestAST
from AST import *
#1712177
class ASTGenSuite(unittest.TestCase):
    def test_declaration0(self):
        '''Basic main function declaration'''
        input = """int main() { }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,300))
    def test_declaration1(self):
        '''single variable declaration'''
        input = """
        int main() { int a; }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([VarDecl("a",IntType())]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,301))
    def test_declaration2(self):
        '''declaration outside function scope'''
        input = """int b;
        int main() { int a; }
        """
        expect = str(Program([VarDecl("b",IntType()),FuncDecl(Id("main"),[],IntType(),Block([VarDecl("a",IntType())]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,302))
    def test_declaration3(self):
        '''multiple declaration comma seperated. also testing array type'''
        input = """int b, c, a[4];
        void func() {
            b = b + 2;
            return b;
        }
        int main() { int a; }
        """
        expect = str(Program([VarDecl("b",IntType()),VarDecl("c",IntType()),VarDecl("a",ArrayType(4,IntType())),FuncDecl(Id("func"),[],VoidType(),Block([BinaryOp("=",Id("b"),BinaryOp("+",Id("b"),IntLiteral(2))),Return(Id("b"))])),FuncDecl(Id("main"),[],IntType(),Block([VarDecl("a",IntType())]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,303))
    def test_declaration4(self):
        '''multiple declaration comma seperated. also testing array type'''
        input = """int b, c, a[4];
        int main() { int a; int b; int d, e[5], f[5]; }
        """
        expect = str(Program([VarDecl("b",IntType()),VarDecl("c",IntType()),VarDecl("a",ArrayType(4,IntType())),FuncDecl(Id("main"),[],IntType(),Block([VarDecl("a",IntType()),VarDecl("b",IntType()),VarDecl("d",IntType()),VarDecl("e",ArrayType(5,IntType())),VarDecl("f",ArrayType(5,IntType()))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,304))
    def test_declaration5(self):
        '''test variable declaration with other type'''
        input = """float a;
        float b, c[2], d;

        int main() { }
        """
        expect = str(Program([VarDecl("a",FloatType()),VarDecl("b",FloatType()),VarDecl("c",ArrayType(2,FloatType())),VarDecl("d",FloatType()),FuncDecl(Id("main"),[],IntType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,305))
    def test_declaration6(self):
        '''test variable declaration with other type: boolean,string'''
        input = """float b, c[2], d;
        int main() {
            string a[5], b;
            boolean b; boolean t, d[100];
        }
        """
        expect = str(Program([VarDecl("b",FloatType()),VarDecl("c",ArrayType(2,FloatType())),VarDecl("d",FloatType()),FuncDecl(Id("main"),[],IntType(),Block([VarDecl("a",ArrayType(5,StringType())),VarDecl("b",StringType()),VarDecl("b",BoolType()),VarDecl("t",BoolType()),VarDecl("d",ArrayType(100,BoolType()))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,306))
    def test_declaration7(self):
        '''simple parameter declaration'''
        input = """
        int main(int a) {
            string a[5], b;
            boolean b; boolean t, d[100];
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[VarDecl("a",IntType())],IntType(),Block([VarDecl("a",ArrayType(5,StringType())),VarDecl("b",StringType()),VarDecl("b",BoolType()),VarDecl("t",BoolType()),VarDecl("d",ArrayType(100,BoolType()))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,307))
    def test_declaration8(self):
        '''multiple parameter declaration'''
        input = """
        int main(int a, string b, boolean c) {
            string a[5], b;
            boolean b; boolean t, d[100];
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[VarDecl("a",IntType()),VarDecl("b",StringType()),VarDecl("c",BoolType())],IntType(),Block([VarDecl("a",ArrayType(5,StringType())),VarDecl("b",StringType()),VarDecl("b",BoolType()),VarDecl("t",BoolType()),VarDecl("d",ArrayType(100,BoolType()))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,308))
    def test_declaration9(self):
        '''multiple parameter declaration including array type'''
        input = """
        int main(int a, float b[], int c[]) {
            string a[5], b;
            boolean b; boolean t, d[100];
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[VarDecl("a",IntType()),VarDecl("b",ArrayPointerType(FloatType())),VarDecl("c",ArrayPointerType(IntType()))],IntType(),Block([VarDecl("a",ArrayType(5,StringType())),VarDecl("b",StringType()),VarDecl("b",BoolType()),VarDecl("t",BoolType()),VarDecl("d",ArrayType(100,BoolType()))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,309))
    def test_declaration10(self):
        '''different return type'''
        input = """
        float main(int a[], float b) {
        }
        void put(int b[]) {

        }


        """
        expect = str(Program([FuncDecl(Id("main"),[VarDecl("a",ArrayPointerType(IntType())),VarDecl("b",FloatType())],FloatType(),Block([])),FuncDecl(Id("put"),[VarDecl("b",ArrayPointerType(IntType()))],VoidType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,310))
    def test_declaration11(self):
        '''different return type: part2'''
        input = """
        float main(int a[], float b) {
        }
        void put(int b[]) {

        }
        string[] multiply() {
            
        }
        

        """
        expect = str(Program([FuncDecl(Id("main"),[VarDecl("a",ArrayPointerType(IntType())),VarDecl("b",FloatType())],FloatType(),Block([])),FuncDecl(Id("put"),[VarDecl("b",ArrayPointerType(IntType()))],VoidType(),Block([])),FuncDecl(Id("multiply"),[],ArrayPointerType(StringType()),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,311))
    def test_declaration12(self):
        '''different return type: part3'''
        input = """
        float main(int a[], float b) {
        }
        void put(int b[]) {

        }
        boolean[] foo(boolean bar, int a, string b[]) {

        }

        """
        expect = str(Program([FuncDecl(Id("main"),[VarDecl("a",ArrayPointerType(IntType())),VarDecl("b",FloatType())],FloatType(),Block([])),FuncDecl(Id("put"),[VarDecl("b",ArrayPointerType(IntType()))],VoidType(),Block([])),FuncDecl(Id("foo"),[VarDecl("bar",BoolType()),VarDecl("a",IntType()),VarDecl("b",ArrayPointerType(StringType()))],ArrayPointerType(BoolType()),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,312))
    def test_declaration13(self):
        '''testing complex declaration: function and variable'''
        input = """
        float c[5], d, e, f[100];
        float main(float a[], boolean b) {
            int a;
            float b;
            return a;
        }

        void put(int b[]) {
            string b,c,d;
            return b;
        }
        

        """
        expect = str(Program([VarDecl("c",ArrayType(5,FloatType())),VarDecl("d",FloatType()),VarDecl("e",FloatType()),VarDecl("f",ArrayType(100,FloatType())),FuncDecl(Id("main"),[VarDecl("a",ArrayPointerType(FloatType())),VarDecl("b",BoolType())],FloatType(),Block([VarDecl("a",IntType()),VarDecl("b",FloatType()),Return(Id("a"))])),FuncDecl(Id("put"),[VarDecl("b",ArrayPointerType(IntType()))],VoidType(),Block([VarDecl("b",StringType()),VarDecl("c",StringType()),VarDecl("d",StringType()),Return(Id("b"))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,313))
    def test_statement0(self):
        '''single return statement inside function'''
        input = """
        float main(int a[], float b) {
            return 0;
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[VarDecl("a",ArrayPointerType(IntType())),VarDecl("b",FloatType())],FloatType(),Block([Return(IntLiteral(0))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,314)) 
    def test_statement1(self):
        '''simple if statement'''
        input = """
        float main(int argc, string argv[]) {
            if (argc)
                return 1;
            return 0;
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[VarDecl("argc",IntType()),VarDecl("argv",ArrayPointerType(StringType()))],FloatType(),Block([If(Id("argc"),Return(IntLiteral(1))),Return(IntLiteral(0))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,315)) 
    def test_statement2(self):
        '''simple if statement followed by a block'''
        input = """
        float main(int argc, string argv[]) {
            if (argc < 2) {
                print("Not enough argument\\n");
                return 1;
            }
            return 0;
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[VarDecl("argc",IntType()),VarDecl("argv",ArrayPointerType(StringType()))],FloatType(),Block([If(BinaryOp("<",Id("argc"),IntLiteral(2)),Block([CallExpr(Id("print"),[StringLiteral("Not enough argument\\n")]),Return(IntLiteral(1))])),Return(IntLiteral(0))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,316))
    def test_statement3(self):
        '''simple if else statement'''
        input = """
        int main() {
            if (argc < 2) {
                print("Not enough argument\\n");
                return 1;
            }
            else return 0;
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([If(BinaryOp("<",Id("argc"),IntLiteral(2)),Block([CallExpr(Id("print"),[StringLiteral("Not enough argument\\n")]),Return(IntLiteral(1))]),Return(IntLiteral(0)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,317))
    def test_statement4(self):
        '''nested if else statement'''
        input = """
        int main() {
            if (argc < 2) {
                if (a = 2) a = 5;
                else donothing();
            }
            else return 0;
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([If(BinaryOp("<",Id("argc"),IntLiteral(2)),Block([If(BinaryOp("=",Id("a"),IntLiteral(2)),BinaryOp("=",Id("a"),IntLiteral(5)),CallExpr(Id("donothing"),[]))]),Return(IntLiteral(0)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,318))
    def test_statement5(self):
        '''ambiguous if else statement'''
        input = """
        int main() {
            if (argc < 2) if (arg > 3) argc = argc + 3;
            else !argc;
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([If(BinaryOp("<",Id("argc"),IntLiteral(2)),If(BinaryOp(">",Id("arg"),IntLiteral(3)),BinaryOp("=",Id("argc"),BinaryOp("+",Id("argc"),IntLiteral(3))),UnaryOp("!",Id("argc"))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,319))
    def test_statement6(self):
        '''c style if else statement'''
        input = """
        int main() {
            if (a > 0 && b > 0)
                a*b == 0;
            else if (a != 0) {
                b = 0;
            }
            else if (b != 0) 
                a == 0;
            else {
                print(a, b);
                return "Nothing";
            }
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([If(BinaryOp("&&",BinaryOp(">",Id("a"),IntLiteral(0)),BinaryOp(">",Id("b"),IntLiteral(0))),BinaryOp("==",BinaryOp("*",Id("a"),Id("b")),IntLiteral(0)),If(BinaryOp("!=",Id("a"),IntLiteral(0)),Block([BinaryOp("=",Id("b"),IntLiteral(0))]),If(BinaryOp("!=",Id("b"),IntLiteral(0)),BinaryOp("==",Id("a"),IntLiteral(0)),Block([CallExpr(Id("print"),[Id("a"),Id("b")]),Return(StringLiteral("Nothing"))]))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,320))
    def test_statement7(self):
        '''ambiguous complex if else statement'''
        input = """
        int main() {
            if (argc < 2) 
            if (arg > 3) 
            if (argc > 4) 
            if (argc[3]) a = 4;
            else a = 5;
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([If(BinaryOp("<",Id("argc"),IntLiteral(2)),If(BinaryOp(">",Id("arg"),IntLiteral(3)),If(BinaryOp(">",Id("argc"),IntLiteral(4)),If(ArrayCell(Id("argc"),IntLiteral(3)),BinaryOp("=",Id("a"),IntLiteral(4)),BinaryOp("=",Id("a"),IntLiteral(5))))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,321))
    def test_statement8(self):
        '''ambiguous complex multilevel if else statement'''
        input = """
        int main() {
            if (argc < 2) 
            if (arg > 3) 
            if (argc > 4) 
            if (argc[3]) a = 4;
            else if (!t)
            if (-t - 2 == 0) t; 
            else 
                b = 0;
            else a = 3;
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([If(BinaryOp("<",Id("argc"),IntLiteral(2)),If(BinaryOp(">",Id("arg"),IntLiteral(3)),If(BinaryOp(">",Id("argc"),IntLiteral(4)),If(ArrayCell(Id("argc"),IntLiteral(3)),BinaryOp("=",Id("a"),IntLiteral(4)),If(UnaryOp("!",Id("t")),If(BinaryOp("==",BinaryOp("-",UnaryOp("-",Id("t")),IntLiteral(2)),IntLiteral(0)),Id("t"),BinaryOp("=",Id("b"),IntLiteral(0))),BinaryOp("=",Id("a"),IntLiteral(3)))))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,322))
    def test_statement9(self):
        '''simple for statement'''
        input = """
        int main() {
            int a;
            for (a > 3; a = 2; a = a + 1) print(a);
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([VarDecl("a",IntType()),For(BinaryOp(">",Id("a"),IntLiteral(3)),BinaryOp("=",Id("a"),IntLiteral(2)),BinaryOp("=",Id("a"),BinaryOp("+",Id("a"),IntLiteral(1))),CallExpr(Id("print"),[Id("a")]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,323))
    def test_statement10(self):
        '''simple for statement followed by a block'''
        input = """
        int main() {
            int a;
            for (a > 3; a = 2; a = a + 1) {
                a; b;
                a[2];
            }
        }
        """
        expect = "Program([FuncDecl(Id(main),[],IntType,Block([VarDecl(a,IntType),For(BinaryOp(>,Id(a),IntLiteral(3));BinaryOp(=,Id(a),IntLiteral(2));BinaryOp(=,Id(a),BinaryOp(+,Id(a),IntLiteral(1)));Block([Id(a),Id(b),ArrayCell(Id(a),IntLiteral(2))]))]))])"
        self.assertTrue(TestAST.checkASTGen(input,expect,324))
    def test_statement11(self):
        '''break, continue, return'''
        input = """
        int main() {
            int a;
            for (a > 3; a = 2; a = a + 1) {
                break;
                continue;
                return 5;
            }
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([VarDecl("a",IntType()),For(BinaryOp(">",Id("a"),IntLiteral(3)),BinaryOp("=",Id("a"),IntLiteral(2)),BinaryOp("=",Id("a"),BinaryOp("+",Id("a"),IntLiteral(1))),Block([Break(),Continue(),Return(IntLiteral(5))]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,325))
    def test_statement12(self):
        '''break, continue, return'''
        input = """
        int main() {
            int a; break;
            for (a > 3; a = 2; a = a + 1) {
                continue;
                return a[5] - (b+1) && a(foo(),t);
            }
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([VarDecl("a",IntType()),Break(),For(BinaryOp(">",Id("a"),IntLiteral(3)),BinaryOp("=",Id("a"),IntLiteral(2)),BinaryOp("=",Id("a"),BinaryOp("+",Id("a"),IntLiteral(1))),Block([Continue(),Return(BinaryOp("&&",BinaryOp("-",ArrayCell(Id("a"),IntLiteral(5)),BinaryOp("+",Id("b"),IntLiteral(1))),CallExpr(Id("a"),[CallExpr(Id("foo"),[]),Id("t")])))]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,326))
    def test_statement13(self):
        '''nested for statement'''
        input = """
        int main() {
            int a; 
			break;
            for (a > 3; a = 2; a = a + 1) 
                for (t; t && a-1;foo(2)[2] )
                    for (a; b; c) {
                        break;
                    }
        }
        """
        expect = "Program([FuncDecl(Id(main),[],IntType,Block([VarDecl(a,IntType),Break(),For(BinaryOp(>,Id(a),IntLiteral(3));BinaryOp(=,Id(a),IntLiteral(2));BinaryOp(=,Id(a),BinaryOp(+,Id(a),IntLiteral(1)));For(Id(t);BinaryOp(&&,Id(t),BinaryOp(-,Id(a),IntLiteral(1)));ArrayCell(CallExpr(Id(foo),[IntLiteral(2)]),IntLiteral(2));For(Id(a);Id(b);Id(c);Block([Break()]))))]))])"
        self.assertTrue(TestAST.checkASTGen(input,expect,327))
    def test_statement14(self):
        '''nested block statement'''
        input = """
            int main(){
                {
                    a>3;
                    {
                        {

                        }
                    }
                    if (3) 5; else 4;
                }
            }

        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([Block([BinaryOp(">",Id("a"),IntLiteral(3)),Block([Block([])]),If(IntLiteral(3),IntLiteral(5),IntLiteral(4))])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,328))
    def test_statement15(self):
        '''multiple block statement '''
        input = """
        int main() {
            {

            }
            {

            }
            {
                
            }
        }

        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([Block([]),Block([]),Block([])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,329))
    def test_statement16(self):
        '''simple do while statement '''
        input = """
        int main() {
            do a + b == 2; t = x*y*z; return 0;
            while a > 3;
        }

        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([Dowhile([BinaryOp("==",BinaryOp("+",Id("a"),Id("b")),IntLiteral(2)),BinaryOp("=",Id("t"),BinaryOp("*",BinaryOp("*",Id("x"),Id("y")),Id("z"))),Return(IntLiteral(0))],BinaryOp(">",Id("a"),IntLiteral(3)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,330))
    def test_statement17(self):
        '''simple do while statement with block '''
        input = """
        int main() {
            do { }
            while a > 3;
        }

        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([Dowhile([Block([])],BinaryOp(">",Id("a"),IntLiteral(3)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,331))
    def test_statement18(self):
        '''simple do while statement with multiple block '''
        input = """
        int main() {
            do { } { } { }
            while a > 3;
        }

        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([Dowhile([Block([]),Block([]),Block([])],BinaryOp(">",Id("a"),IntLiteral(3)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,332))
    def test_statement19(self):
        '''simple do while statement with if else for ínide'''
        input = """
        int main() {
            do {if (x > 3) x(3); else x(5)[2];} 
            for (x; z+1 == 4; z = z % 2) {

            }
            while a > 3;
        }

        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([Dowhile([Block([If(BinaryOp(">",Id("x"),IntLiteral(3)),CallExpr(Id("x"),[IntLiteral(3)]),ArrayCell(CallExpr(Id("x"),[IntLiteral(5)]),IntLiteral(2)))]),For(Id("x"),BinaryOp("==",BinaryOp("+",Id("z"),IntLiteral(1)),IntLiteral(4)),BinaryOp("=",Id("z"),BinaryOp("%",Id("z"),IntLiteral(2))),Block([]))],BinaryOp(">",Id("a"),IntLiteral(3)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,333))
    def test_statement20(self):
        '''simple do while statement with various statement'''
        input = """
        int main() {
            do {if (x > 3) x(3); else x(5)[2];} 
            for (x; z+1 == 4; z = z % 2) {
                t || -z;
            }
            z+1;
            break;
            return a[-2] && 1;
            if (something) if ("Nothing")
            return "OK"; else return "everything";
            while a > 3;
        }

        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([Dowhile([Block([If(BinaryOp(">",Id("x"),IntLiteral(3)),CallExpr(Id("x"),[IntLiteral(3)]),ArrayCell(CallExpr(Id("x"),[IntLiteral(5)]),IntLiteral(2)))]),For(Id("x"),BinaryOp("==",BinaryOp("+",Id("z"),IntLiteral(1)),IntLiteral(4)),BinaryOp("=",Id("z"),BinaryOp("%",Id("z"),IntLiteral(2))),Block([BinaryOp("||",Id("t"),UnaryOp("-",Id("z")))])),BinaryOp("+",Id("z"),IntLiteral(1)),Break(),Return(BinaryOp("&&",ArrayCell(Id("a"),UnaryOp("-",IntLiteral(2))),IntLiteral(1))),If(Id("something"),If(StringLiteral("Nothing"),Return(StringLiteral("OK")),Return(StringLiteral("everything"))))],BinaryOp(">",Id("a"),IntLiteral(3)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,334))
    def test_statement21(self):
        '''nested do-while statement'''
        input = """
        int main() {
            do do do { }
            while (a>5); while (t); while (1 || m(2,t(3)));
        }

        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([Dowhile([Dowhile([Dowhile([Block([])],BinaryOp(">",Id("a"),IntLiteral(5)))],Id("t"))],BinaryOp("||",IntLiteral(1),CallExpr(Id("m"),[IntLiteral(2),CallExpr(Id("t"),[IntLiteral(3)])])))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,335))
    def test_statement22(self):
        '''all statement combined 1'''
        input = """
        int main() {
            int x;
            for (x = 2; x = x - 2; x = x + 1) {
                if (!t || true) {
                    return false;
                } else if (false) {
                    break;
                    
                }
            }
            do {
            int a;
            foo(2);

            } while (println("OK"));
        }

        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([VarDecl("x",IntType()),For(BinaryOp("=",Id("x"),IntLiteral(2)),BinaryOp("=",Id("x"),BinaryOp("-",Id("x"),IntLiteral(2))),BinaryOp("=",Id("x"),BinaryOp("+",Id("x"),IntLiteral(1))),Block([If(BinaryOp("||",UnaryOp("!",Id("t")),BooleanLiteral(True)),Block([Return(BooleanLiteral(False))]),If(BooleanLiteral(False),Block([Break()])))])),Dowhile([Block([VarDecl("a",IntType()),CallExpr(Id("foo"),[IntLiteral(2)])])],CallExpr(Id("println"),[StringLiteral("OK")]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,336))
    def test_statement23(self):
        '''all statement combined 2'''
        input = """
        int main() {
            do for(t + 1; evalueate(); t) {

            } while (x-2); {

            }
        }

        """
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([Dowhile([For(BinaryOp("+",Id("t"),IntLiteral(1)),CallExpr(Id("evalueate"),[]),Id("t"),Block([]))],BinaryOp("-",Id("x"),IntLiteral(2))),Block([])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,337))
    def test_statement24(self):
        '''all statement combined 3'''
        input = """
        void main() {
            int a;
            do a+3; if (a * 2 + f[3])
            if (a < 4) a = 10; else a = foo(3, a[5], !4);
            for (i = 2; i < 10; i = i + 1) { }
            while (foo());
        }

        """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("a",IntType()),Dowhile([BinaryOp("+",Id("a"),IntLiteral(3)),If(BinaryOp("+",BinaryOp("*",Id("a"),IntLiteral(2)),ArrayCell(Id("f"),IntLiteral(3))),If(BinaryOp("<",Id("a"),IntLiteral(4)),BinaryOp("=",Id("a"),IntLiteral(10)),BinaryOp("=",Id("a"),CallExpr(Id("foo"),[IntLiteral(3),ArrayCell(Id("a"),IntLiteral(5)),UnaryOp("!",IntLiteral(4))])))),For(BinaryOp("=",Id("i"),IntLiteral(2)),BinaryOp("<",Id("i"),IntLiteral(10)),BinaryOp("=",Id("i"),BinaryOp("+",Id("i"),IntLiteral(1))),Block([]))],CallExpr(Id("foo"),[]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,338))
    def test_statement25(self):
        '''all statement combined 4'''
        input = """
        void foo() {
            int i, j;
            for (i = 2; t / 2; t-1) 
                for (j = 4; j > 10; j = j * j) {
                    return;
                }
            return x % 2 == 1;
        }

        """
        expect = str(Program([FuncDecl(Id("foo"),[],VoidType(),Block([VarDecl("i",IntType()),VarDecl("j",IntType()),For(BinaryOp("=",Id("i"),IntLiteral(2)),BinaryOp("/",Id("t"),IntLiteral(2)),BinaryOp("-",Id("t"),IntLiteral(1)),For(BinaryOp("=",Id("j"),IntLiteral(4)),BinaryOp(">",Id("j"),IntLiteral(10)),BinaryOp("=",Id("j"),BinaryOp("*",Id("j"),Id("j"))),Block([Return()]))),Return(BinaryOp("==",BinaryOp("%",Id("x"),IntLiteral(2)),IntLiteral(1)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,339))
    def test_statement26(self):
        '''all statement combined 5'''
        input = """
        int f;
        int main() {
            for (i = 0; i < 3; i+1)
            for (t * t; !z; (((((3))))))
            for (foo(foo(2+arr[3>4]));i;1) {
                do do do do do 3+2;
                while 1; while 1; while 1; while 1; while 1;
            }
        }
        """
        expect = str(Program([VarDecl("f",IntType()),FuncDecl(Id("main"),[],IntType(),Block([For(BinaryOp("=",Id("i"),IntLiteral(0)),BinaryOp("<",Id("i"),IntLiteral(3)),BinaryOp("+",Id("i"),IntLiteral(1)),For(BinaryOp("*",Id("t"),Id("t")),UnaryOp("!",Id("z")),IntLiteral(3),For(CallExpr(Id("foo"),[CallExpr(Id("foo"),[BinaryOp("+",IntLiteral(2),ArrayCell(Id("arr"),BinaryOp(">",IntLiteral(3),IntLiteral(4))))])]),Id("i"),IntLiteral(1),Block([Dowhile([Dowhile([Dowhile([Dowhile([Dowhile([BinaryOp("+",IntLiteral(3),IntLiteral(2))],IntLiteral(1))],IntLiteral(1))],IntLiteral(1))],IntLiteral(1))],IntLiteral(1))]))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,340))
    def test_expression0(self):
        '''one op at a time'''
        input = """
        int a;
        float[] main() {
            a = 4 + a;
            return a-b;
        }   
        """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("a"),BinaryOp("+",IntLiteral(4),Id("a"))),Return(BinaryOp("-",Id("a"),Id("b")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,341))
    def test_expression1(self):
        '''one op at a time'''
        input = """
        int a;
        float[] main() {
            a = 4 && a;
            return a || b;
        }   
        """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("a"),BinaryOp("&&",IntLiteral(4),Id("a"))),Return(BinaryOp("||",Id("a"),Id("b")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,342))
    def test_expression2(self):
        '''one op at a time'''
        input = """int a;
        float[] main() {
            a = 4 == a;
            return a != bd;
        } 
        """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("a"),BinaryOp("==",IntLiteral(4),Id("a"))),Return(BinaryOp("!=",Id("a"),Id("bd")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,343)) 
    def test_expression3(self):
        '''one op at a time'''
        input = """
        int a;
        float[] main() {
            a = 4 <= a;
            return a >= bd;
        }   
        """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("a"),BinaryOp("<=",IntLiteral(4),Id("a"))),Return(BinaryOp(">=",Id("a"),Id("bd")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,344)) 
    def test_expression4(self):
        '''one op at a time'''
        input = """
        int a;
        float[] main() {
            a = 4 * a;
            return a % d;
        }   
        """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("a"),BinaryOp("*",IntLiteral(4),Id("a"))),Return(BinaryOp("%",Id("a"),Id("d")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,345)) 
    def test_expression5(self):
        '''one op at a time'''
        input = """
        int a;
        float[] main() {
            a = -4 * a;
            return a % !d;
        }   
        """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("a"),BinaryOp("*",UnaryOp("-",IntLiteral(4)),Id("a"))),Return(BinaryOp("%",Id("a"),UnaryOp("!",Id("d"))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,346))
    def test_expression6(self):
        '''one op at a time'''
        input = """
        int a;
        float[] main() {
            a = a[!3];
            return "Something" + "Nothing";
        }   
        """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("a"),ArrayCell(Id("a"),UnaryOp("!",IntLiteral(3)))),Return(BinaryOp("+",StringLiteral("Something"),StringLiteral("Nothing")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,347))
    def test_expression7(self):
        '''one op at a time'''
        input = """
        int a;
        float[] main() {
            a = a[!3];
            return a(12.3E-4);
        }   
        """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("a"),ArrayCell(Id("a"),UnaryOp("!",IntLiteral(3)))),Return(CallExpr(Id("a"),[FloatLiteral(0.00123)]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,348))
    def test_expression8(self):
        '''one op at a time'''
        input ="""int a;
        float[] main() {
            a = c == d = e == f;
            return a(12.3E-4);
        }     """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("a"),BinaryOp("=",BinaryOp("==",Id("c"),Id("d")),BinaryOp("==",Id("e"),Id("f")))),Return(CallExpr(Id("a"),[FloatLiteral(0.00123)]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,349))
    def test_expression9(self):
        '''testing associativity'''
        input ="""int a;
        float[] main() {
            a = c = d = e = f;
        }     """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("a"),BinaryOp("=",Id("c"),BinaryOp("=",Id("d"),BinaryOp("=",Id("e"),Id("f")))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,350))
    def test_expression10(self):
        '''testing associativity'''
        input ="""int a;
        float[] main() {
            a || b || c || d;
        }     """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("||",BinaryOp("||",BinaryOp("||",Id("a"),Id("b")),Id("c")),Id("d"))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,351))
    def test_expression11(self):
        '''testing associativity'''
        input ="""int a;
        float[] main() {
            b = a && c && d && e;
        }     """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("b"),BinaryOp("&&",BinaryOp("&&",BinaryOp("&&",Id("a"),Id("c")),Id("d")),Id("e")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,352))
    def test_expression12(self):
        '''testing associativity'''
        input ="""int a;
        float[] main() {
            b = a + b - c + d - e;
        }     """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("b"),BinaryOp("-",BinaryOp("+",BinaryOp("-",BinaryOp("+",Id("a"),Id("b")),Id("c")),Id("d")),Id("e")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,353))
    def test_expression13(self):
        '''testing associativity'''
        input ="""int a;
        float[] main() {
            b = a % b * c / d;
        }     """
        expect = str(Program([VarDecl("a",IntType()),FuncDecl(Id("main"),[],ArrayPointerType(FloatType()),Block([BinaryOp("=",Id("b"),BinaryOp("/",BinaryOp("*",BinaryOp("%",Id("a"),Id("b")),Id("c")),Id("d")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,354))
    def test_expression14(self):
        '''testing associativity'''
        input ="""
        void main() {
            a = -!-!5;
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("a"),UnaryOp("-",UnaryOp("!",UnaryOp("-",UnaryOp("!",IntLiteral(5))))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,355))
    def test_expression15(self):
        '''testing precedence'''
        input ="""
        void main() {
            a + b = 12e10;
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",BinaryOp("+",Id("a"),Id("b")),FloatLiteral(120000000000.0))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,356))
    def test_expression16(self):
        '''testing precedence'''
        input ="""
        void main() {
            a = a && c = c || d;
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("a"),BinaryOp("=",BinaryOp("&&",Id("a"),Id("c")),BinaryOp("||",Id("c"),Id("d"))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,357))
    def test_expression17(self):
        '''testing precedence'''
        input ="""
        void main() {
            a = a > c && c || e;
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("a"),BinaryOp("||",BinaryOp("&&",BinaryOp(">",Id("a"),Id("c")),Id("c")),Id("e")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,358))
    def test_expression18(self):
        '''testing precedence'''
        input ="""
        void main() {
            a = a >= c = d != e;
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("a"),BinaryOp("=",BinaryOp(">=",Id("a"),Id("c")),BinaryOp("!=",Id("d"),Id("e"))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,359))
    def test_expression19(self):
        '''testing precedence'''
        input ="""
        void main() {
            a = b > 2 != true; 
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("a"),BinaryOp("!=",BinaryOp(">",Id("b"),IntLiteral(2)),BooleanLiteral(True)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,360))
    def test_expression20(self):
        '''testing precedence'''
        input ="""
        void main() {
            a = b >= 2 != false && 3 * 2 - 4; 
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("a"),BinaryOp("&&",BinaryOp("!=",BinaryOp(">=",Id("b"),IntLiteral(2)),BooleanLiteral(False)),BinaryOp("-",BinaryOp("*",IntLiteral(3),IntLiteral(2)),IntLiteral(4))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,361))
    def test_expression21(self):
        '''testing precedence'''
        input ="""
        void main() {
            a = a - -3 + -4 * 5;
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("a"),BinaryOp("+",BinaryOp("-",Id("a"),UnaryOp("-",IntLiteral(3))),BinaryOp("*",UnaryOp("-",IntLiteral(4)),IntLiteral(5))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,362))
    def test_expression22(self):
        '''testing precedence'''
        input ="""
        void main() {
            a = a + b[2 && false];
        }     """
        expect = "Program([FuncDecl(Id(main),[],VoidType,Block([BinaryOp(=,Id(a),BinaryOp(+,Id(a),ArrayCell(Id(b),BinaryOp(&&,IntLiteral(2),BooleanLiteral(false)))))]))])"
        self.assertTrue(TestAST.checkASTGen(input,expect,363))
    def test_expression23(self):
        '''testing precedence with LP exp RP'''
        input ="""
        void main() {
            a = (a + 3) * 5;
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("a"),BinaryOp("*",BinaryOp("+",Id("a"),IntLiteral(3)),IntLiteral(5)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,364))
    def test_expression24(self):
        '''testing precedence with LP exp RP'''
        input ="""
        void main() {
            a = (a + 3 - c) * 5 * (2 && 3);
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("a"),BinaryOp("*",BinaryOp("*",BinaryOp("-",BinaryOp("+",Id("a"),IntLiteral(3)),Id("c")),IntLiteral(5)),BinaryOp("&&",IntLiteral(2),IntLiteral(3))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,365))
    def test_expression25(self):
        '''testing precedence with LP exp RP'''
        input ="""
        void main() {
            (a = c) = d;
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",BinaryOp("=",Id("a"),Id("c")),Id("d"))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,366))
    def test_expression26(self):
        '''testing precedence with LP exp RP'''
        input ="""
        void main() {
            3 + (4 - 2);
            ((2 >= 3) == 4) == 5;
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("+",IntLiteral(3),BinaryOp("-",IntLiteral(4),IntLiteral(2))),BinaryOp("==",BinaryOp("==",BinaryOp(">=",IntLiteral(2),IntLiteral(3)),IntLiteral(4)),IntLiteral(5))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,367))
    def test_expression27(self):
        '''testing precedence with LP exp RP'''
        input ="""
        void main() {
            a[(2-(4 != (3=1)))/1];
        }     """
        expect = "Program([FuncDecl(Id(main),[],VoidType,Block([ArrayCell(Id(a),BinaryOp(/,BinaryOp(-,IntLiteral(2),BinaryOp(!=,IntLiteral(4),BinaryOp(=,IntLiteral(3),IntLiteral(1)))),IntLiteral(1)))]))])"
        self.assertTrue(TestAST.checkASTGen(input,expect,368))
    def test_expression28(self):
        '''testing precedence with LP exp RP'''
        input ="""
        void main() {
            5 * (c * (d * e / a[2])) * f;
        }     """
        expect = "Program([FuncDecl(Id(main),[],VoidType,Block([BinaryOp(*,BinaryOp(*,IntLiteral(5),BinaryOp(*,Id(c),BinaryOp(/,BinaryOp(*,Id(d),Id(e)),ArrayCell(Id(a),IntLiteral(2))))),Id(f))]))])"
        self.assertTrue(TestAST.checkASTGen(input,expect,369))
    def test_expression29(self):
        '''testing invocation expression'''
        input ="""
        void main() {
            int a; 
            foo(foo(1*2), t-2, !3);
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("a",IntType()),CallExpr(Id("foo"),[CallExpr(Id("foo"),[BinaryOp("*",IntLiteral(1),IntLiteral(2))]),BinaryOp("-",Id("t"),IntLiteral(2)),UnaryOp("!",IntLiteral(3))])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,370))
    def test_expression30(self):
        '''testing invocation expression'''
        input ="""
        void main() {
            int a; 
            foo((((2-5))));
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("a",IntType()),CallExpr(Id("foo"),[BinaryOp("-",IntLiteral(2),IntLiteral(5))])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,371))
    def test_expression31(self):
        '''testing invocation expression'''
        input ="""
        void main() {
            foo();
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([CallExpr(Id("foo"),[])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,372))
    def test_expression32(self):
        '''testing literal'''
        input ="""
        void main() {
            foo(1,-10E022);
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([CallExpr(Id("foo"),[IntLiteral(1),UnaryOp("-",FloatLiteral(1e+23))])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,373))
    def test_expression33(self):
        '''testing literal'''
        input ="""
        void main() {
            foo(1,-.2E02, true, false);
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([CallExpr(Id("foo"),[IntLiteral(1),UnaryOp("-",FloatLiteral(20.0)),BooleanLiteral(True),BooleanLiteral(False)])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,374))
    def test_expression34(self):
        '''testing literal'''
        input ="""
        void main() {
            foo(1,-2.E023, true, false);
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([CallExpr(Id("foo"),[IntLiteral(1),UnaryOp("-",FloatLiteral(2e+23)),BooleanLiteral(True),BooleanLiteral(False)])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,375))
    def test_expression35(self):
        '''testing literal'''
        input ="""
        void main() {
            foo(000001,-2.E023, true, false);
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([CallExpr(Id("foo"),[IntLiteral(1),UnaryOp("-",FloatLiteral(2e+23)),BooleanLiteral(True),BooleanLiteral(False)])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,376))
    def test_expression36(self):
        '''testing literal'''
        input ="""
        void main() {
            foo(000001,-2.E023, "Something here\\r\\n");
        }     """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([CallExpr(Id("foo"),[IntLiteral(1),UnaryOp("-",FloatLiteral(2e+23)),StringLiteral("Something here\\r\\n")])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,377))
    def test_everything0(self):
        '''all thing combined'''
        input ="""
        int f;
        int main() {
            do 
            {
                {
                    if (m < 2 || m > 2) return;
                    {
                        {
                            for (a%2; a; a = a > 2) {

                            }
                        }
                    }
                }
                break;
            }
            while func(x*x*x*x);        }   """
        expect = str(Program([VarDecl("f",IntType()),FuncDecl(Id("main"),[],IntType(),Block([Dowhile([Block([Block([If(BinaryOp("||",BinaryOp("<",Id("m"),IntLiteral(2)),BinaryOp(">",Id("m"),IntLiteral(2))),Return()),Block([Block([For(BinaryOp("%",Id("a"),IntLiteral(2)),Id("a"),BinaryOp("=",Id("a"),BinaryOp(">",Id("a"),IntLiteral(2))),Block([]))])])]),Break()])],CallExpr(Id("func"),[BinaryOp("*",BinaryOp("*",BinaryOp("*",Id("x"),Id("x")),Id("x")),Id("x"))]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,378))
    def test_everything1(self):
        '''all thing combined'''
        input ="""
        int f;
        void enter()
        {
            return;
        }

        void init()
        {
            if (a > 3 * (4-enter())) return; else "lol";
        }

        void print()
        {
        }

        int main()
        {
            enter();
            init();
            print();
        }"""
        expect = str(Program([VarDecl("f",IntType()),FuncDecl(Id("enter"),[],VoidType(),Block([Return()])),FuncDecl(Id("init"),[],VoidType(),Block([If(BinaryOp(">",Id("a"),BinaryOp("*",IntLiteral(3),BinaryOp("-",IntLiteral(4),CallExpr(Id("enter"),[])))),Return(),StringLiteral("lol"))])),FuncDecl(Id("print"),[],VoidType(),Block([])),FuncDecl(Id("main"),[],IntType(),Block([CallExpr(Id("enter"),[]),CallExpr(Id("init"),[]),CallExpr(Id("print"),[])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,379)) 
    def test_everything2(self):
        '''all thing combined'''
        input ="""
        int main() {
            float f;
            f = 1 > 10 * 2 || 0000.E-00000;
            string v;
            v = 2;
            int t; 
            t = "asdada";
            a = das[31231*a[3232]];
            string a[100];
            a[23=232] = !-("2131" < 10); 
        }"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([VarDecl("f",FloatType()),BinaryOp("=",Id("f"),BinaryOp("||",BinaryOp(">",IntLiteral(1),BinaryOp("*",IntLiteral(10),IntLiteral(2))),FloatLiteral(0.0))),VarDecl("v",StringType()),BinaryOp("=",Id("v"),IntLiteral(2)),VarDecl("t",IntType()),BinaryOp("=",Id("t"),StringLiteral("asdada")),BinaryOp("=",Id("a"),ArrayCell(Id("das"),BinaryOp("*",IntLiteral(31231),ArrayCell(Id("a"),IntLiteral(3232))))),VarDecl("a",ArrayType(100,StringType())),BinaryOp("=",ArrayCell(Id("a"),BinaryOp("=",IntLiteral(23),IntLiteral(232))),UnaryOp("!",UnaryOp("-",BinaryOp("<",StringLiteral("2131"),IntLiteral(10)))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,380)) 
    def test_everything3(self):
        '''all thing combined'''
        input ="""

          int main() {
            bob(2)[3 + abc + foo(2)[65 + fob(2) * 7 + (14 || 5)]];
        }"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([ArrayCell(CallExpr(Id("bob"),[IntLiteral(2)]),BinaryOp("+",BinaryOp("+",IntLiteral(3),Id("abc")),ArrayCell(CallExpr(Id("foo"),[IntLiteral(2)]),BinaryOp("+",BinaryOp("+",IntLiteral(65),BinaryOp("*",CallExpr(Id("fob"),[IntLiteral(2)]),IntLiteral(7))),BinaryOp("||",IntLiteral(14),IntLiteral(5))))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,381)) 
    def test_everything4(self):
        '''all thing combined'''
        input ="""int main() {
            int x;
            for (x = 2; x = x - 2; x = x + 1) {
                if (!t || (true || -1)) {
                    return "Satement" + "aasda" * 2;
                } else if (0) {     
                    int a;
                }
            }
            do {
            foo(2);

            } while (println("") || 3+2);
        }"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([VarDecl("x",IntType()),For(BinaryOp("=",Id("x"),IntLiteral(2)),BinaryOp("=",Id("x"),BinaryOp("-",Id("x"),IntLiteral(2))),BinaryOp("=",Id("x"),BinaryOp("+",Id("x"),IntLiteral(1))),Block([If(BinaryOp("||",UnaryOp("!",Id("t")),BinaryOp("||",BooleanLiteral(True),UnaryOp("-",IntLiteral(1)))),Block([Return(BinaryOp("+",StringLiteral("Satement"),BinaryOp("*",StringLiteral("aasda"),IntLiteral(2))))]),If(IntLiteral(0),Block([VarDecl("a",IntType())])))])),Dowhile([Block([CallExpr(Id("foo"),[IntLiteral(2)])])],BinaryOp("||",CallExpr(Id("println"),[StringLiteral("")]),BinaryOp("+",IntLiteral(3),IntLiteral(2))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,382)) 
    def test_everything6(self):
        '''all thing combined'''
        input ="""int f;
        int main() {
            for (i = 0; i < 3; (2-3+i/2)+1)
            for ("nothing"*100;i;1) {
                do do do do do t - 2 * 2; foo()[foo(300000)];
                while 1; while 1; while 1; while 1; while 1;
            }
        }"""
        expect = str(Program([VarDecl("f",IntType()),FuncDecl(Id("main"),[],IntType(),Block([For(BinaryOp("=",Id("i"),IntLiteral(0)),BinaryOp("<",Id("i"),IntLiteral(3)),BinaryOp("+",BinaryOp("+",BinaryOp("-",IntLiteral(2),IntLiteral(3)),BinaryOp("/",Id("i"),IntLiteral(2))),IntLiteral(1)),For(BinaryOp("*",StringLiteral("nothing"),IntLiteral(100)),Id("i"),IntLiteral(1),Block([Dowhile([Dowhile([Dowhile([Dowhile([Dowhile([BinaryOp("-",Id("t"),BinaryOp("*",IntLiteral(2),IntLiteral(2))),ArrayCell(CallExpr(Id("foo"),[]),CallExpr(Id("foo"),[IntLiteral(300000)]))],IntLiteral(1))],IntLiteral(1))],IntLiteral(1))],IntLiteral(1))],IntLiteral(1))])))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,383)) 
    def test_everything7(self):
        '''all thing combined'''
        input ="""int f;
        int main() {
            do 
                if (true * false)
                    do
                        return; 
                    while (9 || 2 <= foo("lit\\neral", a));
            while (1);
        }"""
        expect = str(Program([VarDecl("f",IntType()),FuncDecl(Id("main"),[],IntType(),Block([Dowhile([If(BinaryOp("*",BooleanLiteral(True),BooleanLiteral(False)),Dowhile([Return()],BinaryOp("||",IntLiteral(9),BinaryOp("<=",IntLiteral(2),CallExpr(Id("foo"),[StringLiteral("lit\\neral"),Id("a")])))))],IntLiteral(1))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,384)) 
    def test_everything8(self):
        '''all thing combined'''
        input ="""int f;
        int main() {
            do 
                if (true * false)
                    do
                        return 2 * (3 || 5) % c - f(); 
                    while (9 || 2 <= foo("lit\\neral", a));
            while (1);
        }"""
        expect = str(Program([VarDecl("f",IntType()),FuncDecl(Id("main"),[],IntType(),Block([Dowhile([If(BinaryOp("*",BooleanLiteral(True),BooleanLiteral(False)),Dowhile([Return(BinaryOp("-",BinaryOp("%",BinaryOp("*",IntLiteral(2),BinaryOp("||",IntLiteral(3),IntLiteral(5))),Id("c")),CallExpr(Id("f"),[])))],BinaryOp("||",IntLiteral(9),BinaryOp("<=",IntLiteral(2),CallExpr(Id("foo"),[StringLiteral("lit\\neral"),Id("a")])))))],IntLiteral(1))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,385)) 
    def test_everything9(self):
        '''all thing combined'''
        input ="""int f;
        float[] main(string m[], int xxx) {
    
        }
        int a, b, c[5];
        void nothing(){
            if (-!-!!!3) {
    
            }
            else if (5 || 2) if (m) 
            m[3!=2*foo(123 && false)["haha"]];
            else return true;
        }"""
        expect = str(Program([VarDecl("f",IntType()),FuncDecl(Id("main"),[VarDecl("m",ArrayPointerType(StringType())),VarDecl("xxx",IntType())],ArrayPointerType(FloatType()),Block([])),VarDecl("a",IntType()),VarDecl("b",IntType()),VarDecl("c",ArrayType(5,IntType())),FuncDecl(Id("nothing"),[],VoidType(),Block([If(UnaryOp("-",UnaryOp("!",UnaryOp("-",UnaryOp("!",UnaryOp("!",UnaryOp("!",IntLiteral(3))))))),Block([]),If(BinaryOp("||",IntLiteral(5),IntLiteral(2)),If(Id("m"),ArrayCell(Id("m"),BinaryOp("!=",IntLiteral(3),BinaryOp("*",IntLiteral(2),ArrayCell(CallExpr(Id("foo"),[BinaryOp("&&",IntLiteral(123),BooleanLiteral(False))]),StringLiteral("haha"))))),Return(BooleanLiteral(True)))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,386)) 
    def test_everything10(self):
        '''all thing combined'''
        input ="""int f;
        float[] main(string m[], int xxx) {
    
        }
        int a, b, c[5];
        void nothing(){
            continue; return !3= 2-5+4 * 2 || 100 == 5 >= 8;
        }"""
        expect = str(Program([VarDecl("f",IntType()),FuncDecl(Id("main"),[VarDecl("m",ArrayPointerType(StringType())),VarDecl("xxx",IntType())],ArrayPointerType(FloatType()),Block([])),VarDecl("a",IntType()),VarDecl("b",IntType()),VarDecl("c",ArrayType(5,IntType())),FuncDecl(Id("nothing"),[],VoidType(),Block([Continue(),Return(BinaryOp("=",UnaryOp("!",IntLiteral(3)),BinaryOp("||",BinaryOp("+",BinaryOp("-",IntLiteral(2),IntLiteral(5)),BinaryOp("*",IntLiteral(4),IntLiteral(2))),BinaryOp("==",IntLiteral(100),BinaryOp(">=",IntLiteral(5),IntLiteral(8))))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,387)) 
    def test_everything11(self):
        '''all thing combined'''
        input ="""int f;
        float[] main(string m[], int xxx) {
            for (1;2;3) for(4;5;6) for(foo(foo()+3); !3= 2-5+4 * 2 || 100 == 5 >= 8; 10+1) for (something; a[2*foo()]; 9=(5=4-3)) {
                
            }
        }
        int a, b, c[5];
        void nothing(){
            
        }"""
        expect = "Program([VarDecl(f,IntType),FuncDecl(Id(main),[VarDecl(m,ArrayTypePointer(StringType)),VarDecl(xxx,IntType)],ArrayTypePointer(FloatType),Block([For(IntLiteral(1);IntLiteral(2);IntLiteral(3);For(IntLiteral(4);IntLiteral(5);IntLiteral(6);For(CallExpr(Id(foo),[BinaryOp(+,CallExpr(Id(foo),[]),IntLiteral(3))]);BinaryOp(=,UnaryOp(!,IntLiteral(3)),BinaryOp(||,BinaryOp(+,BinaryOp(-,IntLiteral(2),IntLiteral(5)),BinaryOp(*,IntLiteral(4),IntLiteral(2))),BinaryOp(==,IntLiteral(100),BinaryOp(>=,IntLiteral(5),IntLiteral(8)))));BinaryOp(+,IntLiteral(10),IntLiteral(1));For(Id(something);ArrayCell(Id(a),BinaryOp(*,IntLiteral(2),CallExpr(Id(foo),[])));BinaryOp(=,IntLiteral(9),BinaryOp(=,IntLiteral(5),BinaryOp(-,IntLiteral(4),IntLiteral(3))));Block([])))))])),VarDecl(a,IntType),VarDecl(b,IntType),VarDecl(c,ArrayType(IntType,5)),FuncDecl(Id(nothing),[],VoidType,Block([]))])"
        self.assertTrue(TestAST.checkASTGen(input,expect,388)) 
    def test_everything12(self):
        '''all thing combined'''
        input ="""int f;
        void main() {
            (((1)));
        }
        void nothing(){
           show(); 
        }
        """
        expect = str(Program([VarDecl("f",IntType()),FuncDecl(Id("main"),[],VoidType(),Block([IntLiteral(1)])),FuncDecl(Id("nothing"),[],VoidType(),Block([CallExpr(Id("show"),[])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,389)) 
    def test_everything13(self):
        '''all thing combined'''
        input ="""int f;
        void main() {
            if (((1))) do {
                do do do a + 3; foo(3)[2*foo()];
                while (!-3.2*1000); while false; while "1231313131\\n\\f\\r";
            } while true;
        }
        void nothing(){
           show((show()*10-2.E20),3); 
        }
        """
        expect =str(Program([VarDecl("f",IntType()),FuncDecl(Id("main"),[],VoidType(),Block([If(IntLiteral(1),Dowhile([Block([Dowhile([Dowhile([Dowhile([BinaryOp("+",Id("a"),IntLiteral(3)),ArrayCell(CallExpr(Id("foo"),[IntLiteral(3)]),BinaryOp("*",IntLiteral(2),CallExpr(Id("foo"),[])))],BinaryOp("*",UnaryOp("!",UnaryOp("-",FloatLiteral(3.2))),IntLiteral(1000)))],BooleanLiteral(False))],StringLiteral("1231313131\\n\\f\\r"))])],BooleanLiteral(True)))])),FuncDecl(Id("nothing"),[],VoidType(),Block([CallExpr(Id("show"),[BinaryOp("-",BinaryOp("*",CallExpr(Id("show"),[]),IntLiteral(10)),FloatLiteral(2e+20)),IntLiteral(3)])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,390))
    def test_everything14(self):
        '''all thing combined'''
        input ="""int f;
        void main() {
            a + 5 + 6 * 100-foo(9999999,8 && (false-"hysterial")) = 4 = (something + 3) / 2 % 100 || 3 != 2 = -10E12;
        }
        """
        expect = str(Program([VarDecl("f",IntType()),FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",BinaryOp("-",BinaryOp("+",BinaryOp("+",Id("a"),IntLiteral(5)),BinaryOp("*",IntLiteral(6),IntLiteral(100))),CallExpr(Id("foo"),[IntLiteral(9999999),BinaryOp("&&",IntLiteral(8),BinaryOp("-",BooleanLiteral(False),StringLiteral("hysterial")))])),BinaryOp("=",IntLiteral(4),BinaryOp("=",BinaryOp("||",BinaryOp("%",BinaryOp("/",BinaryOp("+",Id("something"),IntLiteral(3)),IntLiteral(2)),IntLiteral(100)),BinaryOp("!=",IntLiteral(3),IntLiteral(2))),UnaryOp("-",FloatLiteral(10000000000000.0)))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,391))
    def test_everything15(self):
        '''all thing combined'''
        input ="""
        void main() {
            int a;
            do a+3; if (a * 2 + f[3])
            if (a < 4) a = 10; else a = foo(3, a[5], !4);
            for (i = 2; i < 10; i = i + 1) { }
            while (foo());
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("a",IntType()),Dowhile([BinaryOp("+",Id("a"),IntLiteral(3)),If(BinaryOp("+",BinaryOp("*",Id("a"),IntLiteral(2)),ArrayCell(Id("f"),IntLiteral(3))),If(BinaryOp("<",Id("a"),IntLiteral(4)),BinaryOp("=",Id("a"),IntLiteral(10)),BinaryOp("=",Id("a"),CallExpr(Id("foo"),[IntLiteral(3),ArrayCell(Id("a"),IntLiteral(5)),UnaryOp("!",IntLiteral(4))])))),For(BinaryOp("=",Id("i"),IntLiteral(2)),BinaryOp("<",Id("i"),IntLiteral(10)),BinaryOp("=",Id("i"),BinaryOp("+",Id("i"),IntLiteral(1))),Block([]))],CallExpr(Id("foo"),[]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,392))
    def test_everything16(self):
        '''all thing combined'''
        input ="""
            void foo() {
            a > 3------------!4;
        }
        """
        expect = str(Program([FuncDecl(Id("foo"),[],VoidType(),Block([BinaryOp(">",Id("a"),BinaryOp("-",IntLiteral(3),UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("!",IntLiteral(4)))))))))))))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,394))
    def test_everything17(self):
        '''all thing combined'''
        input ="""
            void foo() {
            {
                int a, b, c;
                a=2;
                float f[5];
                if (a == b) f[0] = 1.0;
            }
        }
        """
        expect = str(Program([FuncDecl(Id("foo"),[],VoidType(),Block([Block([VarDecl("a",IntType()),VarDecl("b",IntType()),VarDecl("c",IntType()),BinaryOp("=",Id("a"),IntLiteral(2)),VarDecl("f",ArrayType(5,FloatType())),If(BinaryOp("==",Id("a"),Id("b")),BinaryOp("=",ArrayCell(Id("f"),IntLiteral(0)),FloatLiteral(1.0)))])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,395))
    def test_everything18(self):
        '''all thing combined'''
        input ="""
            void foo() {
            {
                a[a[5*4 + foo(a[5])]];
            }
        }
        """
        expect = str(Program([FuncDecl(Id("foo"),[],VoidType(),Block([Block([ArrayCell(Id("a"),ArrayCell(Id("a"),BinaryOp("+",BinaryOp("*",IntLiteral(5),IntLiteral(4)),CallExpr(Id("foo"),[ArrayCell(Id("a"),IntLiteral(5))]))))])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,396))
    def test_everything19(self):
        '''all thing combined'''
        input ="""
            void main() {
            int a;
            if (a > 3 && a < 5)
            if (a < 4) a = 10; else a = foo(3, a[5], !4);
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("a",IntType()),If(BinaryOp("&&",BinaryOp(">",Id("a"),IntLiteral(3)),BinaryOp("<",Id("a"),IntLiteral(5))),If(BinaryOp("<",Id("a"),IntLiteral(4)),BinaryOp("=",Id("a"),IntLiteral(10)),BinaryOp("=",Id("a"),CallExpr(Id("foo"),[IntLiteral(3),ArrayCell(Id("a"),IntLiteral(5)),UnaryOp("!",IntLiteral(4))]))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,397))
    def test_everything20(self):
        '''all thing combined'''
        input ="""
             void main() {
            int a;
            if (a > 3 && a < 5) 
            if (a < 4) a = 10; else a = foo(3, a[5], !4);
        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("a",IntType()),If(BinaryOp("&&",BinaryOp(">",Id("a"),IntLiteral(3)),BinaryOp("<",Id("a"),IntLiteral(5))),If(BinaryOp("<",Id("a"),IntLiteral(4)),BinaryOp("=",Id("a"),IntLiteral(10)),BinaryOp("=",Id("a"),CallExpr(Id("foo"),[IntLiteral(3),ArrayCell(Id("a"),IntLiteral(5)),UnaryOp("!",IntLiteral(4))]))))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,398))
    def test_everything21(self):
        '''all thing combined'''
        input ="""
            void main() {
            int a;
            if (a > 3) {
                a >= 4;
            }

        }
        """
        expect = str(Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("a",IntType()),If(BinaryOp(">",Id("a"),IntLiteral(3)),Block([BinaryOp(">=",Id("a"),IntLiteral(4))]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,399))

    