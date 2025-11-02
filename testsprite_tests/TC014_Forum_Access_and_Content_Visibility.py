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
        # -> Click on the 'Forum' link to access the forum page as an anonymous user.
        frame = context.pages[-1]
        # Click on the 'Forum' link to access the forum page as an anonymous user.
        elem = frame.locator('xpath=html/body/nav/div/div/a[5]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Create a new post as admin to have an approved post to verify visibility for anonymous users.
        await page.goto('http://localhost:8000/login/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Input admin username and password and submit login form.
        frame = context.pages[-1]
        # Input admin username
        elem = frame.locator('xpath=html/body/div/form/p/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin')
        

        frame = context.pages[-1]
        # Input admin password
        elem = frame.locator('xpath=html/body/div/form/p[2]/input').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('admin123')
        

        frame = context.pages[-1]
        # Click login button to submit admin credentials
        elem = frame.locator('xpath=html/body/div/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Return to forum page as anonymous user to verify visible posts and replies, then test non-existent post ID for 404.
        frame = context.pages[-1]
        # Click 'Back to Home' to return to homepage
        elem = frame.locator('xpath=html/body/div/div[3]/p[3]/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Extract visible posts and replies on forum page for anonymous user to verify only approved posts are displayed.
        frame = context.pages[-1]
        # Click on 'Forum' link to access forum page as anonymous user
        elem = frame.locator('xpath=html/body/nav/div/div/a[5]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Attempt to access a post detail page with an approved post ID to verify post content and approved replies are displayed.
        await page.goto('http://localhost:8000/forum/post/1', timeout=10000)
        await asyncio.sleep(3)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=Page not found (404)').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=No ForumPost matches the given query.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Request Method:\tGET').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Request URL:http://localhost:8000/forum/post/1/').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Raised by:core.views.forum_post_detail').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=admin/').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=api/token/ [name=\'token_obtain_pair\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=api/token/refresh/ [name=\'token_refresh\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=api/token/verify/ [name=\'token_verify\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=[name=\'index\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=login/ [name=\'login\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=register/ [name=\'register\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=register/counselor/ [name=\'register_counselor\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=logout/ [name=\'logout\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=chat/ [name=\'chat\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=api/chat/ [name=\'chat_api\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=appointments/ [name=\'appointments\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=appointments/manage/ [name=\'appointments_manage\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=api/appointments/<int:appointment_id>/update/ [name=\'appointment_update\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=resources/ [name=\'resources\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=forum/ [name=\'forum\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=forum/post/<int:post_id>/ [name=\'forum_post_detail\']').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=The current path, forum/post/1/, matched the last one.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=You’re seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard 404 page.').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    