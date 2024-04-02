'''
The Python equivalent of the Parser.java file. 

Example input:

>> int x = 5.
<type>: int
<var>: x
<var_dec>: int x
<var_dec_list>: int x
<int>: 5
<val>: 5
<val_list>: 5

<var_assign>: int x = 5.
<stmt>
'''

import re

var_assign_pat = re.compile("^(.+) = (.+)\.$")
type_var_dec_pat = re.compile("^(\\w+) (\\w+)$")
type_pat = re.compile("^int|bool$")
int_val_pat = re.compile("^\\d+$")
var_pat = re.compile("^\\w+$")
bool_pat = re.compile("^t$|^f$")

def main():
    while True:
        cmd = input(">> ")
        if cmd == "exit":
            break
        parseCmd(cmd)

def parseCmd(cmd):
    varAssign(cmd)
    print("<stmt>")

def varAssign(cmd):
    m = var_assign_pat.match(cmd)
    match = False
    if m:
        match = True
        match = match and varDecList(m.group(1))
        match = match and valList(m.group(2))
    printMsg(match, "\n<var_assign>", cmd, "variable assignment statement")
    return match

def varDec(cmd):
    m = type_var_dec_pat.match(cmd)
    match = False
    if m:
        match = True
        match = match and type(m.group(1))
        match = match and var(m.group(2))
    else:
        match = var(cmd)
    printMsg(match, "<var_dec>", cmd, "variable declaration")
    return match

def valList(cmd):
    split = cmd.split(", ")
    match = True
    for i in range(len(split)):
        match = match and val(split[i])
    printMsg(match, "<val_list>", cmd, "value list")
    return match

def printMsg(match, nt_name, cmd, item):
    if match:
        print(f"{nt_name}: {cmd}")
    else:
        print(f"Failed to parse: {{cmd}} is not a valid {item}.")

def val(cmd):
    m = int_val_pat.search(cmd)
    match = bool(m)
    if match:
        printMsg(match, "<int>", cmd, "integer")
    else:
        m = bool_pat.search(cmd)
        match = bool(m)
        if match:
            printMsg(match, "<bool>", cmd, "boolean")
        else:
            m = var_pat.search(cmd)
            match = bool_pat(m)
            if match:
                printMsg(match, "<var>", cmd, "variable")

    printMsg(match, "<val>", cmd, "value")
    return match

def valList(cmd):
    split = cmd.split(", ")
    match = True
    for s in split:
        match = match and val(s)
    printMsg(match, "<val_list>", cmd, "value list")
    return match

def varDecList(cmd):
    split = cmd.split(", ")
    match = True
    for i in range(len(split)):
        match = match and varDec(split[i])
    printMsg(match, "<var_dec_list>", cmd, "variable declaration list")
    return match

def type(cmd):
    m = type_pat.search(cmd)
    match = bool(m)
    printMsg(match, "<type>", cmd, "type")
    return match

def var(cmd):
    m = var_pat.search(cmd)
    match = bool(m)
    printMsg(match, "<var>", cmd, "variable")
    return match

if __name__ == "__main__":
    main()