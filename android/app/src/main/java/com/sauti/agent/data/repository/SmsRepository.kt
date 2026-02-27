package com.sauti.agent.data.repository

import com.sauti.agent.data.api.SautiApiService
import com.sauti.agent.data.models.ComposeSmsRequest
import com.sauti.agent.data.models.ComposeSmsResponse
import com.sauti.agent.data.models.ReadSmsRequest
import com.sauti.agent.data.models.ReadSmsResponse
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SmsRepository @Inject constructor(
    private val api: SautiApiService
) {
    suspend fun composeSms(request: ComposeSmsRequest): Result<ComposeSmsResponse> = runCatching {
        val response = api.composeSms(request)
        response.body() ?: throw Exception("Empty response")
    }

    suspend fun readSms(request: ReadSmsRequest): Result<ReadSmsResponse> = runCatching {
        val response = api.readSms(request)
        response.body() ?: throw Exception("Empty response")
    }
}
