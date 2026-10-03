// Task 2: navigator.language reveals a language preference; screen.width and screen.height reveal display size; Intl.DateTimeFormat().resolvedOptions().timeZone reveals the configured time zone; navigator.hardwareConcurrency reveals the reported logical core count; window.devicePixelRatio reveals display scaling; document.referrer reveals navigation origin when referrer policy allows it. Their combination can distinguish browser environments, but each value can be absent, rounded, spoofed, or shared by many people.
// Task 2 protection comparison: Private browsing generally clears session data but does not necessarily change these APIs. Blocking cookies prevents cookie tracking but does not itself hide these properties. Browser fingerprint protection may standardize or reduce exposed values, so it is more directly relevant; its effect varies by browser and setting, and it cannot guarantee anonymity. Extensions may change values but can also create an unusual configuration. See https://developer.mozilla.org/en-US/docs/Web_Storage_API and https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/privacy/websites.
const features = {
  language: navigator.language,
  screen: `${screen.width} × ${screen.height}`,
  time_zone: Intl.DateTimeFormat().resolvedOptions().timeZone,
  logical_cores: navigator.hardwareConcurrency ?? "Unavailable",
  pixel_ratio: window.devicePixelRatio,
  referrer: document.referrer || "None"
};

const output = document.getElementById("feature-output");
for (const [name, value] of Object.entries(features)) {
  const label = document.createElement("dt");
  const result = document.createElement("dd");
  label.textContent = name.replaceAll("_", " ");
  result.textContent = value;
  output.append(label, result);
}

fetch("/collect", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ kind: "active", ...features })
});

// Part 4: A fixed field order and SHA-256 make the same observed feature tuple produce the same identifier. The hash hides raw values from casual reading but does not make them secret, and changing one feature changes the hash. Typing data is excluded because behaviour varies between trials. See https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest.
async function showFingerprint() {
  const source = JSON.stringify(features);
  const bytes = new TextEncoder().encode(source);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  const hash = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, "0")).join("");
  document.getElementById("hash-output").textContent = hash;
  await fetch("/fingerprint", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ hash })
  });
}

showFingerprint();
