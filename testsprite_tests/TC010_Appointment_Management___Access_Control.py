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
        # -> Attempt to access '/appointments/manage/' without authentication.
        await page.goto('http://localhost:8000/appointments/manage/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Log in as counselor with username 'counselor1' and password 'counselor123'.
        frame = context.pages[-1]
        # Input counselor username
        elem = frame.locator('xpath=html/body/div/form/p/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('counselor1')
        

        frame = context.pages[-1]
        # Input counselor password
        elem = frame.locator('xpath=html/body/div/form/p[2]/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('counselor123')
        

        frame = context.pages[-1]
        # Click login button
        elem = frame.locator('xpath=html/body/div/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on 'Appointments' link in the navigation to access the appointments management page.
        frame = context.pages[-1]
        # Click on 'Appointments' link in the navigation bar
        elem = frame.locator('xpath=html/body/nav/div/div/a[3]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Navigate directly to '/appointments/manage/' URL while logged in as counselor to verify access and page content.
        await page.goto('http://localhost:8000/appointments/manage/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Log out counselor1 and log in as admin using admin/admin123 credentials to verify admin access to the appointment management page.
        frame = context.pages[-1]
        # Click logout (counselor1) to log out
        elem = frame.locator('xpath=html/body/nav/div/div/a[7]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on 'Login' link to go to login page for admin login.
        frame = context.pages[-1]
        # Click on 'Login' link to go to login page
        elem = frame.locator('xpath=html/body/nav/div/div/a[6]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Input admin username 'admin' and password 'admin123' and click login.
        frame = context.pages[-1]
        # Input admin username
        elem = frame.locator('xpath=html/body/div/form/p/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin')
        

        frame = context.pages[-1]
        # Input admin password
        elem = frame.locator('xpath=html/body/div/form/p[2]/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin123')
        

        frame = context.pages[-1]
        # Click login button
        elem = frame.locator('xpath=html/body/div/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on 'Appointments' link in the navigation bar to access the appointment management page as admin.
        frame = context.pages[-1]
        # Click on 'Appointments' link in the navigation bar
        elem = frame.locator('xpath=html/body/nav/div/div/a[3]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Navigate directly to '/appointments/manage/' URL while logged in as admin to verify access and page content.
        await page.goto('http://localhost:8000/appointments/manage/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Log out admin user to prepare for regular user login and access test.
        frame = context.pages[-1]
        # Click logout (admin) to log out
        elem = frame.locator('xpath=html/body/nav/div/div/a[7]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on 'Login' link to go to login page for regular user login.
        frame = context.pages[-1]
        # Click on 'Login' link to go to login page
        elem = frame.locator('xpath=html/body/nav/div/div/a[6]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on 'Register as User' link to check if it leads to regular user registration or login page.
        frame = context.pages[-1]
        # Click on 'Register as User' link
        elem = frame.locator('xpath=html/body/div/div/p/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on 'Login here' link to navigate to regular user login page for testuser login.
        frame = context.pages[-1]
        # Click on 'Login here' link to go to regular user login page
        elem = frame.locator('xpath=html/body/main/div/div/p/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=Admin/Counselor Login').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    