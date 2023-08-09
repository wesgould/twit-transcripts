import argparse
from  whisper import load_model
from  whisperx import load_align_model, align
from whisperx.transcribe import DiarizationPipeline, assign_word_speakers


def transcribe(audio_file: str, model_name: str, device: str = "cuda"):
    model = load_model(model_name, device)
    result = model.transcribe(audio_file)

    language_code = result["language"]
    return {
        "segments": result["segments"],
        "language_code": language_code,
    }

def align_segments(
    segments: list[dict[str, any]],
    language_code: str,
    audio_file: str,
    device: str = "cuda",
):
    model_a, metadata = load_align_model(language_code=language_code, device=device)
    result_aligned = align(segments, model_a, metadata, audio_file, device)
    return result_aligned

def diarize(audio_file: str, hf_token: str) -> dict[str, any]:
    diarization_pipeline = DiarizationPipeline(use_auth_token=hf_token)
    diarization_result = diarization_pipeline(audio_file)
    return diarization_result

def assign_speakers(
    diarization_result: dict[str, any], aligned_segments: dict[str, any]
) :
    result_segments, word_seg = assign_word_speakers(
        diarization_result, aligned_segments["segments"]
    )
    results_segments_w_speakers: list[dict[str, any]] = []
    for result_segment in result_segments:
        results_segments_w_speakers.append(
            {
                "start": result_segment["start"],
                "end": result_segment["end"],
                "text": result_segment["text"],
                "speaker": result_segment["speaker"],
            }
        )
    return results_segments_w_speakers

def transcribe_and_diarize(
    audio_file: str,
    hf_token: str,
    model_name: str,
    device: str = "cuda",
):
    transcript = transcribe(audio_file, model_name, device)
    aligned_segments = align_segments(
        transcript["segments"], transcript["language_code"], audio_file, device
    )
    diarization_result = diarize(audio_file, hf_token)
    results_segments_w_speakers = assign_speakers(diarization_result, aligned_segments)
    merged_segments = merge_segments(results_segments_w_speakers)
    # Print the results in a user-friendly way
    for i, segment in enumerate(merged_segments):
        #print(f"Segment {i + 1}:")
        print(f"Start time: {segment['start']:.2f}")
        print(f"End time: {segment['end']:.2f}")
        print(f"Speaker: {segment['speaker']}")
        print(f"Transcript: {segment['text']}")
        print("")

    return merged_segments

def merge_segments(results_segments_w_speakers):
    merged_segments = []
    for segment in results_segments_w_speakers:
        if merged_segments and merged_segments[-1]['speaker'] == segment['speaker']:
            # If the speaker of this segment is the same as the last one,
            # we extend the last segment to include this one.
            merged_segments[-1]['end'] = segment['end']
            merged_segments[-1]['text'] += ' ' + segment['text']
        else:
            # Otherwise, we start a new segment.
            merged_segments.append(segment)
    return merged_segments


# Print the results in a user-friendly way


#transcribe_and_diarize("/mnt/space/mbw0100.wav", 'tokenhere', 'medium', 'cuda')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe and diarize an audio file")
    parser.add_argument("audio_file", type=str, help="Path to the audio file (mp3, wav, etc.)")
    parser.add_argument("--hf_token"tokenhere"Hugging Face token")
    parser.add_argument("--model_name", type=str, default='medium', help="Model name")
    parser.add_argument("--device", type=str, default='cuda', help="Device to use for processing (e.g., 'cuda', 'cpu')")

    args = parser.parse_args()

    transcribe_and_diarize(args.audio_file, args.hf_token, args.model_name, args.device)
