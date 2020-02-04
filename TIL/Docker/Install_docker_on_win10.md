# Windows 10 Home Edition에서 `Docker` 설치하기

## Windows 10 pro & enterprise
- [https://hub.docker.com/?overlay=onboarding](https://hub.docker.com/?overlay=onboarding)에서 `Docker for Windows`를 다운받고
- 이를 설치하면 사용 가능
- [Docker를 활용한 khaiii 설치수난기](https://medium.com/@saerombang11/docker%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-khaiii-%EC%84%A4%EC%B9%98%EC%88%98%EB%82%9C%EA%B8%B0-53d014f9eb58)

## Windows 10 Home Edition
- 위와 같이 설치할 경우 아래의 에러가 발생
   #### Installation failed: one prerequisite is not fulfilled

   ```
   Docker Desktop requires Windows 10 Pro or Enterprise version 15063 to run.
   ```
- `Docker Toolbox`를 통하여 설치해야 함.
- [공식문서](https://docs.docker.com/toolbox/toolbox_install_windows/)에서는 업그레이드하는 것을 추천
   #### Install Docker Toolbox on Windows
   
   >```
   >Legacy desktop solution. Docker Toolbox is for older Mac and Windows systems 
   >that do not meet the requirements of Docker Desktop for Mac and Docker Desktop for Windows.
   >We recommend updating to the newer applications, if possible.
   >```
- [Docker Toolbox Install](https://docs.docker.com/toolbox/toolbox_install_windows/)의 순서대로 설치를 진행

### STEP 1. BIOS 환경에서 CPU 사용 가능하게 만들기
- `Docker`는 **컨테이너 기반의 오픈소스 가상화 플랫폼**. 당연히 가상화가 가능해야 사용할 수 있다.
- BIOS setting으로 들어가서 Virtualization을 `Enable` 상태로 만들어준다.
- 보통 Intel CPU는 `Virtualization Technology, VT-x`, AMD CPU는 `AMD SVM`으로 되어 있고
- Advanced / Security 탭 중에 있다.
- [Intel VT-x와 AMD SVM을 활성화하는 방법](https://www.qnap.com/ko-kr/how-to/faq/article/intel-vt-x%EC%99%80-amd-svm%EC%9D%84-%ED%99%9C%EC%84%B1%ED%99%94%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95/)
- 결과는 `작업관리자 > 성능` 탭에서 아래와 같이 확인할 수 있다.
  <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/check_virtualization.PNG?raw=true"
       width="60%" height="60%">
  
## STEP 2. Docker Toolbox 설치파일 다운로드
- [github.com/docker/toolbox/releases](https://github.com/docker/toolbox/releases) 접속 후 `DockerToolbox-[version].exe` 다운로드
    - 필자는 2020.02.04 시점에서 최신 버전인 `v.19.03.1` 설치

   <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/docker_toolbox2.PNG?raw=true"
    width="95%" height="95%">

- 아래 파일을 다운로드했다면 성공

    <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/dockertoolbox_imoticon.PNG?raw=true">
