"""
This code draws a series of samples from the normal distribution, takes the
square of the averages, and and the average of the squares. The results are
printed to stdout.

This file can be used directly from the command line using 

.. sourcecode:: bash

    pydev normal.py 1 2 10

where ``1`` is the mean, ``2`` is the standard deviation, and ``10`` is the
sample size of the distribution to be studied.

More advanced users should read the documentation of the 
:class:`NormalDistribution` class in order to understand the public API of
this object, should they wish to use it in their scripts.

If imported into a script, there is no ``run`` method that needs to be called
if a variable is updated, the sample is redrawn immediately after assignment.
The averages and outputs will also automatically adapt.

.. warning::
    If users are intending to use this library in a functional manner, purity
    is guaranteed ONLY if the parameters are not changed.

TODO: Implement some kind of asynchronicity when drawing new samples. Early
    experiments were done but were unsuccessful due to a stack overflow
    error caused by invoking ``__setattr__`` when wriiting results. Provide
    each instance with a lock. Acquire and release this lock as necessary.
"""
from collections import namedtuple
from Scientific.IO import ArrayIO
from Scientific.Statistics import mean
from sys import argv
from numpy import random, multiply


class NormalDistribution(object):
    """
    Wraps the relevant functions to calculate the normal distribution, and
    makes this functionality available to other Python scripts through a 
    convenient Python API

    In order to invoke this object, call it using the constructor with the 
    required parameters of the mean, standard deviation, and sample size.

    .. sourcecode:: python
        
        mean = 0
        standard_deviation = 1
        sample_size = 100

        dist = NormalDistribution(mean, standard_deviation, sample_size)

    The Public API of this object is 

    .. sourcecode:: python

        dist.sample_average
        dist.square_sample_average
        dist.output

        len(dist)
        dist[index]

    The first property returns the average of the distribution. The second
    property returns the average of the squares. The third property yields
    a string representation of the results. When run from the command line,
    this is printed to ``stdout``.

    Calling ``len`` on this object returns the sample size, and indexing
    the object with a number will reutrn the sample corresponding to
    ``index``.
    """

    def __init__(self, mean, standard_deviation, sample_size):
        """
        Initialize the NormalDistribution class. This class
        is responsible for calculating the required values from the normal
        distribution. It can be imported into a Python file of your choosing
        for further processing. There is also a code block at the bottom of the
        file showing a sample implementation of this class. This sample
        implementation takes in its arguments from ``stdin`` and prints its
        results to ``stdout``. 
        
        .. note::

            If run from the terminal, ``stdin`` is the  stream
            (set of characters) typed into the terminal, and ``stdout`` is the
            stream that is printed out to the terminal as a result of running
            this program. In UNIX-like operating systems, and in Windows, the
            output of one program can be redirected ("piped") to another, which
            is why I refrained from using the word "terminal.
        
        :param float mean: The mean of the distribution to be sampled
        :param float standard_deviation: The standard deviation of the
            distribution to be sampled
        :param int sample_size: The number of samples that will be drawn
            from the normal distribution

        """

        self.mean = mean
        self.standard_deviation = standard_deviation
        self.sample_size = sample_size
        self.sample = None


    @property
    def sample_average(self):
        """
        Returns the average of the sample drawn from the distribution
        """
        if self.sample is None:
            return None
        else:
            return mean(self.sample)

    @property
    def square_sample_average(self):
        """
        Returns the average of the squares.
        """
        if self.sample is None:
            return None
        else:
            x2 = multiply(self.sample, self.sample)
            return mean(x2)
    
    @property
    def output(self):
        """
        Write a string representation of the square of the average
        and the average of the squares
        """
        return 'output <x^2>= %s \n output <x>= %s' % (
            self.square_sample_average, self.sample_average
        )

    def _calculate_sample(self):
        """
        Responsible for updating the sample when a property has been
        changed. The use of the underscore before this method implies
        that it is a private method, and is not meant to be used in the
        public API.
        """
        sample = random.normal(
            self.mean, self.standard_deviation, self.sample_size
        )

        assert len(sample) == self.sample_size

        return sample
    

    def __len__(self):
        """
        Implements the ``len`` function on instances of this class. Returns the
        value of the sample size
        """
        return self.sample_size

    def __getitem__(self, index):
        """
        Allows indexing of each sample in the distribution sampled from this
        object. This, combined with the ``__len__`` method, also makes this 
        object iterable, just like a list.
        """
        return self.sample[index]

    @property
    def _should_update(self):
        """
        Helper method used by ``__setattr__`` to determine if the sample
        should be redrawn.
        """
        return all(
            (hasattr(self, attr) for attr in 
                ('mean', 'standard_deviation', 'sample_size')
            )
        )

    def __setattr__(self, name, value):
        """
        This method overwrites attribute assignment. It is never called
        directly, but is instead invoked when the ``.`` operator is performed
        on an instance of this object. On assignment, the sample is redrawn. 
        """
        self.__dict__[name] = value
 
        if self._should_update:
            self.__dict__['sample'] = self._calculate_sample()

    def __repr__(self):
        """
        Prints a useful representation of this object for easy debugging"
        """
        return '<%s(mean=%s, standard_deviation=%s, sample_size=%s)>' % (
            self.__class__.__name__, self.mean, self.standard_deviation,
            self.sample_size
        )
        
if __name__ == '__main__':

    Input = namedtuple("Input", ["mean", "standard_deviation", "sample_size"])

    if len(argv)!=4:
        print('usage: pydev %s <mean> <standard deviation> <# of samples>' % argv[0])
        exit()

    user_input = Input(float(argv[1]), float(argv[2]), float(argv[3]))
    distribution = NormalDistribution(
        user_input.mean, user_input.standard_deviation, user_input.sample_size
    )

    print(distribution.output)

