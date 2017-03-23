# Class holding operators' outputs

from collections import defaultdict

class TType:

    def __call__(self, x, y, z):
        return self.ttype[x][y][z]

    def __init__(self):
        self.ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

        # INTEGERS ONLY
        self.ttype['+']['int']['int'] = 'int'
        self.ttype['-']['int']['int'] = 'int'
        self.ttype['*']['int']['int'] = 'int'
        self.ttype['/']['int']['int'] = 'int'
        self.ttype['%']['int']['int'] = 'int'
        self.ttype['<']['int']['int'] = 'int'
        self.ttype['>']['int']['int'] = 'int'
        self.ttype['<<']['int']['int'] = 'int'
        self.ttype['>>']['int']['int'] = 'int'
        self.ttype['|']['int']['int'] = 'int'
        self.ttype['&']['int']['int'] = 'int'
        self.ttype['^']['int']['int'] = 'int'
        self.ttype['<=']['int']['int'] = 'int'
        self.ttype['>=']['int']['int'] = 'int'
        self.ttype['==']['int']['int'] = 'int'
        self.ttype['!=']['int']['int'] = 'int'

        # FLOAT-INT OPERATIONS
        self.ttype['+']['int']['float'] = 'float'
        self.ttype['+']['float']['int'] = 'float'
        self.ttype['+']['float']['float'] = 'float'
        self.ttype['-']['int']['float'] = 'float'
        self.ttype['-']['float']['int'] = 'float'
        self.ttype['-']['float']['float'] = 'float'
        self.ttype['*']['int']['float'] = 'float'
        self.ttype['*']['float']['int'] = 'float'
        self.ttype['*']['float']['float'] = 'float'
        self.ttype['/']['int']['float'] = 'float'
        self.ttype['/']['float']['int'] = 'float'
        self.ttype['/']['float']['float'] = 'float'

        #FLOAT-INT COMPARISONS
        self.ttype['<']['int']['float'] = 'int'
        self.ttype['<']['float']['int'] = 'int'
        self.ttype['<']['float']['float'] = 'int'
        self.ttype['>']['int']['float'] = 'int'
        self.ttype['>']['float']['int'] = 'int'
        self.ttype['>']['float']['float'] = 'int'
        self.ttype['<=']['int']['float'] = 'int'
        self.ttype['<=']['float']['int'] = 'int'
        self.ttype['<=']['float']['float'] = 'int'
        self.ttype['>=']['int']['float'] = 'int'
        self.ttype['>=']['float']['int'] = 'int'
        self.ttype['>=']['float']['float'] = 'int'
        self.ttype['==']['int']['float'] = 'int'
        self.ttype['==']['float']['int'] = 'int'
        self.ttype['==']['float']['float'] = 'int'
        self.ttype['!=']['int']['float'] = 'int'
        self.ttype['!=']['float']['int'] = 'int'
        self.ttype['!=']['float']['float'] = 'int'

        # STRING OPERATIONS
        self.ttype['+']['string']['string'] = 'string'
        self.ttype['*']['string']['int'] = 'string'

        #STRING COMPARISONS
        self.ttype['<']['string']['string'] = 'int'
        self.ttype['>']['string']['string'] = 'int'
        self.ttype['<=']['string']['string'] = 'int'
        self.ttype['>=']['string']['string'] = 'int'
        self.ttype['==']['string']['string'] = 'int'
        self.ttype['!=']['string']['string'] = 'int'