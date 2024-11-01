import re

FILENAME = "invalidboilerbones" + ".txt"

BOILERPLATE = ["file;", "text;", "barebones;", "code;", "public class barebonesProgram;", "public static void main();", "{", "}", "endmain;", "endclass;", "endcode;", "endbarebones;", "endtext;", "endfile;"]

variables = {}
funcs = {}

line_no = 0

def clean(code):
    global funcs
    code = remove_boiler_plate(code)
    comment_lines = []
    clean_code = []
    code_line = code.pop(0)
    while code_line[:-1] != 'endfunctions;':
        if code_line.split()[0] == "func":
            func_name = code_line.split()[1][:-1]
            func_code = []
            func_line = code.pop(0)
            while func_line[:-1] != "endfunc;":
                func_line = func_line.replace("\n", "")
                func_line = func_line.replace("   ", "")
                func_code.append(func_line)
                func_line = code.pop(0)
            funcs[func_name] = func_code
        code_line = code.pop(0)

    for i in range(len(code)):
        if "#" not in code[i][0]:
            code[i] = code[i].replace("\n", "")
            code[i] = code[i].replace("   ", "")
            if code[i].split()[0] == "call":
                for line in funcs[code[i].split()[1][:-1]]:
                    clean_code.append(line)
            else:
                clean_code.append(code[i])
    print(clean_code)
    return clean_code

def remove_boiler_plate(code):
    for i in range(7):
        x = code.pop(0)[:-1]
        y = code.pop()[:-1]
        if x == BOILERPLATE[i] and y == BOILERPLATE[(i + 1) * -1]:
            pass
        else:
            break
    else:
        return code
    with open(FILENAME, "w") as f:
        f.write("")
    raise SyntaxError("INVALID BOILERPLATE, DELETING SOURCE CODE")




def get_arg(code_line, while_flag=False, set_flag=False):
    if while_flag:
        return code_line.split()[1]
    elif set_flag:
        broken_down_line = code_line.split()
        args = (broken_down_line[1], broken_down_line[2][:-1])
        return args
    else:
        return code_line.split()[1][:-1]


def clear(variable_name):
    variables[variable_name] = 0

def incr(variable_name):
    try:
        variables[variable_name] += 1
    except KeyError:
        pass

def decr(variable_name):
    try:
        variables[variable_name] -= 1
    except KeyError:
        pass

def set(vars):
    if vars[1] in variables.keys():
        variables[vars[0]] = variables[vars[1]]
    elif re.sub("[a-zA-Z]+[0-9]*[+*-/][a-zA-Z]+[0-9]*", "MATCH", vars[1]):
        variables[vars[0]] = arithmetic(vars[1])

def arithmetic(statement):
    if "+" in statement:
        args = statement.split("+")
        return variables[args[0]] + variables[args[1]]
    elif "-" in statement:
        args = statement.split("-")
        return variables[args[0]] - variables[args[1]]
    elif "*" in statement:
        args = statement.split("*")
        return variables[args[0]] * variables[args[1]]
    elif "/" in statement:
        args = statement.split("/")
        return variables[args[0]] // variables[args[1]]


def check_while_condition(arg):
    if variables[arg] != 0:
        return True
    else:
        return False

def track_forward():
    global line_no
    depth = 1
    while depth > 0:
        line_no += 1
        if code[line_no] == "end;":
            depth -= 1
        elif re.sub("while .+ not 0 do;", "MATCH", code[line_no]) == "MATCH":
            depth += 1

def track_backward():
    global line_no
    depth = 1
    while depth > 0:
        line_no -= 1
        if code[line_no] == "end;":
            depth += 1
        elif re.sub("while .+ not 0 do;", "MATCH", code[line_no]) == "MATCH":
            depth -= 1
    line_no -= 1

def debug(variable_name):
    print(variables[variable_name])


def read_code():
    with open(FILENAME, "r") as f:
        code = clean(f.readlines())
    return code

def print_vars():
    for key in variables.keys():
        print(f"{key}: {variables[key]}")





def main():
    global code, line_no
    code = read_code()
    while True:
        try:
            line = code[line_no]
            for command in VALID_COMMANDS.keys():
                if re.sub(command, "MATCH", line) == "MATCH":
                    if command == "while [a-zA-Z]+[0-9]* not 0 do;":
                        if check_while_condition(get_arg(line, while_flag=True)):
                            pass
                        else:
                            track_forward()
                        break
                    elif command == "set [a-zA-Z]+[0-9]* [^ ]+;":
                        VALID_COMMANDS[command](get_arg(line, set_flag=True))
                        break
                    elif command == "end;":
                        track_backward()
                        break
                    else:
                        VALID_COMMANDS[command](get_arg(line))
                        break
            else:
                raise SyntaxError(f'line {line_no}: {code[line_no]}')
            line_no += 1
        except IndexError:
            break
    print_vars()






VALID_COMMANDS = {"clear [a-zA-Z]+[0-9]*;": clear,
                  "incr [a-zA-Z]+[0-9]*;": incr,
                  "decr [a-zA-Z]+[0-9]*;": decr,
                  "set [a-zA-Z]+[0-9]* [^ ]+;": set,
                  "[a-zA-Z]+[0-9]*[+*-/][a-zA-Z]+[0-9]*": arithmetic,
                  "while [a-zA-Z]+[0-9]* not 0 do;": None,
                  "debug [a-zA-Z]+[0-9]*;": debug,
                  "end;": None
                  }

if __name__ == "__main__":
    main()
