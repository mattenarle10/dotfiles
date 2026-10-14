#!/usr/bin/env python3
"""Reject misplaced RTK prefixes while the native hook handles compression."""

import json
import re
import sys


# Remove only a leading wrapper; preserve the original shell text and quoting.
MACOS_PREFIX = re.compile(
    r'\A(?P<indent>[ \t]*)rtk[ \t]+(?:proxy[ \t]+)?'
    r'(?=(?:/usr/bin/)?(?:open|osascript|pbcopy|pbpaste)(?:[ \t]|$))'
)


def main():
    raw = sys.stdin.read()
    try:
        event = json.loads(raw)
        if not isinstance(event, dict) or event.get('tool_name') != 'Bash':
            return
        tool_input = event.get('tool_input')
        if not isinstance(tool_input, dict):
            return
        command = tool_input.get('command')
        if not isinstance(command, str):
            return
    except (ValueError, TypeError):
        return

    corrected = MACOS_PREFIX.sub(r'\g<indent>', command, count=1)
    if corrected != command:
        # Hooks run in parallel; deny avoids competing command rewrites.
        print(json.dumps({'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny',
            'permissionDecisionReason': (
                'Do not wrap macOS utilities with RTK. Retry this command '
                'directly, preserving its arguments and normal approvals:\n'
                + corrected
            ),
        }}))


if __name__ == '__main__':
    main()
