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

class SubTest:
    """
    Class SubTest {

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

    def __init__(self, function, name, show_time):
        self.function = function
        self.name = name
        self.result = None
        self.show_time = show_time


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
        if self.result:
            if self.show_time:
                print("[\033[32mpassed\033[39m] : {} ({} sec)"\
                  .format(self.name, time_after - time_before))
            else:
                print("[\033[32mpassed\033[39m] : {}".format(self.name))
        else:
            if self.show_time:
                print("[\033[31mfailed\033[39m] : {} ({} sec)"\
                  .format(self.name, time_after - time_before))
            else:
                print("[\033[31mfailed\033[39m] : {}".format(self.name))

class Test:
    # This is a class created only to make it easy to call
    """
    Class Test
        To test the function "fct":
            Test(fct, "Test of fct")
    """
    def __init__(self, function, name, show_time=False):
        SubTest(function, name, show_time).report()


# ####################################################
# Parser Part
#

def write_header():
    """
    Erase the ex .out.py and write:
        #!/usr/bin/env python3
        from luky import Test
    """
    outfile = open(".out.py", "w")
    outfile.write("#!/usr/bin/env python3\n")
    outfile.write("from luky import Test\n")
    outfile.close()


def write_test_file(path, outfile, show_time):
    """
    Write the import for the test file and the lines of the tests
    """
    functions_names = get_test_functions_names(path)
    line = "from {} import ".format(path[:-3])
    size = len(functions_names)
    for i in range(size - 1):
        line += "{}, ".format(functions_names[i])
    line += "{}\n".format(functions_names[size - 1])
    outfile.write(line)

    for function in functions_names:
        outfile.write("Test({0}, \"{0}\", {1})\n".format(function, show_time))


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
        if lines[i] == "#[test]\n":
            i += 1
            while i < len(lines) and lines[i][:3] != "def":
                i += 1
            if i != len(lines) and lines[i][:3] == "def":
                functions_names.append(get_name(lines[i]))
        i += 1
    test_file.close()
    return functions_names

def main():
    """
    Main function
    """
    if len(sys.argv) == 1:
        print(sys.argv)
        raise "Bad Argument"
    else:
        show_time = False
        paths = sys.argv[1:] # We get all the arguments
        for path in paths:
            # Checking if the files are Python files
            if path == "--time" or path == "-t":
                show_time = True
            elif len(path) <= 3 or path[-3:] != ".py":
                raise "Bad Argument"
    write_header()
    outfile = open(".out.py", "a")
    for path in paths:
        if path != "-t" and path != "--time":
            outfile.write("print(\"---------- {} ----------\")\n".format(path))
            write_test_file(path, outfile, show_time)

    outfile.close()
    call(["python3", ".out.py"])

if __name__ == "__main__":
    main()
