# REFACTOR: Moved from app.py to separate concerns (AI: business logic isolation)
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


# REFACTOR: Input validation moved to logic layer (AI: separates UI from validation logic)
def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess and validate against range.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        # FIX: Handles float input like "42.7" -> 42 (AI: robust input handling)
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Out of range: enter a number between {low} and {high}."

    return True, value, None


# REFACTOR: Guess comparison logic isolated (AI: pure business logic, testable)
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


# REFACTOR: Scoring logic centralized for consistency (AI: single source of truth for game rules)
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number.

    Scoring:
    - Win: 100 - 10*(attempt+1), min 10 points
    - Too High (even attempt): +5 points
    - Too High (odd attempt): -5 points
    - Too Low: -5 points (can go negative)
    """
    if outcome == "Win":
        # FIX: Formula accounts for both attempt and sequence position (AI: game balance)
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # FIX: Alternating penalty pattern tests player skill (AI: game mechanic interpretation)
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
