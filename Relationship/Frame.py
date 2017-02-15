

class Frame:

    def __init__(self):

        self.times = []
        self.correlations = []

        self.total_time = 0.0
        self.final_correlation = None

    def get_total_time(self):
        return self.total_time

    def get_final_correlation(self):
        return self.final_correlation

    def add_correlation(self, duration, correlation):
        """
        Adds a new correlation value with it's appropriate length of time it took up
        :type duration: float
        :type correlation: float
        """

        # Duration must have a positive value
        if duration <= 0:
            raise ValueError("Illegal Duration: The duration of a correlation must be positive.  Received: "+str(duration))

        # Values must be between -1 and 1
        if correlation > 1 or correlation < -1:
            raise ValueError("Illegal Correlation: The correlation must be between (-1,  1).  Received: " + str(correlation))

        # Update all values
        self.times.append(duration)
        self.correlations.append(correlation)
        self.total_time = sum(self.times)
        self.final_correlation = sum(list(map(lambda x: x[0]*x[1], list(zip(self.times, self.correlations))))) / self.total_time
