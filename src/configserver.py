import gc
import log
import uasyncio as asyncio
import ujson
import config


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


async def handle_index(writer):
    log.info("handle_index")
    with open("web.html", "rb") as f:
        await writer.awrite("HTTP/1.0 200 OK\r\n\r\n")
        await writer.awriteiter(f)


async def handle_get_config(writer):
    log.info("handle_get_config")
    with open("config.json", "rb") as f:
        await writer.awrite("HTTP/1.0 200 OK\r\n")
        await writer.awrite("content-type: application/json; charset=utf-8\r\n\r\n")
        await writer.awriteiter(f)


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
    # TODO


async def handle_reboot(writer):
    log.info("handle_reboot")
    await writer.awrite("HTTP/1.0 200\r\n\r\nReboot initiated")

    import machine
    loop = asyncio.get_event_loop()  # pylint: disable=no-member
    loop.call_later_ms(200, machine.reset)


async def handle_request(reader, writer):
    request_obj = await parse_request(reader, include_headers=["content-length"])
    gc.collect()

    if request_obj["path"] == "/":
        await handle_index(writer)
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
    await writer.aclose()
