from src.email_sender import EmailSender


email_sender = EmailSender(password="Sebbacapo17ikki", port=587, smtp_server="smtp.gmail.com", username="epache17@gmail.com")
    
email_sender.send_email(sender_email="epache17@gmail.com", body="hola", receiver_email="sebba30015boga@gmail.com", subject="hola otro yo")