document.getElementById('scan-btn').addEventListener('click', async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (!tab) return;

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: scanPage
    }, (results) => {
        if (results && results[0]) {
            updateUI(results[0].result);
        }
    });
});

function updateUI(matches) {
    const icon = document.getElementById('status-icon');
    const text = document.getElementById('status-text');
    const details = document.getElementById('details');

    if (matches > 0) {
        icon.textContent = "⚠️";
        icon.className = "icon danger";
        text.textContent = "Potential Scam Detected!";
        text.style.color = "#d93025";
        details.textContent = `Found ${matches} suspicious phrases on this page. They have been highlighted in red.`;
    } else {
        icon.textContent = "🛡️";
        icon.className = "icon ok";
        text.textContent = "Page looks safe";
        text.style.color = "#1e8e3e";
        details.textContent = "No known scam patterns detected. Stay vigilant!";
    }
}

// Re-using the logic for manual scan execution via scripting API
function scanPage() {
    const scamKeywords = [
        "lottery", "winner", "otp", "urgent action required", "verify your account", "confirm your details",
        "limited time offer", "you have been selected", "claim your prize", "bank account suspended"
    ];

    const elements = document.querySelectorAll('p, span, div, a, li');
    let matchesFound = 0;

    elements.forEach(el => {
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
