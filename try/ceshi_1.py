class A(object):
    def aa(self):
        return '1'


class B(A):
    def aa(self):
        b = super(B, self).aa()
        print(b)

b = B()
b.aa()
