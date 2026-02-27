package com.sauti.agent.ui.screens.contacts

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.sauti.agent.data.models.Contact
import com.sauti.agent.data.repository.ContactsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed class ContactsUiState {
    object Idle : ContactsUiState()
    object Loading : ContactsUiState()
    data class Success(val contacts: List<Contact>) : ContactsUiState()
    data class Error(val message: String) : ContactsUiState()
}

@HiltViewModel
class ContactsViewModel @Inject constructor(
    private val contactsRepository: ContactsRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<ContactsUiState>(ContactsUiState.Idle)
    val uiState: StateFlow<ContactsUiState> = _uiState.asStateFlow()

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    init { loadContacts() }

    fun setSearchQuery(query: String) {
        _searchQuery.value = query
        loadContacts(query.ifBlank { null })
    }

    fun loadContacts(query: String? = null) {
        viewModelScope.launch {
            _uiState.value = ContactsUiState.Loading
            contactsRepository.getContacts(query)
                .onSuccess { _uiState.value = ContactsUiState.Success(it) }
                .onFailure { _uiState.value = ContactsUiState.Error(it.message ?: "Failed to load contacts") }
        }
    }
}
