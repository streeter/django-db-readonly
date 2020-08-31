from django.db.backends import utils

from readonly.cursor import (
    _is_readonly,
    PatchedCursorWrapper,
    PatchedCursorDebugWrapper,
)

if _is_readonly():
    # Monkey Patching!
    utils.CursorWrapper = PatchedCursorWrapper
    utils.CursorDebugWrapper = PatchedCursorDebugWrapper
