import asyncio
from playwright import async_api
from playwright.async_api import expect

async def run_test():
    pw = None
    browser = None
    context = None
    
    try:
        # Start a Playwright session in asynchronous mode
        pw = await async_api.async_playwright().start()
        
        # Launch a Chromium browser in headless mode with custom arguments
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--window-size=1280,720",         # Set the browser window size
                "--disable-dev-shm-usage",        # Avoid using /dev/shm which can cause issues in containers
                "--ipc=host",                     # Use host-level IPC for better stability
                "--single-process"                # Run the browser in a single process mode
            ],
        )
        
        # Create a new browser context (like an incognito window)
        context = await browser.new_context()
        context.set_default_timeout(5000)
        
        # Open a new page in the browser context
        page = await context.new_page()
        
        # Navigate to your target URL and wait until the network request is committed
        await page.goto("http://localhost:8000/", wait_until="commit", timeout=10000)
        
        # Wait for the main page to reach DOMContentLoaded state (optional for stability)
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=3000)
        except async_api.Error:
            pass
        
        # Iterate through all iframes and wait for them to load as well
        for frame in page.frames:
            try:
                await frame.wait_for_load_state("domcontentloaded", timeout=3000)
            except async_api.Error:
                pass
        
        # Interact with the page elements to simulate user flow
        # -> Click on the 'Resources' link in the top navigation to go to the /resources/ page with no filters.
        frame = context.pages[-1]
        # Click on the 'Resources' link in the top navigation to navigate to the resources page.
        elem = frame.locator('xpath=html/body/nav/div/div/a[4]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Apply filter 'type=video' by selecting 'Videos' from the 'Filter by Type' dropdown and then click 'Apply Filters'.
        frame = context.pages[-1]
        # Click 'Apply Filters' button to apply the selected type filter.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Apply filter 'language=hi' for Hindi resources by selecting 'Hindi' from the language dropdown and clicking 'Apply Filters'.
        frame = context.pages[-1]
        # Click 'Apply Filters' button to apply the selected language filter.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Clear all filters by clicking the 'Clear Filters' link to reset filters and show all resources.
        frame = context.pages[-1]
        # Click 'Clear Filters' link to reset all filters and show all resources.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Apply combined filters 'type=article' and 'language=mr' by selecting 'Articles' and 'Marathi' from the respective dropdowns and clicking 'Apply Filters'.
        frame = context.pages[-1]
        # Click 'Apply Filters' button to apply combined filters for Marathi articles.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=MindCare').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Home').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Chat').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Appointments').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Resources').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Forum').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Login').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Register').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Mental Health Resources').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Culturally contextualized and multilingual resources for Indian students').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Filter by Type:').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=All Types').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Videos').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Meditations').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Articles').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Filter by Language:').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=All Languages').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=English').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Hindi').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Tamil').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Telugu').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Kannada').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Marathi').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=No resources found matching your filters. Try adjusting your search criteria.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=© 2025 MindCare - Mental Health Support Platform for Indian College Students').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=24/7 Helpline: 1800-599-0019 | Confidential & Anonymous Support').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    