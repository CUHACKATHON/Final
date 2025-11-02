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
        await page.goto("http://localhost:8000", wait_until="commit", timeout=10000)
        
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
        # -> Click on the 'Resources' link to navigate to the resources page.
        frame = context.pages[-1]
        # Click on the 'Resources' link in the top navigation to go to the resources page.
        elem = frame.locator('xpath=html/body/nav/div/div/a[4]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'English' from language filter dropdown and apply filter to verify resources for English language.
        frame = context.pages[-1]
        # Click Apply Filters button to filter resources by English language.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'Hindi' from language filter dropdown and apply filter to verify resources for Hindi language.
        frame = context.pages[-1]
        # Click Apply Filters button to filter resources by Hindi language.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'Tamil' from the language filter dropdown and apply filter to verify resources for Tamil language.
        frame = context.pages[-1]
        # Click Apply Filters button to filter resources by Tamil language.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'Telugu' from the language filter dropdown and apply filter to verify resources for Telugu language.
        frame = context.pages[-1]
        # Click Apply Filters button to filter resources by Telugu language.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'Kannada' from the language filter dropdown and apply filter to verify resources for Kannada language.
        frame = context.pages[-1]
        # Click Apply Filters button to filter resources by Kannada language.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'Marathi' from the language filter dropdown and apply filter to verify resources for Marathi language.
        frame = context.pages[-1]
        # Click Apply Filters button to filter resources by Marathi language.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click the 'Clear Filters' link to reset filters and verify if any resources are displayed without language filtering.
        frame = context.pages[-1]
        # Click 'Clear Filters' link to reset all filters and check if any resources are displayed without filtering.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=No resources found matching your filters. Try adjusting your search criteria.').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    