// ==UserScript==
// @name         Xbox 360 Marketplace Fix
// @namespace    http://tampermonkey.net/
// @version      2024-07-19
// @description  Replaces Xbox purchase links with hyperlinks
// @author       VideogameScrapbook
// @match        https://marketplace.xbox.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=tampermonkey.net
// @grant        none
// ==/UserScript==

(function() {
    const targetUrlPattern = /https?:\/\/live\.xbox\.com\/[^"]+\/purchase\/xbox\/[^"]+/;

    const replaceLinks = () => {
        const purchaseLinks = document.querySelectorAll('a[role="button"][data-purchaseurl]');
        purchaseLinks.forEach(link => {
            const url = link.getAttribute('data-purchaseurl');
            if (url && targetUrlPattern.test(url)) {
                const newLink = document.createElement('a');
                newLink.href = url;
                newLink.textContent = 'Purchase Link';
                link.parentNode.replaceChild(newLink, link);
            }
        });
    };

    replaceLinks();
})();