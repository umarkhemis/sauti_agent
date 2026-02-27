package com.sauti.agent.data.models

import com.google.gson.annotations.SerializedName

data class TranscribeResponse(
    val text: String = "",
    val confidence: Double = 0.0,
    val language: String = ""
)

data class DetectLanguageResponse(
    val language: String = "",
    val confidence: Double = 0.0
)

data class TtsRequest(
    val text: String,
    val language: String
)

data class TranslateRequest(
    val text: String,
    @SerializedName("source_language") val sourceLanguage: String,
    @SerializedName("target_language") val targetLanguage: String
)

data class TranslateResponse(
    @SerializedName("translated_text") val translatedText: String = "",
    val text: String = ""
)
