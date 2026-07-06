from app.application.buffer import AudioBuffer

class AudioPipeline:
    def __init__(self):
        self.buffer=AudioBuffer
        self.chunk_count=0
    
    def process_audio_chunk(self, chunk: bytes):
        self.chunk_count+=1
        # store chunk
        self.buffer.add(chunk)
        print(f"Chunk {self.chunk_count} | size={len(chunk)} bytes")
        if self._should_process():
            audio=self.buffer.get_audio()
            print(f"Ready for STT | total_size={len(audio)} bytes")
            self.buffer.reset()
            self.chunk_count=0
            return audio
        return None
    def _should_process(self):
        return self.chunk_count>=10

