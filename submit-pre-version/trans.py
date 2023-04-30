import re


def convert_java_to_python(java_code):
    java_code = remove_comments(java_code)
    java_lines = java_code.split('\n')
    python_code = ''
    indent = 0
    for line in java_lines:
        line = line.strip()

        if '}' in line:
            indent -= 1
            line = line.replace('}', '')

        python_line = convert_java_line_to_python(line)
        if python_line:
            python_code += '    ' * indent + python_line + '\n'

        if '{' in line:
            line = line.replace('{', '')
            indent += 1

    return python_code


def remove_comments(java_code):
    return re.sub(r'(//.*?$|/\*.*?\*/)', '', java_code, flags=re.MULTILINE | re.DOTALL)


def convert_java_line_to_python(line):
    line = line.strip()

    # Convert System.out.println to print
    line = re.sub(r'System\.out\.print(ln)?\s*\(', 'print(', line)

    # Convert basic data types
    line = re.sub(r'\bint\b', 'int', line)
    line = re.sub(r'\bfloat\b', 'float', line)
    line = re.sub(r'\bdouble\b', 'float', line)
    line = re.sub(r'\bboolean\b', 'bool', line)

    # Convert class definition
    class_match = re.match(r'public class (\w+)', line)
    if class_match:
        class_name = class_match.group(1)
        line = f'class {class_name}:'
        return line

    # Conversion method definition
    method_match = re.match(
        r'(public|private|protected)?\s*(static)?\s*(\w+)\s+(\w+)\s*\((.*)\)\s*\{?', line
    )
    if method_match:
        return_type, method_name, params = method_match.group(3, 4, 5)
        params = re.sub(r'\w+\s+(\w+)', r'\1', params)
        line = f'def {method_name}({params}):'
        return line

    # Transform the if statement
    line = re.sub(r'\bif\s*\((.*?)\)\s*\{?', r'if \1:', line)
    # Convert else if statement
    line = re.sub(r'\bif\s*\((.*?)\)\s*\{?', r'if \1:', line)

    # Convert else statement
    line = re.sub(r'\belse\s*\{?', r'else:', line)

    # Transform the for loop
    for_match = re.match(r'\bfor\s*\((.*?);\s*(.*?);\s*(.*?)\)\s*\{?', line)
    if for_match:
        init, cond, update = for_match.group(1, 2, 3)
        line = f'{init}\nwhile {cond}:\n    ' + '{'
        return line + f'\n    {update}'

    # Convert while loop
    line = re.sub(r'\bwhile\s*\((.*?)\)\s*\{?', r'while \1:', line)

    # Transform do-while loops
    do_while_match = re.match(r'\bdo\s*\{?', line)
    if do_while_match:
        line = 'while True:'
        return line

    # Handle the conditional judgment of the do-while loop
    do_while_cond_match = re.match(r'\bwhile\s*\((.*?)\)\s*;', line)
    if do_while_cond_match:
        condition = do_while_cond_match.group(1)
        line = f'    if not {condition}: break'
        return line

    # Call the remove_unnecessary_symbols function here
    line = remove_unnecessary_symbols(line)
    return line if line else None


def remove_unnecessary_symbols(line):
    line = line.rstrip(' {')
    line = line.rstrip(';')
    return line

