package com.sauti.agent.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.sauti.agent.data.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    val preferredLanguage: StateFlow<String> = userRepository.preferredLanguage
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "eng")

    val sessionId: StateFlow<String> = userRepository.sessionId
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")

    init {
        viewModelScope.launch {
            if (sessionId.value.isEmpty()) {
                userRepository.createSession()
            }
        }
    }
}
