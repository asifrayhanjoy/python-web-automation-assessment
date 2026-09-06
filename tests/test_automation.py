import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "automation"))

from config import Settings  # noqa: E402
from utils import verification_is_complete  # noqa: E402


def test_default_target_is_google_recaptcha_demo() -> None:
    assert Settings().base_url == "https://www.google.com/recaptcha/api2/demo"


def test_headed_mode_is_the_default() -> None:
    assert Settings().headless is False


@pytest.mark.parametrize(
    ("checkbox_checked", "token_value", "expected"),
    [(True, "", True), (False, "verified-token", True), (False, "", False)],
)
def test_verification_state_is_detected(
    checkbox_checked: bool, token_value: str, expected: bool
) -> None:
    assert verification_is_complete(checkbox_checked, token_value) is expected


def test_empty_verification_token_is_not_successful() -> None:
    assert verification_is_complete(False, "   ") is False
