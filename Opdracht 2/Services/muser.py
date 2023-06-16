import glob as gl
import os
import tomita.legacy.pysynth as ps

class Muser:
    def __init__(self, bpm: int, songDirectory: str):
        self.bpm = bpm
        self.songDirectory = songDirectory
        self.makeDir()

    def generate(self, song: list, generationNumber: int):
        for trackIndex, track in enumerate(song):
            ps.make_wav(
                track,
                bpm = self.bpm,
                transpose = 1,
                pause = 0.1,
                boost = 1.15,
                repeat = 1,
                fn = self.getTrackFileName(trackIndex),
            )

        ps.mix_files(
            *[self.getTrackFileName(trackIndex) for trackIndex in range (len(song))],
            os.path.join(self.songDirectory, f"Gen {generationNumber}.wav") 
        )

        for fileName in gl.glob(os.path.join(self.songDirectory, "track_*.wav")):
            os.remove(fileName)

    def getTrackFileName(self, trackIndex: int) -> str:
        return os.path.join(self.songDirectory, f"track_{str (1000 + trackIndex) [1:]}.wav")

    def makeDir(self):
        if (not os.path.exists(self.songDirectory)):
            os.makedirs(self.songDirectory)