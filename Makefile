install : chrome.crx
	cp chrome.crx /var/www

chrome.crx : chrome/* chrome.pem
	crxmake --pack-extension=chrome --pack-extension-key=chrome.pem --extension-output=$@

.PHONY : install
