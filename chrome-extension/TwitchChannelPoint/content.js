chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'extract_data') {
    var accountName = document.querySelector('h1').textContent.trim();
    var channelPoints = document.querySelector('div[data-test-selector="community-points-summary"] span').textContent.trim();

    sendResponse({success: true, accountName: accountName, channelPoints: channelPoints});
  }
});
