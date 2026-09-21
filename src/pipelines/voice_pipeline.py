from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embeddings(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio, source_sr=sr)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()

    except Exception as e:
        st.exception(e)
        return None


def identify_speaker(new_embedding,candidates_dict,threshold=0.65,min_margin=0.03):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    new_embedding = np.asarray(new_embedding, dtype=np.float32)
    if np.linalg.norm(new_embedding) == 0:
        return None, 0.0

    best_sid = None
    best_score = -1.0
    second_score = -1.0

    for sid, stored_embedding in candidates_dict.items():

        if stored_embedding is None:
            continue

        stored_embedding = np.asarray(stored_embedding, dtype=np.float32)

        if np.linalg.norm(stored_embedding) == 0:
            continue

        similarity = np.dot(new_embedding, stored_embedding) / (np.linalg.norm(new_embedding) *np.linalg.norm(stored_embedding))
        print(f"{sid} -> {similarity:.4f}")

        if similarity > best_score:
            second_score = best_score
            best_score = similarity
            best_sid = sid

        elif similarity > second_score:
            second_score = similarity

    print("----------------------")
    print("Best SID:", best_sid)
    print("Best Score:", best_score)
    print("Second Score:", second_score)
    print("Margin:", best_score - second_score)
    print("----------------------")

    if (best_score >= threshold and (best_score - second_score) >= min_margin):
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(audio_bytes,candidates_dict,threshold=0.65,min_margin=0.03):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)
        identified_result = {}

        for start, end in segments:
            duration = (end - start) / sr

            # Ignore very short segments
            if duration < 0.6:
                continue

            segment_audio = audio[start:end]

            # Ignore silent segments
            energy = np.sqrt(np.mean(segment_audio ** 2))
            if energy < 0.01:
                continue

            wav = preprocess_wav(segment_audio, source_sr=sr)

            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding,candidates_dict,threshold,min_margin)

            print("Detected:", sid, score)

            if sid is not None:
                if sid not in identified_result or score > identified_result[sid]:
                    identified_result[sid] = float(score)

        print("Final Result:", identified_result)
        return identified_result

    except Exception as e:
        st.exception(e)
        return {}