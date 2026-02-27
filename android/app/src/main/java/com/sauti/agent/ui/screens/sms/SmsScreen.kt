package com.sauti.agent.ui.screens.sms

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.sauti.agent.ui.components.LoadingOverlay

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SmsScreen(
    viewModel: SmsViewModel,
    onBack: () -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()
    val dictatedMessage by viewModel.dictatedMessage.collectAsState()
    val smsContent by viewModel.smsContent.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }
    var selectedTab by remember { mutableIntStateOf(0) }

    LaunchedEffect(uiState) {
        if (uiState is SmsUiState.Error) {
            snackbarHostState.showSnackbar((uiState as SmsUiState.Error).message)
            viewModel.resetState()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("SMS") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            TabRow(selectedTabIndex = selectedTab) {
                Tab(selected = selectedTab == 0, onClick = { selectedTab = 0 }) {
                    Text("Compose", modifier = Modifier.padding(16.dp))
                }
                Tab(selected = selectedTab == 1, onClick = { selectedTab = 1 }) {
                    Text("Read", modifier = Modifier.padding(16.dp))
                }
            }

            when (selectedTab) {
                0 -> ComposeTab(
                    viewModel = viewModel,
                    uiState = uiState,
                    dictatedMessage = dictatedMessage
                )
                1 -> ReadTab(
                    viewModel = viewModel,
                    uiState = uiState,
                    smsContent = smsContent
                )
            }
        }

        if (uiState is SmsUiState.Loading) {
            LoadingOverlay()
        }
    }
}

@Composable
private fun ComposeTab(
    viewModel: SmsViewModel,
    uiState: SmsUiState,
    dictatedMessage: String
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        OutlinedTextField(
            value = dictatedMessage,
            onValueChange = viewModel::setDictatedMessage,
            label = { Text("Dictate your message") },
            modifier = Modifier.fillMaxWidth(),
            minLines = 3
        )
        Button(
            onClick = viewModel::composeSms,
            modifier = Modifier.fillMaxWidth(),
            enabled = dictatedMessage.isNotBlank() && uiState !is SmsUiState.Loading
        ) {
            Text("Compose SMS")
        }

        if (uiState is SmsUiState.ComposedSms) {
            Card(elevation = CardDefaults.cardElevation(4.dp)) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Composed Message", style = MaterialTheme.typography.titleSmall)
                    Spacer(modifier = Modifier.height(8.dp))
                    if (uiState.response.recipient.isNotEmpty()) {
                        Text("To: ${uiState.response.recipient}")
                    }
                    Text(uiState.response.composedMessage.ifEmpty { uiState.response.message })
                }
            }
        }
    }
}

@Composable
private fun ReadTab(
    viewModel: SmsViewModel,
    uiState: SmsUiState,
    smsContent: String
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        OutlinedTextField(
            value = smsContent,
            onValueChange = viewModel::setSmsContent,
            label = { Text("Paste SMS content here") },
            modifier = Modifier.fillMaxWidth(),
            minLines = 4
        )
        Button(
            onClick = viewModel::readSms,
            modifier = Modifier.fillMaxWidth(),
            enabled = smsContent.isNotBlank() && uiState !is SmsUiState.Loading
        ) {
            Text("Read Aloud")
        }

        if (uiState is SmsUiState.ReadSms) {
            Card(elevation = CardDefaults.cardElevation(4.dp)) {
                Text(
                    text = uiState.text,
                    modifier = Modifier.padding(16.dp),
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}
