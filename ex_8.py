class Set:
    def __init__(self, value = []):    # Constructor
        self.data = []                 # Manages a list
        self.concat(value)

    def intersection(self, other):        # other is any sequence
        res = []                       # self is the subject
        for x in self.data:
            if x in other:             # Pick common items
                res.append(x)
        return Set(res)                # Return a new Set

    def union(self, other):            # other is any sequence
        res = self.data[:]             # Copy of my list
        for x in other:                # Add items in other
            if not x in res:
                res.append(x)
        return Set(res)

    def concat(self, value):
        for x in value:                
            if not x in self.data:     # Removes duplicates
                self.data.append(x)

    def issubset(self, other):  return (self & other).data == self.data
    
    def __le__(self, other):    return self.issubset(other)
    
    def __lt__(self, other):    return (self.issubset(other)) and (self.data != other.data)
    
    def issuperset(self, other): return (self & other).data == other.data
    
    def __ge__(self, other):    return self.issuperset(other)
    
    def __gt__(self, other):    return (self.issuperset(other)) and (self.data != other.data)
    
    def __ior__(self, other):  
        self = self | other
        return self

    def intersection_update(self, other): 
        self = self & other
        return self
    
    def __iand__(self, other): return self.intersection_update(other)
    
    def difference_update(self, other): 
        a = []
        for x in self.data:
            if x in other.data:
                a.append(x)
            else:
                continue
        for i in range(0,len(a)):
            self.remove(a[i])
        return self
    
    def __isub__(self, other): return self.difference_update(other)
        
    def symmetric_difference_update(self, other):
        t = []
        a = self & other
        b = self | other
        for i in b.data:
            if i in a.data:
                t.append(i)
        for j in range(0, len(t)):
            b.remove(t[j])         
        return b
    
    def __ixor__(self, other): return self.symmetric_difference_update(other)
    
    def add(self, elem):      
        self.concat(elem)
        return self
    
    def remove(self, elem):
        for i in range(len(self.data)-1):
            if self.data[i] == elem:
                self.data.pop(i)
        return self
    
    def __len__(self):          return len(self.data)        # len(self)
    def __getitem__(self, key): return self.data[key]        # self[i], self[i:j]
    def __and__(self, other):   return self.intersection(other) # self & other
    def __or__(self, other):    return self.union(other)     # self | other
    def __repr__(self):         return 'Set({})'.format(repr(self.data))  
    def __iter__(self):         return iter(self.data)       # for x in self:
    
    
x = Set([1,3,5,7,1,3])
y = Set([2,1,4,5,6])
z = Set([2,1])
a = Set([2,1,4,5,6])
#print(x.issubset(y))
#print(z.issubset(y))
#print(a <= y)
#print(y.issuperset(z))
#print(z < y)
#print(y > a)
#print(y >= a)
#print(x.intersection_update(y))
#print(x.difference_update(y))
x |= y
print(x)
x = Set([1,3,5,7,1,3])
x &= y
print(x)
y -= z
print(y)
y = Set([2,1,4,5,6])
z = Set([2,1])
y ^= z
print(y)