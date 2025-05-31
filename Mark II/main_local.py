'''
Important: **Use headphones**. This script uses the system default audio
input and output, which often won't include echo cancellation. So to prevent
the model from interrupting itself it is important that you use headphones. 
'''

from SPARC.SPARC_Local import SPARC
import asyncio

async def main():
    sparc = SPARC()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(sparc.stt())
        input_message = tg.create_task(sparc.input_message())
        tg.create_task(sparc.send_prompt())
        tg.create_task(sparc.tts())

        await input_message

if __name__ == "__main__":
    asyncio.run(main())
