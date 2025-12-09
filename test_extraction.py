import sys
import os

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

from arxiv2epub import extract_arxiv_id


def test_extraction():
    test_cases = [
        ("2501.00601", "2501.00601"),
        ("https://arxiv.org/abs/2501.00601", "2501.00601"),
        ("2501.00601/", "2501.00601"),
        (" https://arxiv.org/abs/2501.00601/ ", "2501.00601"),
        ("http://arxiv.org/pdf/2101.12345", "2101.12345"),
    ]

    for input_str, expected in test_cases:
        result = extract_arxiv_id(input_str)
        if result == expected:
            print(f"PASS: '{input_str}' -> '{result}'")
        else:
            print(f"FAIL: '{input_str}' -> '{result}' (expected '{expected}')")


if __name__ == "__main__":
    test_extraction()
