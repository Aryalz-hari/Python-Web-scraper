
from csv import writer
from wsgiref import headers
from bs4 import BeautifulSoup
import requests
with open('data4.csv','a', encoding='utf8', newline='') as f:
    the_writer = writer(f)
    header = [ 'CompanyName', 'Address', 'Phone','Email','link']
    the_writer.writerow(header)

    for i in range(1,59):

        html_text = requests.get(
            f"https://www.sahakariakhabar.com/cooperative-directory?page={i}"
        ).text

        soup = BeautifulSoup(html_text, 'lxml')
        jobs= soup.find_all('div', class_="col-lg-9 col-md-8")


        for job in jobs:
                job_title = job.find('div', class_='post-content')
                title_tag = job_title.find("h2").find("a")
                CompanyName = title_tag.get_text(strip=True)
                link = title_tag["href"]

        # Paragraph text (split by <br>)
                info_lines = job_title.find("p").get_text("\n", strip=True).split("\n")

                Address = info_lines[0].replace("Address:", "").strip()
                Phone = info_lines[1].replace("Phone:", "").strip()
                Email = info_lines[2].replace("Email:", "").strip()

                info=[CompanyName, Address,Phone,Email,link]
                the_writer.writerow(info)
