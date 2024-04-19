import re
import sys

assign_pat = re.compile(r"^\s*(\w+)\s*is\s*(.+?)\s*\.$", re.IGNORECASE)
cond_pattern = re.compile(r"^\s*If\s*\((.+?)\)\s*\{(.+?)\}\s*else\s*\{(.+?)\}\s*$", re.IGNORECASE | re.DOTALL)

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

##################added for conditional
def translate_conditional(expr, if_code, else_code):
    condition = translate_expr(expr.strip())
    translated_if_block = translate_code_block(if_code, "    ")
    translated_else_block = translate_code_block(else_code, "    ")
    return f"if {condition}:\n{translated_if_block}else:\n{translated_else_block}"

def translate_code_block(code, indent=""):
    translated_code = ""
    lines = code.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if "If" in line:  
            block, j = extract_block(lines, i)
            i = j  
            cond_match = cond_pattern.match(block)
            if cond_match:
                expr, if_code, else_code = cond_match.groups()
                translated_conditional_block = translate_conditional(expr, if_code, else_code)
                translated_code += f"{indent}{translated_conditional_block}\n"
            else:
                translated_code += f"{indent}# Failed to parse block: {block}\n"
        else:
            match = assign_pat.match(line)
            if match:
                var_name = match.group(1)
                expr = match.group(2)
                py_expr = translate_expr(expr)
                if py_expr is not None:
                    translated_code += f"{indent}{var_name} = {py_expr}\n"
                else:
                    translated_code += f"{indent}# Failed to translate: {line}\n"
            else:
                translated_code += f"{indent}# Unrecognized line: {line}\n"
            i += 1
    return translated_code

def extract_block(lines, start_index):
    #To find end of block
    end_index = start_index + 1 
    return "\n".join(lines[start_index:end_index]), end_index
#####################


def translate_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            ###############added for conditional
            condional_matched = cond_pattern.match(line)
            if condional_matched:
                expr, if_block, else_block = condional_matched.groups()
                translated_conditional_block = translate_conditional(expr, if_block, else_block)
                outfile.write(translated_conditional_block + "\n")
            ###############added for condtional
            else:
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
