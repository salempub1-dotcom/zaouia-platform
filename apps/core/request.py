import hashlib

def client_ip(request):
    forwarded=request.META.get("HTTP_X_FORWARDED_FOR")
    return forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")

def viewer_key(request):
    if request.user.is_authenticated:return f"u{request.user.pk}"
    raw=f"{client_ip(request)}|{request.META.get('HTTP_USER_AGENT','')}"
    return "a"+hashlib.sha1(raw.encode()).hexdigest()[:16]
