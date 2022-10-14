from pathlib import Path
from typing import Protocol, Type
from dataclasses import dataclass

#Protocol -> similar to an interface, but you don't have to explicitly inherit from it
class VideoExporter(Protocol):
    """Basic representation of video exporting codec."""

    def prepare_export(self, video_data):
        """Prepares video data for exporting."""

    def do_export(self, folder: Path):
        """Exports the video data to a folder."""


class LosslessVideoExporter:
    """Lossless video exporting codec."""

    def prepare_export(self, video_data):
        print("Preparing video data for lossless export.")

    def do_export(self, folder: Path):
        print(f"Exporting video data in lossless format to {folder}.")


class H264BPVideoExporter:
    """H.264 video exporting codec with Baseline profile."""

    def prepare_export(self, video_data):
        print("Preparing video data for H.264 (Baseline) export.")

    def do_export(self, folder: Path):
        print(f"Exporting video data in H.264 (Baseline) format to {folder}.")


class H264Hi422PVideoExporter:
    """H.264 video exporting codec with Hi422P profile (10-bit, 4:2:2 chroma sampling)."""

    def prepare_export(self, video_data):
        print("Preparing video data for H.264 (Hi422P) export.")

    def do_export(self, folder: Path):
        print(f"Exporting video data in H.264 (Hi422P) format to {folder}.")


class AudioExporter(Protocol):
    """Basic representation of audio exporting codec."""

    def prepare_export(self, audio_data):
        """Prepares audio data for exporting."""

    def do_export(self, folder: Path):
        """Exports the audio data to a folder."""


class AACAudioExporter:
    """AAC audio exporting codec."""

    def prepare_export(self, audio_data):
        print("Preparing audio data for AAC export.")

    def do_export(self, folder: Path):
        print(f"Exporting audio data in AAC format to {folder}.")


class WAVAudioExporter:
    """WAV (lossless) audio exporting codec."""

    def prepare_export(self, audio_data):
        print("Preparing audio data for WAV export.")

    def do_export(self, folder: Path):
        print(f"Exporting audio data in WAV format to {folder}.")


@dataclass
class MediaExporter:
    video: VideoExporter
    audio: AudioExporter
    
    
@dataclass
class MediaExporterFactory:
    video_class: Type[VideoExporter]
    audio_class: Type[AudioExporter]
    
    def __call__(self) -> MediaExporter:
        return MediaExporter(self.video_class(), self.audio_class())
    

#def read_factory() -> tuple[VideoExporter, AudioExporter]:
def read_factory() -> MediaExporterFactory:
    """Constructs an exporter factory based on the user's preference."""
    
    while True:
        export_quality = input(
            f"Enter desired output quality ({', '.join(factories)}): "
            )
        try:
            return factories[export_quality]
        except KeyError:
            print(f"Unknown output quality option: {export_quality}.")


#Changing from factories to tuples
factories = {
        "low": MediaExporterFactory(H264BPVideoExporter, AACAudioExporter),
        "high": MediaExporterFactory(H264Hi422PVideoExporter, AACAudioExporter),
        "master": MediaExporterFactory(LosslessVideoExporter, WAVAudioExporter),
    }


#def do_export(fac: tuple[VideoExporter, AudioExporter]) -> None:
def do_export(exporter: MediaExporter) -> None:
    # prepare the export
    exporter.video.prepare_export("placeholder_for_video_data")
    exporter.audio.prepare_export("placeholder_for_audio_data")

    # do the export
    folder = Path("/usr/tmp/video")
    exporter.video.do_export(folder)
    exporter.audio.do_export(folder)


def main():
    """Main function."""
    # create the factory
    factory = read_factory()
    
    # use the factory to create the media exporter
    media_exporter = factory()
    
    do_export(media_exporter)


if __name__ == "__main__":
    # perform the exporting job
    main()

