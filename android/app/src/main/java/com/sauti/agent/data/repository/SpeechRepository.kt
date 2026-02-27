package com.sauti.agent.data.repository

import com.sauti.agent.data.api.SautiApiService
import com.sauti.agent.data.models.TranscribeResponse
import com.sauti.agent.data.models.TtsRequest
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.ResponseBody
import java.io.File
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SpeechRepository @Inject constructor(
    private val api: SautiApiService
) {
    suspend fun transcribe(audioFile: File, language: String): Result<TranscribeResponse> = runCatching {
        val requestFile = audioFile.asRequestBody("audio/m4a".toMediaType())
        val audioPart = MultipartBody.Part.createFormData("audio", audioFile.name, requestFile)
        val languagePart = language.toRequestBody("text/plain".toMediaType())
        val response = api.transcribe(audioPart, languagePart)
        response.body() ?: throw Exception("Empty transcription response")
    }

    suspend fun textToSpeech(text: String, language: String): Result<ResponseBody> = runCatching {
        val response = api.textToSpeech(TtsRequest(text, language))
        response.body() ?: throw Exception("Empty TTS response")
    }
}
