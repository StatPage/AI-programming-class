class Setup:
    def __init__(self):
        self._aType = 0     # Type of optimizer
        self._delta = 0     # Step size for axis-parallel mutation
        self._alpha = 0     # Update rate for gradient descent
        self._dx = 0        # increment for calculating derivative

    def setVariables(self, parameters):   # setup에 해당하는 변수들은 setup에서 지정되도록 만든 것이다.
        self._aType = parameters['aType']
        self._delta = parameters['delta']
        self._alpha = parameters['alpha']
        self._dx = parameters['dx']
        self._resolution = parameters['resolution']

    def getAType(self):
        return self._aType