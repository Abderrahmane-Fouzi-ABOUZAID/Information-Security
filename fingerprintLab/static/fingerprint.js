// 1. Four simple, synchronous features that differentiate browsers
const userAgent = navigator.userAgent;
const isBrave = navigator.brave ? "Yes" : "No";
const privacyControl = navigator.globalPrivacyControl ? "Yes" : "No";
const modernBrands = navigator.userAgentData ? navigator.userAgentData.brands.map(b => b.brand).join(", ") : "Unknown";

// 2. Display the collected values on the webpage
const outputElement = document.getElementById("feature-output");
outputElement.innerHTML =
    "User-Agent: " + userAgent + "<br>" +
    "Brave Object: " + isBrave + "<br>" +
    "Global Privacy Control: " + privacyControl + "<br>" +
    "Modern Brands: " + modernBrands;

// 3. Send the collected features to the Flask server
fetch('/collect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        user_agent: userAgent,
        is_brave: isBrave,
        privacy_control: privacyControl,
        modern_brands: modernBrands
    })
});

// so here the features were quite specific to my case, i chose User agent where we can see all the main information of the browser
// and also the feature Brave Object that will detect if there is a Brave Object, so for the browsers that are not Brave it will be false and true for Brave, 
  // Global Privacy Control is not available for all the browsers so it narrows the possibilities 
// Last, Modern brand that will tell exactly the name of the browser normally 
// The combination of all these will give you an idea of the browser that was used for the request 
