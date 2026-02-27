package com.sauti.agent.data.models

import com.google.gson.annotations.SerializedName

data class UserSession(
    val id: String = "",
    @SerializedName("session_id") val sessionId: String = "",
    @SerializedName("created_at") val createdAt: String = ""
)
