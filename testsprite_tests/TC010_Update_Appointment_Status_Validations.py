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
        # -> Click on Login to proceed with authorized user login.
        frame = context.pages[-1]
        # Click on Login link to open login page.
        elem = frame.locator('xpath=html/body/nav/div/div/a[6]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Input username and password for admin and click login.
        frame = context.pages[-1]
        # Input username 'admin' for admin login
        elem = frame.locator('xpath=html/body/div/form/p/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin')
        

        frame = context.pages[-1]
        # Input password 'admin123' for admin login
        elem = frame.locator('xpath=html/body/div/form/p[2]/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin123')
        

        frame = context.pages[-1]
        # Click login button to submit admin credentials
        elem = frame.locator('xpath=html/body/div/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Try login using JSON POST request to /login/ endpoint with admin credentials to obtain JWT token for authorized API access.
        await page.goto('http://localhost:8000/login/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Perform JSON POST login request to /login/ endpoint with admin credentials (admin/admin123) to obtain JWT token for authorized API access.
        await page.goto('http://localhost:8000/api/login/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Perform JSON POST login request to /api/auth/login/ endpoint with admin credentials (admin/admin123) to obtain JWT token for authorized API access.
        await page.goto('http://localhost:8000/api/auth/login/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Input JSON payload with admin credentials {"username": "admin", "password": "admin123"} in the content textarea and click POST to obtain JWT token.
        frame = context.pages[-1]
        # Input JSON payload with admin credentials for token-based login
        elem = frame.locator('xpath=html/body/div/div[2]/div/div[3]/div/div/form/fieldset/div[2]/div/textarea').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('{"username": "admin", "password": "admin123"}')
        

        frame = context.pages[-1]
        # Click POST button to send login request and obtain JWT token
        elem = frame.locator('xpath=html/body/div/div[2]/div/div[3]/div/div/form/fieldset/div[3]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Send POST requests to update appointment status with valid status values ('pending', 'confirmed', 'completed', 'cancelled') using the obtained JWT token.
        await page.goto('http://localhost:8000/api/appointments/1/status/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Send POST requests to /api/appointments/1/update/ with valid status values ('pending', 'confirmed', 'completed', 'cancelled') using JWT token for authorization and verify response status 200.
        await page.goto('http://localhost:8000/api/appointments/1/update/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Input admin credentials and login to authenticate and proceed with appointment status update testing.
        frame = context.pages[-1]
        # Input username 'admin' for login
        elem = frame.locator('xpath=html/body/div/form/p/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin')
        

        frame = context.pages[-1]
        # Input password 'admin123' for login
        elem = frame.locator('xpath=html/body/div/form/p[2]/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin123')
        

        frame = context.pages[-1]
        # Click login button to submit credentials
        elem = frame.locator('xpath=html/body/div/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        try:
            await expect(frame.locator('text=Appointment Status Updated Successfully').first).to_be_visible(timeout=1000)
        except AssertionError:
            raise AssertionError("Test case failed: Appointment status update test plan execution failed. Expected successful update confirmation message not found on the page.")
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    