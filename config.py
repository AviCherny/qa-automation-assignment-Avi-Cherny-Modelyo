import os

UI_BASE_URL = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

WORKERS = int(os.getenv("WORKERS", "1"))  # parallel workers — 1 = serial

# Playwright
PLAYWRIGHT_HEADED = os.getenv("HEADED", "true") == "true"
PLAYWRIGHT_TIMEOUT = int(os.getenv("TIMEOUT", "10000"))
PLAYWRIGHT_TRACE_DIR = "traces/"
PLAYWRIGHT_VIDEO_DIR = "videos/"
