package com.sauti.agent.ui.screens.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountBalanceWallet
import androidx.compose.material.icons.filled.Contacts
import androidx.compose.material.icons.filled.Message
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.sauti.agent.data.models.Language
import com.sauti.agent.ui.components.VoiceButton

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel,
    onNavigateToVoice: () -> Unit,
    onNavigateToSms: () -> Unit,
    onNavigateToContacts: () -> Unit,
    onNavigateToMobileMoney: () -> Unit
) {
    val language by viewModel.preferredLanguage.collectAsState()
    var selectedTab by remember { mutableIntStateOf(0) }

    val navItems = listOf(
        Triple("Home", Icons.Filled.Phone, {}),
        Triple("SMS", Icons.Filled.Message, onNavigateToSms),
        Triple("Contacts", Icons.Filled.Contacts, onNavigateToContacts),
        Triple("Money", Icons.Filled.AccountBalanceWallet, onNavigateToMobileMoney)
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("SautiAgent") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            )
        },
        bottomBar = {
            NavigationBar {
                navItems.forEachIndexed { index, (label, icon, action) ->
                    NavigationBarItem(
                        icon = { Icon(icon, contentDescription = label) },
                        label = { Text(label) },
                        selected = selectedTab == index,
                        onClick = {
                            selectedTab = index
                            if (index != 0) action()
                        }
                    )
                }
            }
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Hello! I'm SautiAgent",
                    style = MaterialTheme.typography.headlineSmall
                )
                Text(
                    text = "Language: ${Language.fromCode(language).displayName}",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.secondary
                )
                Spacer(modifier = Modifier.height(32.dp))

                VoiceButton(
                    isRecording = false,
                    onClick = onNavigateToVoice,
                    size = 100
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Tap to speak",
                    style = MaterialTheme.typography.bodyLarge
                )
            }

            Column {
                Text(
                    text = "Quick Actions",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.padding(bottom = 12.dp)
                )
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    QuickActionCard(
                        title = "SMS",
                        icon = Icons.Filled.Message,
                        onClick = onNavigateToSms,
                        modifier = Modifier.weight(1f)
                    )
                    QuickActionCard(
                        title = "Contacts",
                        icon = Icons.Filled.Contacts,
                        onClick = onNavigateToContacts,
                        modifier = Modifier.weight(1f)
                    )
                }
                Spacer(modifier = Modifier.height(12.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    QuickActionCard(
                        title = "Call",
                        icon = Icons.Filled.Phone,
                        onClick = onNavigateToVoice,
                        modifier = Modifier.weight(1f)
                    )
                    QuickActionCard(
                        title = "Mobile Money",
                        icon = Icons.Filled.AccountBalanceWallet,
                        onClick = onNavigateToMobileMoney,
                        modifier = Modifier.weight(1f)
                    )
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun QuickActionCard(
    title: String,
    icon: ImageVector,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        onClick = onClick,
        modifier = modifier,
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(
                imageVector = icon,
                contentDescription = title,
                modifier = Modifier.size(32.dp),
                tint = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(text = title, style = MaterialTheme.typography.labelLarge)
        }
    }
}
