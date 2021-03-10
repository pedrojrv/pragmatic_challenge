# Pragmatic Institute | The Data Incubator Coding Challenge

Write a program that reads a list of numbers and for each number outputs an estimate of the running mean, running standard deviation, and running median.  The input should be read from standard in, with one number per line.  For each line of input, the program should print to standard out the estimated running mean, running standard deviation, and running median.  That is, given the input

```
1
2
3
137.036
```
 
the program should output values close to

 
```
1,0,1
1.5,0.5,1.5
2,0.816,2
35.759,58.477,2.5
```
 
Some notes:

- Using either the biased or unbiased estimate of the standard deviation is fine, but you should report a number even for the first step.
- There are several ways to define the median for an even number of samples; you may use any of these definitions.
- Output numbers at a reasonable precision.
 

You will probably have to strike a balance between the accuracy of the results and  resources your program requires.  Choose a sensible tradeoff.  Better yet, allow this to be configurable.

Ideally, this program should be able to handle arbitrarily long lists of inputs.  It would be nice for it to output results as soon as possible, instead of needing to wait for all of standard in to be read.  You do not have to worry about malicious input (there won’t be 10 GB on a single line), but gracefully handling malformed input lines is a plus.

Upload your solution to the public DVCS host of your choice, and send us a link to the repository.  You may use any programming language or packages you like, but if you use anything outside of Python 3, Pandas, or Numpy, please include instructions to help us run your code.


# Usage
To use the script, first clone the repository:

```python
git clone https://github.com/pedrojrv/pragmatic_challenge.git
```

Open your python environment, navigate to the just cloned repository directory, and run the `calculate_statistics.py` file as follow:

```shell
cd path/to/the/repository/directory
python calculate_statistics.py
```

You can start typing numbers and get running statistics immediately. The default `precision` is `5` decimals but can be changed dynamically. Special commands include:


| String  | Action |
| :-------------: | :-------------: |
| q, quit, end  | terminates program  |
| flush, reset, clear  | resets statistics dynamically  |
| precision | changes output precision |

# Implementation, Trade-offs, and Assumptions

Assumptions and implementation information for the running statistics calculations can be found under the `RunningStatistics` class documentation:


```python
class RunningStatistics:
    """RunningStatistics Class. It allows to efficiently calculate running statistics including the mean, median, and standard deviation.

    An easy solution to this problem is to simply build an initial NumPy array and append numbers as they come followed by statistics calculations.
    This however starts to become inefficient as the number of values increases since under the hood:
    - The mean is calculated every time for the standard deviation (np.std())
    - The np.median() algorithm first has to re-sort the array, therefore, adding overhead()
    
    Here, the running median is calculated using two heaps. The two heaps are balanced on the go as values are being added to allow for 
    fast extraction of the median value when needed. This functionality has a O(n log(n)) time complexity. An alternative algorithm can 
    provide the solution with O(n) complexity in best-case scenarios and O(n^2) in the worst case both at the cost of space complexity.
    I, therefore, chose this implementation as a good tradeoff, especially for the requested use case. 
    
    Similarly for the mean and standard deviation, the parameters are updated on the go to be able to feed back the required statistics faster.
    The only drawback is the additional overhead but given the use case, it is non-noticable. It is based on Welford's algorithm implementation

    Assumptions:
    - The Delta Degrees of Freedom is set to 0 but can be changed if needed (self.ddof)
    """    
```