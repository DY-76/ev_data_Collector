import smtplib
from email.message import EmailMessage


def sendMail():
    try:
        # STMP 서버의 url과 port 번호
        SMTP_SERVER = 'smtp.gmail.com'
        SMTP_PORT = 465

        # 1. SMTP 서버 연결
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

        EMAIL_ADDR = 'ldy0706test@gmail.com'
        EMAIL_PASSWORD = 'hkpquaivcznztgcl'

        # 2. SMTP 서버에 로그인
        smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)

        # 3. MIME 형태의 이메일 메세지 작성
        message = EmailMessage()
        message.set_content('에러발생!')
        message["Subject"] = "MILAB_evDataCollector 문제 발생 알림"
        message["From"] = EMAIL_ADDR  #보내는 사람의 이메일 계정
        message["To"] = 'tel01030997456@gmail.com'

        # 4. 서버로 메일 보내기
        smtp.send_message(message)

        # 5. 메일을 보내면 서버와의 연결 끊기
        smtp.quit()

    except AttributeError as e:
        pass