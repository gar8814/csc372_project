# SNFL
Read below for the documentation of our language. If you are still having issues after going through the steps, please contact our group.
## Using SNFL
1. Have a file that ends in `.snfl` extension
2. From the command line, run the command `python src/snfl_interpreter.py [your program].snfl`

### Troubleshooting
* *`python` doesn't exist?* Try `python3` in your command instead.
* *`ply` not found?* Run either `pip install ply` or `pip3 install ply`
* To use debug mode, add `-d` to the end of the python run command to see more verbose output

## Variable declaration
`<identifier> is <value>`
### Examples
`juliet is 10`

`hello is "Hello World"`
## Operations
`<op>(<val1>, <val2>)`

### Operators
`add`, `sub`, `mult`, `div`, `mod`

### Examples
`add(1, 2)`

`c is add(a, b)`

`c is div(e,b)`

## if statements
```
if (<condition>) {
    <code>
} else {
    <code>
}
```
### Example
```
if (basicGt) {
    relResult is "Greater than check passed " 
} else {
    relResult is "Greater than check failed " 
}
```

## while loops
```
while (<condition>) {
    <code>
}
```
### Example
```
while (gte(count, 1)) {
    count is sub(count, 1)
}
```

## Comments
Uses `//`
### Example
`// This is a comment`
