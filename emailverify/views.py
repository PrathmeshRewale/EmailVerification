from django.http import HttpResponse, JsonResponse
import re
import dns.resolver
import socket
import smtplib
from datetime import datetime


def index(request, email):

    #Split email Address
    EmailAddress = email
    x = EmailAddress.split('@')


    EmailUser = x[0] # Email User
    EmailDomain = x[1] # Email Domain

    # set all value to null by default
    result = ''
    reason = ''
    isaccept_all = False

    #DNS Check
    try:
        records = dns.resolver.query(EmailDomain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
    except:
        data = {'email': EmailAddress,
                'result': "undeliverable",
                'reason': "invalid_domain",
                'disposable': False,
                'accept_all': False,
                'free': False,
                'user': EmailUser,
                'domain': EmailDomain,
                'mx':"No MX Found",
                'created_at': datetime.now()}

        return JsonResponse(data)
    

    # check if Email Domain Allows Free Emails To Create
    def freeEmailDomain(EmailDomain):
        a_file = open("freemailsdomain.txt","r")
        readlines = a_file.readlines()
        Types = [line.split(",") for line in readlines][0]
        if EmailDomain in Types:
            return True
        else:
            return False


    # check If Email Domin Allows Disposable Emails To Create
    def checkdisposable(EmailDomain):
        a_file = open("disposableemailsdomain.txt","r")
        readlines = a_file.readlines()
        Types = [line.split(",") for line in readlines][0]
        if EmailDomain in Types:
            return True
        else:
            return False
    

    # Check If Domain Also Accepts Invalid Emails
    def checkacceptall(EmailDomain):
        a_file = open("acceptalldomain.txt","r")
        readlines = a_file.readlines()
        Types = [line.split(",") for line in readlines][0]
        if EmailDomain in Types:
            return True
        else:
            #return False
            b_file = open("nonacceptalldomain.txt","r")
            readliness = b_file.readlines()
            Typess = [line.split(",") for line in readliness][0]
            if EmailDomain in Typess:
                return False
            else:
                #return True
                FakeUse = "1hbyu7j7it676"
                FakeEmail = FakeUse + EmailDomain
            #     # Get local server hostname
                host = socket.gethostname()
                # return True
            #     # SMTP lib setup (use debug level for full output)
                server = smtplib.SMTP()
                server.set_debuglevel(0)

            #     #Email From
                Username = "no-reply"
                DomainFrom = socket.gethostname()
                From_Me = Username + DomainFrom

            #     # SMTP Conversation
                server.connect(mxRecord)
                server.helo(host)
                server.mail(From_Me)
                code, message = server.rcpt(str(FakeEmail))
                server.quit()

            #     # Assume 250 as Success
                if code == 250:
            #         #append to file
                    f = open("acceptalldomain.txt", "a")
                    f.write(","+EmailDomain)
                    f.close()
                    return True;
            #         #print('Success')
                else:
                    return False;
                    f = open("nonacceptalldomain.txt", "a")
                    f.write(","+EmailDomain)
                    f.close()
            #         #print('Bad')

    

    #check Syntax
    #addressToVerify ='info@scottbrady91.com'
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', EmailAddress)

    # return HttpResponse(match)
    if match == None:
        pass
    else:
        

        # Check MailBox Exists
        # Get local server hostname
        host = socket.gethostname()

        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)

        # SMTP Conversation
        server.connect(mxRecord)
        server.helo(host)
        server.mail('me@domain.com')
        code, message = server.rcpt(str(EmailAddress))
        server.quit()

        # if code == 250:
        #     return JsonResponse(data)
        # else:
        #     return JsonResponse(data)

        #check result of email
        if checkdisposable(EmailDomain) or checkacceptall(EmailDomain) or freeEmailDomain(EmailDomain):
            result = "risky"
        elif code == 250 and checkdisposable(EmailDomain) == False and checkacceptall(EmailDomain) == False and freeEmailDomain(EmailDomain) == False:
            result = "deliverable"
        else:
            result = "undeliverable"

        # check Email Reason
        if checkacceptall(EmailDomain):
            reason = "accept_all"
        elif checkdisposable(EmailDomain) or freeEmailDomain(EmailDomain):
            reason = "disposable"
        elif code == 250 and checkdisposable(EmailDomain) == False and checkacceptall(EmailDomain) == False and freeEmailDomain(EmailDomain) == False:
            reason = "accepted_email"

        data = {'email': EmailAddress,
                'result': result,
                'reason': reason,
                'disposable': checkdisposable(EmailDomain),
                'accept_all': checkacceptall(EmailDomain),
                'free': freeEmailDomain(EmailDomain),
                'user': EmailUser,
                'domain': EmailDomain,
                'mx':mxRecord,
                'created_at': datetime.now()}

    return JsonResponse(data)
        # Assume 250 as Success
        # if code == 250:
        #     return JsonResponse(data)
        # else:
        #     return JsonResponse(data)

    

    

    

    # data = [{'name': 'Peter', 'email': 'peter@example.org'},
    #         {'name': 'Julia', 'email': 'julia@example.org'}]

    # return JsonResponse(data, safe=False)