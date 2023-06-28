# The Things Stack - LoRaWAN

<details>
<summary> 목차 </summary>

1. [개요](#개요)
1. [삽질일기](#1-삽질일기)
    - docker - Incorrect function
    - tls error
    - localhost issue
    - CLIENT_SECRET
    - the things network's freq
2. [TTS on Docker](#2-the-things-stack을-docker에서-돌려보자)
3. [Append Device to TTN](#3-lorawan에-기기를-등록-해보자)
</details>

## 0. 개요
- 개발 목적

  현재 시대에서는 각종 공과금이나 소비량을 실시간으로 확인하고 관리하는 것이 중요하다고 생각한다.  
  특히, 가스 사용량이 많은 가정이나 사업체에서는 이러한 관리가 중요하다 생각한다.  
  이를 위해 실시간으로 가스 요금을 확인할 수 있는 플랫폼의 개발이 필요하다고 생각하였다.

- BLE vs LoRa

    | 기능 | Bluetooth Low Energy (BLE) | Long Range (LoRaWAN) |
    |---|---|---|
    | 전송 거리 | 최대 100m | 수 km 이상 |
    | 전력 소비 | 저전력 기술 | 매우 저전력 기술 |
    | 데이터 전송 속도 | 1Mbps 이상 | 최대 50kbps |
    | 안전성 | AES-128 | AES-128 |
    | 연결 가능한 기기 수 | 1:7 (BLE 5.0 - 1:1000) | 1:1000 |
    | Downlink | 매우 용이. 직접 연결되어 있기 때문에 실시간으로 downlink 메시지 전송 가능 | 비교적 덜 용이. Downlink 메시지는 장치의 수신 창 동안에만 전송 가능하며, 네트워크 및 전력 소모에 대한 제한이 있음 |


    위의 표를 보다시피 LoRaWAN이 블루투스보다 전력을 적게 사용한다는 것을 볼 수 있다. 따라서 LoRaWAN을 사용하여 개발하고자 한다.

- 개발 환경
    - OS : windows 10 edu 22H2
    - WSL version : wsl2
    - Linux Kernel : Ubuntu 22.04.02 LTS
    - Docker version : 4.18.0

- 개발 기기
    - [HT-M00](https://heltec.org/project/ht-m00/)
    - [lora 32 v2](https://heltec.org/project/wifi-lora-32/)

<div style="text-align: right"><a href="#">top</a></div>

## 1. 삽질일기
1. docker에서 공식 문서에서 제공하는 docker-compose.yml을 docker-compose up으로 실행하니 
    ```
    read C:\Users\<User>\.env: Incorrect function
    ```
    오류가 발생하였음.

    volumes에서 .env를 참조하는데, 이 부분이 문제가 된 것으로 판단하여 해당 부분을 주석 처리하였음

1. TLS 문제
    
    https로 접근을 하려니 tls 인증 서버가 없어 오류 발생
    
    https 대신 http 사용하도록 변경

1. localhost

    localhost로 하니 로그인 token 오류가 발생.

    임시로 현재 ip를 적고, 추후에 dns 설정으로 해결하면 됨

1. token 오류

    OAuth 생성 단계에서 CLIENT_SECRET을 잘못 입력하여 auth가 제대로 되지 않던 문제

    [trouble shooting](https://www.thethingsindustries.com/docs/the-things-stack/host/docker/configuration/#running-the-things-stack-as-localhost) - localhost에서는 1885로 redirect 하지 않는다고 한다.

1. TTN 주파수

    [한국에서 사용 가능한 lora 주파수](https://www.3glteinfo.com/lora/lorawan-frequency-bands/)

    [The Things Network에서 지원하는 lorawan 주파수](https://www.thethingsnetwork.org/docs/lorawan/frequency-plans/)

    TTN에서 제공하는 주파수를 사용하여야 하였으나, 한국에서 사용 가능한 lora 주파수를 gateway에 입력해서 연결이 되지 않았다.


<div style="text-align: right"><a href="#">top</a></div>

***
## 2. The Things Stack을 Docker에서 돌려보자

1. [The Things Stack - docker overview](https://www.thethingsindustries.com/docs/the-things-stack/host/docker/)
1. [The Things Stack - configuration](https://www.thethingsindustries.com/docs/the-things-stack/host/docker/configuration/)
1. [The Things Stack - running](https://www.thethingsindustries.com/docs/the-things-stack/host/docker/running-the-stack/)
1. [The Things Network - support freq](https://www.thethingsnetwork.org/docs/lorawan/frequency-plans/)
1. [MMYU - leisure guardian](https://github.com/LeisureGuardian/LG-API)

위 사이트들를 참고하여 작성하였다.

1. 먼저 [configuration files](https://www.thethingsindustries.com/docs/the-things-stack/host/docker/configuration/#example-configuration-files)에 들어가 Open Source 파일을 받자.

    이때 docker-compose.yml과 ttm-lw-stack-docker.yml을 다운 받는다.

    docker-compose.yml에서 postgres와 redis의 volumes를 주석 처리하자.
    volumes는 사용자 로컬에 저장하겠다는 의미이기에 컨테이너를 지우지 않는 이상 신경 쓸 필요 없다.

1. 폴더 구조를 아래와 같이 만든다.
    ```
    docker-compose.yml
    config/
    └── stack/
        └── ttn-lw-stack-docker.yml
    ```

1. ttn-lw-stack-docker.yml에서 아래의 사항들을 변경한다.
    ```
    https => http
    thethings.example.com => <your ip or dns>
    ```
    이때, your ip에 localhost를 적는 어리석은 짓은 하지 말자. 로그인 시 oauth 오류가 발생한다.

1. 이미지 가져오기

    ``` bash
    docker-compose pull
    ``` 
    
    명령어를 통해 postgres, redis, thethingsnetwork의 도커 이미지를 받아오자.

1. 데이터베이스 초기화

    도커 이미지를 받아왔다면 docker-compose.yml이 있는 최상위 폴더로 이동해 

    ``` bash
    docker-compose run --rm stack is-db migrate
    ``` 

    명령어를 입력해 데이터베이스를 migration 해주자. 이때, postgres가 켜지는 시간이 있으므로, 오류가 뜬다고 해서 당황하지 말고 여러 번 명령어를 입력해주자.
    
1. 유저 등록
    ``` bash
    docker-compose run \
        --rm stack is-db create-admin-user \
        --id admin \
        --email your@email.com
    ```
    명령어를 입력하여 admin 계정을 만들어주도록 하자. 이 명령어에서 admin 계정의 비밀번호를 설정하게 된다.

    윈도우의 아래 명령어로 입력하자.
    ``` shell
    docker-compose run --rm stack is-db create-admin-user --id admin --email your@email.com
    ```

1. OAuth 설정

    로그인 및 회원가입을 위해선 OAuth 설정이 필요하다.

    id는 console/oauth/client-id, secret은 console/oauth/client-secret을 사용하면 된다.

    ``` bash
    SERVER_ADDRESS=https://thethings.example.com
    ID=console
    NAME=Console
    CLIENT_SECRET=console
    REDIRECT_URI=${SERVER_ADDRESS}/console/oauth/callback
    REDIRECT_PATH=/console/oauth/callback
    LOGOUT_REDIRECT_URI=${SERVER_ADDRESS}/console
    LOGOUT_REDIRECT_PATH=/console
    docker-compose run --rm stack is-db create-oauth-client \
    --id ${ID} \
    --name "${NAME}" \
    --owner admin \
    --secret "${CLIENT_SECRET}" \
    --redirect-uri "${REDIRECT_URI}" \
    --redirect-uri "${REDIRECT_PATH}" \
    --logout-redirect-uri "${LOGOUT_REDIRECT_URI}" \
    --logout-redirect-uri "${LOGOUT_REDIRECT_PATH}"
    ```

    윈도우에서는 해당 명령어가 작동하지 않을 수 있다. 노가다지만 하나 하나 변수에 맞게 넣는 수밖에 없다.(나도 그랬다.)

    &lt;DOMAIN&gt;을 자신의 서버 주소, &lt;SECRET&gt;를 ttn-lw-stack-docker.yml의 console/oauth/cilent-secret으로 바꾸자.
    ``` shell
    docker-compose run --rm stack is-db create-oauth-client --id console --name "Console" --owner admin --secret "<SECRET>" --redirect-uri "https://<DOMAIN>/console/oauth/callback" --redirect-uri "/console/oauth/callback" --logout-redirect-uri "https://<DOMAIN>/console" --logout-redirect-uri "/console"
    ```

1. 도커 실행

    ```
    docker-compose up
    ```
    
    명령어를 통해 docker를 실행하고, localhost로 접속을 해보자.

    ```
    error during connect: this error may indicate that the docker daemon is not running
    ```

    위의 오류가 발생하였다면, docker desktop이 실행중인지 확인하자.

    로그인 후 아래의 사진의 페이지로 들어와진다면 성공이다.
    
    ![tts_console](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/dd77682a-adfa-4ddf-bfaa-8195fc01f18c)
    
    이후 lora gateway를 등록해보자.

<div style="text-align: right"><a href="#">top</a></div>

***
## 3. LoRaWAN에 기기를 등록 해보자.

1. 게이트웨이 등록
    
    게이트웨이는 Heltec Inc.의 HT-M00을 사용하였다.

    ![ht-m00_setting](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/bc03ed0d-7e43-47c3-a9b8-31b965cc81b5)
    
    HT-M00 설정 창. 설정 방법은 [이곳](https://docs.heltec.org/en/gateway/ht-m00/quick_start.html#configure-the-gateway)을 확인하자.
    
    WiFi는 2.4GHz로 연결하자. 5GHz를 지원하지 않는다.
    
    서버 주소는 본인이 연 The Things Stack 서버의 IP 주소 및 DNS를 입력하자.
    
    포트는 1700 고정이다.
    
    컴퓨터 방화벽에서 1700 포트를 UDP로 열자!

    ![tts_console_register_gateway](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/f5171ea3-e603-4949-b783-9609990f33d5)
    
    TTS Console에서 게이트웨이 등록
    
    Gateway ID는 Gateway EUI를 기준으로 자동으로 설정된다.
    
    Frequency plan은 한국에서 사용하므로 South Korea로 설정하자.
    
    ***Require authenticated connection은 체크 해제하자!***
    
    해당 옵션이 켜져있으면 연결이 제대로 되지 않는다. 이 부분에서 삽질을 많이 했다.

    ![tts_console_edit_gateway](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/616e1359-66cc-4a4a-8f9d-6b183a72d457)
    
    TTS Console 게이트웨이 General Setting에서 서버 주소 등록
    
    HT-M00에 등록한 서버 주소를 넣자.
    
    ![KakaoTalk_20230530_211721452](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/b78d4199-2846-4344-843b-8b825c134059)

    TTS Console에 연결된 게이트웨이 상황
    
    위의 과정을 잘 따라왔다면, 위와 같이 연결이 되었다고 뜰 것이다.

1. Application 생성

    lora node를 등록하기 위해서는 Application을 생성해줘야 한다.

    Application 탭에 들어가서 Create Application을 누르자.

    ![1-1](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/17d0a451-9136-436b-bf0c-86e11d299ac6)

    Application Name을 입력한 후 Create Application 버튼을 누르자.

    ![1-2](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/216a47d0-bb8f-44e5-8ee9-7aa3cc3fc571)

    Application을 만들었다면, 아래의 화면이 뜰 것이다.  
    Register end device를 누르자.
   
    ![1-3](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/8e17507d-c809-4fea-8478-2ab8704bacdc)

1. lora node 등록

    현재 [lora 32 v2](https://heltec.org/project/wifi-lora-32/)를 node로 사용하고자 한다.  
    아래와 같이 입력하자.  
    단, JoinEUI는 다르게 설정해도 상관없다. 우리는 JoinEUI를 재설정할 수 있다.

    ![2-1](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/61aa314e-6f64-4e66-897f-1f70f76acedd)

    위와 같이 입력하였다면, Arduino IDE를 켜자.  
    여기서부터는 잠시 다른 github repo를 참고하도록 한다.  
    [Heltec ESP32+LoRa Series Quick Start](https://docs.heltec.org/en/node/esp32/quick_start.html)  
    [Heltec_ESP32 Library](https://github.com/HelTecAutomation/Heltec_ESP32)  
    위 두 사이트를 참고하여 dependency를 설정하고, library를 다운받는다.

    이후 `file - examples - ESP32_LoRaWAN - OTAA_OLED` 예제를 사용해 진행한다. OLED가 없는 경우, `file - examples - ESP32_LoRaWAN - OTAA`를 사용한다.  
    해당 예제를 열면 45-49줄에 아래와 같은 코드가 뜰 것이다.  
    모든 값은 MSB로 등록한다.
    
    ``` c
    /*license for Heltec ESP32 LoRaWan, quary your ChipID relevant license: http://resource.heltec.cn/search */
    uint32_t  license[4] = {0x00000000,0x00000000,0x00000000,0x00000000};
    /* OTAA para*/
    uint8_t DevEui[] = { 0x22, 0x32, 0x33, 0x00, 0x00, 0x88, 0x88, 0x02 };
    uint8_t AppEui[] = { 0x70, 0xB3, 0xD5, 0x7E, 0xD0, 0x02, 0xB1, 0x8A };
    uint8_t AppKey[] = { 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x66, 0x01 };
    ```
    <details>
    <summary><del>license 발급</del></summary>

    현재 오류로 인해 작동되지 않음. 하지만 발급받는 법을 알고싶은 사람을 위해 남겨둔다.

    library를 다운받았으면 아래 사진과 같이 `file - examples - esp32 - GetChipID` 를 이용해 ChipID를 얻자.  
    이후 Serial Monitor를 이용해 Chip ID를 얻을 수 있다.

    ```
    ESP32 Chip model = ESP32-D0WDQ6 Rev 1
    This chip has 2 cores
    ESP32ChipID=34554CA8CCXX
    ```
    해당 ChipID를 [license](http://www.heltec.cn/search/)를 얻는 사이트에 넣으면 license가 나오게 된다. 잘 메모해두자.

    얻은 값을 위의 코드부의 license에 넣는다.
    </details>

    **현재(23.06.28) license를 이용해 코드를 실행하면 아래의 오류가 발생**
    ``` c
    ELF file SHA256: 0000000000000000

    Rebooting...
    ets Jun  8 2016 00:22:57

    rst:0xc (SW_CPU_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
    configsip: 0, SPIWP:0xee
    clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
    mode:DIO, clock div:1
    load:0x3fff0030,len:1344
    load:0x40078000,len:13864
    load:0x40080400,len:3608
    entry 0x400805f0
    ESP32 MCU init...

    abort() was called at PC 0x4008258e on core 1


    Backtrace:0x40083ca9:0x3ffb2660 0x40089239:0x3ffb2680 0x4008e01d:0x3ffb26a0 0x4008258e:0x3ffb2720 0x40082b64:0x3ffb2770 0x400d505c:0x3ffb2790 0x400d57ed:0x3ffb27b0 0x400d1896:0x3ffb27f0 0x400dbd6e:0x3ffb2820
    ```
    해결 방법은 [이곳](https://github.com/HelTecAutomation/ESP32_LoRaWAN/issues/91#issuecomment-1279974663)을 참고하자.

    먼저, 아래와 같이 설정하자. 
    - Gateway가 달라지면 설정이 달라질 수 있다.  
    Gateway의 스펙을 잘 알아두자.  
    - port는 해당 보드가 연결된 port를 선택하면 된다.  
    장치 관리자에서 CP210x의 COM포트를 찾자.
    - 한국은 REGION_KR920을 선택하면 된다.
    - DEVEUI는 CUSTOM으로 사용해도 되고, GenerateByChipId를 사용해도 된다.  
    둘 다 DEVEUI를 출력해준다.

    ![2-3](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/500f6133-b24e-4b7e-8a88-390a20cf0238)

    ![2-4](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/fbc11743-749e-475c-b821-5e37549b57f0)

    위와 같은 DevEUI를 얻은 경우, 다시 Application 설정으로 돌아가자.  
    얻은 DevEUI를 넣고, AppEUI를 generate 해주자.

    해당 과정을 완료하면 아래와 같은 화면일 것이다.  
    DevEui, AppEui, AppKey를 MSB로 코드에 넣자.  
    빨간 버튼을 누르면 헥사코드로 바꿔준다. 잘 이용하자.

    ![2-5](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/375803b5-b46f-4de5-bb0c-d115ff8da3c5)

    노드 화면이 아래와 같이 되어있다면 연결이 된 것이다.

    ![2-6](https://github.com/kit-teamcook-2023/the-things-stack_lora/assets/81803973/53d6c2b2-518b-4723-9d70-7ba08cb08276)

<div style="text-align: right"><a href="#">top</a></div>
