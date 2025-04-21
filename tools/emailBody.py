import re
from dataclasses import dataclass


@dataclass
class LinkedinJob:
    title: str
    company: str
    url: str


def extractJobs(emailBody):
    # 1. Get content after the first empty line
    parts = emailBody.split('\n\n', 1)
    if len(parts) < 2:
        return []

    content = parts[1]

    # 2. Split into items using the delimiter
    items = content.split('---------------------------------------------------------')

    # 3. Remove leading/trailing whitespace and filter out empty items
    items = [item.strip() for item in items if item.strip()]

    # 4. Remove the last item
    items = items[:-1]

    # 5. Remove empty lines within each item
    cleaned_items = []
    for item in items:
        lines = [line.strip() for line in item.splitlines() if line.strip()]
        cleaned_items.append(lines)

    # 6. Convert each item into an object (Title, Company, URL)
    jobs = []
    for lines in cleaned_items:
        # Find the URL line
        url = None
        for line in lines:
            match = re.search(r'(https://www\.linkedin\.com/comm/jobs/view/\d+[^ ]*)', line)
            if match:
                url = match.group(1)
                break
        if len(lines) >= 2 and url:
            job = LinkedinJob(lines[0], lines[1], url)
            jobs.append(job)

    return jobs


def formatJob(job):
    formattedJob = f'| {job.title[:50].ljust(50)} | {job.company[:30].ljust(30)} | {job.url[:40]} |'
    return formattedJob


def printJob(job):
    formattedJob = formatJob(job)
    print(formattedJob)
