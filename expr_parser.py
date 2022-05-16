import enum
from typing import TypeVar
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

    def tokenize(self):
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
            ty = TokenKind.MODULO
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


def get_op_priority(op: TokenKind) -> int:
    if op == TokenKind.DOUBLE_STAR:
        return 2
    if op == TokenKind.STAR or op == TokenKind.SLASH or op == TokenKind.MODULO:
        return 1
    if op == TokenKind.PLUS or op == TokenKind.MINUS:
        return 0
    assert False, "unknown operator"


def token_to_binary_op(kind: TokenKind) -> BinaryOperator:
    if kind == TokenKind.PLUS:
        return BinaryOperator.ADD
    if kind == TokenKind.MINUS:
        return BinaryOperator.SUB
    if kind == TokenKind.STAR:
        return BinaryOperator.MUL
    if kind == TokenKind.SLASH:
        return BinaryOperator.DIV
    if kind == TokenKind.MODULO:
        return BinaryOperator.REM
    if kind == TokenKind.DOUBLE_STAR:
        return BinaryOperator.POWER
    assert False, "unknown token kind -> operator"


def token_to_unary_op(kind: TokenKind) -> UnaryOperator:
    if kind == TokenKind.SQRT:
        return UnaryOperator.SQRT
    assert False, "unknown token kind -> operator"


class ExpressionParser:
    def __init__(self, expression: str, variables: dict, big_number_type=BigNum):
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
        expr = self.parse()
        return expr

    def parse(self) -> Expr:
        return self.parse_precedence(self.parse_expr(), 0)

    def parse_expr(self) -> Expr:
        tok = self.eat()
        if tok.kind == TokenKind.NUMBER:
            return NumericExpr(self.big_number_type(self.original_text[tok.loc.start:tok.loc.end]))
        if tok.kind == TokenKind.OPEN_PAREN:
            expr = self.parse()
            if self.eat().kind != TokenKind.CLOSED_PAREN:
                raise ValueError("expected )")
            return expr
        if tok.kind == TokenKind.SQRT:
            subexpression = self.parse_expr()
            op = token_to_unary_op(tok.kind)
            return UnaryExpr(op, subexpression)
        if tok.kind == TokenKind.VARIABLE:
            return VariableExpr(self.original_text[tok.loc.start:tok.loc.end])
        assert False, "unknown token"

    def parse_precedence(self, left, min_priority) -> Expr:
        lookahead = self.peek()
        while not self.precedence_expr_is_done() and get_op_priority(lookahead.kind) >= min_priority:
            op = self.eat()
            right = self.parse_expr()

            lookahead = self.peek()
            while not self.precedence_expr_is_done() and get_op_priority(lookahead.kind) > get_op_priority(op.kind):
                right = self.parse_precedence(right, min_priority + 1)
                lookahead = self.peek()

            binary_operator = token_to_binary_op(op.kind)
            left = BinaryExpr(left, binary_operator, right)
        return left

    def peek(self) -> Token:
        assert self.offset < len(self.tokens), "can't peek when stream already terminated"
        return self.tokens[self.offset]

    def eat(self) -> Token:
        assert self.offset < len(self.tokens), "can't eat when stream already terminated"
        self.offset += 1
        return self.tokens[self.offset - 1]

    def next_is_end(self) -> bool:
        return self.peek().kind == TokenKind.END

    def precedence_expr_is_done(self):
        return self.next_is_end() or self.peek().kind == TokenKind.CLOSED_PAREN


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
                return self.solve_normal(expr.subexpression, variables).sqrt()
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


def expr_solve(expr: Expr, variables: dict, big_number_type=BigNum):
    result = str(expr.dump()) + '\n'
    while not isinstance(expr, NumericExpr):
        expr = Solver(big_number_type).solve_leftmost(expr, variables)
        result += str(expr.dump()) + '\n'
    if isinstance(expr, NumericExpr):
        return result, expr.value
    assert False, "unreachable"
