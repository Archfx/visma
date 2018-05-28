"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module's basic purpose is to be able to tokenize every possible input given by the user into a consistent key-value pair format for each equation/expression. Redundant data has been provided with the tokens on purpose, to make the job of future developers easier.
Still far from perfect and requires a bit of clean up.
Note: Please try to maintain proper documentation
-1 -> power
-2 -> value
-3 -> sqrt expression
-4 -> sqrt power
Logic Description:
"""

# TODO: Add token formation for tan, sin, cos, cot, sec, cosec and log
import math
import copy
from visma.functions.structure import Function, Equation, Expression
from visma.functions.variable import Variable, Constant
from visma.functions.operator import Binary, Sqrt

symbols = ['+', '-', '*', '/', '(', ')', '{', '}', '[', ']', '^', '=']
greek = [u'\u03B1', u'\u03B2', u'\u03B3']
constants = [u'\u03C0', 'e', 'i']
# inputLaTeX = ['\\times', '\\div', '\\alpha', '\\beta', '\\gamma', '\\pi', '+', '-', '=', '^', '\\sqrt']
# inputGreek = ['*', '/', u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0', '+', '-', '=', '^', 'Sqrt']
# TODO: Add latex input support
inputLaTeX = ['\\times', '\\div', '+', '-', '=', '^', '\\sqrt']
inputGreek = ['*', '/', '+', '-', '=', '^', 'Sqrt']

words = ['tan', 'Sqrt', 'sin', 'sec', 'cos', 'cosec', 'log', 'cot', 'sinh', 'cosh']


def is_variable(term):
    """Checks if given term is variable

    Args:
        term: a term of equation

    Returns:
        True: if term is variable
        False: otherwise
    """
    if term in greek:
        return True
    elif (term[0] >= 'a' and term[0] <= 'z') or (term[0] >= 'A' and term[0] <= 'Z'):
        x = 0
        while x < len(term):
            if term[x] < 'A' or (term[x] > 'Z' and term[x] < 'a') or term[x] > 'z':
                return False
            x += 1
        return True


def is_number(term):
    if isinstance(term, int) or isinstance(term, float):
        return True
    else:
        x = 0
        dot = 0
        if term[0] == '-':
            x += 1
            while x < len(term):
                if (term[x] < '0' or term[x] > '9') and (dot != 0 or term[x] != '.'):
                    return False
                if term[x] == '.':
                    dot += 1
                x += 1
            if x >= 2:
                return True
            else:
                return False
        else:
            while x < len(term):
                if (term[x] < '0' or term[x] > '9') and (dot != 0 or term[x] != '.'):
                    return False
                if term[x] == '.':
                    dot += 1
                x += 1
        return True


def get_num(term):
    return float(term)


def remove_spaces(eqn):
    """
    Gets rid of whitespaces from the input equation
    """
    cleanEqn = ''
    for char in eqn:
        if char != ' ':
            cleanEqn += char
    return cleanEqn


def get_terms(eqn):
    """Separate terms of the input equation into a list

    Args:
        eqn: Input equation

    Returns
        terms: List of terms
    """
    x = 0
    terms = []
    while x < len(eqn):
        if (eqn[x] >= 'a' and eqn[x] <= 'z') or (eqn[x] >= 'A' and eqn[x] <= 'Z') or eqn[x] in greek:
            if eqn[x] == 's':
                i = x
                buf = eqn[x]
                while (i - x) < len("qrt"):
                    i += 1
                    if i < len(eqn):
                        buf += eqn[i]
                if buf == 'Sqrt':
                    terms.append(buf)
                    x = i + 1
                    continue

                i = x
                buf = eqn[x]
                while (i - x) < len("in"):
                    i += 1
                    if i < len(eqn):
                        buf += eqn[i]
                if buf == "sin":
                    if buf + eqn[i+1] == "sinh":
                        terms.append(buf + eqn[i+1])
                        x = i + 2
                        continue
                    else:
                        terms.append(buf)
                        x = i + 1
                        continue

                i = x
                buf = eqn[x]
                while (i - x) < len("ec"):
                    i += 1
                    if i < len(eqn):
                        buf += eqn[i]
                if buf == "sec":
                    terms.append(buf)
                    x = i + 1
                    continue

                terms.append(eqn[x])

            elif eqn[x] == 'l':
                i = x
                buf = eqn[x]
                while (i - x) < len("og"):
                    i += 1
                    if i < len(eqn):
                        buf += eqn[i]
                if buf == "log":
                    terms.append(buf)
                    x = i + 1
                    continue
                terms.append(eqn[x])

            elif eqn[x] == 'e':
                terms.append('exp')

            elif eqn[x] == 'i':
                terms.append('iota')

            elif eqn[x] == 't':
                i = x
                buf = eqn[x]
                while (i - x) < len("an"):
                    i += 1
                    if i < len(eqn):
                        buf += eqn[i]
                if buf == "tan":
                    terms.append(buf)
                    x = i + 1
                    continue
                terms.append(eqn[x])

            elif eqn[x] == 'c':
                i = x
                buf = eqn[x]
                while (i - x) < len("osec"):
                    i += 1
                    if i < len(eqn):
                        buf += eqn[i]
                if buf == "cosec":
                    terms.append(buf)
                    x = i + 1
                    continue

                i = x
                buf = eqn[x]
                while (i - x) < len("os"):
                    i += 1
                    if i < len(eqn):
                        buf += eqn[i]
                if buf == "cos":
                    if buf + eqn[i+1] == "cosh":
                        terms.append(buf + eqn[i+1])
                        x = i + 2
                        continue
                    else:
                        terms.append(buf)
                        x = i + 1
                        continue

                i = x
                buf = eqn[x]
                while (i - x) < len("ot"):
                    i += 1
                    if i < len(eqn):
                        buf += eqn[i]
                if buf == "cot":
                    terms.append(buf)
                    x = i + 1
                    continue

                terms.append(eqn[x])

            else:
                terms.append(eqn[x])
            x += 1
        elif eqn[x] == '\\':
            buf = '\\'
            x += 1
            while x < len(terms):
                if (eqn[x] >= 'a' and eqn[x] <= 'z') or (eqn[x] >= 'A' and eqn[x] <= 'Z'):
                    buf += eqn[x]
                    x += 1
            terms.append(buf)
        elif eqn[x] >= '0' and eqn[x] <= '9':
            buf = ''
            buf = eqn[x]
            x += 1
            dot = 0
            while x < len(eqn):
                if (eqn[x] >= '0' and eqn[x] <= '9'):
                    buf += eqn[x]
                    x += 1
                elif eqn[x] == '.':
                    if dot == 0:
                        buf += eqn[x]
                        dot += 1
                        x += 1
                    else:
                        break
                else:
                    break
            terms.append(buf)
        elif eqn[x] in symbols:
            terms.append(eqn[x])
            x += 1
        else:
            x += 1
    return terms


def normalize(terms):
    """
    Change input from Latex to Greek
    """
    for term in terms:
        for i, x in enumerate(inputLaTeX):
            if x == term:
                term = inputGreek[i]
    return terms


def tokenize_symbols(terms):
    """Assigns a token to each term in terms list
    """
    symTokens = []
    for i, term in enumerate(terms):
        symTokens.append('')
        if term in symbols:
            if term == '*' or term == '/':
                if (is_variable(terms[i - 1]) or is_number(terms[i - 1]) or terms[i - 1] == ')') and (is_variable(terms[i + 1]) or is_number(terms[i + 1]) or terms[i + 1] == '(' or ((terms[i + 1] == '-' or terms[i + 1] == '+') and (is_variable(terms[i + 2]) or is_number(terms[i + 2])))):
                    symTokens[-1] = 'Binary'
            elif term == '+' or term == '-':
                if i == 0:
                    symTokens[-1] = 'Unary'
                elif terms[i - 1] in ['-', '+', '*', '/', '=', '^', '(']:
                    symTokens[-1] = 'Unary'
                elif (is_variable(terms[i - 1]) or is_number(terms[i - 1]) or terms[i - 1] == ')' or terms[i - 1] == ')') and (is_variable(terms[i + 1]) or is_number(terms[i + 1]) or terms[i + 1] == '(' or terms[i + 1] in words or ((terms[i + 1] == '-' or terms[i + 1] == '+') and (is_variable(terms[i + 2]) or is_number(terms[i + 2]) or terms[i + 2] in words))):
                    symTokens[-1] = 'Binary'
                else:
                    # pass
                    print(terms[i - 1], terms[i], is_number(terms[i + 1]))
            elif term == '=':
                symTokens[-1] = 'Binary'
        elif term == 'Sqrt':
            symTokens[-1] = 'Sqrt'
    return symTokens


def check_negative_number(terms, symTokens):
    for i, symToken in enumerate(symTokens):
        if symToken == 'Unary':
            if is_number(terms[i + 1]) and i + 1 < len(terms):
                terms[i + 1] = terms[i] + terms[i + 1]
            terms.pop(i)
            symTokens.pop(i)
    return terms, symTokens


def check_equation(terms, symTokens):
    brackets = 0
    sqrBrackets = 0
    equators = 0
    for i, term in enumerate(terms):
        if term == '(':
            brackets += 1
        elif term == ')':
            brackets -= 1
            if brackets < 0:
                return False
        # TODO: logger.log("Too many ')'")
        elif term == '[':
            sqrBrackets += 1
        elif term == ']':
            sqrBrackets -= 1
            if sqrBrackets < 0:
                return False
        # TODO: logger.log("Too many ']'")
        elif term == '^':
            if symTokens[i + 1] == 'Binary':
                return False
        # TODO: logger.log("Check around '^'")
        elif is_variable(term) or is_number(term):
            if i + 1 < len(terms):
                if terms[i + 1] == '(':
                    return False
        elif term == '>' or term == '<':
            if terms[i+1] != '=':
                equators += 1
            if equators > 1:
                return False
        elif term == '=':
            equators += 1
            if equators > 1:
                return False
        # TODO: logger.log("Inappropriate number of equator(=,<,>)")
        elif term == ';':
            equators = 0
    if len(terms) != 0:
        i = len(terms) - 1
        if symTokens[i] == 'Binary' or symTokens[i] == 'Unary' or brackets != 0 or sqrBrackets != 0:
            return False
    return True


def get_variable(terms, symTokens, scope, coeff=1):
    # DBP: print terms
    variable = Variable()
    value = []
    coefficient = coeff
    power = []
    x = 0
    level = 0
    while x < len(terms):
        if is_variable(terms[x]):
            value.append(terms[x])
            power.append(1)
            level += 1
            x += 1
        elif is_number(terms[x]):
            if x + 1 < len(terms) and terms[x + 1] != '^':
                coefficient *= get_num(terms[x])
            else:
                value.append(get_num(terms[x]))
                power.append(1)
            level += 1
            x += 1
        elif symTokens[x] == 'Unary':
            if terms[x] == '-':
                coefficient *= -1
            x += 1
        elif terms[x] == '^':
            x += 1
            if terms[x] == '(':
                x += 1
                binary = 0
                nSqrt = 0
                varTerms = []
                varSymTokens = []
                brackets = 0
                while x < len(terms):
                    if terms[x] != ')' or brackets != 0:
                        if symTokens[x] == 'Binary':
                            if brackets == 0:
                                binary += 1
                        elif terms[x] == '(':
                            brackets += 1
                        elif terms[x] == ')':
                            brackets -= 1
                        elif symTokens[x] == 'Sqrt':
                            if brackets == 0:
                                nSqrt += 1
                        varTerms.append(terms[x])
                        varSymTokens.append(symTokens[x])
                        x += 1
                    else:
                        break
                if x + 1 < len(terms) and terms[x + 1] == '^':
                    x += 2
                    binary2 = 0
                    nSqrt2 = 0
                    brackets2 = 0
                    varSymTokens2 = []
                    varTerms2 = []
                    power2 = []
                    while x < len(terms):
                        if symTokens[x] != 'Binary' or brackets != 0:
                            if symTokens[x] == 'Binary':
                                if brackets2 == 0:
                                    binary2 += 1
                            elif terms[x] == '(':
                                brackets2 += 1
                            elif terms[x] == ')':
                                brackets2 -= 1
                            elif symTokens[x] == 'Sqrt':
                                if nSqrt2 == 0:
                                    nSqrt2 += 1
                            varTerms2.append(terms[x])
                            varSymTokens2.append(symTokens[x])
                            x += 1
                        else:
                            break
                    if len(varTerms2) == 1:
                        if is_variable(terms[x - 1]):
                            variable = Variable()
                            variable.value = [terms[x - 1]]
                            variable.power = [1]
                            variable.coefficient = 1
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tempScope.append(-1)
                            variable.scope = tempScope
                            power2.append(variable)
                        elif is_number(terms[x - 1]):
                            variable = Constant()
                            variable.value = get_num(terms[x - 1])
                            variable.power = 1
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tempScope.append(-1)
                            variable.scope = tempScope
                            power2.append(variable)
                    else:
                        if binary2 == 0 and nSqrt2 == 0:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tempScope.append(-1)
                            power2.append(get_variable(varTerms2, varSymTokens2, tempScope))
                        else:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tempScope.append(-1)
                            power2.append(get_token(varTerms2, varSymTokens2, tempScope))
                    if len(varTerms) == 1:
                        if is_variable(varTerms[-1]):
                            variable = Variable()
                            variable.value = [varTerms[-1]]
                            variable.power = power2
                            variable.coefficient = coeff
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            variable.scope = tempScope
                            power[-1] = variable
                        elif is_number(varTerms[-1]):
                            variable = Constant()
                            variable.value = get_num(varTerms[-1])
                            variable.power = power2
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            variable.scope = tempScope
                            power[-1] = variable
                    else:
                        if binary == 0 and nSqrt == 0:
                            variable = Variable()
                            variable.power = power2
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            variable.value = get_variable(varTerms, varSymTokens, tempScope)
                            variable.coefficient = 1
                            power[-1] = variable
                        else:
                            variable = Equation()
                            variable.power = power2
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            variable.value = get_token(varTerms, varSymTokens, tempScope)
                            variable.coefficient = 1
                            power[-1] = variable
                else:
                    # print varTerms, is_number(varTerms[0])
                    if len(varTerms) == 1:
                        if is_variable(varTerms[0]):
                            power[-1] = varTerms[0]
                        elif is_number(varTerms[0]):
                            power[-1] *= get_num(varTerms[0])
                    else:
                        if binary == 0 and nSqrt == 0:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            power[-1] = get_variable(varTerms,
                                                     varSymTokens, tempScope)
                        else:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            power[-1] = get_token(varTerms,
                                                  varSymTokens, tempScope)
                x += 1

            elif is_variable(terms[x]) or is_number(terms[x]):
                if x + 1 < len(terms):
                    if terms[x + 1] == '^' or is_number(terms[x]) or is_variable(terms[x]):
                        varTerms = []
                        varSymTokens = []
                        brackets = 0
                        nSqrt = 0
                        binary = 0
                        while x < len(terms):
                            if symTokens[x] != 'Binary' or brackets != 0:
                                if terms[x] == '(':
                                    brackets += 1
                                elif terms[x] == ')':
                                    brackets -= 1
                                elif symTokens[x] == 'Binary':
                                    if brackets == 0:
                                        binary += 1
                                elif symTokens[x] == 'Sqrt':
                                    if brackets == 0:
                                        nSqrt += 1
                                varTerms.append(terms[x])
                                varSymTokens.append(symTokens[x])
                                x += 1
                            else:
                                break
                        if binary != 0 or nSqrt != 0:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            power[-1] = get_token(varTerms,
                                                  varSymTokens, tempScope)
                        else:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            power[-1] = get_variable(varTerms,
                                                     varSymTokens, tempScope)

                    else:
                        if is_number(terms[x]):
                            power[-1] = get_num(terms[x])
                        else:
                            power[-1] = terms[x]
                        x += 1
                else:
                    if is_number(terms[x]):
                        power[-1] = get_num(terms[x])
                    else:
                        power[-1] = terms[x]
                    x += 1

            elif symTokens[x] == 'Unary':
                coeff = 1
                if terms[x] == '-':
                    coeff = -1
                x += 1
                if terms[x] == '(':
                    x += 1
                    binary = 0
                    varTerms = []
                    varSymTokens = []
                    brackets = 0
                    nSqrt = 0
                    while x < len(terms):
                        if terms[x] != ')' or brackets != 0:
                            if symTokens[x] == 'Binary':
                                if brackets == 0:
                                    binary += 1
                            if terms[x] == '(':
                                brackets += 1
                            elif terms[x] == ')':
                                brackets -= 1
                            elif symTokens[x] == 'Sqrt':
                                if brackets == 0:
                                    nSqrt += 1
                            varTerms.append(terms[x])
                            varSymTokens.append(symTokens[x])
                            x += 1
                        else:
                            break
                    if x + 1 < len(terms):
                        if terms[x + 1] == '^':
                            x += 2
                            binary2 = 0
                            nSqrt2 = 0
                            brackets2 = 0
                            varSymTokens2 = []
                            varTerms2 = []
                            power2 = []
                            while x < len(terms):
                                if symTokens[x] != 'Binary' or brackets != 0:
                                    if symTokens[x] == 'Binary':
                                        if brackets2 == 0:
                                            binary2 += 1
                                    elif terms[x] == '(':
                                        brackets2 += 1
                                    elif terms[x] == ')':
                                        brackets2 -= 1
                                    elif symTokens[x] == 'Sqrt':
                                        if nSqrt2 == 0:
                                            nSqrt2 += 1
                                    varTerms2.append(terms[x])
                                    varSymTokens2.append(symTokens[x])
                                    x += 1
                                else:
                                    break
                            if len(varTerms2) == 1:
                                if is_variable(terms[x - 1]):
                                    variable = Variable()
                                    variable.value = terms[x - 1]
                                    variable.power = [1]
                                    variable.coefficient = 1
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    tempScope.append(-1)
                                    variable.scope = tempScope
                                    power2.append(variable)
                                elif is_number(terms[x - 1]):
                                    variable = Constant()
                                    variable.value = get_num(terms[x - 1])
                                    variable.power = 1
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    tempScope.append(-1)
                                    variable.scope = tempScope
                                    power2.append(variable)
                            else:
                                if binary2 == 0 and nSqrt2 == 0:
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    tempScope.append(-1)
                                    power2.append(get_variable(
                                        varTerms2, varSymTokens2, tempScope))
                                else:
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    tempScope.append(-1)
                                    power2.append(
                                        get_token(varTerms2, varSymTokens2, tempScope))
                            if len(varTerms) == 1:
                                if is_variable(varTerms[-1]):
                                    variable = Variable()
                                    variable.value = [varTerms[-1]]
                                    variable.power = power2
                                    variable.coefficient = coeff
                                    power[-1] = variable
                                elif is_number(varTerms[-1]):
                                    variable = Constant()
                                    variable.value = coeff * \
                                        get_num(varTerms[-1])
                                    variable.power = power2
                                    power[-1] = variable
                            else:
                                if binary == 0 and nSqrt == 0:
                                    variable = Variable()
                                    variable.power = power2
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    variable.value = get_variable(varTerms, varSymTokens, tempScope)
                                    variable.coefficient = coeff
                                    power[-1] = variable
                                else:
                                    variable = Equation()
                                    variable.power = power2
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    variable.value = get_token(varTerms, varSymTokens, tempScope)
                                    variable.coefficient = coeff
                                    variable.type = "equation"
                                    power[-1] = variable
                        else:
                            if len(varTerms) == 1:
                                if is_variable(terms[x - 1]):
                                    variable = Variable()
                                    variable.value = [terms[x - 1]]
                                    variable.power = power2
                                    variable.coefficient = coeff
                                    power[-1] = variable
                                elif is_number(terms[x - 1]):
                                    power[-1] *= (coeff * get_num(terms[x - 1]))
                            else:
                                if binary == 0 and nSqrt == 0:
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    power[-1] = get_variable(varTerms,
                                                             varSymTokens, tempScope,  coeff)
                                else:
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    power[-1] = get_token(varTerms,
                                                          varSymTokens, tempScope, coeff)

                    else:
                        if len(varTerms) == 1:
                            if is_variable(terms[x - 1]):
                                variable = Variable()
                                variable.value = [terms[x - 1]]
                                variable.power = power2
                                variable.coefficient = coeff
                                power[-1] = variable
                            elif is_number(terms[x - 1]):
                                power[-1] *= (coeff * get_num(terms[x - 1]))
                        else:
                            if binary == 0 and nSqrt == 0:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                power[-1] = get_variable(varTerms,
                                                         varSymTokens, tempScope, coeff)
                            else:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                power[-1] = get_token(varTerms,
                                                      varSymTokens, tempScope, coeff)
                    x += 1

                elif is_variable(terms[x]) or is_number(terms[x]):

                    if x + 1 < len(terms):
                        if terms[x + 1] == '^' or is_number(terms[x]) or is_variable(terms[x]):
                            varTerms = []
                            varSymTokens = []
                            brackets = 0
                            binary = 0
                            nSqrt = 0
                            while x < len(terms):
                                if symTokens[x] != 'Binary' or brackets != 0:
                                    if terms[x] == '(':
                                        brackets += 1
                                    elif terms[x] == ')':
                                        brackets -= 1
                                    elif symTokens[x] == 'Binary':
                                        if brackets == 0:
                                            binary += 1
                                    elif symTokens[x] == 'Sqrt':
                                        if brackets == 0:
                                            nSqrt += 1
                                    varTerms.append(terms[x])
                                    varSymTokens.append(symTokens[x])
                                    x += 1
                                else:
                                    break
                            if binary != 0 or nSqrt != 0:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                power[-1] = get_token(varTerms,
                                                      varSymTokens, tempScope, coeff)
                            else:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                power[-1] = get_variable(varTerms,
                                                         varSymTokens, tempScope, coeff)

                        else:
                            if is_number(terms[x]):
                                power[-1] = get_num(terms[x])
                            else:
                                power[-1] = terms[x]
                            x += 1
                    else:
                        if is_number(terms[x]):
                            power[-1] = get_num(terms[x])
                        else:
                            power[-1] = terms[x]
                        x += 1
    variable.scope = scope
    variable.value = value
    variable.power = copy.deepcopy(power)
    variable.coefficient = coefficient
    # DBP: print terms
    # DBP: print variable.scope, variable.coefficient, variable.value, variable.power
    return variable


def get_token(terms, symTokens, scope=None, coeff=1):
    if scope is None:
        scope = []
    eqn = Expression()
    tokens = []
    x = 0
    level = 0
    while x < len(terms):
        if is_variable(terms[x]) and symTokens[x] != 'Sqrt':
            varTerms = []
            varSymTokens = []
            brackets = 0
            nSqrt = 0
            binary = 0
            while x < len(terms):
                if symTokens[x] != 'Binary' or brackets != 0:
                    if terms[x] == '(':
                        brackets += 1
                    elif terms[x] == ')':
                        brackets -= 1
                    elif symTokens[x] == 'Sqrt':
                        if brackets == 0:
                            nSqrt += 1
                    varTerms.append(terms[x])
                    varSymTokens.append(symTokens[x])
                    x += 1
                else:
                    break
            x -= 1
            tempScope = []
            tempScope.extend(scope)
            tempScope.append(level)
            if nSqrt != 0:
                variable = get_token(varTerms, varSymTokens, tempScope)
            else:
                variable = get_variable(varTerms, varSymTokens, tempScope)
            level += 1
            tokens.append(variable)
        elif is_number(terms[x]):
            if x + 1 < len(terms) and (terms[x + 1] == '^' or is_variable(terms[x + 1])):
                varTerms = []
                brackets = 0
                nSqrt = 0
                varSymTokens = []
                while x < len(terms):
                    if symTokens[x] != 'Binary' or brackets != 0:
                        if terms[x] == ')':
                            brackets += 1
                        elif terms[x] == '(':
                            brackets -= 1
                        elif symTokens == 'Sqrt':
                            nSqrt += 1
                        varTerms.append(terms[x])
                        varSymTokens.append(symTokens[x])
                    else:
                        break
                    x += 1
                x -= 1
                if nSqrt != 0:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    variable = get_token(varTerms, varSymTokens, tempScope)
                else:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    variable = get_variable(
                        varTerms, varSymTokens, tempScope)
                level += 1
                tokens.append(variable)
            else:
                variable = Constant()
                tempScope = []
                tempScope.extend(scope)
                tempScope.append(level)
                variable.scope = tempScope
                variable.power = 1
                variable.value = get_num(terms[x])
                level += 1
                tokens.append(variable)
        elif terms[x] in ['='] or symTokens[x] == 'Binary':
            operator = Binary()
            operator.value = terms[x]
            tempScope = []
            tempScope.extend(scope)
            tempScope.append(level)
            # CHECKME:
            if symTokens[x] == '':
                operator.type = "other"
            else:
                operator.type = symTokens[x]
            operator.scope = tempScope
            level += 1
            tokens.append(operator)
        elif terms[x] == '(':
            x += 1
            binary = 0
            varTerms = []
            varSymTokens = []
            brackets = 0
            nSqrt = 0
            while x < len(terms):
                if terms[x] != ')' or brackets != 0:
                    if symTokens[x] == 'Binary':
                        if brackets == 0:
                            binary += 1
                    if terms[x] == '(':
                        brackets += 1
                    elif terms[x] == ')':
                        brackets -= 1
                    elif symTokens[x] == 'Sqrt':
                        if brackets == 0:
                            nSqrt += 1
                    varTerms.append(terms[x])
                    varSymTokens.append(symTokens[x])
                    x += 1
                else:
                    break
            if x + 1 < len(terms):
                if terms[x + 1] == '^':
                    x += 2
                    binary2 = 0
                    nSqrt2 = 0
                    brackets2 = 0
                    varSymTokens2 = []
                    varTerms2 = []
                    power2 = []
                    while x < len(terms):
                        if symTokens[x] != 'Binary' or brackets2 != 0:
                            if symTokens[x] == 'Binary':
                                if brackets2 == 0:
                                    binary2 += 1
                            elif terms[x] == '(':
                                brackets2 += 1
                            elif terms[x] == ')':
                                brackets2 -= 1
                            elif symTokens[x] == 'Sqrt':
                                if nSqrt2 == 0:
                                    nSqrt2 += 1
                            varTerms2.append(terms[x])
                            varSymTokens2.append(symTokens[x])
                            x += 1
                        else:
                            break
                    if len(varTerms2) == 1:
                        if is_variable(terms[x - 1]):
                            variable = Variable()
                            variable.value = terms[x - 1]
                            variable.power = [1]
                            variable.coefficient = 1
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tempScope.append(-1)
                            variable.scope = tempScope
                            power2.append(variable)
                        elif is_number(terms[x - 1]):
                            variable = Constant
                            variable.value = get_num(terms[x - 1])
                            variable.power = 1
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tempScope.append(-1)
                            variable.scope = tempScope
                            power2.append(variable)
                    else:
                        if binary2 == 0 and nSqrt2 == 0:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tempScope.append(-1)
                            power2.append(get_variable(
                                varTerms2, varSymTokens2, tempScope))
                        else:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tempScope.append(-1)
                            power2.append(
                                get_token(varTerms2, varSymTokens2, tempScope))
                    if len(varTerms) == 1:
                        if is_variable(varTerms[-1]):
                            variable = Variable()
                            variable.value = [varTerms[-1]]
                            variable.power = power2
                            variable.coefficient = coeff
                            tokens.append(variable)
                        elif is_number(varTerms[-1]):
                            variable = Constant()
                            variable.value = coeff * get_num(varTerms[-1])
                            variable.power = power2
                            tokens.append(variable)
                    else:
                        if binary == 0 and nSqrt == 0:
                            variable = Variable()
                            variable.power = power2
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            variable.value = get_variable(
                                varTerms, varSymTokens, tempScope)
                            variable.coefficient = coeff
                            tokens.append(variable)
                        else:
                            variable = Equation()
                            variable.power = power2
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            variable.value = get_token(
                                varTerms, varSymTokens, tempScope)
                            variable.coefficient = coeff
                            tokens.append(variable)
                else:
                    if len(varTerms) == 1:
                        if is_variable(terms[x - 1]):
                            variable = Variable()
                            variable.value = [terms[x - 1]]
                            variable.power = power2
                            variable.coefficient = coeff
                            tokens.append(variable)
                        elif is_number(terms[x - 1]):
                            tokens.append(coeff * get_num(terms[x - 1]))
                    else:
                        if binary == 0 and nSqrt == 0:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tokens.append(get_variable(
                                varTerms, varSymTokens, tempScope,  coeff))
                        else:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tokens.append(
                                get_token(varTerms, varSymTokens, tempScope, coeff))

            else:
                if len(varTerms) == 1:
                    if is_variable(terms[x - 1]):
                        variable = Variable()
                        variable.value = [terms[x - 1]]
                        variable.power = power2
                        variable.coefficient = coeff
                        tokens.append(variable)
                    elif is_number(terms[x - 1]):
                        tokens.append(coeff * get_num(terms[x - 1]))
                else:
                    if binary == 0 and nSqrt == 0:
                        tempScope = []
                        tempScope.extend(scope)
                        tempScope.append(level)
                        tokens.append(get_variable(
                            varTerms, varSymTokens, tempScope, coeff))
                    else:
                        tempScope = []
                        tempScope.extend(scope)
                        tempScope.append(level)
                        tokens.append(
                            get_token(varTerms, varSymTokens, tempScope, coeff))
            level += 1
        elif symTokens[x] == 'Unary':
            coeff = 1
            if terms[x] == '-':
                coeff *= -1
            x += 1
            if terms[x] == '(':
                x += 1
                binary = 0
                varTerms = []
                varSymTokens = []
                brackets = 0
                nSqrt = 0
                while x < len(terms):
                    if terms[x] != ')' or brackets != 0:
                        if symTokens[x] == 'Binary':
                            if brackets == 0:
                                binary += 1
                        if terms[x] == '(':
                            brackets += 1
                        elif terms[x] == ')':
                            brackets -= 1
                        elif symTokens[x] == 'Sqrt':
                            if brackets == 0:
                                nSqrt += 1
                        varTerms.append(terms[x])
                        varSymTokens.append(symTokens[x])
                        x += 1
                    else:
                        break
                if x + 1 < len(terms):
                    if terms[x + 1] == '^':
                        x += 2
                        binary2 = 0
                        nSqrt2 = 0
                        brackets2 = 0
                        varSymTokens2 = []
                        varTerms2 = []
                        power2 = []
                        while x < len(terms):
                            if symTokens[x] != 'Binary' or brackets != 0:
                                if symTokens[x] == 'Binary':
                                    if brackets2 == 0:
                                        binary2 += 1
                                elif terms[x] == '(':
                                    brackets2 += 1
                                elif terms[x] == ')':
                                    brackets2 -= 1
                                elif symTokens[x] == 'Sqrt':
                                    if nSqrt2 == 0:
                                        nSqrt2 += 1
                                varTerms2.append(terms[x])
                                varSymTokens2.append(symTokens[x])
                                x += 1
                            else:
                                break
                        if len(varTerms2) == 1:
                            if is_variable(terms[x - 1]):
                                variable = Variable
                                variable.value = terms[x - 1]
                                variable.power = [1]
                                variable.coefficient = 1
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                variable.scope = tempScope
                                power2.append(variable)
                            elif is_number(terms[x - 1]):
                                variable = Constant()
                                variable.value = get_num(terms[x - 1])
                                variable.power = 1
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                variable.scope = tempScope
                                power2.append(variable)
                        else:
                            if binary2 == 0 and nSqrt2 == 0:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                power2.append(get_variable(
                                    varTerms2, varSymTokens2, tempScope))
                            else:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                power2.append(
                                    get_token(varTerms2, varSymTokens2, tempScope))
                        if len(varTerms) == 1:
                            if is_variable(varTerms[-1]):
                                variable = Variable()
                                variable.value = [varTerms[-1]]
                                variable.power = power2
                                variable.coefficient = coeff
                                tokens.append(variable)
                            elif is_number(varTerms[-1]):
                                variable = Constant
                                # CHECKME:
                                variable.value = coeff * \
                                    get_num(varTerms[-1])
                                variable.power = power2
                                tokens.append(variable)
                        else:
                            if binary == 0 and nSqrt == 0:
                                variable = Variable()
                                variable.power = power2
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                variable.value = get_variable(
                                    varTerms, varSymTokens, tempScope)
                                variable.coefficient = coeff
                                tokens.append(variable)
                            else:
                                variable = Expression()
                                variable.power = power2
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                variable.value = get_token(
                                    varTerms, varSymTokens, tempScope)
                                variable.coefficient = coeff
                                tokens.append(variable)
                    else:
                        if len(varTerms) == 1:
                            if is_variable(terms[x - 1]):
                                variable = Variable()
                                variable.value = [terms[x - 1]]
                                variable.power = power2
                                variable.coefficient = coeff
                                tokens.append(variable)
                            elif is_number(terms[x - 1]):
                                tokens.append(coeff * get_num(terms[x - 1]))
                        else:
                            if binary == 0 and nSqrt == 0:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tokens.append(get_variable(
                                    varTerms, varSymTokens, tempScope,  coeff))
                            else:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tokens.append(
                                    get_token(varTerms, varSymTokens, tempScope, coeff))

                else:
                    if len(varTerms) == 1:
                        if is_variable(terms[x - 1]):
                            variable = Variable()
                            variable.value = [terms[x - 1]]
                            variable.power = power2
                            variable.coefficient = coeff
                            tokens.append(variable)
                        elif is_number(terms[x - 1]):
                            tokens.append((coeff * get_num(terms[x - 1])))
                    else:
                        if binary == 0 and nSqrt == 0:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tokens.append(get_variable(
                                varTerms, varSymTokens, tempScope, coeff))
                        else:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tokens.append(
                                get_token(varTerms, varSymTokens, tempScope, coeff))
                x += 1
                level += 1
            elif is_variable(terms[x]):
                varTerms = []
                varSymTokens = []
                brackets = 0
                binary = 0
                nSqrt = 0
                while x < len(terms):
                    if symTokens[x] != 'Binary' or brackets != 0:
                        if terms[x] == '(':
                            brackets += 1
                        elif terms[x] == ')':
                            brackets -= 1
                        elif symTokens[x] == 'Sqrt':
                            nSqrt += 1
                        elif symTokens[x] == 'Binary':
                            if brackets == 0:
                                binary += 1
                        varTerms.append(terms[x])
                        varSymTokens.append(symTokens[x])
                        x += 1
                    else:
                        break
                x -= 1
                if nSqrt != 0 or binary != 0:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    variable = get_token(
                        varTerms, varSymTokens, tempScope, coeff)
                else:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    variable = get_variable(
                        varTerms, varSymTokens, tempScope, coeff)
                level += 1
                tokens.append(variable)

            elif is_number(terms[x]):
                if x + 1 < len(terms):
                    if terms[x + 1] == '^' or is_variable(terms[x + 1]):
                        varTerms = []
                        varSymTokens = []
                        brackets = 0
                        binary = 0
                        nSqrt = 0
                        while x < len(terms):
                            if symTokens[x] != 'Binary' or brackets != 0:
                                if terms[x] == ')':
                                    brackets += 1
                                elif terms[x] == '(':
                                    brackets -= 1
                                elif symTokens[x] == 'Sqrt':
                                    nSqrt += 1
                                elif symTokens[x] == 'Binary':
                                    if brackets == 0:
                                        binary += 1
                                varTerms.append(terms[x])
                                varSymTokens.append(symTokens[x])
                            else:
                                break
                            x += 1
                        x -= 1
                        if nSqrt != 0 or binary != 0:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            variable = get_token(
                                varTerms, varSymTokens, tempScope, coeff)
                        else:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            variable = get_variable(
                                varTerms, varSymTokens, tempScope, coeff)
                        level += 1
                        tokens.append(variable)
                    else:
                        variable = Constant()
                        variable.value = coeff * get_num(terms[x])
                        variable.power = 1
                        tempScope = []
                        tempScope.extend(scope)
                        tempScope.append(level)
                        variable.scope = tempScope
                        level += 1
                        tokens.append(variable)
                else:
                    # SIMPLIFY:
                    variable = Constant()
                    variable.value = coeff * get_num(terms[x])
                    variable.power = 1
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    variable.scope = tempScope
                    level += 1
                    tokens.append(variable)
        elif symTokens[x] == 'Sqrt':
            x += 2
            binary = 0
            brackets = 0
            sqrBrackets = 0
            nSqrt = 0
            varTerms = []
            varSymTokens = []
            while x < len(terms):
                if terms[x] != ']' or sqrBrackets != 0 or brackets != 0:
                    if terms[x] == '(':
                        brackets += 1
                    elif terms[x] == ')':
                        brackets -= 1
                    elif symTokens[x] == 'Binary':
                        binary += 1
                    elif terms[x] == '[':
                        sqrBrackets += 1
                    elif terms[x] == ']':
                        sqrBrackets -= 1
                    elif symTokens[x] == 'Sqrt':
                        nSqrt += 1
                    varTerms.append(terms[x])
                    varSymTokens.append(symTokens[x])
                    x += 1
                else:
                    break
            operator = Sqrt()
            if len(varTerms) == 1:
                if is_number(terms[x - 1]):
                    variable = Constant()
                    variable.value = get_num(terms[x - 1])
                    variable.power = 1
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(0)
                    variable.scope = tempScope
                    operator.power = variable
                elif is_variable(terms[x - 1]):
                    variable = Variable()
                    variable.value = [terms[x - 1]]
                    variable.power = [1]
                    variable.coefficient = 1
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(0)
                    variable.scope = tempScope
                    operator.power = variable
            else:
                if binary != 0 or nSqrt != 0:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(0)
                    operator.power = get_token(
                        varTerms, varSymTokens, tempScope)
                else:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(0)
                    operator.power = get_variable(
                        varTerms, varSymTokens, tempScope)
            x += 2
            binary = 0
            brackets = 0
            nSqrt = 0
            varTerms = []
            varSymTokens = []
            while x < len(terms):
                if terms[x] != ')' or brackets != 0:
                    if terms[x] == '(':
                        brackets += 1
                    elif terms[x] == ')':
                        brackets -= 1
                    elif symTokens[x] == 'Binary':
                        if brackets == 0:
                            binary += 1
                    elif symTokens[x] == 'Sqrt':
                        nSqrt += 1
                    varTerms.append(terms[x])
                    varSymTokens.append(symTokens[x])
                    x += 1
                else:
                    break
            if len(varTerms) == 1:
                if is_number(terms[x - 1]):
                    variable = Constant()
                    variable.value = get_num(terms[x - 1])
                    variable.power = 1
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(1)
                    variable.scope = tempScope
                    operator.expression = variable
                elif is_variable(terms[x - 1]):
                    variable = Variable()
                    variable.value = [terms[x - 1]]
                    variable.power = [1]
                    variable.coefficient = 1
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(1)
                    variable.scope = tempScope
                    operator.expression = variable
            else:
                if binary == 0 and nSqrt == 0:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(1)
                    operator.expression = get_variable(
                        varTerms, varSymTokens, tempScope)
                else:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(1)
                    operator.expression = get_token(
                        varTerms, varSymTokens, tempScope)
            level += 1
            tokens.append(operator)
        x += 1
    eqn.scope = scope
    eqn.coefficient = coeff
    eqn.tokens = tokens
    # DBP: print terms
    # DBP: print eqn
    return eqn


def clean(eqn):
    cleanEqn = remove_spaces(eqn)
    terms = get_terms(cleanEqn)
    normalizedTerms = normalize(terms)
    symTokens = tokenize_symbols(normalizedTerms)
    terms, symTokens = check_negative_number(normalizedTerms, symTokens)
    if check_equation(normalizedTerms, symTokens):
        tokens = get_token(normalizedTerms, symTokens)
        return tokens.tokens


def constant_variable(variable):

    constant = True

    for var in variable.value:
        if isinstance(var, Function):
            if var.__class__ == Expression:
                result, token = constant_conversion(var.tokens)
                if not result:
                    constant = False
            elif var.__class__ == Variable:
                if not constant_variable(var):
                    constant = False
        elif not is_number(var):
            constant = False

    for p in variable.power:
        if isinstance(p, Function):
            if p.__class__ == Expression:
                result, token = constant_conversion(p.tokens)
                if not result:
                    constant = False
            elif p.__class__ == Variable:
                if not constant_variable(p):
                    constant = False
        elif not is_number(p):
            constant = False

    return constant


def evaluate_constant(constant):
    if isinstance(constant, Function):
        if is_number(constant.value):
            return math.pow(constant.value, constant.power)
        elif isinstance(constant.value, list):
            val = 1
            if constant.coefficient is not None:
                val *= constant.coefficient
            for i, c_val in enumerate(constant.value):
                val *= math.pow(c_val, constant.power[i])
            return val
    elif is_number(constant):
        return constant


def constant_conversion(tokens):
    constantExpression = True
    print tokens
    for token in tokens:
        if token.__class__ == Variable():
            constant = True
            if not constant_variable(token):
                constant = False
                constantExpression = False
            if constant:
                token.__class__ = Constant
                token.value = evaluate_constant(token)
                token.power = 1

        elif token.__class__ == Binary:
            constantExpression = False

        elif token.__class__ == Expression:
            result, token = constant_conversion(token.__tokens__)
            if not result:
                constantExpression = False
    return constantExpression, tokens


def tokenizer(eqn=" {x-1} * {x+1} = x"):
    result, tokens = constant_conversion(clean(eqn))
    return tokens


def get_lhs_rhs(tokens):
    lhs = []
    rhs = []
    eqn = False
    if not isinstance(tokens, list):
        return False, False
    for token in tokens:
        if token.__class__ == Binary:
            if token.value == '=':
                eqn = True
            elif not eqn:
                lhs.append(token)
            else:
                rhs.append(token)
        elif not eqn:
            lhs.append(token)
        else:
            rhs.append(token)
    return lhs, rhs


def get_variables_value(tokens):
    variableDict = {}
    for token in tokens:
        if token.__class__ == Variable:
            variableDict[token.value[0]] = None
    return variableDict


if __name__ == "__main__":
    '''
    eqn = 'sqrt + sin(x) + sec - tan * cos / cot = cosec'
    cleanEqn = remove_spaces(eqn)
    terms = get_terms(cleanEqn)
    normalizedTerms = normalize(terms)
    symTokens = tokenize_symbols(normalizedTerms)
    terms, symTokens = check_negative_number(normalizedTerms, symTokens)
    print terms
    print	 symTokens
    '''

    print(get_lhs_rhs(tokenizer('0.2x^(2.0) + y^3 + 4z + 7.0x - 34.0 = 0')))

# -xy^22^22^-z^{s+y}^22=sqrt[x+1]{x}
# x+y=2^-{x+y}
# x + 6.00 / 3 + 2 - 2x
# x^{1} - x^{-1}
