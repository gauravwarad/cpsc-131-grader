import os
import zipfile
import subprocess
import shutil
# from distutils.dir_util import copy_tree
import re

def find_todos(file_content):
    todos = []
    start_line = None
    for i, line in enumerate(file_content):
        if "//////////////////////// TO-DO" in line:
            start_line = i
        if "///////////////////// END-TO-DO" in line and start_line is not None:
            todos.append((start_line, i))
            start_line = None
    return todos
def replace_and_grade(file_a, file_b, line_a, line_b, line_x, line_y):
    # Read the contents of file B
    lines_b = read_file(file_b)

    # Cut contents from line_a to line_b (1-based index)
    original_contents = lines_b[line_a-1:line_b]
    
    # Remove the cut contents from lines_b
    del lines_b[line_a-1:line_b]

    # Read the contents of file A
    lines_a = read_file(file_a)

    # Get the contents to insert from line_x to line_y (1-based index)
    insert_contents = lines_a[line_x-1:line_y]
    
    # Insert the new contents at line_a in lines_b
    lines_b[line_a-1:line_a-1] = insert_contents

    # # Perform some operation (for demonstration, we'll just reverse the contents)
    # # You can replace this with any other operation as needed
    # processed_contents = [line[::-1] for line in lines_b]

    # Write the modified contents back to file B (optional)
    write_file(file_b, lines_b)

    # grading operation here
    print("updated solution file is ---- \n\n")
    # print(lines_b)
    grade(os.path.dirname(file_b))

    # Restore the original contents back to file B
    # Remove the inserted contents first
    del lines_b[line_a-1:line_a-1+len(insert_contents)]
    
    # Then insert the original contents back
    lines_b[line_a-1:line_a-1] = original_contents

    # Write back the restored contents to file B
    write_file(file_b, lines_b)

def grade(directory):
    # Specify the directory containing your C++ code
    # directory = '/path/to/your/directory'
    # Specify the command you want to run
    command = '../Build.sh'
    command2 = './project_g++'
    # Specify the output file where you want to append the results
    output_file = '/home/banana/grader/output.txt'
    # print(directory)
    # Change to the specified directory
    os.chdir(directory)

    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            result2 = subprocess.run(command2, shell=True, capture_output=True, text=True, input = '\x04')
            result3 = subprocess.run("pwd",shell=True, capture_output=True, text=True)
            print(result3.stdout)
            print(result2.stdout)
            if result2.returncode == 0:
                if "(100.00%)" in result2.stdout:
                    write_comment(output_file, "successful. full points to gryffindor\n")
                else:
                    
                    write_comment(output_file, "successful, but not 100 percent\n")
                
            else:
                write_comment(output_file, "oops, ./project_g++ failed; 0 points\n")
        else:
            write_comment(output_file, "oops, build failed; 0 points\n")
        
        print("Output appended to", output_file)

    except Exception as e:
        print("An error occurred:", e)

def write_comment(output_file, comment):
    output_file = '/home/banana/grader/output.txt'
    with open(output_file, "a") as f:
            # Write the stdout and stderr to the file
            f.write(comment)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()
    
def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.writelines(content)

def create_temp(filepath):
        # Extract the file name from the file path
    filename = os.path.basename(filepath)

    # Define the /temp directory in the current working directory
    temp_dir = os.path.join(os.getcwd(), "temp")

    # If /temp directory exists, remove it and create a new one
    if os.path.exists(temp_dir):
        print(f"Removing existing /temp directory: {temp_dir}")
        shutil.rmtree(temp_dir)

    # Define the destination path in the /temp folder
    destination = os.path.join(temp_dir, filename)

    try:
        # Copy the file to the /temp folder
        # shutil.copy(filepath, destination)
        shutil.copytree("C++ Development Root", temp_dir)

        print(f"File copied to: {temp_dir}")
        # os.rename(destination, os.path.join(temp_dir, "Printing.cpp"))
        # Call the process function with the copied file path
        # grade(destination)
        # print("assume we're grading - ", destination)
    except IOError as e:
        print(f"Error copying file: {e}")

def grade_driver(filepath, student_name):

    print("currently grading - ", student_name, " for the file - ", filepath)
    write_comment("", f"\n\nCurrently Grading {student_name} \n")
    create_temp(filepath)
    sol_file = "/home/banana/grader/temp/SourceCode/GroceryItem.cpp"
    sol_content = read_file(sol_file)

    sol_todos = find_todos(sol_content)

    student_content = read_file(filepath)
    student_todos = find_todos(student_content)

    if len(sol_todos) != len(student_todos):
        print("number of todos mismatch - ending program")
        return

    for i in range(0, len(sol_todos)):
        sol_start, sol_end = sol_todos[i]
        stu_start, stu_end = student_todos[i]
        write_comment("", f"TODO {i+1}\n")
        replace_and_grade(filepath, sol_file, sol_start, sol_end, stu_start, stu_end)
        

