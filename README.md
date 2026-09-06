# Python Web Automation Assessment

A Python + Playwright web automation assessment demonstrating reliable browser automation, verification-state detection, form submission, logging, screenshots, and pytest-based testing.

## Project Purpose

This project demonstrates a professional Playwright workflow against Google's public [reCAPTCHA demo page](https://www.google.com/recaptcha/api2/demo).

The automation:

1. Launches a headed Chromium browser.
2. Opens the Google reCAPTCHA demo page.
3. Waits for the page and verification component to load.
4. Pauses for a person to complete the permitted verification manually.
5. Detects the verification state.
6. Submits the demo form.
7. Detects the final submission result.
8. Captures screenshots.
9. Records structured execution logs.
10. Handles timeouts and unexpected errors safely.

The project does **not** bypass, defeat, solve, or automate reCAPTCHA and does not use CAPTCHA-solving services.

## Features

- Playwright browser automation with Chromium
- Headed browser execution
- Reliable page and element waits
- Manual reCAPTCHA verification
- Verification-state detection
- Demo form submission
- Success and failure screenshots
- Structured execution logging
- Timeout and exception handling
- Offline pytest unit tests
- Clean project structure
- Git/GitHub ready

## Technology Stack

- Python 3.9+
- Playwright
- Chromium
- pytest
- Python logging
- Git
- GitHub

No FastAPI, database, frontend framework, or backend service is required for this assessment.

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

### 1. Clone the repository

```bash
git clone https://github.com/asifrayhan/python-web-automation-assessment.git
cd python-web-automation-assessment
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Install Chromium

```bash
playwright install chromium
```

## Run the Automation

Run the automation from the project root:

```bash
python automation/main.py
```

The browser runs in **headed mode** because the verification step requires a person to complete the permitted reCAPTCHA verification manually.

For normal execution, keep `HEADLESS=false` because the verification step requires a visible browser.

### Expected Workflow

```text
Start
  |
Launch Chromium
  |
Open reCAPTCHA Demo Page
  |
Detect Verification Component
  |
Wait for Manual Verification
  |
Confirm Verification State
  |
Submit Demo Form
  |
Detect Final Result
  |
Save Screenshot
  |
Write Execution Log
  |
Complete Successfully
```

## Configuration

The automation supports the following environment variables:

```bash
BASE_URL=https://www.google.com/recaptcha/api2/demo
HEADLESS=false
VERIFICATION_TIMEOUT_MS=180000
PAGE_TIMEOUT_MS=30000
```

| Variable | Description | Default |
| --- | --- | --- |
| `BASE_URL` | Google reCAPTCHA demo page | `https://www.google.com/recaptcha/api2/demo` |
| `HEADLESS` | Run the browser without a visible UI | `false` |
| `VERIFICATION_TIMEOUT_MS` | Maximum manual verification wait time | `180000` |
| `PAGE_TIMEOUT_MS` | Page operation timeout | `30000` |

The default verification timeout is **three minutes**.

## Run Tests

Run the test suite with:

```bash
pytest -q
```

The tests are offline unit tests. They do not require CAPTCHA solving, external services, or a running application server.

Current test validation:

```text
6 passed
```

## Output

### Screenshots

Successful automation produces:

```text
screenshots/success.png
```

Failed automation can produce:

```text
screenshots/error.png
```

### Logs

Execution logs are written to:

```text
logs/automation.log
```

The logs record important automation stages such as:

- Browser startup
- Page loading
- Verification detection
- Verification completion
- Form submission
- Final result detection
- Screenshot creation
- Errors and exceptions
- Browser shutdown

## Architecture

### `automation/main.py`

Main Playwright automation workflow responsible for:

- Launching Chromium
- Opening the demo page
- Detecting the verification component
- Waiting for manual verification
- Detecting verification state
- Submitting the form
- Detecting the final result
- Capturing screenshots
- Handling exceptions
- Closing the browser safely

### `automation/config.py`

Central configuration for:

- Demo URL
- Browser mode
- Page timeout
- Verification timeout
- Screenshot and log paths

### `automation/utils.py`

Reusable utilities for:

- Logging configuration
- Verification-state evaluation

### `tests/test_automation.py`

Offline pytest unit tests covering core helper and configuration behavior.

## Verification and Safety Limitation

This project intentionally uses **manual/permitted verification only**.

It does not:

- Automatically click or solve CAPTCHA challenges
- Attempt to bypass reCAPTCHA
- Inject CAPTCHA tokens
- Use CAPTCHA-solving APIs or external solver services
- Automate challenge answers
- Defeat anti-bot protections
- Circumvent verification mechanisms
- Circumvent Google's security controls

The human verification step is intentionally preserved as part of the assessment workflow.

## Error Handling

The automation includes defensive error handling for:

- Page load failures
- Missing verification components
- Verification timeouts
- Form submission errors
- Unexpected Playwright exceptions
- Screenshot failures
- Browser shutdown

When an error occurs, the automation records the failure in the log and attempts to capture an error screenshot before safely closing the browser.

## GitHub Readiness

The repository is configured to avoid committing generated or environment-specific files such as:

```text
.venv/
.pytest_cache/
__pycache__/
*.pyc
.env
logs/automation.log
screenshots/success.png
screenshots/error.png
.DS_Store
```

Only source code, tests, configuration, documentation, and required placeholder files are intended to be committed.

## Validation Status

The project has been validated with:

- Python environment working
- Chromium launching successfully
- Playwright automation completing successfully
- Manual reCAPTCHA verification working
- Verification-state detection working
- Demo form submission working
- Success screenshot generation working
- Execution logging working
- Pytest test suite passing

Latest test result:

```text
6 passed in 0.01s
```

## Demo

A short demonstration video can be added here showing:

1. Project structure
2. Automation command
3. Chromium browser launch
4. Manual verification
5. Verification-state detection
6. Demo form submission
7. Success result
8. Screenshot and log generation

> Demo video link will be added after recording the final walkthrough.

## Author

**MD. ASIF RAYHAN JOY**

Full-Stack Web Developer

- GitHub: [asifrayhan](https://github.com/asifrayhan)
- Portfolio: [Portfolio](https://portfolio-neon-omega-77.vercel.app/)
- LinkedIn: [LinkedIn](https://www.linkedin.com/in/md-asif-rayhan-joy-4177372a4/)
