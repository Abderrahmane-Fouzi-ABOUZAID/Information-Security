// Task 4: Speed in words per minute is (typed characters ÷ 5) ÷ (elapsed milliseconds ÷ 60000). Five characters is the conventional word equivalent, so this measures speed consistently without depending on the sentence's actual word boundaries. The algorithm records the first typed character's time, counts Backspace presses, compares each input with the target, then calculates and sends the result once the strings match exactly. One short trial is not a reliable identity test because speed changes with context.
const target = document.getElementById("target-sentence").textContent;
const input = document.getElementById("typing-input");
const results = document.getElementById("results");
let start = null;
let corrections = 0;
let complete = false;

input.addEventListener("keydown", event => {
  if (complete) return;
  if (event.key === "Backspace") corrections++;
});

input.addEventListener("input", () => {
  if (complete) return;
  if (start === null && input.value.length > 0) start = performance.now();
  if (start === null || input.value !== target) return;

  const seconds = (performance.now() - start) / 1000;
  const wpm = (target.length / 5) / (seconds / 60);
  complete = true;
  input.disabled = true;
  results.textContent = `Time: ${seconds.toFixed(2)} s | Speed: ${wpm.toFixed(2)} WPM | Backspace corrections: ${corrections}`;
  fetch("/collect", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ kind: "typing", seconds: Number(seconds.toFixed(2)), wpm: Number(wpm.toFixed(2)), corrections })
  });
});

document.getElementById("restart-button").addEventListener("click", () => {
  start = null;
  corrections = 0;
  complete = false;
  input.disabled = false;
  input.value = "";
  results.textContent = "";
  input.focus();
});
