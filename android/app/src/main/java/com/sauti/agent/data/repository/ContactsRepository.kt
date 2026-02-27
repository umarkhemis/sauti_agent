package com.sauti.agent.data.repository

import com.sauti.agent.data.api.SautiApiService
import com.sauti.agent.data.models.Contact
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ContactsRepository @Inject constructor(
    private val api: SautiApiService
) {
    suspend fun getContacts(query: String? = null): Result<List<Contact>> = runCatching {
        val response = api.getContacts(query)
        response.body() ?: emptyList()
    }
}
