# Windows 10 Home Edition에서 `Docker` 설치하기

>## Windows 10 pro & enterprise
- [https://hub.docker.com/?overlay=onboarding](https://hub.docker.com/?overlay=onboarding)에서 `Docker for Windows`를 다운받고
- 이를 설치하면 사용 가능
- [Docker를 활용한 khaiii 설치수난기](https://medium.com/@saerombang11/docker%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-khaiii-%EC%84%A4%EC%B9%98%EC%88%98%EB%82%9C%EA%B8%B0-53d014f9eb58)

>## Windows 10 Home Edition
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

## STEP 1. BIOS 환경에서 가상화 기능 활성화하기
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

## STEP 3. Docker Toolbox 설치
- `STEP 2`에서 받은 파일을 실행, 모든 설정을 `default`로 진행해도 무방함

   <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/dockertoolbox1.PNG?raw=true">
   <br><br>
   <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/dockertoolbox2.PNG?raw=true">
   <br><br>
   
   - `Git fot Windows`는 선택
   
   <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/dockertoolbox3.PNG?raw=true">
   <br><br>
   <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/dockertoolbox4.PNG?raw=true">
   <br><br>
   <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/dockertoolbox5.PNG?raw=true">
   <br><br>
   <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/dockertoolbox6.PNG?raw=true">
   
- 위 과정을 진행하면 아래와 `바탕화면`에 바로가기 파일이 생성됨

   <img src="https://github.com/jinmang2/bring_it_on/blob/master/img/Docker/docker_quick_starter.PNG?raw=true">
   
## STEP 4. 설치 확인
- `바탕화면`의 `Docker Quickstart Terminal` 실행

   ```docker
   Creating CA: C:\\Users\\jinma\\.docker\\machine\\certs\\ca.pem
   Creating client certificate: C:\\Users\\jinma\\.docker\\machine\\certs\\cert.pem
   Running pre-create checks...
   (default) Image cache directory does not exist, creating it at C:\\Users\\jinma\\.docker\\machine\\cache...
   (default) No default Boot2Docker ISO found locally, downloading the latest release...
   (default) Latest release for github.com/boot2docker/boot2docker is v19.03.5
   default) Downloading C:\\Users\\jinma\\.docker\\machine\\cache\\boot2docker.iso 
        from https://github.com/boot2docker/boot2docker/releases/download/v19.03.5/boot2docker.iso...
   (default) 0%....10%....20%....30%....40%....50%....60%....70%....80%....90%....100%
   Creating machine...
   default) Copying C:\\Users\\jinma\\.docker\\machine\\cache\\boot2docker.iso 
        to C:\\Users\\jinma\\.docker\\machine\\machines\\default\\boot2docker.iso...
   (default) Creating VirtualBox VM...
   (default) Creating SSH key...
   (default) Starting the VM...
   (default) Check network to re-create if needed...
   (default) Windows might ask for the permission to create a network adapter. 
        Sometimes, such confirmation window is minimized in the taskbar.
   (default) Found a new host-only adapter: "VirtualBox Host-Only Ethernet Adapter #2"
   (default) Windows might ask for the permission to configure a network adapter. 
        Sometimes, such confirmation window is minimized in the taskbar.
   (default) Windows might ask for the permission to configure a dhcp server. 
        Sometimes, such confirmation window is minimized in the taskbar.
   (default) Waiting for an IP...
   Waiting for machine to be running, this may take a few minutes...
   Detecting operating system of created instance...
   Waiting for SSH to be available...
   Detecting the provisioner...
   Provisioning with boot2docker...
   Copying certs to the local machine directory...
   Copying certs to the remote machine...
   Setting Docker configuration on the remote daemon...
   Checking connection to Docker...
   Docker is up and running!
   To see how to connect your Docker Client to the Docker Engine running on this virtual machine, 
        run: C:\\Program Files\\Docker Toolbox\\docker-machine.exe env default
   

                           ##         .
                     ## ## ##        ==
               ## ## ## ## ##    ===
          /"""""""""""""""""\\___/ ===
     ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
          \\______ o           __/
             \\    \\         __/
               \\____\\_______/
               
   docker is configured to use the default machine with IP 192.168.99.100
   For help getting started, check out the docs at https://docs.docker.com
   
   Start interactive shell
   
   jinma@LAPTOP-GLIL0B1N MINGW64 /c/Program Files/Docker Toolbox
   ```
- 위와 같이 고래그림이 뜨면 준비 완료.
- `docker run hello-world`로 테스트해보자.

    ```docker
    jinma@LAPTOP-GLIL0B1N MINGW64 /c/Program Files/Docker Toolbox
    $ docker run hello-world
    Unable to find image \'hello-world:latest\' locally
    latest: Pulling from library/hello-world
    1b930d010525: Pull complete
    Digest: sha256:9572f7cdcee8591948c2963463447a53466950b3fc15a247fcad1917ca215a2f
    Status: Downloaded newer image for hello-world:latest
    
    Hello from Docker!
    This message shows that your installation appears to be working correctly.
    
    To generate this message, Docker took the following steps:
     1. The Docker client contacted the Docker daemon.
     2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
        (amd64)
     3. The Docker daemon created a new container from that image which runs the
        executable that produces the output you are currently reading.
     4. The Docker daemon streamed that output to the Docker client, which sent it
        to your terminal.
    
    To try something more ambitious, you can run an Ubuntu container with:
     $ docker run -it ubuntu bash
     
    Share images, automate workflows, and more with a free Docker ID:
     https://hub.docker.com/
    
    For more examples and ideas, visit:
     https://docs.docker.com/get-started/
    ```
- 위와 같이 `hello-world:latest` 이미지를 pull해온 후 `Hello from Docker!` 및 그 아래의 메세지가 출력된다면 성공.
