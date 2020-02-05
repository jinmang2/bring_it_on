# Port에 대해 공부

## [네트워크 통신에서 포트를 왜 사용하는가? Well-Known port란, 종류](https://jwprogramming.tistory.com/26)
이 글은 2016년 작성.
#### 용어부터 정리
- localhost: 루프백 주소
- 포트
    - 논리적인 접속장소
    - 인터넷 프로토콜인 TCP/IP를 사용할 때에는 클라이언트 프로그램이 네트워크 상의 특정 서버 프로그램을 지정하는 방법으로 사용
- 웹 프로토콜 : HTTP
- 인터넷 프로토콜 TCP/IP

#### 개념
- TCP/IP의 상위 프로토콜을 사용하는 응용프로그램에서는 미리 지정된 포트번호를 가짐
    - 이를 IANA(Internet Assigned Numbers Authority)에 의해 지정
    - "잘 알려진 포트들(Well-known ports)"이라고 부름
- 다른 응용프로그램 프로세스들은 매번 접속할 때마다 포트번호가 동적으로 부여
- 서버 프로그램이 처음 시작되면 지정된 포트번호로 **바인드**
- 바인드되면 두 개의 컴퓨터간 네트워크를 이용한 통신 시, 발신지 컴퓨터에서 출발한 사용자 데이터(패킷)은 TCP/IP의 각 계층을 거치며 
  최종적으로 목적지 주소(IP)를 가진 컴퓨터에 도달
- 데이터를 넘길 pc에는 FTP, Mail, Telnet, SSH, Web 등 다양한 종류의 응용프로그램이 기동
    - 얘네가 TCP/IP의 TCP 프로토콜 위에 만든 network protocol들
- 수신측 컴퓨터가 인터넷 계층에서 패킷을 수신한 후 응용계층으로 데이터를 전달하려고 할 때,
- 컴퓨터 내에 사용중인 **많은 응용프로그램들 중 누구에게** 데이터를 전달해야 하는지 구분해야 함
- 운영체제는 이 때 응용프로그램의 논리적인 주소인 Port 번호를 이용
- 즉, 각각의 응용프로그램(서비스)에 유일한 논리적 주소인 Port 번호를 할당하여, 전송계층에서 응용프로그램을 구분할 수 있도록 함

#### 아하... 그래서 결론?
- IP Address: 컴퓨터를 찾을 때 필요한 주소
- Port: 컴퓨터 안에서 프로그램을 찾을 때 필요한 주소

#### Port Number
- 0~1023포트까지는 **Well-Known Port Number**라고 하며 미리 특수용도로 지정되어 있기 때문에 
- 가급적 개인적으로 테스트용 프로그램을 개발 시에는 이 번호를 피하는 것이 좋음

#### Well-Known Port Number
- 21: FTP
- 22: SSH
- 23: Telnet
    - 인터넷을 통하여 원격지의 호스트 컴퓨터에 접속할 때 지원되는 인터넷 표준 프로토콜
- 25: SMTP(Simple Mail Transfer Protocol)
- 53: DNS
- 61: SNMP(Simple Network Management Protocol)
- 80: HTTP(HyperText Transfer protocol)
    - 인터넷에서, 웹 서버와 사용자의 인터넷 브라우저 사이에 문서를 전송하기 위해 사용되는 통신 규약
- 110: POP3(Post Office Protocol version 3)
    - 인터넷에서 전자 우편을 가져오기 위한 프로토콜
- 115: SFTP
- 135: RPC
- 139: NetBIOS
- 143: IMAP(Internet messaging access protocol)
    - 인터넷 메일 서버에서, 메일을 읽기 위한 인터넷 표준 통신 규약의 한가지. POP3보다도 유연하고 뛰어난 성능
- 194: IRC
- 443: HTTPS(SSL)(HyperText Transfer Protocol over Secure Socket Layer)
    - 월드 와이드 웹(WWW) 통신 프로토콜인 HTTP의 보안이 강화된 버전
- 445: SMB
- 3389: 원격데스크탑 연결

## [컴퓨터에서 말하는 포트(port)란?](https://m.blog.naver.com/PostView.nhn?blogId=onnuri67&logNo=30075970880&proxyReferer=https%3A%2F%2Fwww.google.com%2F)
이 글은 2009년 작성. 최근 글로 다시 봐야함!

#### 지식검색 발췌 자료들

>#### Q1)
- 인터넷에서 일반적인 network application들은 TCP/IP 프로토콜을 사용
- HTTP, FTP, TELNET, SSH, SMTP, POP3 등등은 모두 다 TCP/IP의 TCP 프로토콜 위에다가 만든 네트웤 프로토콜들
- 서버가 되는 머신에는 이런 TCP 커넥션을 받을 수 있는 포트라는걸 열어둠
- 포트번호는 한 IP Address에 1~65535까지 존재
- 1~1023은 Well Known Ports로 잘 알려진 프로토콜들이 사용하는 포트
- 1024~49151까지의 포트는 IANA에 등록된 Registered Ports들
- 49151~65535까지는 Dynamic and/or Private Ports
- [http://www.iana.org/assignments/port-numbers](http://www.iana.org/assignments/port-numbers) 참고
- 포트 설정은 `Firewall`에서 실시
- 최근은 OS에서 지원하기도 함

>#### Q2)
- 영어로 항구(Port), USB 포트, 패러렐 포트(프린터 꽂는 포트) 개념 생각
- 네트워크 상에서 상호간의 컴퓨터를 연결하는 부분 혹은 통로
- 컴퓨터에서 모든 Port가 열려있는 것이 아님
- 방화벽 프로그램, XP서비스팩2의 방화벽 기능, 인터넷 공유기를 사용할 경우 어떤 Port는 막혀있음
- 정확하게 표현하면, HTTP나 IPX 등 일상적으로 사용하는 프로토콜에서 열어줄 필요가 있는 포트를 제외한 다른 모든 포트들은 막혀있음
- 공유기:포트 포워딩, 방화벽에서 특정포트를 여는 방법은 알아서 찾으시길...

## [PORT 역할 및 의미](https://m.blog.naver.com/wind1237/140190026607)
이 글은 2013년에 작성
#### 포트 번호
- PORT 번호는 **TCP와 UDP가 상위 계층에 제공하는 주소 표현 방식**
- 네트워크 서비스를 제공하는 포트 번호는 컴퓨터의 파일 시스템에 보관됨
- 때문에 일반 사용자가 포트 번호를 직접 지정하는 경우는 없음
- 사용자가 연결을 원하는 서버의 호스트 IP 주소만 클라이언트 프로그램에게 지정,
- 포트 번호 선택은 프로그램에서 자동으로 해줌
- TCP와 UDP는 별도의 포트 주소 공간을 관리, 동일한 포트 번호를 사용할 수 있다.
- 즉, 두 프로토콜에서 돌일한 포트 번호를 할당해도 서로 다른 포트로 간주
- 포트
    - 통신포트(COM1, COM2, LPT1, LPT2, USB 포트...)
    - TCP/IP 포트
- 여기서의 포트는 가상의 소프트웨어적인 포트
- 프로토콜 규약인 TCP/IP에서 지정하는 포트, 하드웨어적으로 연결이 된 네트워크망에서 
- 컴퓨터들끼리 서로 통신을 하는데 필요한 규약이 TCP/IP에서 통신을 할 때 동시다발적인 통신을 가능케 하기 위하여
- 포트라는 가상의 "문"이 정의되는 것
- TCP/IP는 인터넷의 기본적인 통신 프로토콜, 인트라넷이나 엑스트라넷과 같은 사설 망에서도 사용

#### Well-Known Port Number
- 0: Researved
- 1: TCP MUX(TCP 멀티플렉스)
- 5: RJE(Remote Job Entry)
- 7: ECHO
- 9: DISCARD
- 11: SYSTAT(활성 사용자)
- 13: DAYTIME(주간)
- 15: NETSTAT(네트워크 상태 프로그램)
- 17: QOTD(해당일 인용문)
- 19: CHARGEN(문자 발생기)
- 20: FTP-DATA(파일전송 프로토콜(데이터))
- 21: FTP(파일전송 프로토콜)
- 23: TELNET(단말기 연결)
- 25: SMTP(간단한 메일 전송 프로토콜)
- 37: TIME(시간)
- 42: NAME(호스트 이름)
- 43: WHOIS(누구)
- 53: NAMESERVE(도메인 이름 서버)
- 79: FINGER(finger)
- 101: HOSTNAMES(NIC 호스트 이름 서버)
- 103: X400(X400 메일 서비스)
- 113: AUTH(인증 서비스)
- 117: UUCP-PATH(UUCP 경로 서비스)
- 119: NNTP(USENET 뉴스 전송 프로토콜)
- 129: PWDGEN(암호 발생기 프로토콜)
- 160-223: RESERVED(예약되어 있음)



