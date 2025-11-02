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
        # -> Click on the 'Resources' link in the navigation bar to go to the resources page without filters.
        frame = context.pages[-1]
        # Click on the 'Resources' link in the navigation bar to navigate to the resources page.
        elem = frame.locator('xpath=html/body/nav/div/div/a[4]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'Videos' from the 'Filter by Type' dropdown and click 'Apply Filters' to verify only video resources are displayed.
        frame = context.pages[-1]
        # Click 'Apply Filters' button to apply the video type filter.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'Hindi' from the 'Filter by Language' dropdown and click 'Apply Filters' to verify resources filtered by type 'video' and language 'hi'.
        frame = context.pages[-1]
        # Click 'Apply Filters' button to apply the language filter 'Hindi' along with type 'video'.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on 'Clear Filters' to reset filters and verify that all resource types and languages are listed.
        frame = context.pages[-1]
        # Click 'Clear Filters' to reset all filters and show all resources.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'Meditations' from the 'Filter by Type' dropdown and click 'Apply Filters' to check for available meditation resources.
        frame = context.pages[-1]
        # Click 'Apply Filters' button to apply the meditation type filter.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'Articles' from the 'Filter by Type' dropdown and click 'Apply Filters' to check for available article resources.
        frame = context.pages[-1]
        # Click 'Apply Filters' button to apply the article type filter.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Select 'English' from the 'Filter by Language' dropdown and click 'Apply Filters' to check for resources in English language.
        frame = context.pages[-1]
        # Click 'Apply Filters' button to apply the language filter 'English'.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click 'Clear Filters' to reset filters and verify the page returns to showing all resource types and languages (even if no resources are listed). Then stop as the task is complete.
        frame = context.pages[-1]
        # Click 'Clear Filters' to reset all filters and show all resources.
        elem = frame.locator('xpath=html/body/main/div/div[2]/form/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=All Types').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Videos').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Meditations').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Articles').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=All Languages').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=English').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Hindi').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Tamil').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Telugu').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Kannada').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Marathi').first).to_be_visible(timeout=30000)
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
    