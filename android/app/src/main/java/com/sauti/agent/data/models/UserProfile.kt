package com.sauti.agent.data.models

import com.google.gson.annotations.SerializedName

data class UserProfile(
    val id: Int = 0,
    val username: String = "",
    val email: String = "",
    @SerializedName("phone_number") val phoneNumber: String = "",
    @SerializedName("preferred_language") val preferredLanguage: String = "eng",
    @SerializedName("primary_telecom") val primaryTelecom: String = "MTN",
    @SerializedName("onboarding_complete") val onboardingComplete: Boolean = false
)

data class UserProfileUpdate(
    @SerializedName("phone_number") val phoneNumber: String? = null,
    @SerializedName("preferred_language") val preferredLanguage: String? = null,
    @SerializedName("primary_telecom") val primaryTelecom: String? = null,
    @SerializedName("onboarding_complete") val onboardingComplete: Boolean? = null
)

enum class Language(val code: String, val displayName: String) {
    LUGANDA("lug", "Luganda"),
    ACHOLI("ach", "Acholi"),
    RUNYANKOLE("nyn", "Runyankole"),
    LUSOGA("lso", "Lusoga"),
    LUGBARA("lgg", "Lugbara"),
    ENGLISH("eng", "English");

    companion object {
        fun fromCode(code: String) = values().find { it.code == code } ?: ENGLISH
    }
}

enum class Telecom(val displayName: String) {
    MTN("MTN"),
    AIRTEL("Airtel")
}
