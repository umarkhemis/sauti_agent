package com.sauti.agent.data.api

import com.sauti.agent.data.models.*
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.*

interface SautiApiService {

    // Users
    @GET("users/profile/")
    suspend fun getProfile(): Response<UserProfile>

    @PUT("users/profile/")
    suspend fun updateProfile(@Body profile: UserProfileUpdate): Response<UserProfile>

    @POST("users/session/")
    suspend fun createSession(@Body body: Map<String, String>): Response<UserSession>

    @DELETE("users/session/{session_id}/")
    suspend fun deleteSession(@Path("session_id") sessionId: String): Response<Unit>

    // Speech
    @Multipart
    @POST("speech/transcribe/")
    suspend fun transcribe(
        @Part audio: MultipartBody.Part,
        @Part("language") language: RequestBody
    ): Response<TranscribeResponse>

    @Multipart
    @POST("speech/detect-language/")
    suspend fun detectLanguage(
        @Part audio: MultipartBody.Part
    ): Response<DetectLanguageResponse>

    @POST("speech/tts/")
    suspend fun textToSpeech(@Body request: TtsRequest): Response<ResponseBody>

    @POST("speech/translate/")
    suspend fun translate(@Body request: TranslateRequest): Response<TranslateResponse>

    // USSD
    @POST("ussd/build-code/")
    suspend fun buildUssdCode(@Body request: UssdBuildRequest): Response<UssdBuildResponse>

    @POST("ussd/parse/")
    suspend fun parseUssdResponse(@Body request: UssdParseRequest): Response<UssdParseResponse>

    // SMS
    @POST("sms/compose/")
    suspend fun composeSms(@Body request: ComposeSmsRequest): Response<ComposeSmsResponse>

    @POST("sms/read/")
    suspend fun readSms(@Body request: ReadSmsRequest): Response<ReadSmsResponse>

    // Contacts
    @GET("contacts/")
    suspend fun getContacts(@Query("search") query: String? = null): Response<List<Contact>>
}
