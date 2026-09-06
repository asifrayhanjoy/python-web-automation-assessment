import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _as_bool(value: str, default: bool) -> bool:
    if value.lower() in {"1", "true", "yes", "on"}:
        return True
    if value.lower() in {"0", "false", "no", "off"}:
        return False
    return default


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://www.google.com/recaptcha/api2/demo")
    headless: bool = _as_bool(os.getenv("HEADLESS", "false"), False)
    verification_timeout_ms: int = int(os.getenv("VERIFICATION_TIMEOUT_MS", "180000"))
    page_timeout_ms: int = int(os.getenv("PAGE_TIMEOUT_MS", "30000"))
    screenshots_dir: Path = PROJECT_ROOT / "screenshots"
    logs_dir: Path = PROJECT_ROOT / "logs"

    def ensure_output_directories(self) -> None:
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
