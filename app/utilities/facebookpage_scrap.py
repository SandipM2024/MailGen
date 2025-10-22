import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from urllib.parse import urlparse, parse_qs, unquote
import requests
# ==============================
# Selenium Setup Helper
# ==============================
def create_driver():
    """Initialize Selenium Chrome WebDriver with required options."""
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)



# ==============================
# Scrape Facebook About Section
# ==============================
def scrape_facebook_page_about(url: str) -> dict:
    """
    Scrape Facebook page about section using Selenium.
    Returns page name, followers, following, categories, contact info, and websites.
    """
    driver = create_driver()
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

    websites={
        "websites_social_links": []
    }
   
    for url in websites_list:
        
        if "about_contact_and_basic_info" in url:
            websites["contact_info_page"] = url
        elif "about_profile_transparency" in url:
            websites["transparency_page"] = url
        elif "about_details" in url:
            websites["details_page"] = url
        elif "l.php" in url:
            # Decode external redirected URL
            print(url, "url")

            parsed_url = urlparse(url)
            query = parse_qs(parsed_url.query)
            print(query, "query")

            if "u" in query:
                decoded_link = unquote(query["u"][0])
                websites["websites_social_links"].append(decoded_link)
        else:
            websites["other"] = url
    print("website", websites)
    return {
        "page_name": page_name,
        "followers": followers,
        "following": following,
        "categories": categories,
        "contact_info": contact_info,
        "websites": websites,
    }


# ==============================
# Scrape Facebook Page Transparency
# ==============================
def scrape_facebook_page_transparency(url: str) -> dict:
    """
    Scrape Facebook Page Transparency data from a given Facebook 'about_profile_transparency' URL.
    Returns structured JSON data.
    """
    driver = create_driver()
    driver.get(url)
    time.sleep(5)  # Wait for JS content to render

    soup = BeautifulSoup(driver.page_source, "html.parser")
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



def scrape_facebook_about_description(url: str) -> dict:
    """
    Scrape the Facebook About page and extract the full description and website links.
    Handles multiple <span> elements with the same class.
    """
    driver = create_driver()
    driver.get(url)
    time.sleep(5)  # Wait for JS content to render

    soup = BeautifulSoup(driver.page_source, "html.parser")
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


