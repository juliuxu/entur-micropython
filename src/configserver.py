import gc
import log
import uasyncio as asyncio
import ujson
import config
import wifi


async def parse_request(reader, include_headers=True):
    request_line = await reader.readline()
    (method, path, _) = request_line.split()

    headers = {}
    while True:
        line = await reader.readline()
        if line == b"\r\n":
            break
        key, value = line.decode().split(":", 1)
        if include_headers is True or key.lower() in include_headers:
            headers[key.lower()] = value.strip()

    content_length = int(headers.get("content-length", 0))
    body = await reader.readexactly(content_length)
    return {
        "method": method.decode(),
        "path": path.decode().split("?", 1)[0],
        "body": body.decode(),
        "headers": headers
    }

async def awriteiter(writer, f):
    for buf in f:
        await writer.awrite(buf)

async def handle_static(path, writer):
    log.info("handle_static")
    with open("web/{}".format(path), "rb") as f:
        await writer.awrite("HTTP/1.0 200 OK\r\n\r\n")
        await awriteiter(writer, f)


async def handle_get_config(writer):
    log.info("handle_get_config")
    with open("config.json", "rb") as f:
        await writer.awrite("HTTP/1.0 200 OK\r\n")
        await writer.awrite("content-type: application/json; charset=utf-8\r\n\r\n")
        await awriteiter(writer, f)


async def handle_set_config(body, writer):
    log.info("handle_set_config")
    try:
        new_config = ujson.loads(body)
        if config.set_config(new_config):
            await writer.awrite("HTTP/1.0 204 No Content\r\n\r\n")
        else:
            await writer.awrite("HTTP/1.0 400 Bad Request\r\n\r\nInvalid config keys")
    except Exception:
        await writer.awrite("HTTP/1.0 400 Bad Request\r\n\r\nInvalid json")


async def handle_get_info(writer):
    await writer.awrite("HTTP/1.0 200 OK\r\n")
    await writer.awrite("content-type: application/json\r\n\r\n")

    info = {
        "wifi_ip": wifi.get_wifi_ip(),
        "wifi_status": wifi.get_wifi_status(),
        "wifi_access_points": wifi.get_access_points(),
        "ap_ip": wifi.get_ap_ip(),
        "ap_essid": wifi.get_ap_essid()
    }
    await writer.awrite(ujson.dumps(info))


async def handle_reboot(writer):
    log.info("handle_reboot")
    await writer.awrite("HTTP/1.0 200\r\n\r\nReboot initiated")

    import machine
    loop = asyncio.get_event_loop()  # pylint: disable=no-member
    loop.call_later_ms(200, machine.reset)


async def handle_request(reader, writer):
    request_obj = await parse_request(reader, include_headers=["content-length"])
    
    log.info("handle_request {}".format(request_obj["path"]))
    
    # STATIC
    if request_obj["path"] == "/":
        await handle_static("index.html", writer)
    elif request_obj["path"] == "/bundle.js":
        await handle_static("bundle.js", writer)
    elif request_obj["path"] == "/bundle.css":
        await handle_static("bundle.css", writer)
    elif request_obj["path"] == "/favicon.png":
        await handle_static("favicon.png", writer)

    # API
    elif request_obj["method"] == "GET" and request_obj["path"] == "/config":
        await handle_get_config(writer)
    elif request_obj["method"] == "PUT" and request_obj["path"] == "/config":
        await handle_set_config(request_obj["body"], writer)
    elif request_obj["path"] == "/reboot":
        await handle_reboot(writer)
    elif request_obj["path"] == "/info":
        await handle_get_info(writer)
    else:
        await writer.awrite("HTTP/1.0 404 Not Found\r\n\r\n404 Not Found")
    await writer.wait_closed()
