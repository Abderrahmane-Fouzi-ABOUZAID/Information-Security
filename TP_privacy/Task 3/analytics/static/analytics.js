var name = "analytics_id";
var match = document.cookie.match(/(?:^|; )analytics_id=([^;]*)/);
var id = match ? match[1] : "";

if (!id) {
  id = Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2);
  document.cookie = name + "=" + id + "; Max-Age=31536000; Path=/; SameSite=Lax";
}

var url = "http://analytics.test:8004/collect?publisher=" + encodeURIComponent(location.hostname)
  + "&id=" + encodeURIComponent(id)
  + "&page=" + encodeURIComponent(location.pathname);

var request = new Image();
request.src = url;
