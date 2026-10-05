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

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
