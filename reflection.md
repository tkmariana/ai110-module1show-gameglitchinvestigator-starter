# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
it looks likes a simple game, it doesnt have a lot of game instructions. In the developer debug info
is not very clear for me, I don't understand the secret
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  show hint button is not working
  it saying atempst allowed 8 but says I have 7 left when starts

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| hint  | give me a hint    | nothing happened| app.py line 165       |
|attemps| 8 attemps left    | 7 attemps left  | app.py line 111       |
**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|enter negative number| error message: out of range number | Go LOWER! | app.py line 14 |
|out range positive   | error message: out of range number | Go LOWER! | app.py line 32 |
|guess number never correct even when I was 1 and said lower number | winning message             | Go LOWER! | app.py line 32 |
| new game should reset history| should reset history when click on reset | when reset the history never clears out | app.py |
| after losing a new game should be able to start game| should be able to start new game | Game over. Start a new game to try again. | app.py line 134|
| when changing difficulty should be able to reset to new game | change dificulty from medium to hard all developer debug onfo should reset | Developer Debug Info didnt reset | app.py
| secret and score is hard to understand | I cant understand secret and score | secret 42, score -20 | app.py
| click submit guess | guess added to history and attempts increase immediately | need to click submit twice before guess is added to history and attempts update | app.py line 151
| secret number should be hidden | secret should show ***HIDDEN*** and have reveal button | secret number visible right away spoils game | app.py
---

## 2. How did you use AI as a teammate?

I used Claude Code (Claude) to help me fix all the bugs I found. Claude was really helpful because it could explain WHY something was broken, not just tell me what was wrong.

**One AI suggestion that was correct:**
Claude noticed that the balloons animation wasn't showing when I won. It told me the problem: I was calling st.rerun() right after st.balloons(), which was interrupting the animation before it could finish. Claude suggested moving st.rerun() so it only happens during the game (when you make a wrong guess), but NOT when you win or lose. I tested this by playing the game and guessing the right number - boom, balloons showed up! That was awesome and Claude was totally right about the root cause. I found this was the issue by manually playing and seeing the animation work after the fix at line 151 in app.py.

**One AI suggestion I changed:**
Claude wrote all the tests for me but got the scoring formula wrong in the test expectations. It wrote tests expecting `100 - 10*attempts` but the actual code does `100 - 10*(attempts+1)`. I ran `pytest tests/test_game_logic.py -v` and got 5 test failures. Instead of believing Claude's tests, I looked at the actual logic_utils.py code and saw the +1 was there. So I fixed the test math to match the real code - like for attempt 2, it should expect 70 points, not 80. It wasn't that Claude was wrong about how to test, just wrong about the formula itself. After I fixed the numbers, all 33 tests passed and I trusted them.

---

## 3. Debugging and testing your fixes

**How I decided if a bug was really fixed:**
I mostly just played the game and saw if the bug still happened. Like with the "need to click submit twice" bug - I'd enter a number, click Submit once, and check if it showed up in the debug info right away. Before the fix, I had to click twice. After Claude added st.rerun(), it worked on the first click. That was my proof it was fixed. I did this over and over for each bug - reproduce it, apply the fix, test it manually in the app.

**Test I ran and what it showed me:**
I ran `python -m pytest tests/test_game_logic.py -v` and got 33 tests total. First time I ran it, 5 tests failed about the scoring. I saw the error messages like "assert 80 == 90" which told me my test expectations were wrong. This made me realize I needed to check what the actual code was doing, not guess. So I looked at logic_utils.py line 55 and saw `100 - 10 * (attempt_number + 1)` with that +1 right there. So I fixed my test formulas to match what the code actually does. Then all 33 tests passed and I knew my code was working correctly for all the cases Claude wrote tests for.

**How Claude helped with testing:**
Claude organized the tests really well with different classes for each function (TestCheckGuess, TestParseGuess, etc.). It also wrote tests for edge cases I wouldn't have thought of, like negative numbers and floating point inputs. When the tests failed, Claude helped me understand that the formula was the issue, not the logic itself. That helped me trust the tests after I fixed them.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
