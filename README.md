# Twit-transcripts

Whisper AI created transcripts for TWiT network podcasts.

## Why?

As an avid listener of the network for the last 18 years, I often find myself trying to remember what someone said, how something was phrased, or "what was it that they said about privacy regulation?" Obviously, it's pretty tough to remember the episode (or even the right show), and it's impractical to re-listen to thousands of hours of audio. So I had the idea of transcribing the audio and video so that it's easily searchable text.

I first kicked this off after Jason Snell mentioned whispercpp as his pick-of-the-week on MacBreak Weekly. It's a fantastic project by Georgi Gerganov, and you can find information on it [here](https://github.com/ggerganov/whisper.cpp). He's ported the OpenAI Whisper code to C++ and even added support for the Core ML cores on Apple Silicon. His implementation is the fastest I've seen so far (especially when taking advantage of the ML cores on the M-series chips). I am able to transcribe 60 minutes of audio in less than 2 minutes.

## Usage

Feel free to clone the repo and use whatever tool you want to search through the text. I personally use either [fzf](https://github.com/junegunn/fzf) or telescope via Neovim--which is an incredibly fast fuzzy-finding search.

Each episode will include metadata at the beginning of the file. This is pulled directly from the .mp3 using ffmpeg.

I'm also posting some of the scripts I used to transcribe in case you wanted to try it yourself.

## Limitations

To make it manageable, I've transcribed using Whisper's "base" model. For me, it was the best balance between accuracy and performance. I ran tests of the medium vs base, and while medium was marginally better, for my purposes, it didn't warrant the performance hit. (I couldn't get the medium model to work with Core ML yet.) But what this means is that the transcripts aren't perfect. It messes up names and abbreviations. If there was music, a sound clip being played, or lots of people talking at once, that part of the transcript may be a little wonky.

It doesn't do diarization (yet). So, it doesn't distinguish who is saying what. I hope to incorporate this soon, but the diarization in whispercpp (and whisper in general) is broken. There are some agglomerative clustering hacks some people have pulled off, and Nvidia has its proprietary NeMo tools that may be able to help. For now, I am focusing on transcribing all the shows.

Since I don't have access to the original .wav format, which is required by whispercpp to work, I had to convert all the lossy mp3s into "lossless" wav. This probably impacts the quality of the transcription, but without having the original .wavs, it's the best I can do.

## TO-DO

- [X] TWiT
- [O] MacBreak
- [o] TWiG
- [ ] Windows Weekly
- [ ] diarization

Security Now is one of my favorite shows on the network, but Steve Gibson has paid for manual transcription since the first episode. They can be found on his site: grc.com

