import subprocess
import sys
import time
from collections import defaultdict

def write_type_plain(count):
    with open('Test.java', 'w') as f:
        f.write("public class Test {\n");
        f.write("public <")
        for i in range(count):
            if i > 0:
                f.write(", ")
            f.write("A" + str(i + 1))
        f.write("> void testMethod() {}")
        f.write("}")
        
def write_type_compact(count):
    with open('Test.java', 'w') as f:
        f.write("public class Test {\n")
        f.write("public <")
        for i in range(count):
            if (i > 0):
                f.write(", ")
            f.write(type_var(i))
        f.write("> void testMethod() {}")
        f.write("}")

def write_type_compact_extends(count):
    with open('Test.java', 'w') as f:
        f.write("public class Test {\n")
        f.write("public <")
        for i in range(count):
            if (i > 0):
                f.write(", ")
            s = type_var(i)
            f.write(s)
            if (s != 'A'):
                f.write(" extends A")
        f.write("> void testMethod() {}")
        f.write("}")
        
substitutes = {
    'if': 'À',
    'do': 'Á'
}
        
def type_var(i):
    type_var_chars = [to_id_letter(i % 53)]
    remainder = i // 53
    while (remainder > 0):
        type_var_chars.append(to_id_char(remainder % 64))
        remainder = remainder // 64
    type_var = ''.join(type_var_chars)
    if type_var in substitutes:
        return substitutes[type_var]
    return type_var
        
def to_id_letter(i):
    if i < 26:
        return chr(65 + i)
    elif i < 52:
        return chr(97 + i - 26)
    else:
        return "$"

def to_id_char(i):
    if i < 52:
        return to_id_letter(i)
    elif i < 62:
        return str(i - 52)
    elif i == 63:
        return "_"
    else:
        return "$"

def find_max(f):
    failed = False
    largest_success = 8
    target = 8
    smallest_failure = sys.maxsize
    
    while largest_success + 1 < smallest_failure:
        if not failed:
            target = largest_success * 2
        else:
            target = (largest_success + smallest_failure) // 2
        f(target)
        status = subprocess.call(["javac", "/home/justin/code/typecount/Test.java"])
        if status is not 0:
            failed = True
            smallest_failure = target
        else:
            largest_success = target
    return largest_success

if __name__ == "__main__":
    print("largest type: ", find_max(write_type_plain))
    print("compact identifiers: ", find_max(write_type_compact))
    print("with extends:", find_max(write_type_compact_extends))
