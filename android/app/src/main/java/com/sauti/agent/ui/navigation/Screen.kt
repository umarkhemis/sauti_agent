package com.sauti.agent.ui.navigation

sealed class Screen(val route: String) {
    object Onboarding : Screen("onboarding")
    object Home : Screen("home")
    object Voice : Screen("voice")
    object Sms : Screen("sms")
    object Contacts : Screen("contacts")
    object MobileMoney : Screen("mobile_money")
}
