# Genetic-Algo

We built An Automata in the model of WRAP_AROUND that simulates the phenomenon of "waves" of the corona disease.
We presented the simulation using a graphical display. We started with N creatures, where the size of the automaton is 200*200. D is the initial percentage of patients out of N creatures.
These creatures move randomly, so in each generation each creature can move to any of the 8 cells surrounding it or stay in place.
R percent of the creatures move faster than the other creatures, and change their positions by 10 cells.
When an infected cell is adjacent to an uninfected cell, there is a probability P that the healthy cell will not become infected.
When the percentage of patients is higher than T (Threshold), people are more careful and the risk of infection decreases, and vice versa.
An infected cell remains infected and infectious for X generations, and an infected cell will not become infected again during the simulation.

Running instructions:
- Copy the exe file and put it in a folder.
- In the same folder, put the input txt file.
- Choose the algorithm you want to run by running: regular, darvini or lemarci.

**running example in cmd in the folder:
algo.exe example.txt regular
algo.exe example.txt darvini
algo.exe example.txt lemarci
**
