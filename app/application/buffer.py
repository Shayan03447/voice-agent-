class AudioBuffer:
    def __init__(self):
        self.chunks=[]
    def add(self, chunk: bytes):
        self.chunks.append(chunk)
    def size(self):
        return len(self.chunks)
    def get_audio(self):
        return b"".join(self.chunks)
    def reset(self):
        self.chunks=[]
        


