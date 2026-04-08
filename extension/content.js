const scamKeywords = [
  "lottery", "winner", "otp", "urgent action required", "verify your account", "confirm your details",
  "limited time offer", "you have been selected", "claim your prize", "bank account suspended"
];

function scanAndHighlight() {
  const elements = document.querySelectorAll('p, span, div, a, li');
  let matchesFound = 0;

  elements.forEach(el => {
    // Only process leaf nodes to prevent breaking layout
    if (el.children.length > 0) return; 

    let text = el.textContent || "";
    if (!text.trim()) return;
    
    let lowerText = text.toLowerCase();
    let hasScam = scamKeywords.some(keyword => lowerText.includes(keyword));

    if (hasScam) {
        let newHtml = text;
        scamKeywords.forEach(keyword => {
            const regex = new RegExp(`(${keyword})`, 'gi');
            if (regex.test(newHtml)) {
                newHtml = newHtml.replace(regex, `<span class="aegis-scam-highlight" title="⚠️ Potential Scam Detected!">$1</span>`);
                matchesFound++;
            }
        });
        if (newHtml !== text) {
            el.innerHTML = newHtml;
        }
    }
  });

  return matchesFound;
}

// Run scanner initially
setTimeout(scanAndHighlight, 1000);
