# The Things Stack - LoRa

## 삽질일기

1. docker에서 공식 문서에서 제공하는 docker-compose.yml을 docker-compose up으로 실행하니 
    ```
    read C:\Users\<User>\.env: Incorrect function
    ```
    오류가 발생하였음.

    volumes에서 .env를 참조하는데, 이 부분이 문제가 된 것으로 판단하여 해당 부분을 주석 처리하였음

2. TLS 문제
    
    https로 접근을 하려니 tls 인증 서버가 없어 오류 발생
    
    https 대신 http 사용하도록 변경

3. localhost

    localhost로 하니 로그인 token 오류가 발생.

    임시로 현재 ip를 적고, 추후에 dns 설정으로 해결하면 됨

4. token 오류

    OAuth 생성 단계에서 CLIENT_SECRET을 잘못 입력하여 auth가 제대로 되지 않던 문제

## The Things Stack을 Docker에서 돌려보자!

0. [The Things Stack - docker overview](https://www.thethingsindustries.com/docs/the-things-stack/host/docker/)
1. [The Things Stack - configuration](https://www.thethingsindustries.com/docs/the-things-stack/host/docker/configuration/)
2. [The Things Stack - running](https://www.thethingsindustries.com/docs/the-things-stack/host/docker/running-the-stack/)

위 사이트들를 참고하여 작성하였다.

1. 윈도우 10 edu 22H2, wsl2, ubuntu 22.04.2 LTS, docker 4.18.0 을 기준으로 한다.



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
    thethings.example.com => <your ip>
    ```
    이때, your ip에 localhost를 적는 어리석은 짓은 하지 말자. 로그인 시 oauth 오류가 발생한다.

1. 이미지 가져오기

    ``` docker pull ``` 
    
    명령어를 통해 postgres, redis, thethingsnetwork의 도커 이미지를 받아오자.

1. 데이터베이스 초기화

    도커 이미지를 받아왔다면 docker-compose.yml이 있는 최상위 폴더로 이동해 

    ```docker-compose run --rm stack is-db migrate``` 

    명령어를 입력해 데이터베이스를 migration 해주자. 이때, postgres가 켜지는 시간이 있으므로, 오류가 뜬다고 해서 당황하지 말고 여러 번 명령어를 입력해주자.
    
1. 유저 등록
    ```
    docker-compose run \
        --rm stack is-db create-admin-user \
        --id admin \
        --email your@email.com
    ```
    명령어를 입력하여 admin 계정을 만들어주도록 하자. 이 명령어에서 admin 계정의 비밀번호를 설정하게 된다.

1. OAuth 설정

    로그인 및 회원가입을 위해선 OAuth 설정이 필요하다.

    id는 console/oauth/client-id, secret은 console/oauth/client-secret을 사용하면 된다.

    ```
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

1. 도커 실행

    ```docker-compose up```
    
    명령어를 통해 docker를 실행하고, localhost로 접속을 해보자.

    ```error during connect: this error may indicate that the docker daemon is not running```

    위의 오류가 발생하였다면, docker desktop이 실행중인지 확인하자.

    로그인 후 아래의 사진의 페이지로 들어와진다면 성공이다.