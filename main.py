import requests
from bs4 import BeautifulSoup


def get_urls_with_filtered_titles(url, filters=None, country_filter=None, url_prefix=None):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the page contains job postings directly
        job_postings = soup.find_all('div', class_='Page-CareersPage-position')
        if job_postings:
            urls_with_filtered_titles = []

            for job_posting in job_postings:
                title = job_posting.find('h3', class_='Page-CareersPage-title')
                if title:
                    title_text = title.text.strip()

                    # Check if the title contains any of the specified filters
                    if filters and any(filter_str.lower() in title_text.lower() for filter_str in filters):
                        # Check country filter if provided
                        if country_filter and country_filter.lower() in title_text.lower():
                            full_url = url_prefix + title_text.replace(' ', '').replace('-', '') if url_prefix else ''
                            urls_with_filtered_titles.append({'url': full_url, 'title': title_text})
                        elif not country_filter:
                            full_url = url_prefix + title_text.replace(' ', '').replace('-', '') if url_prefix else ''
                            urls_with_filtered_titles.append({'url': full_url, 'title': title_text})
                    elif not filters:
                        # Check country filter if provided
                        if country_filter and country_filter.lower() in title_text.lower():
                            full_url = url_prefix + title_text.replace(' ', '').replace('-', '') if url_prefix else ''
                            urls_with_filtered_titles.append({'url': full_url, 'title': title_text})
                        elif not country_filter:
                            full_url = url_prefix + title_text.replace(' ', '').replace('-', '') if url_prefix else ''
                            urls_with_filtered_titles.append({'url': full_url, 'title': title_text})

            return urls_with_filtered_titles

        # If no job postings found, treat it as a normal page with URLs
        urls_with_titles = []
        for a in soup.find_all('a', href=True):
            href = a.get('href')
            title = a.text.strip()

            # Check if the title contains any of the specified filters
            if filters and any(filter_str.lower() in title.lower() for filter_str in filters):
                # Check country filter if provided
                if country_filter and country_filter.lower() in title.lower():
                    full_url = url_prefix + href if url_prefix else href
                    urls_with_titles.append({'url': full_url, 'title': title})
                elif not country_filter:
                    full_url = url_prefix + href if url_prefix else href
                    urls_with_titles.append({'url': full_url, 'title': title})
            elif not filters:
                # Check country filter if provided
                if country_filter and country_filter.lower() in title.lower():
                    full_url = url_prefix + href if url_prefix else href
                    urls_with_titles.append({'url': full_url, 'title': title})
                elif not country_filter:
                    full_url = url_prefix + href if url_prefix else href
                    urls_with_titles.append({'url': full_url, 'title': title})
            #print(url_prefix + "   " + href)
        return urls_with_titles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

def main():
    num_companies = int(input("Enter the number of companies: "))

    for company_num in range(1, num_companies + 1):
        print(f"\nCompany {company_num}:")
        url = input("Enter a URL: ")
        if not url:
            url = 'https://careers.mobileye.com/jobs'
        country_filter = input("Enter a country to filter titles (or leave blank for all): ")
        filters = input("Enter a comma-separated list of wanted data in the title (or leave blank for all): ").split(',')
        url_prefix = input("Enter a prefix for the output URLs (or leave blank for none): ")
        if not url_prefix:
            url_prefix = 'https://careers.mobileye.com'

        urls_with_filtered_titles = get_urls_with_filtered_titles(url, filters, country_filter, url_prefix)

        if urls_with_filtered_titles:
            print("\nFiltered URLs found on the page:")
            for entry in urls_with_filtered_titles:
                print(f"Title: {entry['title']}, URL: {entry['url']}")
        else:
            print("No matching titles found on the page.")

if __name__ == "__main__":
    main()

