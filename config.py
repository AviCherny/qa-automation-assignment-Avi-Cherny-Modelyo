import os

UI_BASE_URL = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

# Playwright
PLAYWRIGHT_HEADLESS = os.getenv("HEADED") != "true"
PLAYWRIGHT_TIMEOUT = int(os.getenv("TIMEOUT", "10000"))
PLAYWRIGHT_TRACE_DIR = "traces/"
PLAYWRIGHT_VIDEO_DIR = "videos/"
