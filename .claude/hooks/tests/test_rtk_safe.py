import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import unittest
from unittest.mock import patch


HOOK = Path(__file__).resolve().parents[1] / 'rtk-safe.py'
spec = importlib.util.spec_from_file_location('rtk_safe', HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


class HookTests(unittest.TestCase):
    def invoke(self, command=None, event=None):
        if event is None:
            event = {'tool_name': 'Bash', 'tool_input': {'command': command}}
        raw = event if isinstance(event, str) else json.dumps(event)
        with patch.object(hook.sys, 'stdin', io.StringIO(raw)), \
                patch.object(hook.sys, 'stdout', io.StringIO()) as output:
            hook.main()
            text = output.getvalue()
        return json.loads(text) if text else None

    @unittest.skipUnless(shutil.which('rtk'), 'RTK is not installed')
    def test_native_hook_still_compresses_supported_commands(self):
        self.assertIsNone(self.invoke('git status --short'))
        result = subprocess.run(
            ['rtk', 'hook', 'claude'], text=True, capture_output=True,
            input=json.dumps({'tool_name': 'Bash', 'tool_input': {
                'command': 'git status --short',
            }}), check=True,
        )
        output = json.loads(result.stdout)['hookSpecificOutput']
        self.assertEqual(output['updatedInput']['command'], 'rtk git status --short')

    def test_raw_unsupported_command_is_untouched(self):
        for command in ('open -R "/tmp/a b.md"', 'osascript -e "display dialog 1"',
                        'pbcopy', 'pbpaste', 'unknown-local-tool --flag'):
            with self.subTest(command=command):
                self.assertIsNone(self.invoke(command))

    def test_invalid_prefix_gets_exact_retry_without_approval(self):
        for utility in ('open', '/usr/bin/open', 'osascript', 'pbcopy', 'pbpaste'):
            for prefix in ('rtk ', 'rtk proxy '):
                command = f'{utility} -R "/tmp/a b.md" && printf "%s" "open"'
                with self.subTest(utility=utility, prefix=prefix):
                    specific = self.invoke(prefix + command)['hookSpecificOutput']
                    self.assertEqual(specific['permissionDecision'], 'deny')
                    self.assertTrue(specific['permissionDecisionReason'].endswith('\n' + command))
                    self.assertNotIn('updatedInput', specific)

    def test_no_partial_name_or_argument_matches(self):
        for command in ('rtk openapi --help', 'echo "rtk open -R file"',
                        'rtk git status', 'rtk proxy custom-command', 'git status'):
            self.assertIsNone(self.invoke(command))

    def test_malformed_and_non_bash_events(self):
        for event in ('not JSON', '[]', '{}', '{"tool_name":"Read"}',
                      '{"tool_name":"Bash","tool_input":null}',
                      '{"tool_name":"Bash","tool_input":{"command":5}}'):
            self.assertIsNone(self.invoke(event=event))

    def test_both_hooks_are_registered_once(self):
        settings = HOOK.parents[1] / 'settings.json'
        data = json.loads(settings.read_text())
        commands = [h['command'] for group in data['hooks']['PreToolUse']
                    if group['matcher'] == 'Bash' for h in group['hooks']]
        self.assertEqual(commands.count('rtk hook claude'), 1)
        self.assertEqual(commands.count('python3 "$HOME/.claude/hooks/rtk-safe.py"'), 1)


if __name__ == '__main__':
    unittest.main()
