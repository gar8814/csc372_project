import re
import sys

# Regex patterns for parsing
assign_pat = re.compile(r"^\s*(\w+)\s*is\s*(.+?)\s*\.$", re.IGNORECASE)

def translate_expr(expr):
    expr = expr.strip()
    try:
        if expr.startswith("add("):
            return translate_op_expr(expr, 'add', '+')
        elif expr.startswith("sub("):
            return translate_op_expr(expr, 'sub', '-')
        elif expr.startswith("div("):
            return translate_op_expr(expr, 'div', '/')
        elif expr.startswith("mult("):
            return translate_op_expr(expr, 'mult', '*')
        elif expr.startswith("mod("):
            return translate_op_expr(expr, 'mod', '%')
        elif expr.startswith("and("):
            return translate_op_expr(expr, 'and', 'and')
        elif expr.startswith("or("):
            return translate_op_expr(expr, 'or', 'or')
        elif expr.startswith("not("):
            return "not " + translate_expr(expr[4:-1])
        elif expr.startswith("gt("):
            return translate_op_expr(expr, 'gt', '>')
        elif expr.startswith("lt("):
            return translate_op_expr(expr, 'lt', '<')
        elif expr.startswith("gte("):
            return translate_op_expr(expr, 'gte', '>=')
        elif expr.startswith("lte("):
            return translate_op_expr(expr, 'lte', '<=')
        elif expr.startswith("eq("):
            return translate_op_expr(expr, 'eq', '==')
        elif expr.isdigit():
            return expr
        elif expr.replace('.', '', 1).isdigit():
            return expr
        elif expr[0] == '"' and expr[-1] == '"':
            return expr
        elif expr.lower() in ["true", "false"]:
            return expr.lower()
        else:
            return expr  # variable name
    except Exception as e:
        print(f"Error translating expression '{expr}': {str(e)}", file=sys.stderr)
        return None

def translate_op_expr(expr, func_name, op):
    args = expr[len(func_name) + 1:-1]
    arg1, arg2 = map(translate_expr, args.split(','))
    return f"({arg1} {op} {arg2})"

def translate_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            match = assign_pat.match(line)
            if match:
                var_name = match.group(1)
                expr = match.group(2)
                py_expr = translate_expr(expr)
                if py_expr is not None:
                    py_line = f"{var_name} = {py_expr}\n"
                    outfile.write(py_line)
                else:
                    outfile.write(f"# Failed to translate: {line}\n")
            else:
                outfile.write(f"# Unrecognized line: {line}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python trans.py <inputfile> <outputfile>", file=sys.stderr)
        sys.exit(1)
    input_file, output_file = sys.argv[1], sys.argv[2]
    translate_file(input_file, output_file)
    print("Translation completed successfully.")
