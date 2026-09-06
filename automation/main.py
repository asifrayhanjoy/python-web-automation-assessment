import argparse
import logging
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, Playwright, TimeoutError as PlaywrightTimeoutError, sync_playwright

from config import Settings
from utils import configure_logging, verification_is_complete


class AutomationError(RuntimeError):
    """Raised when the permitted verification workflow cannot complete safely."""


def launch_browser(playwright: Playwright, settings: Settings, logger: logging.Logger) -> Browser:
    logger.info("Starting Playwright...")
    logger.info("Launching Chromium...")
    return playwright.chromium.launch(headless=settings.headless)


def open_demo_page(browser: Browser, settings: Settings, logger: logging.Logger) -> Page:
    page = browser.new_page()
    page.set_default_timeout(settings.page_timeout_ms)
    logger.info("Opening Google reCAPTCHA demo...")
    page.goto(settings.base_url, wait_until="domcontentloaded")
    page.locator("body").wait_for(state="visible")
    logger.info("Page loaded successfully.")
    return page


def detect_verification_component(page: Page, logger: logging.Logger) -> None:
    try:
        page.locator('iframe[title="reCAPTCHA"]').first.wait_for(state="visible")
    except PlaywrightTimeoutError as exc:
        raise AutomationError("The reCAPTCHA verification component was not detected.") from exc
    logger.info("Verification component detected.")


def _verification_state(page: Page) -> tuple[bool, str]:
    checkbox_checked = False
    checkbox_frame = page.locator('iframe[title="reCAPTCHA"]').first.content_frame
    try:
        checkbox_checked = checkbox_frame.locator('[role="checkbox"]').get_attribute("aria-checked") == "true"
    except PlaywrightTimeoutError:
        pass
    token = page.locator("#g-recaptcha-response, #recaptcha-token").first
    token_value = token.input_value() if token.count() else ""
    return checkbox_checked, token_value


def wait_for_verification(page: Page, settings: Settings, logger: logging.Logger) -> None:
    logger.info("Waiting for permitted/manual verification...")
    try:
        page.wait_for_function(
            """() => {
                const token = document.querySelector('#g-recaptcha-response, #recaptcha-token');
                return Boolean(token?.value);
            }""",
            timeout=settings.verification_timeout_ms,
        )
    except PlaywrightTimeoutError as exc:
        raise AutomationError(
            "Manual verification was not completed before the timeout. "
            "Complete the reCAPTCHA in the headed browser; this project never solves it automatically."
        ) from exc
    checkbox_checked, token_value = _verification_state(page)
    if not verification_is_complete(checkbox_checked, token_value):
        raise AutomationError("Verification state could not be confirmed.")
    logger.info("Verification completed.")
    logger.info("Verification state confirmed.")


def submit_demo_form(page: Page, logger: logging.Logger) -> None:
    logger.info("Submitting the demo form...")
    submit_button = page.locator('input[type="submit"], button[type="submit"]').first
    try:
        submit_button.wait_for(state="visible")
        submit_button.click()
        page.wait_for_load_state("domcontentloaded")
    except PlaywrightTimeoutError as exc:
        raise AutomationError("The demo form submit control was not available.") from exc
    logger.info("Demo form submitted.")


def detect_final_result(page: Page, logger: logging.Logger) -> str:
    result = page.locator("body").inner_text()
    success_markers = ("success", "verified", "verification successful")
    if not any(marker in result.lower() for marker in success_markers):
        raise AutomationError("The final page did not show a successful verification result.")
    logger.info("Final verification result detected.")
    return result


def capture_screenshot(page: Page, path: Path, logger: logging.Logger) -> None:
    page.screenshot(path=str(path), full_page=True)
    logger.info("Screenshot saved to %s.", path)


def run_automation() -> dict[str, Any]:
    settings = Settings()
    settings.ensure_output_directories()
    logger = configure_logging(settings.logs_dir / "automation.log")
    browser = None
    page = None
    logger.info("# ==================================================")
    logger.info("PYTHON WEB AUTOMATION ASSESSMENT")
    with sync_playwright() as playwright:
        try:
            browser = launch_browser(playwright, settings, logger)
            page = open_demo_page(browser, settings, logger)
            detect_verification_component(page, logger)
            wait_for_verification(page, settings, logger)
            submit_demo_form(page, logger)
            result = detect_final_result(page, logger)
            capture_screenshot(page, settings.screenshots_dir / "success.png", logger)
            logger.info("AUTOMATION COMPLETED SUCCESSFULLY")
            logger.info("# ==================================================")
            return {"success": True, "result": result}
        except Exception:
            logger.exception("Automation failed.")
            if page is not None:
                try:
                    capture_screenshot(page, settings.screenshots_dir / "error.png", logger)
                except Exception:
                    logger.exception("Could not capture the error screenshot.")
            raise
        finally:
            if browser is not None:
                browser.close()
                logger.info("Browser closed safely.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the permitted Google reCAPTCHA demo workflow.")
    return parser.parse_args()


if __name__ == "__main__":
    parse_args()
    run_automation()
