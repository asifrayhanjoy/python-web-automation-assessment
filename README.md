# Python Web Automation Assessment

## Project Purpose

This project demonstrates a professional, safety-conscious Playwright workflow against Google's public reCAPTCHA demo page:

`https://www.google.com/recaptcha/api2/demo`

The automation launches headed Chromium, waits for the page and verification component, pauses for a person to complete the permitted verification, detects the resulting state, submits the demo form, detects the final result, and records logs and screenshots.

This project does **not** bypass, defeat, solve, or automate reCAPTCHA. It does not use CAPTCHA-solving services or attempt to evade anti-bot controls.

## Technology Stack

- Python 3.9+
- Playwright
- Chromium
- pytest
- Python `logging`
- Git/GitHub

No FastAPI, database, frontend framework, or backend service is required.

## Project Structure

```text
python-web-automation-assessment/
├── automation/
│   ├── main.py
│   ├── config.py
│   └── utils.py
├── tests/
│   └── test_automation.py
├── screenshots/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

Use Python 3.9 or newer:

```bash
cd python-web-automation-assessment
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install the Playwright Chromium browser:

```bash
playwright install chromium
```

## Run the Automation

The automation must be run in a headed browser because a human must complete the permitted verification step:

```bash
source .venv/bin/activate
python automation/main.py
```

Workflow:

1. Start Playwright and Chromium.
2. Open the Google reCAPTCHA demo page.
3. Wait for the page and reCAPTCHA iframe.
4. Leave the verification interaction to the human operator.
5. Detect the completed state using publicly exposed page state.
6. Submit the demo form using its normal submit control.
7. Detect the successful final result.
8. Save the success screenshot and close Chromium safely.

Do not click the reCAPTCHA checkbox from automation. Complete it manually in the headed browser when prompted. The default manual timeout is three minutes.

## Configuration

Configuration is read from environment variables:

```bash
BASE_URL=https://www.google.com/recaptcha/api2/demo
HEADLESS=false
VERIFICATION_TIMEOUT_MS=180000
PAGE_TIMEOUT_MS=30000
```

For safety and observability, headed mode is the default. `HEADLESS=true` is available for diagnostics, but manual verification generally requires headed mode.

## Run Tests

```bash
pytest -q
```

The tests are offline unit tests. They validate the Google demo target, headed default, and verification-state detection without attempting to solve or automate reCAPTCHA.

## Output

- Successful run: `screenshots/success.png`
- Failed run after a page opens: `screenshots/error.png`
- Execution log: `logs/automation.log`

The log includes clear milestones such as:

```text
[INFO] Starting Playwright...
[INFO] Launching Chromium...
[INFO] Opening Google reCAPTCHA demo...
[INFO] Page loaded successfully.
[INFO] Verification component detected.
[INFO] Waiting for permitted/manual verification...
[INFO] Verification completed.
[INFO] Verification state confirmed.
[INFO] Screenshot saved.
[INFO] AUTOMATION COMPLETED SUCCESSFULLY
```

## Architecture

- `automation/config.py` owns environment-based settings and output directories.
- `automation/utils.py` owns logging setup and the small verification-state predicate.
- `automation/main.py` owns browser lifecycle, reliable waits, verification detection, form submission, final-result detection, screenshots, and error handling.
- `tests/test_automation.py` covers the deterministic parts without contacting or attempting to solve the protected interaction.

## Verification and Safety Limitation

The reCAPTCHA checkbox and any challenge are strictly manual/permitted interactions. Playwright only observes completion state after the operator finishes. The project does not inject tokens, click challenge controls, use external solvers, defeat reCAPTCHA, hide automation, or circumvent Google's anti-bot mechanisms.

The public demo page may change its markup, network behavior, or availability. If that happens, the selectors should be reviewed against the current page rather than bypassing the verification mechanism.

## Error Handling

Timeouts and unexpected exceptions are logged at `ERROR` level. A failure screenshot is attempted when a page exists, and the browser is closed in a `finally` block inside the Playwright context.

## GitHub Readiness

Generated logs, screenshots, Python caches, virtual environments, and `.env` files are excluded by `.gitignore`. No secrets are required or stored.
