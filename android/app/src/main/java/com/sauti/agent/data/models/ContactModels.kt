package com.sauti.agent.data.models

import com.google.gson.annotations.SerializedName

data class Contact(
    val id: Int = 0,
    @SerializedName("contact_name") val contactName: String = "",
    @SerializedName("phone_number") val phoneNumber: String = "",
    val telecom: String = "",
    val relationship: String = ""
)
