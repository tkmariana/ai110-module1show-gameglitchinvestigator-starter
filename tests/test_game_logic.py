"""
Pytest tests for game logic functions in logic_utils.py
Tests all the refactored game logic to ensure correctness.
"""

import pytest
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


class TestGetRangeForDifficulty:
    """Tests for get_range_for_difficulty function."""

    def test_easy_range(self):
        """Easy difficulty should return range 1-20."""
        low, high = get_range_for_difficulty("Easy")
        assert low == 1
        assert high == 20

    def test_normal_range(self):
        """Normal difficulty should return range 1-100."""
        low, high = get_range_for_difficulty("Normal")
        assert low == 1
        assert high == 100

    def test_hard_range(self):
        """Hard difficulty should return range 1-50."""
        low, high = get_range_for_difficulty("Hard")
        assert low == 1
        assert high == 50

    def test_unknown_difficulty_defaults_to_normal(self):
        """Unknown difficulty should default to Normal range."""
        low, high = get_range_for_difficulty("Impossible")
        assert low == 1
        assert high == 100


class TestCheckGuess:
    """Tests for check_guess function."""

    def test_winning_guess(self):
        """Correct guess should return Win outcome with message."""
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"
        assert message == "🎉 Correct!"

    def test_guess_too_high(self):
        """Guess higher than secret should return Too High."""
        outcome, message = check_guess(60, 50)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"

    def test_guess_too_low(self):
        """Guess lower than secret should return Too Low."""
        outcome, message = check_guess(40, 50)
        assert outcome == "Too Low"
        assert message == "📈 Go HIGHER!"

    def test_boundary_guess_just_below_secret(self):
        """Guess just below secret should be Too Low."""
        outcome, message = check_guess(49, 50)
        assert outcome == "Too Low"

    def test_boundary_guess_just_above_secret(self):
        """Guess just above secret should be Too High."""
        outcome, message = check_guess(51, 50)
        assert outcome == "Too High"


class TestParseGuess:
    """Tests for parse_guess function."""

    def test_valid_integer_guess(self):
        """Valid integer input should parse successfully."""
        ok, guess, err = parse_guess("42", 1, 100)
        assert ok is True
        assert guess == 42
        assert err is None

    def test_valid_float_guess_converts_to_int(self):
        """Float input like 42.7 should convert to int 42."""
        ok, guess, err = parse_guess("42.7", 1, 100)
        assert ok is True
        assert guess == 42
        assert err is None

    def test_empty_string_error(self):
        """Empty string should return error."""
        ok, guess, err = parse_guess("", 1, 100)
        assert ok is False
        assert guess is None
        assert err == "Enter a guess."

    def test_none_input_error(self):
        """None input should return error."""
        ok, guess, err = parse_guess(None, 1, 100)
        assert ok is False
        assert guess is None
        assert err == "Enter a guess."

    def test_non_numeric_input_error(self):
        """Non-numeric input should return error."""
        ok, guess, err = parse_guess("abc", 1, 100)
        assert ok is False
        assert guess is None
        assert err == "That is not a number."

    def test_guess_too_low(self):
        """Guess below range should return error."""
        ok, guess, err = parse_guess("0", 1, 100)
        assert ok is False
        assert guess is None
        assert err == "Out of range: enter a number between 1 and 100."

    def test_guess_too_high(self):
        """Guess above range should return error."""
        ok, guess, err = parse_guess("101", 1, 100)
        assert ok is False
        assert guess is None
        assert err == "Out of range: enter a number between 1 and 100."

    def test_guess_at_range_boundary_low(self):
        """Guess at low boundary should be valid."""
        ok, guess, err = parse_guess("1", 1, 100)
        assert ok is True
        assert guess == 1
        assert err is None

    def test_guess_at_range_boundary_high(self):
        """Guess at high boundary should be valid."""
        ok, guess, err = parse_guess("100", 1, 100)
        assert ok is True
        assert guess == 100
        assert err is None

    def test_negative_number_out_of_range(self):
        """Negative numbers should be out of range."""
        ok, guess, err = parse_guess("-5", 1, 100)
        assert ok is False
        assert guess is None
        assert "Out of range" in err


class TestUpdateScore:
    """Tests for update_score function."""

    def test_win_on_first_attempt(self):
        """Winning on first attempt should give 100 - 10*(1+1) = 80 points."""
        new_score = update_score(0, "Win", 1)
        assert new_score == 80

    def test_win_on_second_attempt(self):
        """Winning on second attempt should give 100 - 10*(2+1) = 70 points."""
        new_score = update_score(0, "Win", 2)
        assert new_score == 70

    def test_win_on_ninth_attempt(self):
        """Winning on ninth+ attempt should give minimum 10 points."""
        new_score = update_score(0, "Win", 9)
        assert new_score == 10

    def test_win_accumulates_on_existing_score(self):
        """Win should add points to existing score."""
        new_score = update_score(50, "Win", 2)
        assert new_score == 50 + 70  # 100 - 10*(2+1) = 70

    def test_too_high_on_even_attempt_adds_points(self):
        """Too High on even attempt (0, 2, 4...) should add 5 points."""
        new_score = update_score(0, "Too High", 2)
        assert new_score == 5

    def test_too_high_on_odd_attempt_removes_points(self):
        """Too High on odd attempt (1, 3, 5...) should subtract 5 points."""
        new_score = update_score(0, "Too High", 1)
        assert new_score == -5

    def test_too_low_always_removes_points(self):
        """Too Low should always subtract 5 points."""
        new_score = update_score(10, "Too Low", 1)
        assert new_score == 5

    def test_too_low_on_even_attempt(self):
        """Too Low on even attempt should still subtract 5 points."""
        new_score = update_score(10, "Too Low", 2)
        assert new_score == 5

    def test_score_can_go_negative(self):
        """Score should be able to go negative with wrong guesses."""
        score = 0
        score = update_score(score, "Too High", 1)  # -5
        score = update_score(score, "Too Low", 1)   # -10
        score = update_score(score, "Too High", 3)  # -15
        assert score == -15

    def test_win_after_wrong_guesses_brings_score_positive(self):
        """Win after penalties should bring cumulative score positive."""
        score = 0
        score = update_score(score, "Too High", 1)  # -5
        score = update_score(score, "Too Low", 1)   # -10
        score = update_score(score, "Win", 3)       # -10 + 60 = 50 (100 - 10*4)
        assert score == 50

    def test_unknown_outcome_returns_unchanged_score(self):
        """Unknown outcome should return score unchanged."""
        new_score = update_score(42, "Unknown", 5)
        assert new_score == 42


class TestGameFlow:
    """Integration tests for complete game scenarios."""

    def test_easy_win_game_flow(self):
        """Test a complete easy game where player wins."""
        # Setup
        low, high = get_range_for_difficulty("Easy")
        secret = 15

        # First guess - too low
        ok, guess1, err = parse_guess("10", low, high)
        assert ok is True
        outcome1, _ = check_guess(guess1, secret)
        assert outcome1 == "Too Low"
        score = update_score(0, outcome1, 1)
        assert score == -5

        # Second guess - correct
        ok, guess2, err = parse_guess("15", low, high)
        assert ok is True
        outcome2, _ = check_guess(guess2, secret)
        assert outcome2 == "Win"
        score = update_score(score, outcome2, 2)
        assert score == -5 + 70  # -5 + (100 - 10*(2+1)) = -5 + 70 = 65
        assert score == 65

    def test_hard_game_with_multiple_wrong_guesses(self):
        """Test hard difficulty game with several wrong guesses."""
        # Setup
        low, high = get_range_for_difficulty("Hard")
        secret = 25

        score = 0
        attempts = 0

        # Multiple guesses
        guesses = [10, 30, 20, 22, 25]

        for guess_val in guesses:
            attempts += 1
            ok, guess_int, err = parse_guess(str(guess_val), low, high)
            assert ok is True
            outcome, _ = check_guess(guess_int, secret)
            score = update_score(score, outcome, attempts)

            if outcome == "Win":
                break

        assert attempts == 5
        assert outcome == "Win"
        assert score > 0  # Should be positive despite wrong guesses

    def test_loss_game_flow(self):
        """Test game flow when player loses (out of attempts)."""
        low, high = get_range_for_difficulty("Normal")
        secret = 50
        attempt_limit = 8

        score = 0
        attempts = 0

        # Make 8 wrong guesses
        wrong_guesses = [10, 20, 30, 40, 45, 55, 60, 70]

        for guess_val in wrong_guesses:
            attempts += 1
            ok, guess_int, err = parse_guess(str(guess_val), low, high)
            assert ok is True
            outcome, _ = check_guess(guess_int, secret)
            score = update_score(score, outcome, attempts)

            if attempts >= attempt_limit:
                break

        assert attempts == attempt_limit
        assert score < 0  # Should be negative from multiple penalties
