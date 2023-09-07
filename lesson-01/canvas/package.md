# Course Functions and Objects

To simplify the process of creating your assignments we have created a Python package that contains common libraries. You will need to install this package using `pip` and `git`. Run the following command in a terminal. Make sure that you use the same Python version that Visual Code is using when you are running your programs.

You need to have `git` installed on your computer. [Instructions to installing git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


```
Mac or Windows:
<python path used in VS Code> -m pip install git+https://github.com/byui-cse/cse251-course-files.git
```

### Finding the path of Python used by VSCode

The following code will include the common files for the course. Most of your assignments include this already but if it
is ever missing, you can import it into your assignments:

```python
# Include cse 251 common Python files
from cse251 import *
```

### Functions

`print_dict(dict, title='')`

This function is used while debugging your programs where it will print a dictionary in a readable format.


### Log Class

A class called Log has be created for the course. It will allow you to create log files while running your programs. Some of these log files will be required for your assignments. It has built in timing methods to help will timing your functions and code. 


Example of creating and using the Log class.

```python
log = Log(show_terminal=True)
log.write('Hello World')
```

When a Log() object is created without a filename, the Log() object will create a file using the current date and time. For example: `1121-120631.log`. The file format is `MMDD-HHMMSS.log`. This log file is created in the same directory of your program.

### Plots Class

This class, `Plots`, is used to create simple Matplotlib plots.

Currently, is contains the methods `line_plot` and `bar_plot`.