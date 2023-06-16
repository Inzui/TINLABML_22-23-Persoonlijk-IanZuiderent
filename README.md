# TINLABML 22-23 Personal Assignments
## Ian Zuiderent, 1004784, TI3B
Git Repository for the personal assignments for TINLab Machine Learning 22-23.

## Personal Assignment 1
* Three seperate implementations of the assignment can be started.
* Starting one of the programs is done by starting the corresponding ".py" file with Python.
* "MainClasses.py" starts the program that uses seperate classes for Nodes/Links.
* "MainMatrixes.py" starts the program that uses lists for Nodes/Links.
* "MainNumpy.py" starts the program that uses Numpy Matrixes for Nodes/Links.

## Personal Assignment 2
* Starting the program is done by starting the "main.py" file with Python.
* The program will place the generated songs in Python's current working directory. 
In other words, if I start the program from my working directory Desktop, a folder called "Songs" will appear on my desktop.
* It is possible to have the program not generate songs, but only print the songs in the console. To do this, set in "main.py" the parameter "debugMode" to True, in the Main constructor (Line 63). This saves an enormous amount of time ;).
* The first 3 generations are generated randomly. Only after this, a genetic algorithm is applied. This is done to increase diversity at the beginning.