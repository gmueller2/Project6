import smtplib
import yagmail

# TO DO:
# fix the emailer tests
# build/run the league tests


class Emailer:

    sender_address = None
    _sole_instance = None

    @classmethod
    def configure(cls, sender_address):
        cls.sender_address = sender_address

    @classmethod
    def instance(cls):  # this needs to be included - also included as something as a singleton
        if cls._sole_instance is None:
            cls._sole_instance = Emailer()
        return cls._sole_instance

    @classmethod
    def send_plain_email(cls, recipients, subject, message):
        yag = yagmail.SMTP('genestestemail@gmail.com')
        try:
            yag.send(to=recipients, subject=subject, contents=message)
            print('Email successfully sent!')
        except yagmail.YagAddressError:
            print('Address has invalid format.')
        except smtplib.SMTPException as auth_error:
            print('Auth format is not supported.')
            print(auth_error)
        except smtplib.SMTPAuthenticationError:
            print('App specific password required.')
        finally:
            yag.smtp.close()


