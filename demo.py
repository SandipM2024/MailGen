# import re
# from googleapiclient.discovery import build

# # Replace with your actual keys
# # API_KEY = "AIzaSyBlw5PZeC-0HakqnMphXj761yju4xhAFFs"  # Your Google API key
# API_KEY = "AIzaSyBlw5PZeC-0HakqnMphXj761yju4xhAFFs"

# SEARCH_ENGINE_ID = "268d69758392d4ba1" 
# def google_search(query, api_key, cse_id, **kwargs):
#     """Perform a Google Custom Search."""
#     service = build("customsearch", "v1", developerKey=api_key)
#     res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
#     return res.get("items", [])

# def extract_facebook_pages(company_name):
#     """
#     Extract only main Facebook page links for the given company.
#     """
#     query = f"site:facebook.com {company_name}"
#     results = google_search(query, API_KEY, SEARCH_ENGINE_ID)

#     page_links = []
#     for item in results:
#         link = item.get("link", "")
#         # Match only main page URLs (skip posts, photos, etc.)
#         if re.match(r"^https://www\.facebook\.com/[^/]+/?$", link):
#             page_links.append(link)

#     return page_links

# if __name__ == "__main__":
#     company_name = "trade"  # Example company
#     pages = extract_facebook_pages(company_name)
#     print(pages, "pages")
#     if pages:
#         print("Facebook Page Links Found:")
#         for page in pages:
#             print(page)
#     else:
#         print("No valid Facebook pages found.")

# import requests
# from bs4 import BeautifulSoup
# import re

# def scrape_facebook_page_about(url, cookies):
#     """
#     Scrape Facebook page about section for page name, followers, and following count.
#     """
#     headers = {
#         "User-Agent": (
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#             "AppleWebKit/537.36 (KHTML, like Gecko) "
#             "Chrome/129.0.0.0 Safari/537.36"
#         ),
#         "Accept-Language": "en-US,en;q=0.9",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#         "Connection": "keep-alive",
#         "Referer": "https://www.facebook.com/",
#     }

#     # STEP 1: Fetch the page
#     response = requests.get(url, headers=headers, cookies=cookies)
#     print(f"Status Code: {response.status_code}")
#     if response.status_code != 200:
#         return {
#             "error": f"Failed to fetch page. Status code: {response.status_code}",
#             "page_name": None,
#             "followers": None,
#             "following": None,
#         }

#     # STEP 2: Parse HTML
#     soup = BeautifulSoup(response.text, "html.parser")

#     # STEP 3: Extract Page Name
#     page_name_tag = soup.find("h1")
#     page_name = page_name_tag.get_text(strip=True) if page_name_tag else None

#     # STEP 4: Extract followers and following
#     followers = None
#     following = None

#     for link in soup.find_all("a", href=True):
#         text = link.get_text(strip=True)
#         href = link["href"].lower()
#         if "followers" in href:
#             match = re.search(r"([\d.,KMB]+)", text)
#             if match:
#                 followers = match.group(1)
#         elif "following" in href:
#             match = re.search(r"([\d.,KMB]+)", text)
#             if match:
#                 following = match.group(1)

#     return {
#         "page_name": page_name,
#         "followers": followers,
#         "following": following,
#     }


# # Example usage
# if __name__ == "__main__":
#     url = "https://www.facebook.com/cssoftsolutionsindiaprivateltd/about"

#     # Add cookies from your browser
#     cookies = {
#         "c_user": "123456789",
#         "xs": "123:abcxyz",
#         "datr": "xyz123...",
#         "fr": "0x8AbCdEf...",
#         "spin": "r.100000000_blah",
#     }

#     data = scrape_facebook_page_about(url, cookies)
#     print(data)


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import re
# import time
# import chromedriver_autoinstaller
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options


# def scrape_facebook_page_about(url, driver_path="chromedriver"):
#     """
#     Scrape Facebook page about section using Selenium to avoid 400/404 errors.
#     """

#     chromedriver_autoinstaller.install()

#     # Selenium setup
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--window-size=1920,1080")

#     driver = webdriver.Chrome(options=options)
#     # Load the page
#     driver.get(url)
#     time.sleep(5)  # wait for JS to render

#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     driver.quit()

#     # Extract Page Name
#     page_name_tag = soup.find("h1")
#     page_name = page_name_tag.get_text(strip=True) if page_name_tag else None

#     # Extract followers / following
#     followers = None
#     following = None

#     for link in soup.find_all("a", href=True):
#         text = link.get_text(strip=True)
#         href = link["href"].lower()
#         if "followers" in href:
#             match = re.search(r"([\d.,KMB]+)", text)
#             if match:
#                 followers = match.group(1)
#         elif "following" in href:
#             match = re.search(r"([\d.,KMB]+)", text)
#             if match:
#                 following = match.group(1)

#     return {
#         "page_name": page_name,
#         "followers": followers,
#         "following": following,
#     }

# # Example usage
# if __name__ == "__main__":
#     url = "https://www.facebook.com/cssoftsolutionsindiaprivateltd/about"
#     data = scrape_facebook_page_about(url)
#     print(data)




# def scrape_facebook_page_about(url):
#     """
#     Scrape Facebook page about section using Selenium.
#     Returns page name, followers, following, categories, contact info, and websites.
#     """
#     # Auto-install matching ChromeDriver
#     chromedriver_autoinstaller.install()

#     # Selenium setup
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--window-size=1920,1080")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")

#     driver = webdriver.Chrome(options=options)

#     # Load the page
#     driver.get(url)
#     time.sleep(5)  # Wait for JS to render

#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     driver.quit()

#     # --- Extract Page Name ---
#     page_name_tag = soup.find("h1")
#     page_name = page_name_tag.get_text(strip=True) if page_name_tag else None

#     # --- Extract followers / following ---
#     followers = None
#     following = None
#     for link in soup.find_all("a", href=True):
#         text = link.get_text(strip=True)
#         href = link["href"].lower()
#         if "followers" in href:
#             match = re.search(r"([\d.,KMB]+)", text)
#             if match:
#                 followers = match.group(1)
#         elif "following" in href:
#             match = re.search(r"([\d.,KMB]+)", text)
#             if match:
#                 following = match.group(1)

    
#     return {
#         "page_name": page_name,
#         "followers": followers,
#         "following": following,
#         # "categories": categories,
#         # "contact_info": contact_info,
#         # "websites": websites
#     }

# # Example usage
# if __name__ == "__main__":
#     url = "https://www.facebook.com/cssoftsolutionsindiaprivateltd/about"
#     data = scrape_facebook_page_about(url)
#     print(data)


import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from urllib.parse import urlparse, parse_qs, unquote
def scrape_facebook_page_about(url):
    """
    Scrape Facebook page about section using Selenium.
    Returns page name, followers, following, categories, contact info, and websites.
    """
    # Auto-install matching ChromeDriver
    chromedriver_autoinstaller.install()

    # Selenium setup
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    # Load the page
    driver.get(url)
    time.sleep(5)  # Wait for JS to render

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # --- Extract Page Name ---
    page_name_tag = soup.find("h1")
    page_name = page_name_tag.get_text(strip=True) if page_name_tag else None

    # --- Extract followers / following ---
    followers = None
    following = None
    for link in soup.find_all("a", href=True):
        text = link.get_text(strip=True)
        href = link["href"].lower()
        if "followers" in href:
            match = re.search(r"([\d.,KMB]+)", text)
            if match:
                followers = match.group(1)
        elif "following" in href:
            match = re.search(r"([\d.,KMB]+)", text)
            if match:
                following = match.group(1)

    # --- Extract Categories ---
    categories =""
    category_section = soup.find(lambda tag: tag.name=="span" and "Categories" in tag.text)
    if category_section:
        categories_parent = category_section.find_parent("div", class_="xat24cr")
        if categories_parent:
            categories_texts = categories_parent.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen xo1l8bm xzsf02u")
            for cat in categories_texts:
                text = cat.get_text(strip=True)
                if text and text != "Categories":
                    # categories.append(text)
                    categories +=text

    # --- Extract Contact Info ---
    contact_info = {}
    contact_section = soup.find(lambda tag: tag.name=="span" and "Contact info" in tag.text)
    if contact_section:
        contact_parent = contact_section.find_parent("div", class_="xat24cr")
        print(contact_parent, "cantect parent")
        if contact_parent:
            # Address
            address_tag = contact_parent.find("span", string=re.compile(r"Address|I-"))
            contact_info['address'] = address_tag.get_text(strip=True) if address_tag else None
              # Extract Service Areas
            service_area_tag = soup.find("div", string=re.compile("Service area", re.IGNORECASE))
            if service_area_tag:
                service_area_value = service_area_tag.find_previous("span")
                if service_area_value:
                    areas = [area.strip() for area in service_area_value.text.split("·")]
                    contact_info["service_areas"] = areas

            # # Phone
            # phone_tag = contact_parent.find("span", string=re.compile(r"\d{5,}"))
            # contact_info['phone'] = phone_tag.get_text(strip=True) if phone_tag else None
             # Extract Mobile Number
            mobile_tag = soup.find("div", string=re.compile("Mobile", re.IGNORECASE))
            if mobile_tag:
                mobile_value = mobile_tag.find_previous("span")
                # print(mobile_value, "mobile_value")
                if mobile_value:
                    contact_info["mobile"] = mobile_value.text.strip()
            # Email
            email_tag = contact_parent.find("span", string=re.compile(r"@"))
            contact_info['email'] = email_tag.get_text(strip=True) if email_tag else None

    # --- Extract Websites / Social Links ---
    websites_list = []
    social_section = soup.find(lambda tag: tag.name=="span" and "Websites" in tag.text)
    if social_section:
        social_parent = social_section.find_parent("div", class_="xat24cr")
        if social_parent:
            links = social_parent.find_all("a", href=True)
            # print(links, "link")
            for link in links:
                websites_list.append(link['href'])

    websites={}
    for url in websites_list:
        if "about_contact_and_basic_info" in url:
            websites["contact_info_page"] = url
        elif "about_profile_transparency" in url:
            websites["transparency_page"] = url
        elif "about_details" in url:
            websites["details_page"] = url
        # elif "l.php" in url:
        #     # Decode external redirected URL
        #     parsed_url = urlparse(url)
        #     query = parse_qs(parsed_url.query)
        #     # if "u" in query:
        #     #     decoded_link = unquote(query["u"][0])
        # websites["websites_social_links"] = url
        else:
            websites["websites_social_links"] = url
   
    return {
        "page_name": page_name,
        "followers": followers,
        "following": following,
        "categories": categories,
        "contact_info": contact_info,
        "websites": websites
    }




def scrape_facebook_page_transparency(url: str) -> dict:
    """
    Scrape Facebook Page Transparency data from a given Facebook 'about_profile_transparency' URL.
    Returns structured JSON data.
    """

    # Auto-install matching ChromeDriver
    chromedriver_autoinstaller.install()

    # Selenium setup
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        # Load the page
        driver.get(url)
        time.sleep(5)  # wait for JS content to render

        # Parse the rendered page
        soup = BeautifulSoup(driver.page_source, "html.parser")
    finally:
        driver.quit()

    # Initialize result
  
    page_transparency={
            "page_id": None,
            "creation_date": None,
            "admin_info": [],
            "ads_status": None
        }
    

    # --- Extract Page ID ---
    page_id_tag = soup.find("span", string=re.compile(r"^\d{6,}$"))  # numeric value like 430691120394330
    if page_id_tag:
        page_transparency["page_id"] = page_id_tag.get_text(strip=True)

    # --- Extract Creation Date ---
    creation_date_tag = soup.find("span", string=re.compile(r"\d{1,2} \w+ \d{4}"))  # e.g., 4 February 2014
    if creation_date_tag:
        page_transparency["creation_date"] = creation_date_tag.get_text(strip=True)

    # --- Extract Admin Info ---
    admin_info_tag = soup.find("span", string=re.compile(r"admins?", re.IGNORECASE))
    if admin_info_tag:
        page_transparency["admin_info"].append(
            admin_info_tag.get_text(strip=True)
        )

    # --- Extract Ads Status ---
    ads_status_tag = soup.find("span", string=re.compile(r"ads", re.IGNORECASE))
    if ads_status_tag:
        page_transparency["ads_status"] = ads_status_tag.get_text(strip=True)

    return page_transparency


import time
import re
import requests



def scrape_facebook_about_description(url: str) -> dict:
    """
    Scrape the Facebook About page and extract the full description and website links.
    Handles multiple <span> elements with the same class.
    """
    chromedriver_autoinstaller.install()

    # Selenium setup
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)  # wait for JS content to render
        soup = BeautifulSoup(driver.page_source, "html.parser")
    finally:
        driver.quit()

    about_details = {
        "description": "",
        "links": []
    }

    # --- Step 1: Extract full description ---
    # Find the container that holds the About text
    container = soup.find("div", class_= "xyamay9 xsfy40s x1gan7if xf7dkkf")
    if container:
        # Collect all <span> tags inside this container that match the description class
        spans = container.find_all("span", class_=lambda c: c and "x193iq5w" in c.split())
        description_text = "\n".join(span.get_text(separator="\n", strip=True) for span in spans)
        about_details["description"] = description_text

    # --- Step 2: Extract external website links ---
    for link in soup.find_all("a", href=True):
        href = link["href"]

        # Decode Facebook redirect links
        match = re.search(r"u=(https?%3A%2F%2F[^&]+)", href)
        if match:
            decoded_link = requests.utils.unquote(match.group(1))
            about_details["links"].append(decoded_link)
        elif href.startswith("http") and "facebook.com" not in href:
            about_details["links"].append(href)

    # Remove duplicate links
    about_details["links"] = list(set(about_details["links"]))

    return about_details


# Example Usage
# if __name__ == "__main__":
#     url = "https://www.facebook.com/cssoftsolutionsindiaprivateltd/about_details"
#     data = scrape_facebook_about_description(url)
#     print(data)


# # Example usage
if __name__ == "__main__":
    # about_url = "https://www.facebook.com/ETRADE/about"
    about_url = "https://www.facebook.com/cssoftsolutionsindiaprivateltd/about"
    # page_transparency_url = "https://www.facebook.com/cssoftsolutionsindiaprivateltd/about_profile_transparency"
    about_data = scrape_facebook_page_about(about_url)
    # # page_transparency=scrape_facebook_page_transparency(page_transparency_url)
    print(about_data)
    # # print(page_transparency)
    # about_detail_url = "https://www.facebook.com/cssoftsolutionsindiaprivateltd/about_details"
    # data = scrape_facebook_about_details(about_detail_url)
    # print(data)

