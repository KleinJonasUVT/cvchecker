function sendHeight() {
    var height = document.documentElement.scrollHeight || document.body.scrollHeight;
    window.parent.postMessage({ height: height }, 'https://tilburg.ai/ai-tool-advisor/');
}

// Initial send and setup observer
window.onload = function() {
    sendHeight();
    var observer = new MutationObserver(function(mutations) {
        sendHeight();
    });
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true
    });
};

// Update height on resize as well
window.onresize = sendHeight;