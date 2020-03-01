# 원격 저장소에 올라간 커밋 되돌리기

## 1. 로컬에서 커밋 되돌린 후 강제 푸시
로컬에서 `$ git reset`명령어를 이용, 커밋을 되돌림
```
$ git reset --hard HEAD~1 # 1개의 commit 되돌림
>>> HEAD is now at b12c97c Add files via upload
```
`-f`, `--force`를 명령어에 추가하여 강제로 덮어씌움
```
$ git push -f origin master
```
>#### 주의사항
- 혼자만 사용하는 branch에 commit을 push했고 이를 되돌리고 싶은 경우
- 팀원들과 직접 커뮤니케이션해서 내가 되돌린 commit을 pull로 땡겨간 팀원이 없다고 확인된 경우만 사용바람.

## 2. git revert 사용
- `$ git revert`명령어를 사용, revert 커밋을 커밋 히스토리에 쌓는 방식을 채용
- 특정 커밋을 되돌리는 작업도 하나의 커밋으로 간주, 커밋 히스토리에 추가
- 내가 되돌린 작업을 다른 팀원들과 공유 가능
```
# commit한 순서와 거꾸로 revert해야함
# 우리가 생각하는 실행 취소

$ git revert 03001425c69fe8eccf219db243d9ecc9a60d64b8 # Revert "Commit C"
$ git revert 16e2e7f1789973a227a5e6bb47221ed683a8b1ae # Revert "Commit B"
$ git revert b31064c29b55f826d1dae3f1bddecc4a27a10e36 # Revert "Commit A"
```
`--no-commit`옵션을 사용하여 revert를 위한 커밋을 하나만 생성할 수 있음
```
$ git revert --no-commit 03001425c69fe8eccf219db243d9ecc9a60d64b8 # Revert "Commit C"
$ git revert --no-commit 16e2e7f1789973a227a5e6bb47221ed683a8b1ae # Revert "Commit B"
$ git revert --no-commit b31064c29b55f826d1dae3f1bddecc4a27a10e36 # Revert "Commit A"
```
- 복수개의 커밋에 대해서 revert 지원
- 특정 커밋의 hash가 아닌 `[되돌리고 싶은 커밋의 범위]`를 인수로 입력
```
$ git revert --no-commit HEAD~3.. # 또는 master~3..master
```
index에 올라간 변경들을 한꺼번에 커밋한 다음, 원격 저장소에 푸쉬
```
$ git commit -m "Revert "Commit C, B, A"'
```
```
$ git push origin master
```

## 실전 활용 예제
![f1](https://user-images.githubusercontent.com/37775784/75620960-ff6f5400-5bd1-11ea-92db-a3ff08503da8.png)
![f2](https://user-images.githubusercontent.com/37775784/75620961-00a08100-5bd2-11ea-8b37-02255e0bee60.png)
![f3](https://user-images.githubusercontent.com/37775784/75620962-01d1ae00-5bd2-11ea-9ea6-eaf8a726fad0.png)
![f4](https://user-images.githubusercontent.com/37775784/75620963-0302db00-5bd2-11ea-9b4d-c7e2c885918d.png)
![f5](https://user-images.githubusercontent.com/37775784/75620964-04340800-5bd2-11ea-9cc2-b9113a38e5f9.png)
![f6](https://user-images.githubusercontent.com/37775784/75620965-04cc9e80-5bd2-11ea-8cb7-bc1678e2856d.png)


## Reference
- [원격 저장소에 올라간 커밋 되돌리기](https://jupiny.com/2019/03/19/revert-commits-in-remote-repository/)
- [How to revert multiple git commits?](https://stackoverflow.com/questions/1463340/how-to-revert-multiple-git-commits)
- [2.3 Git의 기초 - 커밋 히스토리 조회하기](https://git-scm.com/book/ko/v2/Git%EC%9D%98-%EA%B8%B0%EC%B4%88-%EC%BB%A4%EB%B0%8B-%ED%9E%88%EC%8A%A4%ED%86%A0%EB%A6%AC-%EC%A1%B0%ED%9A%8C%ED%95%98%EA%B8%B0)
- [How to exit git log or git diff [duplicate]](https://stackoverflow.com/questions/9483757/how-to-exit-git-log-or-git-diff)
- [[Git] git add 취소하기, git commit 취소하기, git push 취소하기](https://gmlwjd9405.github.io/2018/05/25/git-add-cancle.html)
