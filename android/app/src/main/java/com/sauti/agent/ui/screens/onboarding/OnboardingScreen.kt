package com.sauti.agent.ui.screens.onboarding

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.sauti.agent.ui.components.LanguageSelector
import com.sauti.agent.ui.components.LoadingOverlay

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OnboardingScreen(
    viewModel: OnboardingViewModel,
    onOnboardingComplete: () -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()
    val selectedLanguage by viewModel.selectedLanguage.collectAsState()
    val phoneNumber by viewModel.phoneNumber.collectAsState()
    val selectedTelecom by viewModel.selectedTelecom.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(uiState) {
        if (uiState is OnboardingUiState.Success) {
            onOnboardingComplete()
        }
    }

    Scaffold(snackbarHost = { SnackbarHost(snackbarHostState) }) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(24.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Welcome to SautiAgent",
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "Your voice-first assistant for Uganda",
                style = MaterialTheme.typography.bodyLarge
            )
            Spacer(modifier = Modifier.height(32.dp))

            LanguageSelector(
                selectedLanguage = selectedLanguage,
                onLanguageSelected = viewModel::setLanguage,
                label = "Preferred Language"
            )
            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = phoneNumber,
                onValueChange = viewModel::setPhoneNumber,
                label = { Text("Phone Number") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone),
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "Telecom Provider",
                style = MaterialTheme.typography.labelLarge
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                listOf("MTN", "AIRTEL").forEach { telecom ->
                    RadioButton(
                        selected = selectedTelecom == telecom,
                        onClick = { viewModel.setTelecom(telecom) }
                    )
                    Text(telecom)
                }
            }
            Spacer(modifier = Modifier.height(32.dp))

            Button(
                onClick = viewModel::completeOnboarding,
                modifier = Modifier.fillMaxWidth(),
                enabled = uiState !is OnboardingUiState.Loading
            ) {
                Text("Get Started")
            }
        }

        if (uiState is OnboardingUiState.Loading) {
            LoadingOverlay(message = "Setting up your profile...")
        }
    }
}
