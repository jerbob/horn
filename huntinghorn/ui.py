from typing import Optional

from prompt_toolkit import completion, key_binding, prompt
from prompt_toolkit.filters import completion_is_selected, has_completions

from huntinghorn.constants import horns
from huntinghorn.utils import Horn


key_bindings = key_binding.KeyBindings()
completer = completion.FuzzyWordCompleter(horns.keys())


@key_bindings.add("enter", filter=has_completions & ~completion_is_selected)
def validate_text(event: key_binding.key_processor.KeyPressEvent) -> None:
    """Validate the current selection once enter is pressed."""
    event.current_buffer.go_to_completion(0)
    event.current_buffer.validate_and_handle()


def prompt_for_horn() -> Optional[Horn]:
    """Prompt the user to select a Horn."""
    name = str(prompt(
        "Horn: ",
        completer=completer,
        complete_while_typing=True,
        key_bindings=key_bindings,
    ))
    print()
    return horns.get(name)
