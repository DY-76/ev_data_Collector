#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from sqlalchemy import create_engine
import smtp

# Logger
from Logger import set_logger
logger = set_logger()

def parse(item):
    try:
        STATNM = item.find("statNm").get_text()
        STATID = item.find("statId").get_text()
        CHGERID = item.find("chgerId").get_text()
        CHGERTYPE = item.find("chgerType").get_text()
        ADDR = item.find("addr").get_text()
        LOCATION = item.find("location").get_text()
        LAT = item.find("lat").get_text()
        LNG = item.find("lng").get_text()
        USETIME = item.find("useTime").get_text()
        BUSIID = item.find("busiId").get_text()
        BNM = item.find("bnm").get_text()
        BUSINM = item.find("busiNm").get_text()
        BUSICALL = item.find("busiCall").get_text()
        STAT = item.find("stat").get_text()
        STATUPDDT = item.find("statUpdDt").get_text()
        LASTTSDT = item.find("lastTsdt").get_text()
        LASTTEDT = item.find("lastTedt").get_text()
        NOWTSDT = item.find("nowTsdt").get_text()
        OUTPUT = item.find("output").get_text()
        METHOD = item.find("method").get_text()
        ZCODE = item.find("zcode").get_text()
        ZSCODE = item.find("zscode").get_text()
        KIND = item.find("kind").get_text()
        KINDDETAIL = item.find("kindDetail").get_text()
        PARKINGFREE = item.find("parkingFree").get_text()
        LIMITYN = item.find("limitYn").get_text()
        LIMITDETAIL = item.find("limitDetail").get_text()
        DELYN = item.find("delYn").get_text()
        DELDETAIL = item.find("delDetail").get_text()
        return {
            "statNm": STATNM,
            "statId": STATID,
            "chgerId": CHGERID,
            "chgerType": CHGERTYPE,
            "addr": ADDR,
            "location": LOCATION,
            "lat": LAT,
            "lng": LNG,
            "useTime": USETIME,
            "busiId": BUSIID,
            "bnm": BNM,
            "busiNm": BUSINM,
            "busiCall": BUSICALL,
            "stat": STAT,
            "statUpdDt": STATUPDDT,
            "lastTsdt": LASTTSDT,
            "lastTedt": LASTTEDT,
            "nowTsdt": NOWTSDT,
            "output": OUTPUT,
            "method": METHOD,
            "zcode": ZCODE,
            "zscode": ZSCODE,
            "kind": KIND,
            "kindDetail": KINDDETAIL,
            "parkingFree": PARKINGFREE,
            "limitYn": LIMITYN,
            "limitDetail": LIMITDETAIL,
            "delYn": DELYN,
            "delDetail": DELDETAIL
        }
    # 버그나 parsing 항목 이슈 컨트롤을 위한 예외처리
    except AttributeError as e:
        return {
            "statNm": None,
            "statId": None,
            "chgerId": None,
            "chgerType": None,
            "addr": None,
            "location": None,
            "lat": None,
            "lng": None,
            "useTime": None,
            "busiId": None,
            "bnm": None,
            "busiNm": None,
            "busiCall": None,
            "stat": None,
            "statUpdDt": None,
            "lastTsdt": None,
            "lastTedt": None,
            "nowTsdt": None,
            "output": None,
            "method": None,
            "zcode": None,
            "zscode": None,
            "kind": None,
            "kindDetail": None,
            "parkingFree": None,
            "limitYn": None,
            "limitDetail": None,
            "delYn": None,
            "delDetail": None
        }

def Colec(Num, Zcode, DB):
    try:
        """
        ~made for LDY~
        :param Num: 총 호출할 데이터 수 입니다. 지역당 9000개 정도면 충분합니다.
        :param Zcode: 지역코드입니다. 자세한건 가이드 참조
        :param DB: 저장할 DB 명 입니다.
        :return: 수집한 데이터를 DB에 저장합니다.
        """
        # API 호출
        logger.info("API OriginalData Request..")
        url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'
        params ={'serviceKey' : 'Zxc+L1BY7vTH4mkcjzGShFsue5yUAk2q55yjb3nUf7EeeXcsQTv9nE7qIjVN2oU01PuQMJ+iHQGuo2fa2ZlJlw==', 'pageNo' : '1', 'numOfRows' : Num, 'zcode' : Zcode }
        response = requests.get(url, params=params)

        # Item 화
        soup = BeautifulSoup(response.text, 'lxml-xml')
        logger.info("stat : "+soup.find("resultMsg").get_text())
        logger.debug("statCode : "+soup.find("resultCode").get_text())


        items = soup.find_all("item")

        # 데이터 임시저장소
        row = []
        tot_sum = 0
        for item in tqdm(items, ascii=True, desc="Parsing "):
            row.append(parse(item))
            tot_sum += 1

        # pandas 데이터프레임에 넣기
        df = pd.DataFrame(row)

        # 현재 시간기반 테이블명 생성
        now = datetime.now()
        current_time = now.strftime("%Y%m%d%H%M%S")
        current_time = 'origin_'+current_time

        # mysql DB 연결
        # DEBUG용 DB값 = root:0706@localhost/test01
        db_connection_str = 'mysql+pymysql://'+DB
        db_connection = create_engine(db_connection_str)
        conn = db_connection.connect()
        logger.debug("DB Connect!")

        # DB에 df 저장
        df.to_sql(name=current_time, con=db_connection, if_exists='append',index=False)
        logger.debug("DB APPEND COMPLETE!")

    except AttributeError as e:
        logger.debug("DB APPEND FAILED!")
        smtp.sendMail()