package com.sauti.agent.ui.screens.mobilemoney

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.sauti.agent.data.models.UssdBuildRequest
import com.sauti.agent.data.api.SautiApiService
import com.sauti.agent.data.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed class MobileMoneyUiState {
    object Idle : MobileMoneyUiState()
    object Loading : MobileMoneyUiState()
    data class UssdCode(val code: String, val operation: String) : MobileMoneyUiState()
    data class Error(val message: String) : MobileMoneyUiState()
}

@HiltViewModel
class MobileMoneyViewModel @Inject constructor(
    private val api: SautiApiService,
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<MobileMoneyUiState>(MobileMoneyUiState.Idle)
    val uiState: StateFlow<MobileMoneyUiState> = _uiState.asStateFlow()

    fun performOperation(intent: String) {
        viewModelScope.launch {
            _uiState.value = MobileMoneyUiState.Loading
            try {
                val profile = userRepository.getProfile().getOrNull()
                val telecom = profile?.primaryTelecom ?: "MTN"
                val response = api.buildUssdCode(
                    UssdBuildRequest(intent = intent, telecom = telecom)
                )
                val body = response.body()
                val code = body?.ussdCode ?: body?.code ?: ""
                if (code.isNotEmpty()) {
                    _uiState.value = MobileMoneyUiState.UssdCode(code, intent)
                } else {
                    _uiState.value = MobileMoneyUiState.Error("Could not generate USSD code")
                }
            } catch (e: Exception) {
                _uiState.value = MobileMoneyUiState.Error(e.message ?: "Operation failed")
            }
        }
    }

    fun resetState() { _uiState.value = MobileMoneyUiState.Idle }
}
