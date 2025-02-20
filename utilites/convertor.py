from pydub import AudioSegment
from datetime import datetime
import asyncio, os

def conver_audio_format(input_path : str, output_path : str, output_format : str = 'ogg', input_format : str = 'mp3') -> bool:
    try:
        audio = AudioSegment.from_file(input_path, format = input_format)
        audio.export(output_path, format=output_format)
        return True
    except Exception as e:
        print('conver_audio_format:', e)
        return False
    

async def conver_audio_format_async(input_path : str, output_path : str, output_format : str = 'ogg', input_format : str = 'mp3') -> bool:
    return await asyncio.to_thread(conver_audio_format, input_path, output_path, output_format = output_format, input_format = input_format)