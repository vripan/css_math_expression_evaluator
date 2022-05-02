import enum
import unittest
from typing import List, TypeVar
from bignum import BigNum

T = TypeVar('T')


class TokenKind(enum.IntEnum):
    NUMBER = 0
    PLUS = 1
    MINUS = 2
    STAR = 3
    SLASH = 4
    DOUBLE_STAR = 5
    SQRT = 6
    MODULO = 7
    VARIABLE = 8
    OPEN_PAREN = 9
    CLOSED_PAREN = 10
    END = 11


def is_operator(text: str):
    return text in ['+', '-', '*', '/', '%']


class SourceLocation:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __repr__(self):
        return str(self.__dict__)


class Token:
    def __init__(self, kind: TokenKind, loc: SourceLocation = 0):
        self.kind = kind
        self.loc = loc

    def __repr__(self):
        return str(self.__dict__)


class ExpressionTokenizer:
    def __init__(self, source: str):
        self.source = source
        self.offset = 0
        self.tokens = []

    def tokenize(self) -> list[Token]:
        while self.offset < len(self.source):
            first = self.source[self.offset]

            if first.isnumeric():
                self.tokenize_number()
            elif first.isspace():
                self.offset += 1
            elif first.isalpha():
                self.tokenize_variable()
            elif is_operator(first):
                self.tokenize_operator()
            elif first == '(' or first == ')':
                ty = TokenKind.OPEN_PAREN if first == '(' else TokenKind.CLOSED_PAREN
                token = Token(ty, SourceLocation(self.offset, self.offset + 1))
                self.tokens.append(token)
                self.offset += 1
            else:
                raise ValueError("unknown token")

        self.tokens.append(Token(TokenKind.END, SourceLocation(self.offset, self.offset)))
        return self.tokens

    def tokenize_number(self):
        start = self.offset
        while self.offset < len(self.source):
            if not self.source[self.offset].isnumeric():
                break
            self.offset += 1

        token = Token(TokenKind.NUMBER, SourceLocation(start, self.offset))
        self.tokens.append(token)

    def tokenize_variable(self):
        start = self.offset
        while self.offset < len(self.source):
            if not self.source[self.offset].isalpha():
                break
            self.offset += 1

        ty = TokenKind.SQRT if self.source[start:self.offset] == 'sqrt' else TokenKind.VARIABLE
        token = Token(ty, SourceLocation(start, self.offset))
        self.tokens.append(token)

    def tokenize_operator(self):
        if self.source[self.offset:].startswith("**"):
            token = Token(TokenKind.DOUBLE_STAR, SourceLocation(self.offset, self.offset + 2))
            self.offset += 2
            self.tokens.append(token)
            return

        op = self.source[self.offset]
        if op == '+':
            ty = TokenKind.PLUS
        elif op == '-':
            ty = TokenKind.MINUS
        elif op == '*':
            ty = TokenKind.STAR
        elif op == '/':
            ty = TokenKind.SLASH
        elif op == '%':
            ty = TokenKind.PERCENT
        else:
            assert False, "unknown operator"

        token = Token(ty, SourceLocation(self.offset, self.offset + 1))
        self.offset += 1
        self.tokens.append(token)


class Expr:
    def dump(self):
        assert False, "unreachable"


class NumericExpr(Expr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.__dict__)

    def dump(self) -> str:
        return str(self.value)


class BinaryOperator(enum.IntEnum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    POWER = 4
    REM = 5

    def __str__(self):
        if self == BinaryOperator.ADD:
            return '+'
        if self == BinaryOperator.SUB:
            return '-'
        if self == BinaryOperator.MUL:
            return '*'
        if self == BinaryOperator.DIV:
            return '/'
        if self == BinaryOperator.REM:
            return '%'
        if self == BinaryOperator.POWER:
            return '**'
        assert False, "unknown binary operator"


class BinaryExpr(Expr):
    def __init__(self, left: Expr, op: BinaryOperator, right: Expr):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return str(self.__dict__)

    def dump(self, parens=True) -> str:
        result = f'{self.left.dump()} {str(self.op)} {self.right.dump()}'
        if parens:
            result = f'({result})'
        return result


class UnaryOperator(enum.IntEnum):
    SQRT = 0

    def __str__(self):
        if self == UnaryOperator.SQRT:
            return 'sqrt'
        assert False, "unknown unary operator"


class UnaryExpr(Expr):
    def __init__(self, op: UnaryOperator, subexpression: Expr):
        self.op = op
        self.subexpression = subexpression

    def __repr__(self):
        return str(self.__dict__)

    def dump(self) -> str:
        result = f'{str(self.op)} {self.subexpression.dump()}'
        return result


class VariableExpr(Expr):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def __repr__(self):
        return str(self.__dict__)

    def dump(self) -> str:
        result = f'{self.variable_name}'
        return result


class LiteralError(BaseException):
    pass


class Literal:
    def __init__(self, parts):
        self.parts = parts

    @staticmethod
    def parse_literal(tokens):
        assert False, "unreachable"


class Grammar:
    def __init__(self, productions):
        self.productions = productions


class ParseError(BaseException):
    pass


class Parser:
    def __init__(self, grammar: Grammar, start: int):
        self.grammar = grammar
        self.start = start

    def parse(self, tokens: List[Token]):
        start_symbol, _ = self.grammar.productions[self.start]
        lst = self._parse_prod(start_symbol, tokens)
        return start_symbol.parse_literal(lst)

    def _parse_prod(self, product, tokens):
        rules = None
        for prod, r in self.grammar.productions:
            if prod == product:
                rules = r
                break
        assert rules is not None, "could not find rules for symbol"

        for rule in rules:
            aux_tokens = tokens.copy()
            try:
                for i, t in enumerate(rule):
                    if isinstance(t, Token):
                        if isinstance(tokens[i], Token) and t.kind == tokens[i].kind:
                            continue
                        raise LiteralError

                    # if non literal
                    tokens = self._parse_prod(t, tokens)

                    tokens = t.parse_literal(tokens)  # todo: parse literal must be static
                return tokens
            except LiteralError:
                tokens = aux_tokens
                continue
            except IndexError:
                tokens = aux_tokens
                continue

        # if not found alternative, error
        raise ParseError


class ProductActuallyValue(Literal):
    def __init__(self, parts):
        Literal.__init__(self, parts)

    @staticmethod
    def parse_literal(tokens):
        if isinstance(tokens[0], Token) or tokens[0].kind != TokenKind.NUMBER:
            raise LiteralError
        val = ProductActuallyValue([tokens[0]])
        tokens = tokens[1:]
        tokens.insert(0, val)
        return tokens


class Sum(Literal):
    def __init__(self, parts):
        Literal.__init__(self, parts)

    @staticmethod
    def parse_literal(tokens):
        if not isinstance(tokens[0], ProductActuallyValue):
            raise Literal
        new_t = [tokens[0]]
        tokens = tokens[1:]
        while len(tokens) >= 2:
            op = tokens[0]
            prd = tokens[1]
            if not isinstance(op, Token) or (op.kind != TokenKind.PLUS and op.kind != TokenKind.MINUS):
                raise Literal
            if not isinstance(prd, ProductActuallyValue):
                raise Literal
            tokens = tokens[2:]
            new_t.append(op)
            new_t.append(prd)
        tokens.insert(0, Sum(new_t))
        return tokens


class Expr(Literal):
    def __init__(self, parts):
        Literal.__init__(self, parts)

    @staticmethod
    def parse_literal(tokens):
        if len(tokens) != 1 or not isinstance(tokens[0], Sum):
            raise LiteralError
        return [Expr(tokens)]


class ExpressionParser(Parser):
    grammar = Grammar([
        [Expr, [
            [Sum]
        ]],
        [Sum, [
            [ProductActuallyValue],
            [ProductActuallyValue, Token(TokenKind.PLUS), ProductActuallyValue],
            [ProductActuallyValue, Token(TokenKind.MINUS), ProductActuallyValue]
        ]],
        [ProductActuallyValue, [
            [Token(TokenKind.NUMBER)]
        ]]
    ])

    def __init__(self, expression: str, variables: dict, big_number_type=BigNum):
        Parser.__init__(self, self.grammar, 0)

        assert big_number_type is not None
        assert big_number_type.__add__ is not None
        assert big_number_type.__sub__ is not None
        assert big_number_type.__mul__ is not None
        assert big_number_type.__floordiv__ is not None
        assert big_number_type.__mod__ is not None
        assert big_number_type.__pow__ is not None
        assert len(expression) > 0, "expression can't be empty"

        self.original_text = expression
        self.vars = variables
        self.tokens = []
        self.offset = 0
        self.big_number_type = big_number_type

    def run(self):
        self.tokens = ExpressionTokenizer(self.original_text).tokenize()
        expr = self.parse(self.tokens)
        return expr


class Solver:
    def __init__(self, big_number_type):
        self.has_reached_leftmost = False
        self.big_number_type = big_number_type

    def solve_normal(self, expr: Expr, variables: dict):
        if isinstance(expr, BinaryExpr):
            left = self.solve_normal(expr.left, variables)
            right = self.solve_normal(expr.right, variables)

            if expr.op == BinaryOperator.ADD:
                result = left + right
            elif expr.op == BinaryOperator.SUB:
                if left < right:
                    raise ValueError(f"{left}-{right} would result in negative number")
                result = left - right
            elif expr.op == BinaryOperator.MUL:
                result = left * right
            elif expr.op == BinaryOperator.DIV:
                if right == self.big_number_type(0):
                    raise ValueError("can't divide by 0")
                result = left // right
            elif expr.op == BinaryOperator.POWER:
                result = left ** right
            elif expr.op == BinaryOperator.REM:
                if right == self.big_number_type(0):
                    raise ValueError("can't divide by 0")
                result = left % right
            else:
                assert False, "unknown operator"
            return result
        elif isinstance(expr, UnaryExpr):
            if expr.op == UnaryOperator.SQRT:
                return self.solve_normal(expr.subexpression, variables) ** (1 / 2)
            else:
                assert False, "unknown operator"
        elif isinstance(expr, VariableExpr):
            return variables[expr.variable_name]
        elif isinstance(expr, NumericExpr):
            return expr.value
        else:
            assert False, "unknown node type"

    def solve_leftmost(self, expr: Expr, variables: dict) -> Expr:
        is_leftmost_binary = not self.has_reached_leftmost and isinstance(expr, BinaryExpr) \
                             and isinstance(expr.left, NumericExpr) and isinstance(expr.right, NumericExpr)

        is_leftmost_unary = not self.has_reached_leftmost and isinstance(expr, UnaryExpr) and isinstance(
            expr.subexpression, NumericExpr)
        is_leftmost_variable = not self.has_reached_leftmost and isinstance(expr, VariableExpr)

        if is_leftmost_binary or is_leftmost_unary or is_leftmost_variable:
            self.has_reached_leftmost = True
            return NumericExpr(self.solve_normal(expr, variables))

        if isinstance(expr, BinaryExpr):
            left = self.solve_leftmost(expr.left, variables)
            right = self.solve_leftmost(expr.right, variables)
            return BinaryExpr(left, expr.op, right)
        elif isinstance(expr, UnaryExpr):
            subexpression = self.solve_leftmost(expr.subexpression, variables)
            return UnaryExpr(expr.op, subexpression)
        elif isinstance(expr, VariableExpr):
            return expr
        if isinstance(expr, NumericExpr):
            return expr
        assert False, "unknown node type"


def solve(original_text: str, expr: Expr, variables: dict, big_number_type=BigNum):
    result = ""
    while not isinstance(expr, NumericExpr):
        expr = Solver(big_number_type).solve_leftmost(expr, variables)
        result += str(expr.dump()) + '\n'
    if isinstance(expr, NumericExpr):
        return result, expr.value
    assert False, "unreachable"


def run_one(text: str, variables: dict, big_number_type=BigNum):
    expr = ExpressionParser(text, variables, big_number_type).run()
    (string, result) = solve(text, expr, variables, big_number_type)
    string = text + '\n' + str(expr.dump()) + '\n' + string + '\n'
    print(string)
    return result


class TestCases(unittest.TestCase):
    def test_rem(self):
        with_big = run_one("5 % 2 + 0", {})
        with_int = run_one("5 % 2 + 0", {}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 1)

    def test_unknown_token(self):
        with self.assertRaises(Exception):
            run_one("```x - 1", {"x": BigNum(0)})

    def test_missing_paren(self):
        with self.assertRaises(Exception):
            run_one("(x - 1", {})

    def test_sub_negative(self):
        with self.assertRaises(Exception):
            run_one("x - 1", {"x": BigNum(0)})

    def test_div_0(self):
        with self.assertRaises(Exception):
            run_one("2 / x", {"x": BigNum(0)})
        with self.assertRaises(Exception):
            run_one("2 % x", {"x": BigNum(0)})

    def test_complex(self):
        with_big = run_one("2 ** (1 + 2 * x - 3 / sqrt y)", {"x": BigNum(2), "y": BigNum(9)})
        with_int = int(run_one("2 ** (1 + 2 * x - 3 / sqrt y)", {"x": int(2), "y": int(9)}, int))
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 16)

    def test_vars(self):
        with_big = run_one("(x * 2 + y * z) ** t",
                           {"x": BigNum(2), "y": BigNum(3), "z": BigNum(4), "t": BigNum(2)})
        with_int = run_one("(x * 2 + y * z) ** t",
                           {"x": int(2), "y": int(3), "z": int(4), "t": int(2)}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_big, 256)

    def test_sqrt(self):
        with_big = run_one("sqrt 9 + sqrt 4", {})
        with_int = int(run_one("sqrt 9 + sqrt 4", {}, int))
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 5)

    def test_special(self):
        with_big = run_one("2 ** 3 + 5 * 6 - 3", {})
        with_int = run_one("2 ** 3 + 5 * 6 - 3", {}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 35)

    def test_basic(self):
        with_big = run_one("1 + 2 * 3 + 4 * 5", {})
        with_int = run_one("1 + 2 * 3 + 4 * 5", {}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 27)

    def test_parens(self):
        with_big = run_one("(1 + 2) * (3 + 4 * 5)", {})
        with_int = run_one("(1 + 2) * (3 + 4 * 5)", {}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 69)

    def test_super_basic(self):
        with_big = run_one("1 + 1", {})
        with_int = run_one("1 - 2", {}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 2)


if __name__ == "__main__":
    unittest.main()
