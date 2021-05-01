# massive-email-receiver
Just receive and store emails. 

Configure config.yml, for example:

```yaml
motor:
  uri: mongodb://localhost

massive_email_receiver:
  hostname: localhost
  port: 20025
  mongo_database: emails
```

and run `python main.py`

# Test the server
You can use this snippet

```python
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('This is a test')

src = "test@example.com"
dst = "me@lol.com"
msg['Subject'] = 'My subject'
msg['From'] = src
msg['To'] = dst

s = smtplib.SMTP('127.0.0.1', port=20025)
s.sendmail(src, [dst], msg.as_string())
s.quit()
```

Run the server and this test client and your mongo database should have the sent messages
