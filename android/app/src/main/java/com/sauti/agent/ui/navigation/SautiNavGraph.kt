package com.sauti.agent.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.sauti.agent.ui.screens.contacts.ContactsScreen
import com.sauti.agent.ui.screens.home.HomeScreen
import com.sauti.agent.ui.screens.mobilemoney.MobileMoneyScreen
import com.sauti.agent.ui.screens.onboarding.OnboardingScreen
import com.sauti.agent.ui.screens.onboarding.OnboardingViewModel
import com.sauti.agent.ui.screens.sms.SmsScreen
import com.sauti.agent.ui.screens.voice.VoiceScreen

@Composable
fun SautiNavGraph() {
    val navController = rememberNavController()
    val onboardingViewModel: OnboardingViewModel = hiltViewModel()
    val onboardingComplete by onboardingViewModel.onboardingComplete.collectAsState(initial = false)

    val startDestination = if (onboardingComplete) Screen.Home.route else Screen.Onboarding.route

    NavHost(navController = navController, startDestination = startDestination) {
        composable(Screen.Onboarding.route) {
            OnboardingScreen(
                viewModel = hiltViewModel(),
                onOnboardingComplete = {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(Screen.Onboarding.route) { inclusive = true }
                    }
                }
            )
        }
        composable(Screen.Home.route) {
            HomeScreen(
                viewModel = hiltViewModel(),
                onNavigateToVoice = { navController.navigate(Screen.Voice.route) },
                onNavigateToSms = { navController.navigate(Screen.Sms.route) },
                onNavigateToContacts = { navController.navigate(Screen.Contacts.route) },
                onNavigateToMobileMoney = { navController.navigate(Screen.MobileMoney.route) }
            )
        }
        composable(Screen.Voice.route) {
            VoiceScreen(
                viewModel = hiltViewModel(),
                onBack = { navController.popBackStack() }
            )
        }
        composable(Screen.Sms.route) {
            SmsScreen(
                viewModel = hiltViewModel(),
                onBack = { navController.popBackStack() }
            )
        }
        composable(Screen.Contacts.route) {
            ContactsScreen(
                viewModel = hiltViewModel(),
                onBack = { navController.popBackStack() }
            )
        }
        composable(Screen.MobileMoney.route) {
            MobileMoneyScreen(
                viewModel = hiltViewModel(),
                onBack = { navController.popBackStack() }
            )
        }
    }
}
