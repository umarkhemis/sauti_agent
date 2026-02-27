package com.sauti.agent.data.models

import com.google.gson.annotations.SerializedName

data class UssdBuildRequest(
    val intent: String,
    val telecom: String,
    val params: Map<String, String> = emptyMap()
)

data class UssdBuildResponse(
    @SerializedName("ussd_code") val ussdCode: String = "",
    val code: String = ""
)

data class UssdParseRequest(
    @SerializedName("raw_response") val rawResponse: String,
    val intent: String,
    val language: String
)

data class UssdParseResponse(
    val success: Boolean = false,
    @SerializedName("spoken_response") val spokenResponse: String = "",
    val data: Map<String, Any> = emptyMap()
)
