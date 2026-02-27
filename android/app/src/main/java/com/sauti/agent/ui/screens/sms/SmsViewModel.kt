package com.sauti.agent.ui.screens.sms

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.sauti.agent.data.models.ComposeSmsRequest
import com.sauti.agent.data.models.ComposeSmsResponse
import com.sauti.agent.data.models.ReadSmsRequest
import com.sauti.agent.data.repository.SmsRepository
import com.sauti.agent.data.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed class SmsUiState {
    object Idle : SmsUiState()
    object Loading : SmsUiState()
    data class ComposedSms(val response: ComposeSmsResponse) : SmsUiState()
    data class ReadSms(val text: String) : SmsUiState()
    data class Error(val message: String) : SmsUiState()
}

@HiltViewModel
class SmsViewModel @Inject constructor(
    private val smsRepository: SmsRepository,
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<SmsUiState>(SmsUiState.Idle)
    val uiState: StateFlow<SmsUiState> = _uiState.asStateFlow()

    private val _dictatedMessage = MutableStateFlow("")
    val dictatedMessage: StateFlow<String> = _dictatedMessage.asStateFlow()

    private val _smsContent = MutableStateFlow("")
    val smsContent: StateFlow<String> = _smsContent.asStateFlow()

    fun setDictatedMessage(msg: String) { _dictatedMessage.value = msg }
    fun setSmsContent(content: String) { _smsContent.value = content }

    fun composeSms() {
        viewModelScope.launch {
            _uiState.value = SmsUiState.Loading
            val language = userRepository.preferredLanguage.first()
            val sessionId = userRepository.sessionId.first()
            smsRepository.composeSms(
                ComposeSmsRequest(
                    dictatedMessage = _dictatedMessage.value,
                    language = language,
                    sessionId = sessionId
                )
            ).onSuccess { _uiState.value = SmsUiState.ComposedSms(it) }
             .onFailure { _uiState.value = SmsUiState.Error(it.message ?: "Failed to compose SMS") }
        }
    }

    fun readSms() {
        viewModelScope.launch {
            _uiState.value = SmsUiState.Loading
            val language = userRepository.preferredLanguage.first()
            smsRepository.readSms(
                ReadSmsRequest(smsContent = _smsContent.value, language = language)
            ).onSuccess { _uiState.value = SmsUiState.ReadSms(it.spokenResponse.ifEmpty { it.summary }) }
             .onFailure { _uiState.value = SmsUiState.Error(it.message ?: "Failed to read SMS") }
        }
    }

    fun resetState() { _uiState.value = SmsUiState.Idle }
}
