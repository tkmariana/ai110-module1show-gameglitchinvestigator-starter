# FIX: Refactored all game logic into logic_utils.py using AI code organization
import random
import streamlit as st
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIX: When difficulty changes, reset game state (AI identified missing difficulty tracker)
if "previous_difficulty" not in st.session_state:
    st.session_state.previous_difficulty = difficulty

if st.session_state.previous_difficulty != difficulty:
    st.session_state.previous_difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.info("Difficulty changed. New game started.")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: Hide secret number by default to prevent spoilers (user feedback + AI implementation)
if "show_secret" not in st.session_state:
    st.session_state.show_secret = False

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Reset status="playing" to fix "can't start game after losing" bug (AI root cause analysis)
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.history = []
    st.session_state.status = "playing"  # CRITICAL: prevents st.stop() from blocking new game
    st.session_state.score = 0
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if show_hint:
    midpoint = (low + high) // 2
    if st.session_state.secret <= midpoint:
        st.info(f"Hint: The secret is between {low} and {midpoint}.")
    else:
        st.info(f"Hint: The secret is between {midpoint + 1} and {high}.")

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
        st.rerun()  # FIX: Refresh immediately for invalid input (AI: prevents double-click bug)
    else:
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            # FIX: Improved final message with context (score, attempts ratio) - AI UX improvement
            st.success(
                f"You won! 🎉\n"
                f"Secret: {st.session_state.secret} | "
                f"Attempts: {st.session_state.attempts}/{attempt_limit} | "
                f"Score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! 💔\n"
                    f"Secret: {st.session_state.secret} | "
                    f"Attempts used: {st.session_state.attempts}/{attempt_limit} | "
                    f"Score: {st.session_state.score}"
                )
            else:
                # FIX: Only rerun mid-game guesses to preserve balloons on win/loss (AI: prevents animation interrupt)
                st.rerun()

st.divider()

# FIX: Moved debug info to bottom so score always shows updated value (AI: fixed stale score display)
with st.expander("Developer Debug Info"):
    col_secret1, col_secret2 = st.columns([2, 1])
    with col_secret1:
        if st.session_state.show_secret:
            st.write("🔢 Secret (number to guess):", st.session_state.secret)
        else:
            st.write("🔢 Secret (number to guess): ***HIDDEN***")
    with col_secret2:
        # FIX: Added reveal button to hide secret until clicked (user + AI collaboration)
        if st.button("🔓 Reveal", key="reveal_secret"):
            st.session_state.show_secret = not st.session_state.show_secret
            st.rerun()

    # FIX: Improved labels with clarity about what each stat means (AI: UX enhancement)
    st.write("📊 Attempts used:", st.session_state.attempts)
    st.write("⭐ Score (updated each guess):", st.session_state.score)
    st.write("🎯 Difficulty:", difficulty)
    st.write("📝 History:", st.session_state.history)

st.caption("Built by an AI that claims this code is production-ready.")
