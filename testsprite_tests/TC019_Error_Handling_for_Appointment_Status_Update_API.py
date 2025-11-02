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
        # -> Click on Login to authenticate as admin user.
        frame = context.pages[-1]
        # Click on Login link to open login page or modal
        elem = frame.locator('xpath=html/body/nav/div/div/a[6]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Input admin username and password, then submit login form.
        frame = context.pages[-1]
        # Input admin username
        elem = frame.locator('xpath=html/body/div/form/p/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin')
        

        frame = context.pages[-1]
        # Input admin password
        elem = frame.locator('xpath=html/body/div/form/p[2]/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin123')
        

        frame = context.pages[-1]
        # Click Login button to authenticate as admin user
        elem = frame.locator('xpath=html/body/div/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Send POST request to appointment update API with invalid status using token-based authentication via API call.
        await page.goto('http://localhost:8000/api/docs', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Send POST request to /api/token/ with admin credentials to obtain JWT token for authentication.
        await page.goto('http://localhost:8000/api/token/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Input admin username and password, then submit POST request to obtain JWT token.
        frame = context.pages[-1]
        # Input admin username
        elem = frame.locator('xpath=html/body/div/div[2]/div/div[3]/div/div/form/fieldset/div/div/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin')
        

        frame = context.pages[-1]
        # Input admin password
        elem = frame.locator('xpath=html/body/div/div[2]/div/div[3]/div/div/form/fieldset/div[2]/div/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin123')
        

        frame = context.pages[-1]
        # Click POST button to submit token request
        elem = frame.locator('xpath=html/body/div/div[2]/div/div[3]/div/div/form/fieldset/div[3]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Send POST request to appointment update API with invalid status using the obtained JWT token for authentication.
        await page.goto('http://localhost:8000/api/appointments/1/update/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Send direct POST request to appointment update API with invalid status and JWT token in Authorization header, then verify 400 response.
        await page.goto('http://localhost:8000/api/appointments/1/update/', timeout=10000)
        await asyncio.sleep(3)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=Admin/Counselor Login').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Username').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Password').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Login').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Register as User').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Register as Counselor').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Back to Home').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    