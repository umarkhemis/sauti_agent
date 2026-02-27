package com.sauti.agent.ui.screens.onboarding

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.sauti.agent.data.models.UserProfileUpdate
import com.sauti.agent.data.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed class OnboardingUiState {
    object Idle : OnboardingUiState()
    object Loading : OnboardingUiState()
    object Success : OnboardingUiState()
    data class Error(val message: String) : OnboardingUiState()
}

@HiltViewModel
class OnboardingViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    val onboardingComplete = userRepository.onboardingComplete

    private val _uiState = MutableStateFlow<OnboardingUiState>(OnboardingUiState.Idle)
    val uiState: StateFlow<OnboardingUiState> = _uiState.asStateFlow()

    private val _selectedLanguage = MutableStateFlow("eng")
    val selectedLanguage: StateFlow<String> = _selectedLanguage.asStateFlow()

    private val _phoneNumber = MutableStateFlow("")
    val phoneNumber: StateFlow<String> = _phoneNumber.asStateFlow()

    private val _selectedTelecom = MutableStateFlow("MTN")
    val selectedTelecom: StateFlow<String> = _selectedTelecom.asStateFlow()

    fun setLanguage(language: String) { _selectedLanguage.value = language }
    fun setPhoneNumber(phone: String) { _phoneNumber.value = phone }
    fun setTelecom(telecom: String) { _selectedTelecom.value = telecom }

    fun completeOnboarding() {
        viewModelScope.launch {
            _uiState.value = OnboardingUiState.Loading
            val result = userRepository.updateProfile(
                UserProfileUpdate(
                    phoneNumber = _phoneNumber.value,
                    preferredLanguage = _selectedLanguage.value,
                    primaryTelecom = _selectedTelecom.value,
                    onboardingComplete = true
                )
            )
            result.onSuccess {
                userRepository.saveLanguage(_selectedLanguage.value)
                userRepository.saveTelecom(_selectedTelecom.value)
                userRepository.saveOnboardingComplete(true)
                _uiState.value = OnboardingUiState.Success
            }.onFailure {
                // Save locally even if API fails
                userRepository.saveLanguage(_selectedLanguage.value)
                userRepository.saveTelecom(_selectedTelecom.value)
                userRepository.saveOnboardingComplete(true)
                _uiState.value = OnboardingUiState.Success
            }
        }
    }
}
