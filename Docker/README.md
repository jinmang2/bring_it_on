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

  ![title](https://github.com/jinmang2/bring_it_on/blob/master/img/cpu_virtualization_enable.PNG?raw=true)

## 2. Docker Toolbox 설치
- [Docker docs](https://docs.docker.com/toolbox/toolbox_install_windows/)를 참고하여 설치
- 아래의 `Toolbox Releases`를 통하여 설치

  ![title](https://github.com/jinmang2/bring_it_on/blob/master/img/install_docker_toolbox.PNG?raw=true)

- `DockerToolbox-19.03.1.exe` 파일을 실행

  ![title](https://github.com/jinmang2/bring_it_on/blob/master/img/docker_toolbox.PNG?raw=true)

- 설치되면 바탕화면에 다음과 같은 바로가기 파일이 생성된다.

  ![title]()
