/**
 * Acts as a poor man's configuration. Takes a URL path (everthing from the 
 * first/third slash on, "/foo/bar") and returns the absolute URL to pass to eg 
 * XHR.
 */
function getrburl(page) {
	return "http://192.168.10.111:5678"+page;
}
