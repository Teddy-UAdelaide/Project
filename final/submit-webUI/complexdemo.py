import re


def main():
    java_code = """
    public class Main {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
            int result = add(1, 2);
            System.out.println(result);

            if (result > 0) {
                System.out.println("Positive");
            } else if (result == 0) {
                System.out.println("Zero");
            } else {
                System.out.println("Negative");
            }

            for (int i = 0; i < 10; i++) {
                System.out.println(i);
            }

            int j = 0;
            while (j < 5) {
                System.out.println(j);
                j++;
            }

            int k = 0;
              do {
                System.out.println(k);
                k++;
            } while (k < 3);
        }

        public static int add(int a, int b) {
            return a + b;
        }
    }
    """
    python_code = convert_java_to_python(java_code)
    print(python_code)


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
        if method_name == "main" and "String[] args" in params:
            line = "if __name__ == '__main__':"
        else:
            line = f'def {method_name}({params}):'
        return line

    # convert if statement
    line = re.sub(r'\bif\s*\((.*?)\)\s*\{?', r'if \1:', line)
    # convert else if statement
    line = re.sub(r'\belse if\s*\((.*?)\)\s*\{?', r'elif \1:', line)

    # convert else statement
    line = re.sub(r'\belse\s*\{?', r'else:', line)

    # convert the for loop
    for_match = re.match(r'\bfor\s*\((\w+\s+\w+)\s*=\s*(\d+);\s*(\w+)\s*<\s*(\d+);\s*(\w+\+)\)\s*\{?', line)
    if for_match:
        var_def, start, var, end, _ = for_match.groups()
        line = f"{var_def}\nfor {var} in range({start}, {end}):"
        return line

    # Transform the while loop
    line = re.sub(r'\bwhile\s*\((.*?)\)\s*\{?', r'while \1:', line)

    # convert do-while loop
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

    # convert try statement
    if line.startswith("try {"):
        line = "try:"
        return line

    # convert catch statement
    catch_match = re.match(r'catch\s*\((.*?)\)\s*\{?', line)
    if catch_match:
        exception = catch_match.group(1).split()[-1]
        line = f"except {exception}:"
        return line

    # convert finally statement
    if line.startswith("finally {"):
        line = "finally:"
        return line
    # convert switch statement
    global switch_var
    switch_var = None
    switch_match = re.match(r'switch\s*\((.*?)\)\s*\{?', line)
    if switch_match:
        switch_var = switch_match.group(1)
        line = f'switch_{switch_var} = {switch_var}\n'
        return line

    # convert case statement
    case_match = re.match(r'case\s+(.*?):', line)
    if case_match:
        case_value = case_match.group(1)
        line = f'if switch_{switch_var} == {case_value}:'
        return line

    # convert default statement
    if line.startswith('default:'):
        line = f'else:'
        return line

    # Call the remove_unnecessary_symbols function here
    line = remove_unnecessary_symbols(line)
    return line if line else None


def remove_unnecessary_symbols(line):
    line = line.rstrip(' {')
    line = line.rstrip(';')
    return line


if __name__ == 'main':
    main()
