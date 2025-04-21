emailBody1 = """Your job alert for software developer in Greater Melbourne Area
30+ new jobs match your preferences.

Software Engineer - Web Developer
micro1
APAC
This company is actively hiring
View job: https://www.linkedin.com/comm/jobs/view/4207844770/?trackingId=0123456789

---------------------------------------------------------


Senior Software Engineer - Product Engineering
Displayr
Australia
Apply with resume & profile
View job: https://www.linkedin.com/comm/jobs/view/4207297676/?trackingId=0123456789

---------------------------------------------------------


Software Engineer
Send Payments
Australia
This company is actively hiring
Apply with resume & profile
View job: https://www.linkedin.com/comm/jobs/view/4206446154/?trackingId=0123456789

---------------------------------------------------------


Software Engineer - L3 Support
Canonical
Melbourne, VIC
1 school alum
View job: https://www.linkedin.com/comm/jobs/view/4208215839/?trackingId=0123456789

---------------------------------------------------------


C++ Competitive Programming Checker
micro1
APAC
This company is actively hiring
View job: https://www.linkedin.com/comm/jobs/view/4208220524/?trackingId=0123456789

---------------------------------------------------------

See all jobs on LinkedIn:  https://www.linkedin.com/comm/jobs/search?geoId=90009521


Job search smarter with Premium
https://www.linkedin.com/comm/premium/products/?upsellOrderOrigin=email_job_alert_digest_taj_upsell&utype=job&lipi=urn%3Ali%3Apage%3Aemail_email_job_alert_digest_0123456789


----------------------------------------

This email was intended for me 😀
Learn why we included this: https://www.linkedin.com/help/linkedin/answer/4788?lang=en&lipi=urn%3Ali%3Apage%3Aemail_email_job_alert_digest_0123456789
You are receiving Job Alert emails.
Manage your job alerts:  https://www.linkedin.com/comm/jobs/alerts?lipi=urn%3Ali%3Apage%3Aemail_email_job_alert_digest_0123456789
Unsubscribe: https://www.linkedin.com/job-alert-email-unsubscribe?savedSearchId=0123456789

© 2025 LinkedIn Corporation, 1zwnj000 West Maude Avenue, Sunnyvale, CA 94085.
LinkedIn and the LinkedIn logo are registered trademarks of LinkedIn.
"""

emailBody2 = """Your job alert for software developer in Melbourne
30+ new jobs match your preferences.

Senior Full Stack Engineer - Contract - Immediate Start
Davidson
Melbourne, VIC
1 company alum
View job: https://www.linkedin.com/comm/jobs/view/4207298100/?trackingId=0123456789

---------------------------------------------------------


Senior Software Engineer
preezie
Greater Melbourne Area
1 school alum
Apply with resume & profile
View job: https://www.linkedin.com/comm/jobs/view/4206245041/?trackingId=0123456789

---------------------------------------------------------


Senior .Net Developer
Bupa
Melbourne, VIC
2 connections
View job: https://www.linkedin.com/comm/jobs/view/4206241653/?trackingId=0123456789

---------------------------------------------------------


Senior Software Engineer
Frostbite
Melbourne, VIC
View job: https://www.linkedin.com/comm/jobs/view/4204924192/?trackingId=0123456789

---------------------------------------------------------


Technical Lead
Suncorp Group
Greater Melbourne Area
1 company alum
View job: https://www.linkedin.com/comm/jobs/view/4206265621/?trackingId=0123456789

---------------------------------------------------------


Senior Software Engineer - C# .Net
WiseTech Global
Melbourne, VIC
This company is actively hiring
View job: https://www.linkedin.com/comm/jobs/view/4185411066/?trackingId=0123456789

---------------------------------------------------------

See all jobs on LinkedIn:  https://www.linkedin.com/comm/jobs/search?geoId=100992797


Job search smarter with Premium
https://www.linkedin.com/comm/premium/products/?upsellOrderOrigin=email_job_alert_digest_taj_upsell&utype=job&lipi=urn%3Ali%3Apage%3Aemail_email_job_alert_digest_0123456789


----------------------------------------

This email was intended for me 😀
Learn why we included this: https://www.linkedin.com/help/linkedin/answer/4788?lang=en&lipi=urn%3Ali%3Apage%3Aemail_email_job_alert_digest_0123456789
You are receiving Job Alert emails.
Manage your job alerts:  https://www.linkedin.com/comm/jobs/alerts?lipi=urn%3Ali%3Apage%3Aemail_email_job_alert_digest_0123456789
Unsubscribe: https://www.linkedin.com/job-alert-email-unsubscribe?savedSearchId=0123456789

© 2025 LinkedIn Corporation, 1zwnj000 West Maude Avenue, Sunnyvale, CA 94085.
LinkedIn and the LinkedIn logo are registered trademarks of LinkedIn.
"""

from pathlib import Path
import sys
sutPath = str(Path(Path(__file__).parent.parent.parent, 'tools'))
sys.path.insert(1, sutPath)
print(f'SUT path: {sutPath}')

import emailBody


def __printJobs(jobs):
    charCount = len(emailBody.formatJob(jobs[0]))
    print("-" * charCount)
    for job in jobs:
        emailBody.printJob(job)
    print("-" * charCount)


if __name__ == "__main__":
    jobs = emailBody.extractJobs(emailBody1)
    if len(jobs) != 5:
        raise Exception(f'Expecting 5 jobs but found {len(jobs)}.')
    __printJobs(jobs)

    jobs = emailBody.extractJobs(emailBody2)
    if len(jobs) != 6:
        raise Exception(f'Expecting 5 jobs but found {len(jobs)}.')
    __printJobs(jobs)
