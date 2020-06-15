import PyInline
from time import time

m = PyInline.build(code="""
  long my_add(int m) {
    long sum = 0;
    for (int i=0; i<m; i++)
        sum += i;
    return sum;
  }
""", language="C")


def my_add2(m):
    sum = 0
    for i in range(m):
        sum += i
    return sum


start = time()
sum1 = m.my_add(1000000)
end = time()
print(sum1, end - start)


start = time()
sum2 = my_add2(1000000)
# sum2 = sum(range(1,1000000)) # 这个可能会快些
end = time()
print(sum2, end - start)
