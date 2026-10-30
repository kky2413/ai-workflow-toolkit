#!/usr/bin/env python3
"""Opt-in GET health check for loopback HTTP only; never follows redirects."""
import argparse
import ipaddress
import json
import urllib.error
import urllib.parse
import urllib.request

class RefuseRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise ValueError("리다이렉트 추적은 차단됩니다")

def check(url, timeout=5.0):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "http" or parsed.username or parsed.password or parsed.fragment:
        raise ValueError("인증 없는 localhost HTTP URL만 허용합니다")
    if parsed.hostname not in ("127.0.0.1", "::1", "localhost"):
        raise ValueError("외부 호스트 접근은 허용하지 않습니다")
    host = "127.0.0.1" if parsed.hostname == "localhost" else parsed.hostname
    if not ipaddress.ip_address(host).is_loopback:
        raise ValueError("루프백 주소가 아닙니다")
    if not (0 < timeout <= 30):
        raise ValueError("timeout은 0초 초과·30초 이하여야 합니다")
    port = parsed.port or 80
    url_host = f"[{host}]" if ":" in host else host
    path = urllib.parse.urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
    target = f"http://{url_host}:{port}{path}"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), RefuseRedirect)
    try:
        with opener.open(urllib.request.Request(target, method="GET"), timeout=timeout) as resp:
            return {"status": resp.status, "ok": 200 <= resp.status < 400}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "ok": False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="예: http://127.0.0.1:3000/health")
    parser.add_argument("--timeout", type=float, default=5)
    args = parser.parse_args()
    try:
        report = check(args.url, args.timeout)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["ok"] else 1
    except (OSError, ValueError, urllib.error.URLError) as exc:
        parser.exit(2, f"오류: {exc}\n")

if __name__ == "__main__":
    raise SystemExit(main())
