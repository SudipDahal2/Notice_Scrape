def scrape_notices():
    from bs4 import BeautifulSoup
    import requests 
    import warnings
    import urllib #python library for handling URLs


    # Get the web page content
    url = "https://iost.tu.edu.np/notices"

    response = requests.get(url,verify=False) #HTTPS request bypass -> HTTP
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    notices_data = []

    # Find and print all the links
    # for link in soup.find_all('a'):
    #     print(link.get('href'))

    for notice in soup.select('.recent-post-wrapper'):
        title = notice.find('h5').get_text(strip=True)
        notice_link = notice.find('a')['href']
        #notices.append({'title': title, 'link': link})
        notice_link = urllib.parse.urljoin(url, notice_link)  # urllib.parse.urljoin() ensures relative links become full URLs
    # print(notices)

    # Visit notice page
        detail_response = requests.get(notice_link, verify=False)
        detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

        file_link = None


        # Check for PDF
        pdf_tag = detail_soup.find('a', href=lambda href: href and href.endswith('.pdf'))
        if pdf_tag:
            file_link = urllib.parse.urljoin(notice_link, pdf_tag['href'])

        # If no PDF, check for image
        if not file_link:
            img_tag = detail_soup.find('img')
            if img_tag and img_tag.get('src'):
                file_link = urllib.parse.urljoin(notice_link, img_tag['src'])

        notices_data.append({
            'title': title,
            'notice_link': notice_link,
            'file_link': file_link
        })
    return notices_data


# Print results
if __name__ == "__main__":
    data = scrape_notices()

    for n in data:
        print(f"Title: {n['title']}")
        print(f"Notice Link: {n['notice_link']}")
        print(f"File Link: {n['file_link']}")
        print('-' * 50)
