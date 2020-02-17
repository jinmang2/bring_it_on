# 파이썬은 메서드 오버로딩이 없다!
- 자바는 가능
```java
class Adder{  
      static int add(int a,int b)
      {
          return a+b;
      }  
      static int add(int a,int b,int c)
      {
          return a+b+c;
      }  
  }  
```
- 파이썬은 메서드 오버로딩이 없다.
```python
 class Korea:
    
      def __init__(self, name,population, captial):
          self.name = name
          self.population = population
          self.capital = captial
    
      def show(self):
          print(
              """
              국가의 이름은 {} 입니다.
              국가의 인구는 {} 입니다.
              국가의 수도는 {} 입니다.
              """.format(self.name, self.population, self.capital)
          )
    
      def show(self, abc):
          print('abc :', abc)
```
