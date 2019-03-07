#!/usr/bin/env python3
import sys
import time
from subprocess import call

class Test:

    def __init__(self, function, name, show_time, show_color):
        self.function = function
        self.name = name
        self.result = None
        self.show_time = show_time
        self.show_color = show_color

    def run(self):
        try:
            self.function()
            self.result = True
        except:
            self.result = False

    def report(self):
        time_before = time.time()
        self.run()
        time_after = time.time()
        if self.show_color:
            if self.result:
                output = "[\033[32mpassed\033[39m] : {}".format(self.name)
            else:
                output = "[\033[31mfailed\033[39m] : {}".format(self.name)
        else:
            if self.result:
                output = "[passed] : {}".format(self.name)
            else:
                output = "[failed] : {}".format(self.name)
        if self.show_time:
            output += " ({} sec)".format(time_after - time_before)
        print(output)
        return self.result

def write_header(outfile):
    outfile.write("#!/usr/bin/env python3\n")
    outfile.write("import luky, sys, os\n")

def write_import_path(path, outfile):
    if '/' in path:
        directories = path[:-3].split('/')[:-1]
        imported_path = ','.join(["'{}'".format(directory) for directory in directories])
        import_line = "sys.path.append(os.path.join(os.path.dirname(__file__), {}))\n".format(imported_path)
        outfile.write(import_line)
        return path[:-3].split('/')[-1]
    return path[:-3]


def write_test_file(path, outfile, show_time, hide_color):
    functions_names = get_test_functions_names(path)
    imported_file_name = write_import_path(path, outfile)
    line = "from {} import ".format(imported_file_name)
    size = len(functions_names)
    if size > 0:
        for i in range(size - 1):
            line += "{}, ".format(functions_names[i])
        line += "{}\n".format(functions_names[size - 1])
        outfile.write(line)

        outfile.write("tests_passed = 0\n")
        for function in functions_names:
            outfile.write("tests_passed += luky.Test({0}, \"{0}\", {1}, {2}).report()\n"
                          .format(function, show_time, not hide_color))
        outfile.write("print(\"Tests passed:\", tests_passed, \"/ {}\")\n".format(size))

def get_name(line):
    """
    Return the name of the function
    that is defined in the line

    Every function that we are getting the name
    do not have argument.
    This is why to take for 4 to -4
        4: for the 'def '
        -4: for the '():'
    """
    return line[4:-4]

def get_test_functions_names(path):
    functions_names = []
    test_file = open(path, "r")
    lines = test_file.readlines()
    i = 0
    while i < len(lines):
        if lines[i][:7] == "#[test]":
            i += 1
            while i < len(lines) and lines[i][:3] != "def":
                i += 1
            if i != len(lines) and lines[i][:3] == "def":
                functions_names.append(get_name(lines[i]))
        i += 1
    test_file.close()
    return functions_names

def display_help():
    print("######################## LUKY ########################\n")
    print("Usage:")
    print("\t ./luky.py tests_file.py other_tests_file.py\n")
    print("Arguments:")
    print("-t or --time: Displays the execution time of each test")
    print("--no-color: Do not show 'passed' and 'failed' in color")
    print("-h or --help: Displays this help\n\n")

def main():
    if len(sys.argv) == 1:
        print("Bad Argument\n")
        display_help()
        return
    else:
        show_time = False
        hide_color = False
        show_help = False
        paths = sys.argv[1:] # We get all the arguments
        for path in paths:
            # Checking if the files are Python files
            if path == "--time" or path == "-t":
                show_time = True
            elif path == "--no-color":
                hide_color = True
            elif path == "-h" or path == "--help":
                show_help = True
            elif len(path) <= 3 or path[-3:] != ".py":
                print("Bad Argument: The file must end by '.py'")
                print("Run with -h or --help to see the help")
                return
    if show_help:
        display_help()
    else:
        outfile = open(".out.py", "a")
        write_header(outfile)
        for path in paths:
            if path not in ["-t", "--time", "--no-color", "-h", "--help"]:
                outfile.write("print(\"---------- {} ----------\")\n".format(path))
                write_test_file(path, outfile, show_time, hide_color)
        outfile.close()
        call(["python3", "-B", ".out.py"])
        call(["rm", ".out.py"])

if __name__ == "__main__":
    main()
