package com.sauti.agent.data.models

import com.google.gson.annotations.SerializedName

data class ComposeSmsRequest(
    @SerializedName("dictated_message") val dictatedMessage: String,
    val language: String,
    @SerializedName("recipient_name") val recipientName: String = "",
    @SerializedName("recipient_phone") val recipientPhone: String = "",
    @SerializedName("session_id") val sessionId: String = ""
)

data class ComposeSmsResponse(
    @SerializedName("composed_message") val composedMessage: String = "",
    val message: String = "",
    val recipient: String = "",
    val phone: String = ""
)

data class ReadSmsRequest(
    @SerializedName("sms_content") val smsContent: String,
    @SerializedName("sender_name") val senderName: String = "",
    val language: String
)

data class ReadSmsResponse(
    val summary: String = "",
    @SerializedName("spoken_response") val spokenResponse: String = ""
)
