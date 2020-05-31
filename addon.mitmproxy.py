import json
from mitmproxy import http
from mitmproxy import ctx


def intercept(flow: http.HTTPFlow, message: str) -> None:
    header = {"Content-Type": "application/json"}

    obj = {"message": message}
    body = bytes(json.dumps(obj), "utf-8")

    ctx.log.info("Wow!")

    flow.response = http.HTTPResponse.make(200, body, header)


def request(flow: http.HTTPFlow) -> None:
    if "interceptreq" in flow.request.pretty_url:
        intercept(flow, "Intercepted on Request!")


def response(flow: http.HTTPFlow) -> None:
    if "interceptres" in flow.request.pretty_url:
        intercept(flow, "Intercepted on Response!")
