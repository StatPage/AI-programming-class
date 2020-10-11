class Rectangle:   # class의 첫문자는 대문자를 써야 한다.
    def __init__(self, width=1, height=1):   # initializer method
        self._width = width   # instance variables 혹은 property of class 라고 읽을 수 있다.
        self._height = height   # 보통 self. 다음에 _를 붙여준다.
        
    def setWidth(self, width):   # mutator method. 보통 변수 앞에 set을 붙여 이름을 지어준다.
        self._width = width
        
    def setHeight(self, height):   # mutator method
        self._height = height
        
    def getWidth(self):   # accessor mehtods
        return self._width
    
    def getHeight(self):
        return self._height
    
    def area(self):    # other methods
        return self._width * self._height
    
    def perimeter(self):
        return 2 * (self._width + self._height)
    
    def __str__(self):   # state-representation methods
        return ("Width: " +str(self._width) + "\nHeight" + str(self._height))
