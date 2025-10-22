import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

def scrape_facebook_page(url, num_posts=5):
    """
    Scrape the latest posts from a Facebook page with improved data extraction
    """
    # Install ChromeDriver automatically
    chromedriver_autoinstaller.install()

    # Selenium setup
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    posts = []

    try:
        print(f"Accessing Facebook page: {url}")
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Scroll to load more content (Facebook uses lazy loading)
        print("Scrolling to load more content...")
        for i in range(4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        
        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # More specific approach to find posts
        print("Looking for posts...")
        
        # Method 1: Look for elements with specific data attributes
        post_elements = soup.find_all(lambda tag: tag.has_attr('data-pagelet') and any(x in tag['data-pagelet'] for x in ['FeedUnit', 'MainFeed', 'Story']))
        
        # Method 2: If first method didn't find enough, try other selectors
        if len(post_elements) < num_posts:
            additional_elements = soup.select('div[role="article"], div.x1yztbdb, div.x1iorvi4, div.x1uvtmcs')
            post_elements.extend([e for e in additional_elements if e not in post_elements])
        
        print(f"Found {len(post_elements)} potential posts")
        
        # Process the found posts
        processed_count = 0
        for i, post in enumerate(post_elements):
            if processed_count >= num_posts:
                break
                
            try:
                post_data = extract_post_data(post)
                if post_data and post_data.get('text', '').strip() and len(post_data['text']) > 30:
                    posts.append(post_data)
                    processed_count += 1
                    print(f"Processed post {processed_count}")
                else:
                    print(f"Skipping element {i+1} - no substantial content extracted")
            except Exception as e:
                print(f"Error processing element {i+1}: {e}")
                continue
        
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()
    
    return posts

def extract_post_data(post_element):
    """
    Extract data from a single post element with improved text extraction
    """
    try:
        # Extract post text - try multiple approaches
        text = extract_text_improved(post_element)
        
        # Extract post time
        time_text = extract_time(post_element)
        
        # Extract reactions/likes
        reactions = extract_reactions(post_element)
        
        # Extract post URL
        post_url = extract_url(post_element)
        
        # Extract images if available
        images = extract_images(post_element)
        
        return {
            'text': text,
            'time': time_text,
            'reactions': reactions,
            'url': post_url,
            'images': images
        }
        
    except Exception as e:
        print(f"Error extracting post data: {e}")
        return None

def extract_text_improved(post_element):
    """Improved text extraction with better filtering"""
    # First try: look for specific text containers
    text_selectors = [
        'div[data-ad-preview="message"]',
        'div.x1iorvi4', 
        'div.userContent',
        'div._5pbx',
        'div.x1y1aw1k',
        'div.x1lliihq',
        'div.x1jx94hy',
        'div.x1l90r2v',  # Another common text container
        'div.x6s0dn4'    # Another potential text container
    ]
    
    # Try each selector
    for selector in text_selectors:
        text_elements = post_element.select(selector)
        for text_elem in text_elements:
            text = text_elem.get_text(separator=' ', strip=True)
            # Clean up text (remove extra spaces, etc.)
            text = re.sub(r'\s+', ' ', text).strip()
            if text and len(text) > 30:  # Ensure we have meaningful text
                return text
    
    # Second approach: look for spans with substantial text
    span_elements = post_element.find_all('span', string=lambda text: text and len(text.strip()) > 20)
    for span in span_elements:
        text = span.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text).strip()
        if text and len(text) > 30:
            return text
    
    # Third approach: get all text but filter out short fragments
    all_text = []
    for string in post_element.stripped_strings:
        if len(string) > 10:  # Only consider substantial text fragments
            all_text.append(string)
    
    if all_text:
        result = ' '.join(all_text)
        result = re.sub(r'\s+', ' ', result).strip()
        if len(result) > 30:
            return result
    
    # Final fallback - get all text and clean it up
    full_text = post_element.get_text(separator=' ', strip=True)
    full_text = re.sub(r'\s+', ' ', full_text).strip()
   
    return full_text if len(full_text) > 30 else ""

def extract_time(post_element):
    """Extract time from post"""
    time_selectors = [
        'abbr._5ptz',
        'span._5pr2',
        'a._5pcq',
        'span.tojvnm2t',
        'span.x4k7w5x',
        'span.x1lliihq.x1plvlek',
        'span.x1nxh6w3',  # Another time selector
        'a.x1i10hfl.x1qjc9v5'  # Time link
    ]
    
    for selector in time_selectors:
        time_elem = post_element.select_one(selector)
        if time_elem:
            time_text = time_elem.get_text(strip=True)
            if time_text and any(x in time_text.lower() for x in ['min', 'hour', 'day', 'week', 'month', 'year']):
                return time_text
    
    # Try to find time via alternative approach - look for elements containing time words
    time_pattern = re.compile(r'\b(\d+\s*(min|hr|hour|h|d|day|wk|week|mo|month|yr|year)s?)\b', re.IGNORECASE)
    for element in post_element.find_all(text=time_pattern):
        if time_pattern.search(element):
            return element.strip()
    
    return ""

def extract_reactions(post_element):
    """Extract reactions from post"""
    reaction_selectors = [
        'span._81hb',
        'div._4arz',
        'span.x1e56ztr',
        'span.x1xm1mqw',
        'div.x1i10hfl',
        'div.x6s0dn4.x78zum5.x1qughib',  # Reactions container
        'span.x1qvwoe0'  # Another reactions selector
    ]
    
    for selector in reaction_selectors:
        reaction_elem = post_element.select_one(selector)
        if reaction_elem:
            reactions = reaction_elem.get_text(strip=True)
            # Filter out non-reaction text
            if reactions and any(x in reactions for x in ['K', 'M', 'Like', 'Comment', 'Share']):
                return reactions
    
    # Look for reaction elements with specific attributes
    reaction_elems = post_element.find_all(lambda tag: tag.has_attr('aria-label') and 'reaction' in tag['aria-label'].lower())
    if reaction_elems:
        return reaction_elems[0].get_text(strip=True)
    
    return ""

def extract_url(post_element):
    """Extract post URL"""
    url_selectors = [
        'a._5pcq[href*="/posts/"]',
        'a.x1i10hfl[href*="/posts/"]',
        'a[href*="/posts/"]',
        'a[href*="/story/"]',
        'a[aria-label*="Story"]'
    ]
    
    for selector in url_selectors:
        url_elem = post_element.select_one(selector)
        if url_elem and 'href' in url_elem.attrs:
            href = url_elem['href']
            if href.startswith('/'):
                return "https://www.facebook.com" + href
            else:
                return href
    
    return ""

def extract_images(post_element):
    """Extract image URLs from post"""
    img_selectors = [
        'img.x1ey2m1c',
        'img.xz74otr',
        'img._5dec',
        'img[src*="facebook.com"]',
        'img[src*="fbcdn.net"]',
        'img[alt*="Image"]'
    ]
    
    images = []
    for selector in img_selectors:
        img_elements = post_element.select(selector)
        for img in img_elements:
            if 'src' in img.attrs and img['src'] and not img['src'].startswith('data:'):
                images.append(img['src'])
    
    return images

def save_to_file(posts, filename="facebook_posts.json"):
    """Save scraped posts to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filename}")

def main():
    """Main function to run the scraper"""
    # Replace with your target Facebook page URL
    facebook_page_url = "https://www.facebook.com/cssoftsolutionsindiaprivateltd"
    
    print("Starting Facebook scraper...")
    latest_posts = scrape_facebook_page(facebook_page_url, num_posts=5)
    
    print(f"\nSuccessfully scraped {len(latest_posts)} posts:")
    for i, post in enumerate(latest_posts, 1):
        print(f"\n--- Post {i} ---")
        print(f"Time: {post['time']}")
        print(f"Reactions: {post['reactions']}")
        # print(f"Text: {post['text'][:200]}..." if len(post['text']) > 200 else f"Text: {post['text']}")
        print(f"Text: {post['text']}")
        print(f"URL: {post['url']}")
        print(f"Images: {(post['images'])} found")
    
    # Save to JSON file
    save_to_file(latest_posts)

if __name__ == "__main__":
    main()