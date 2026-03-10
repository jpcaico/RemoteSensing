# Usually, one thing happens after another
# Concurrent code: 

# assynchronous does not necessarily mean faster, it just means that we can have multiple things happening at the same time, but not necessarily faster. It is useful for I/O bound tasks, like making API calls, reading/writing files, etc. It allows us to make better use of our resources and improve the responsiveness of our applications.
# it excels at whats called IO bound tasks, which are tasks that spend a lot of time waiting for input/output operations to complete, such as making API calls, reading/writing files, or querying databases. By using async code, we can allow other tasks to run while waiting for these operations to complete, improving the overall efficiency and responsiveness of our applications.


import asyncio
import time

def sync_function(test_param: str) -> str:
    print("This is a synchronous function")
    time.sleep(0.1)
    return f"Sync result: {test_param}"



async def main():
    # sync_result = sync_function("Test")
    # print(sync_result)

    loop = asyncio.get_running_loop()
    future = loop.create_future()
    print(f"Empty Future: {future}")

    future.set_result("Future Result: Test")
    future_result = await future
    print(future_result)

if __name__ == "__main__":
    asyncio.run(main())