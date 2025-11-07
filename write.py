import time
import random
import argparse
import sys
from typing import Callable

# write.py
# A simple typer using pyautogui. Edit TEXT below or pass --text "your text".
# Focus the target window within initial_delay seconds.

try:
    import pyautogui
except ImportError:
    print("pyautogui is required. Install with: pip install pyautogui")
    sys.exit(1)

pyautogui.FAILSAFE = True  # move mouse to a corner to abort

# Try to provide a reliable clipboard paste helper for characters that
# cannot be typed directly by pyautogui on some keyboard layouts (e.g. å, ä, ö).
_clipboard_copy: Callable[[str], None]
try:
    import pyperclip

    def _clipboard_copy(s: str):
        pyperclip.copy(s)
except Exception:
    # Fallback to tkinter clipboard if pyperclip is not available. This
    # may still fail in some headless or restricted environments, so we
    # leave a final fallback that raises an informative error if neither
    # approach works when needed.
    try:
        import tkinter as _tk

        def _clipboard_copy(s: str):
            r = _tk.Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(s)
            # ensure the clipboard is updated
            r.update()
            r.destroy()
    except Exception:
        def _clipboard_copy(s: str):
            raise RuntimeError("No clipboard helper available; install 'pyperclip' to enable pasting non-ASCII characters")

# Default text to type if none provided via CLI
TEXT = "Hello, World!\nThis is a test of the typing script.\nHere are some Swedish letters: åäö ÅÄÖ\n"

def simulate_typing(text: str, initial_delay: float = 5.0,
                    min_interval: float = 0.01, max_interval: float = 0.10,
                    randomize: bool = True):
    """
    Type `text` using pyautogui.
    - initial_delay: seconds to wait before starting (to focus target window)
    - min_interval / max_interval: per-character delay range in seconds
    - randomize: if True, choose a random interval per character between min/max;
                 if False, uses fixed interval = min_interval
    Newlines and tabs are converted to enter/tab key presses for reliability.
    """
    if min_interval < 0 or max_interval < 0 or min_interval > max_interval:
        raise ValueError("Invalid interval values")

    print(f"Starting in {initial_delay} seconds. Move focus to the target window. (Abort: move mouse to a corner)")
    try:
        time.sleep(initial_delay)
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            if ch == "\n":
                pyautogui.press("enter")
                i += 1
                continue
            if ch == "\t":
                pyautogui.press("tab")
                i += 1
                continue

            # Determine interval for this step (used for sleeping after action)
            if randomize and max_interval > min_interval:
                interval = random.uniform(min_interval, max_interval)
            else:
                interval = min_interval

            # If the upcoming 'word' (sequence until whitespace) contains any
            # non-ASCII characters, paste the whole word at once. This
            # prevents composition/IME issues that can insert a stray space
            # when switching between typing and pasting at a character
            # boundary (e.g. "hallå" becoming "hall å").
            if not ch.isspace():
                # find end of the current word
                j = i
                has_non_ascii = False
                while j < n and not text[j].isspace():
                    if ord(text[j]) > 127:
                        has_non_ascii = True
                    j += 1

                if has_non_ascii:
                    word = text[i:j]
                    try:
                        _clipboard_copy(word)
                        pyautogui.hotkey('ctrl', 'v')
                    except RuntimeError as re:
                        print(f"Clipboard helper error: {re}. Falling back to direct write for {word!r}.")
                        pyautogui.write(word, interval=0)

                    # Sleep a bit to simulate typing time for the pasted chunk
                    # (approximate per-character delay)
                    time.sleep(interval * max(1, len(word)))
                    i = j
                    continue

            # Default: type single character (ASCII or others as direct write)
            try:
                pyautogui.write(ch, interval=0)
            except Exception:
                # If direct write fails for some reason, try clipboard fallback
                try:
                    _clipboard_copy(ch)
                    pyautogui.hotkey('ctrl', 'v')
                except Exception as e:
                    print(f"Failed to input character {ch!r}: {e}")
            time.sleep(interval)
            i += 1
    except KeyboardInterrupt:
        print("\nTyping interrupted by user.")
        return

def parse_args():
    p = argparse.ArgumentParser(description="Type text by simulating keypresses with pyautogui.")
    p.add_argument("--text", "-t", type=str, help="Text to type. If omitted, uses TEXT in the file.")
    p.add_argument("--file", "-f", type=str, help="Path to a file whose contents will be typed.")
    p.add_argument("--delay", "-d", type=float, default=5.0, help="Initial delay in seconds before typing starts.")
    p.add_argument("--min-interval", type=float, default=0.02, help="Minimum per-character delay (seconds).")
    p.add_argument("--max-interval", type=float, default=0.12, help="Maximum per-character delay (seconds).")
    p.add_argument("--no-random", action="store_true", help="Disable per-character interval randomization.")
    return p.parse_args()

def main():
    args = parse_args()


    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                text = fh.read()
        except Exception as e:
            print(f"Failed to read file: {e}")
            sys.exit(1)
    elif args.text is not None:
        text = args.text
    else:
        # Try to read text.txt if present
        try:
            with open("text.txt", "r", encoding="utf-8") as fh:
                text = fh.read()
            print("Using text from text.txt.")
        except Exception:
            text = TEXT
            print("Using default TEXT variable.")

    simulate_typing(text,
                    initial_delay=args.delay,
                    min_interval=args.min_interval,
                    max_interval=args.max_interval,
                    randomize=not args.no_random)

if __name__ == "__main__":
    main()