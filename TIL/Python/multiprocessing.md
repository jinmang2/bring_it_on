```python
import time

# 시작시간
start_time = time.time()

# 멀티쓰레드 사용하지 않는 경우 (20만 카운트)
def count(name):
    a = 0
    for i in range(1, 50000001):
        a += i
        
num_list = ['p1', 'p2', 'p3', 'p4']
for num in num_list:
    count(num)
    
print(f"\r--- {time.time() - start_time} seconds ---")
```

    --- 9.069438457489014 seconds ---



```python
import multiprocessing

multiprocessing.cpu_count()
```




    40




```python
import multiprocessing
import time

# 시작시간
start_time = time.time()

# 멀티쓰레드 사용하는 경우 (20만 카운트)
# Pool 사용해서 함수 실행을 병렬
def count(name):
    a = 0
    for i in range(1, 50000001):
        a += i
        
num_list = ['p1', 'p2' ,'p3', 'p4']

# 멀티 쓰레딩 Pool 사용
pool = multiprocessing.Pool(processes=30) # 현재 시스템에서 사용할 프로세스 개수
pool.map(count, num_list)
pool.close()
pool.join()

print(f"--- {time.time() - start_time} seconds ---")
```

    --- 2.736788272857666 seconds ---
