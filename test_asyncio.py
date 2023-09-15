import asyncio

async def read_chat(text:str):
    print(f'{text}...')
    await asyncio.sleep(1)
    print(f'FIN...{text}!')

async def listing_mic(text:str):
    print(f'{text}...')
    await asyncio.sleep(1)
    print(f'FIN...{text}!')

async def run_main_twice():
    # Create two tasks that run the main() function concurrently
    task1 = asyncio.create_task(read_chat('Leyendo el chat de Twitch!'))
    task2 = asyncio.create_task(listing_mic('Escuchando a Ricardo!'))

    # Wait for both tasks to complete
    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    # Run the run_main_twice() function to run the main() function twice in parallel
    asyncio.run(run_main_twice())
