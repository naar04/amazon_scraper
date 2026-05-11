import os
import json
import asyncio
from playwright.async_api import async_playwright

# Configuration
CATEGORIES = [
    "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/",
    "https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/"
]

async def scrape_amazon():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        deals = []
        
        for url in CATEGORIES:
            await page.goto(url, wait_until="networkidle")
            # Selector for product cards (Amazon updates these often)
            products = await page.query_selector_all(".zg-grid-general-faceout")
            
            for product in products[:15]: # Check first 15 items
                try:
                    # Logic to find 4+ stars
                    rating_text = await product.query_selector(".a-icon-alt")
                    rating = float((await rating_text.inner_text()).split()[0])
                    
                    # Logic to check if "On Sale" (usually has a secondary price)
                    price_drop = await product.query_selector(".a-color-secondary")
                    
                    if rating >= 4.0 and price_drop:
                        title = await (await product.query_selector(".p13n-sc-truncate-desktop-type2")).inner_text()
                        link = "https://www.amazon.com" + await (await product.query_selector(".a-link-normal")).get_attribute("href")
                        
                        deals.append({
                            "title": title[:100],
                            "link": link,
                            "rating": rating
                        })
                except Exception:
                    continue
                    
        await browser.close()
        return deals[:5] # Return top 5 total

# Run and save to a temporary file
if __name__ == "__main__":
    found_deals = asyncio.run(scrape_amazon())
    with open("latest_deals.json", "w") as f:
        json.dump(found_deals, f)
