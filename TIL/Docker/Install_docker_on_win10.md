# khaiii를 위한 Docker 설치 삽질기... Windows 10 Home
## 0. Topology
- Windows 10 pro는 Saerom Bang님의 [Docker를 활용한 khaiii 설치수난기](https://medium.com/@saerombang11/docker를-활용한-khaiii-설치수난기-53d014f9eb58)를 보면 손쉽게 build 가능
- 그러나 Windows 10 Home edition은 `Docker for Windows` 설치가 불가능..
- ETRI 형태소 분석기 대신 khaiii를 사용해보고자 이와 같이 삽질한 작업을 남기고자 한다.

## 1. BIOS 환경에서 CPU 사용 가능하게 만들기
- BIOS setting으로 들어가서 Virtualization을 `Enable` 상태로 만들어준다.
- 보통 Intel CPU는 `Virtualization Technology, VT-x`, AMD CPU는 `AMD SVM`으로 되어 있고
- Advanced / Security 탭 중에 있다.
- [Intel VT-x와 AMD SVM을 활성화하는 방법](https://www.qnap.com/ko-kr/how-to/faq/article/intel-vt-x%EC%99%80-amd-svm%EC%9D%84-%ED%99%9C%EC%84%B1%ED%99%94%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95/)
- 결과는 `작업관리자 > 성능` 탭에서 아래와 같이 확인할 수 있다.
  <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/check_virtualization.PNG?raw=true"
       width="60%" height="60%">
  
## 2. Docker Toolbox 설치
- [Docker docs](https://docs.docker.com/toolbox/toolbox_install_windows/)를 참고하여 설치
- 아래의 `Toolbox Releases`를 통하여 설치
  ![title](https://github.com/jinmang2/bring_it_on/blob/master/img/install_docker_toolbox.PNG?raw=true)
- `DockerToolbox-19.03.1.exe` 파일을 실행
  ![title](https://github.com/jinmang2/bring_it_on/blob/master/img/docker_toolbox.PNG?raw=true)
- 설치되면 바탕화면에 다음과 같은 바로가기 파일이 생성된다.
  ![title](https://github.com/jinmang2/bring_it_on/blob/master/img/docker_quick.PNG?raw=true)
- ㅇㅁㄴㄹㅇㅁ

## Reference
- [이제는, 딥러닝 개발환경도 Docker로 올려보자!!](http://moducon.kr/2018/wp-content/uploads/sites/2/2018/12/leesangsoo_slide.pdf)
- [PyTorch/Tensorflow를 위한 Docker 시작하기](https://www.quantumdl.com/entry/PyTorchTensorflow%EB%A5%BC-%EC%9C%84%ED%95%9C-Docker-%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0)
- [Install Docker Toolbox on Windows](https://docs.docker.com/toolbox/toolbox_install_windows/)
- [DockerHub/pytorch/pytorch](https://hub.docker.com/r/pytorch/pytorch)
- [초보를 위한 도커 안내서 - 설치하고 컨테이너 실행하기](https://subicura.com/2017/01/19/docker-guide-for-beginners-2.html)
- [65. [Docker] Dockerfile 개요 및 간단한 작성법 가이드](http://blog.naver.com/PostView.nhn?blogId=alice_k106&logNo=220646382977&parentCategoryNo=7&categoryNo=&viewDate=&isShowPopularPosts=true&from=search)
- [github.com/nvidia-docker](https://github.com/NVIDIA/nvidia-docker)
- [[docker]도커 처음 사용자를 위한 윈도우 도커 설치 및 실행하기](https://steemit.com/kr/@mystarlight/docker)
- [데이터 사이언스 스쿨 - 도커 툴박스](https://datascienceschool.net/view-notebook/c792824fa32443bca59ba59285c62228/)
- [ZETAWIKI - 윈도우 도커 툴박스 설치](https://zetawiki.com/wiki/%EC%9C%88%EB%8F%84%EC%9A%B0_Docker_Toolbox_%EC%84%A4%EC%B9%98)
- [[Docker] 도커 이미지와 컨테이너 삭제 방법](https://brunch.co.kr/@hopeless/10)
- [삵, Docker 이미지 생성(run), 확인(ps), 삭제(rm)](https://sarc.io/index.php/cloud/1158-docker-run-ps-rm)
- [How to install telnet in Docker for Windows 10](https://stackoverflow.com/questions/39286441/how-to-install-telnet-in-docker-for-windows-10)
- [Docker - 이미지와 컨테이너, 10분 정리](https://www.sangkon.com/hands-on-docker-part1/)
- [ZETAWIKI = 파이썬가상환경 virtualenv, venv](https://zetawiki.com/wiki/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EA%B0%80%EC%83%81%ED%99%98%EA%B2%BD_virtualenv,_venv)
- [Docker 정리 #8 (Dockerfile)](https://jungwoon.github.io/docker/2019/01/13/Docker-8/)
- [vim - 01. 저장 및 종료](https://www.opentutorials.org/course/730/4561)
- [WARNING: apt does not have a stable CLI interface. Use with caution in scripts.](https://github.com/hackafake/hackafake-backend/issues/32)
- [간단하게 살펴보는 Docker for Windows](https://www.sysnet.pe.kr/2/0/11204)
- [[ Docker ] dangling image ( 이름 없는 이미지 / none 이미지 / <none>:<none> 이미지) 제거](https://web-front-end.tistory.com/102)
- [Dockerfile Entrypoint 와 CMD의 올바른 사용 방법](https://bluese05.tistory.com/77)
- [dockerfile 역할과 활용 정리](https://lejewk.github.io/docker-dockerfile/)
- [Windows docker build warning non-windows docker host](https://stackoverflow.com/questions/46080312/windows-docker-build-warning-non-windows-docker-host)
