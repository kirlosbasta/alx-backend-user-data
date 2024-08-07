#!/usr/bin/python3
""" Check response
"""

if __name__ == "__main__":
    from api.v1.auth.auth import Auth

    a = Auth()
    res = a.require_auth("/api/v1/status", ["/api/v1/stats/", "/api/v1/status/", "/api/v1/users/"])
    if res:
        print("require_auth must return False when path is in excluded_paths - slash tolerant")
        exit(1)
    print("OK", end="")
    