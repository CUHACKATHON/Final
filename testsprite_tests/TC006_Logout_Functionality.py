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
        # -> Click on the Login link to go to the login page.
        frame = context.pages[-1]
        # Click on the Login link to navigate to the login page.
        elem = frame.locator('xpath=html/body/nav/div/div/a[6]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Input admin username and password, then click login button.
        frame = context.pages[-1]
        # Input admin username
        elem = frame.locator('xpath=html/body/div/form/p/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin')
        

        frame = context.pages[-1]
        # Input admin password
        elem = frame.locator('xpath=html/body/div/form/p[2]/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin123')
        

        frame = context.pages[-1]
        # Click login button to submit login form
        elem = frame.locator('xpath=html/body/div/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Try to navigate back to home page and check if logout link is available or try alternative login method or user.
        frame = context.pages[-1]
        # Click 'Back to Home' link to return to home page and check for logout or login options.
        elem = frame.locator('xpath=html/body/div/div[3]/p[3]/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on Login link to navigate to login page and attempt login.
        frame = context.pages[-1]
        # Click on Login link to navigate to login page
        elem = frame.locator('xpath=html/body/nav/div/div/a[6]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Input admin username and password, then click login button to attempt login.
        frame = context.pages[-1]
        # Input admin username
        elem = frame.locator('xpath=html/body/div/form/p/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin')
        

        frame = context.pages[-1]
        # Input admin password
        elem = frame.locator('xpath=html/body/div/form/p[2]/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin123')
        

        frame = context.pages[-1]
        # Click login button to submit login form
        elem = frame.locator('xpath=html/body/div/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Try alternative login method using JSON POST request to /login/ endpoint to obtain JWT token for authentication.
        await page.goto('http://localhost:8000/api/login/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Navigate to /api/auth/login/ to attempt JSON POST login for JWT token.
        await page.goto('http://localhost:8000/api/auth/login/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Input JSON payload with admin credentials and click POST button to attempt login.
        frame = context.pages[-1]
        # Input JSON payload with admin credentials
        elem = frame.locator('xpath=html/body/div/div[2]/div/div[3]/div/div/form/fieldset/div[2]/div/textarea').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('{"username":"admin","password":"admin123"}')
        

        frame = context.pages[-1]
        # Click POST button to send JSON login request
        elem = frame.locator('xpath=html/body/div/div[2]/div/div[3]/div/div/form/fieldset/div[3]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Navigate to home page or dashboard to verify login state and presence of logout link.
        await page.goto('http://localhost:8000', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Check if logout link is present in the navigation bar or elsewhere on the page to trigger logout.
        await page.mouse.wheel(0, 300)
        

        # -> Try to find logout link or user menu by scrolling down or searching for logout link text on the page.
        await page.mouse.wheel(0, 500)
        

        # -> Check localStorage for JWT token presence to confirm token storage and then navigate to a protected page to trigger UI update for logged-in state.
        await page.goto('http://localhost:8000/appointments/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Manually clear any session or token data and navigate to home page to verify logout state and redirection.
        await page.goto('http://localhost:8000/logout/', timeout=10000)
        await asyncio.sleep(3)
        

        await page.goto('http://localhost:8000', timeout=10000)
        await asyncio.sleep(3)
        

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
        await expect(frame.locator('text=Your Mental Health Matters').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    