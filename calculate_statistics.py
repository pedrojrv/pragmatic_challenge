import sys  # module to get input from user
from math import sqrt 
from heapq import heappush, heappop


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
    def __init__(self):        
        # variables for mean and standard deviation
        self.num_values = 0 # counter of values
        self.ddof = 0       # delta degrees of freedom
        self.old_m, self.old_s, self.new_m, self.new_s = 0, 0, 0, 0

        # partitions for both heaps to calculate median 
        self.low_partition = []
        self.high_partition = []
        

    def add_number(self, x):
        # In this section we add the numbers to the heaps
        if not self.high_partition or x > self.high_partition[0]:
            heappush(self.high_partition, x)
        else:
            heappush(self.low_partition, -x)  
        self.rebalance()

        # In this subsection we update the metrics needed to calculate the mean and standard deviation
        self.num_values += 1

        if self.num_values == 1:
            self.old_m = self.new_m = x
            self.old_s = 0
        else:
            self.new_m = self.old_m + ((x - self.old_m) / self.num_values)
            self.new_s = self.old_s + ((x - self.old_m) * (x - self.new_m))
            self.old_m = self.new_m
            self.old_s = self.new_s

    def rebalance(self):
        if len(self.low_partition) - len(self.high_partition) > 1:
            heappush(self.high_partition, -heappop(self.low_partition))
        elif len(self.high_partition) - len(self.low_partition) > 1:
            heappush(self.low_partition, -heappop(self.high_partition))

    def median(self):
        # if both lenghts are the same we know we need to take the average of the two middle values
        if len(self.low_partition) == len(self.high_partition):
            median = (-self.low_partition[0] + self.high_partition[0])/2
        # else we know that the low partition ccontains the median due to the rebalance if low partition has more values
        elif len(self.low_partition) > len(self.high_partition):
            median = -self.low_partition[0]
        # else is the first value in the right partition
        else:
            median = self.high_partition[0]
        return median

    def mean(self):
        # returns the current mean
        if self.num_values >= 1:
            return self.new_m
        else:
            return 0

    def std(self):
        # Instructions mentioned that we want an output for the first number. If we have no values the std is zero.
        if self.num_values > 1:
            std = sqrt(self.new_s / (self.num_values - self.ddof))
            return std
        else:
            return 0

    def flush(self):
        self.num_values = 0


def is_number(string):
    """Checks if string is a number.

    Args:
        string (str): string to evaluate.

    Returns:
        bool: True if string is a number else False
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


stats_object = RunningStatistics()
precision = 5

# We start by reading each line in stdin 
for line in sys.stdin: 
    # Next we remove trailing and leading whitespace
    line = line.rstrip().strip()

    # we give the user the ability to quit the program by typing "q", "quit", "end"
    if line in ["q", "quit", "end"]: 
        break

    # by typing flush, reset, clear, or their initials we can clear the current running statistics
    if line in ["flush", "reset", "clear"]:
        stats_object.flush()

    if line == "precision":
        precision = int(input("Decimals to include in output: "))

    # if we detect spaces then multiple numbers may be passed, we parse them here
    elif ' ' in line:
        # create a list by splitting line by its spaces
        split = line.split()
        # next, we iterate through each value
        for i in split:
            # if it is a number then we proceed by processing it as usual
            if is_number(i):
                # pushing value to stats_object object and printing statistics
                stats_object.add_number(float(i))
                print("{}, {}, {}".format(round(stats_object.mean(), precision), round(stats_object.std(), precision), round(stats_object.median(), precision)))
                # print("Mean: {}, Standard Deviation: {}, Median: {}".format(round(stats_object.mean(), precision), round(stats_object.std(), precision), round(stats_object.median(), precision)))
    
    # if a single value is passed we make sure it is a number
    elif not is_number(line):
        print("Warning: non numeric characters encountered. Ignoring.")
    # if it is a number, we process it as usual
    else:
        stats_object.add_number(float(line))
        print("{}, {}, {}".format(round(stats_object.mean(), precision), round(stats_object.std(), precision), round(stats_object.median(), precision)))
        # print("Mean: {}, Standard Deviation: {}, Median: {}".format(round(stats_object.mean(), precision), round(stats_object.std(), precision), round(stats_object.median(), precision)))

print("Exited. Have a good day!") 


