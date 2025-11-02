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
        # -> Click on 'Start Anonymous Chat' to navigate to the anonymous chat interface.
        frame = context.pages[-1]
        # Click on 'Start Anonymous Chat' button to open the anonymous chat interface.
        elem = frame.locator('xpath=html/body/main/div/div/div[2]/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Send an initial message to the chatbot without a session ID.
        frame = context.pages[-1]
        # Input initial message to chatbot without session ID.
        elem = frame.locator('xpath=html/body/main/div/div[5]/textarea').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('Hello, how are you?')
        

        frame = context.pages[-1]
        # Click Send button to send the initial message.
        elem = frame.locator('xpath=html/body/main/div/div[5]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Send a follow-up message to the chatbot to verify if the conversation context is maintained without an explicit session ID.
        frame = context.pages[-1]
        # Input follow-up message to test session persistence without session ID.
        elem = frame.locator('xpath=html/body/main/div/div[5]/textarea').nth(0)
        await page.wait_for_timeout(3000); await elem.fill('Can you remember what I said earlier?')
        

        frame = context.pages[-1]
        # Click Send button to send the follow-up message.
        elem = frame.locator('xpath=html/body/main/div/div[5]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=Hello, how are you?').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Namaste! I\'m here to listen and help. What would you like to talk about?').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Can you remember what I said earlier?').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    