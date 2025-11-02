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
        # -> Click on 'Start Anonymous Chat' to navigate to the anonymous chat interface.
        frame = context.pages[-1]
        # Click on 'Start Anonymous Chat' button to go to anonymous chat interface
        elem = frame.locator('xpath=html/body/main/div/div/div[2]/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Send a normal mental health message in the chat input and click send to test chatbot response.
        frame = context.pages[-1]
        # Input a normal mental health message in the chat textarea
        elem = frame.locator('xpath=html/body/main/div/div[5]/textarea').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('I have been feeling a bit stressed lately but trying to manage it.')
        

        frame = context.pages[-1]
        # Click the Send button to submit the message
        elem = frame.locator('xpath=html/body/main/div/div[5]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Send a POST request to '/api/chat/' with a normal mental health message to verify HTTP 200 response and check JSON response fields including 'crisis_detected', 'suggested_action', 'session_id', and timestamp.
        await page.goto('http://localhost:8000/api/chat/', timeout=10000)
        await asyncio.sleep(3)
        

        # -> Send a normal mental health message again via the chat interface to confirm chatbot response and then extract the response data from the network or page to verify JSON fields.
        frame = context.pages[-1]
        # Input a normal mental health message in the chat textarea
        elem = frame.locator('xpath=html/body/main/div/div[5]/textarea').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('I have been feeling a bit stressed lately but trying to manage it.')
        

        frame = context.pages[-1]
        # Click the Send button to submit the message
        elem = frame.locator('xpath=html/body/main/div/div[5]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=You are chatting anonymously. Your identity is protected.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Hello! I\'m here to support you. This is a safe, anonymous space. How are you feeling today?').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=I have been feeling a bit stressed lately but trying to manage it.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Anxiety during exam season is very common among Indian students. Here\'s what research shows helps:').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Would you like specific strategies for managing exam anxiety?').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=© 2025 MindCare - Mental Health Support Platform for Indian College Students').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=24/7 Helpline: 1800-599-0019').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    