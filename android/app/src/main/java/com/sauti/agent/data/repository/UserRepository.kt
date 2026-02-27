package com.sauti.agent.data.repository

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import com.sauti.agent.data.api.SautiApiService
import com.sauti.agent.data.models.UserProfile
import com.sauti.agent.data.models.UserProfileUpdate
import com.sauti.agent.data.models.UserSession
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "sauti_prefs")

@Singleton
class UserRepository @Inject constructor(
    private val api: SautiApiService,
    @ApplicationContext private val context: Context
) {
    companion object {
        val SESSION_ID_KEY = stringPreferencesKey("session_id")
        val LANGUAGE_KEY = stringPreferencesKey("preferred_language")
        val TELECOM_KEY = stringPreferencesKey("primary_telecom")
        val ONBOARDING_COMPLETE_KEY = booleanPreferencesKey("onboarding_complete")
    }

    val sessionId: Flow<String> = context.dataStore.data.map { it[SESSION_ID_KEY] ?: "" }
    val preferredLanguage: Flow<String> = context.dataStore.data.map { it[LANGUAGE_KEY] ?: "eng" }
    val onboardingComplete: Flow<Boolean> = context.dataStore.data.map { it[ONBOARDING_COMPLETE_KEY] ?: false }

    suspend fun getProfile(): Result<UserProfile> = runCatching {
        val response = api.getProfile()
        response.body() ?: throw Exception("Empty response")
    }

    suspend fun updateProfile(update: UserProfileUpdate): Result<UserProfile> = runCatching {
        val response = api.updateProfile(update)
        response.body() ?: throw Exception("Empty response")
    }

    suspend fun createSession(): Result<UserSession> = runCatching {
        val response = api.createSession(emptyMap())
        val session = response.body() ?: throw Exception("Empty response")
        saveSessionId(session.sessionId.ifEmpty { session.id })
        session
    }

    suspend fun saveSessionId(sessionId: String) {
        context.dataStore.edit { it[SESSION_ID_KEY] = sessionId }
    }

    suspend fun saveLanguage(language: String) {
        context.dataStore.edit { it[LANGUAGE_KEY] = language }
    }

    suspend fun saveTelecom(telecom: String) {
        context.dataStore.edit { it[TELECOM_KEY] = telecom }
    }

    suspend fun saveOnboardingComplete(complete: Boolean) {
        context.dataStore.edit { it[ONBOARDING_COMPLETE_KEY] = complete }
    }
}
