#!/usr/bin/env python3
"""
Parser to identify tests in a file
"""
import sys
import time
from subprocess import call

# ####################################################
# Test Class
#

class Test:
    """
    Class Test {

        function: function to execute
            can contain assert,
            must not have parameters

        name: the name of the test

        result: the result of the test
            failed or passed
        show_time: bool to tell if we should print the exec time
            of the function
    }
    """

    def __init__(self, function, name, show_time, show_color):
        self.function = function
        self.name = name
        self.result = None
        self.show_time = show_time
        self.show_color = show_color


    def run(self):
        """
        Try to run the function, update the result depending of
        if the function exits successfully or not
        """
        try:
            self.function()
            self.result = True
        except:
            self.result = False
    
    def report(self):
        """
        Show a report of the execution of the function
        """
        time_before = time.time()
        self.run()
        time_after = time.time()
        output = "["
        if self.show_color:
            if self.result:
                output += "\033[32mpassed\033[39m] : {}".format(self.name)
            else:
                output += "\033[31mfailed\033[39m] : {}".format(self.name)
        else:
            if self.result:
                output += "passed] : {}".format(self.name)
            else:
                output += "failed] : {}".format(self.name)
        if self.show_time:
            output += " ({} sec)".format(time_after - time_before)

        print(output)
        return self.result

# ####################################################
# Parser Part
#

def write_header(outfile):
    """
    Erase the ex .out.py and write:
        #!/usr/bin/env python3.5
        from Luky import luky
    """
    outfile.write("#!/usr/bin/env python3.5\n")
    outfile.write("from Luky import luky\n")


def write_test_file(path, outfile, show_time, hide_color):
    """
    Write the import for the test file and the lines of the tests
    """
    functions_names = get_test_functions_names(path)
    line = "from {} import ".format(path[:-3])
    size = len(functions_names)
    if size > 0:
        for i in range(size - 1):
            line += "{}, ".format(functions_names[i])
        line += "{}\n".format(functions_names[size - 1])
        outfile.write(line)

        outfile.write("tests_passed = 0\n")

        for function in functions_names:
            outfile.write("tests_passed += luky.Test({0}, \"{0}\", {1}, {2}).report()\n"\
                          .format(function, show_time, not hide_color))
        outfile.write("print(\"Tests passed:\", tests_passed, \"/ {}\")\n".format(size))

def get_name(line):
    """
    Get the fonction name from a line like :
        "def function_name():"
    """
    return line[4:-4]

def get_test_functions_names(path):
    """
    Get the names of the function that should be tested
    They are taged with "#[test]"
    """
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
    """
    Displays the help for Luky
    """
    print("######################## LUKY ########################\n")
    print("Usage:")
    print("\t ./luky.py tests_file.py other_tests_file.py\n")
    print("Arguments:")
    print("-t or --time: Displays the execution time of each test")
    print("--no-color: Do not show 'passed' and 'failed' in color")
    print("-h or --help: Displays this help\n\n")


def main():
    """
    Main function
    """
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
    outfile = open(".out.py", "a")
    write_header(outfile)
    for path in paths:
        if path not in ["-t", "--time", "--no-color", "-h", "--help"]:
            outfile.write("print(\"---------- {} ----------\")\n".format(path))
            write_test_file(path, outfile, show_time, hide_color)

    outfile.close()
    # Run the file
    call(["python3", ".out.py"])
    # Delete the file
    call(["rm", ".out.py"])
    call(["rm", "-rf", "__pycache__"])

if __name__ == "__main__":
    main()
