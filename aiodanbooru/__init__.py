def run(func):
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())