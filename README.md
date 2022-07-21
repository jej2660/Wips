# Wips
## Summary

본 프로젝트 Wips는 비인가 AP를 탐색 하여 무선 네트워크 상에서 발생 할 수 있는 보안 위협을 해결 할 수 있는 도구이다.  고가의 보안장비 도입 없이 Monitor mode 를 지원하는 랜카드가 장착된 pc만 존재 한다면 동일한 기능을 구현 가능하다. 라즈베리파이 같은 소형 pc에 프로그렘을 탑재하여 사용할 경우 높은 경제성을 기대한다. 
또한 해당 프로젝트의 경우 대부분의 소스코드가 python으로 작성 하였기 때문에 OS 별 platform 별 호환성이 뛰어나다.

## Update(2022.07.21)
* 무선 환경에서 사용가능한 방화벽 도입
* 라즈베리파이 포팅 및 모니터 모드가 가능한 무선 랜카드로 소규모 wips 구현
* Block List page 구현

## How to start

### Requirment

- monitor mode 지원 랜카드
- python3

```bash
$ pip install requirement.txt
$ sudo ./setup.sh
$ cd ./web
$ sudo python ./main.py flask run
```

## License

**MIT License**

## 외부 리소스 정보

https://github.com/secdev/scapy **GNU General Public License v2.0**

[https://github.com/pallets/flask/](https://github.com/pallets/flask/)  clause BSD License
