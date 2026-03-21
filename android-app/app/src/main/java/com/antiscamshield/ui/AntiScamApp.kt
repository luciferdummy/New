package com.antiscamshield.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.antiscamshield.data.AppRepository
import com.antiscamshield.engine.FraudDetectionEngine
import com.antiscamshield.model.PaymentEvent
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

private enum class Screen { DASHBOARD, SIMULATION, HISTORY, SETTINGS, GUARDIAN }

@Composable
fun AntiScamApp(repository: AppRepository) {
    var selected by remember { mutableStateOf(Screen.DASHBOARD) }
    Scaffold(
        bottomBar = {
            NavigationBar {
                Screen.entries.forEach { screen ->
                    NavigationBarItem(
                        selected = selected == screen,
                        onClick = { selected = screen },
                        label = { Text(screen.name.lowercase().replaceFirstChar { it.uppercase() }) },
                        icon = {}
                    )
                }
            }
        }
    ) { padding ->
        when (selected) {
            Screen.DASHBOARD -> DashboardScreen(padding)
            Screen.SIMULATION -> SimulationScreen(padding, repository)
            Screen.HISTORY -> HistoryScreen(padding, repository)
            Screen.SETTINGS -> SettingsScreen(padding)
            Screen.GUARDIAN -> GuardianScreen(padding)
        }
    }
}

@Composable
private fun DashboardScreen(padding: PaddingValues) {
    Column(
        modifier = Modifier.fillMaxSize().padding(padding).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("Anti-Scam Payment Protection", style = MaterialTheme.typography.headlineMedium)
        FeatureCard("Live Protection", "Accessibility, SMS, and notifications watch for risky payment behavior.")
        FeatureCard("Risk Engine", "Scores transactions from 0 to 100 using local rules and backend analysis.")
        FeatureCard("Overlay Warning", "Shows a large, high-contrast warning before risky payments proceed.")
    }
}

@Composable
private fun SimulationScreen(padding: PaddingValues, repository: AppRepository) {
    var result by remember { mutableStateOf("Tap below to simulate a risky collect request.") }
    val engine = remember { FraudDetectionEngine(repository) }
    val scope = rememberCoroutineScope()
    Column(
        modifier = Modifier.fillMaxSize().padding(padding).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("Transaction Simulation", style = MaterialTheme.typography.headlineMedium)
        Button(onClick = {
            scope.launch(Dispatchers.IO) {
                val event = PaymentEvent(
                    source = "SIMULATION",
                    amount = 15000.0,
                    receiver = "Unknown Merchant",
                    upiId = "fraudster@upi",
                    message = "Urgent refund collect request. Click bit.ly/pay now",
                    hasOtpContext = true,
                    isCollectRequest = true
                )
                val assessment = engine.analyzeEvent(event)
                repository.persistAssessment(event, assessment)
                withContext(Dispatchers.Main) {
                    result = "Risk ${assessment.riskScore}/100 (${assessment.riskLevel})\n${assessment.reasons.joinToString()}"
                }
            }
        }, modifier = Modifier.fillMaxWidth()) {
            Text("Simulate High-Risk Payment")
        }
        Text(result)
    }
}

@Composable
private fun HistoryScreen(padding: PaddingValues, repository: AppRepository) {
    val logs = remember { mutableStateListOf<String>() }
    LaunchedEffect(Unit) {
        logs.clear()
        logs += repository.recentTransactions().map {
            "${it.receiver} • ₹${it.amount} • ${it.riskLevel} • ${it.reasons}"
        }
    }
    LazyColumn(modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        items(logs) { item -> FeatureCard("Logged Transaction", item) }
    }
}

@Composable
private fun SettingsScreen(padding: PaddingValues) {
    Column(
        modifier = Modifier.fillMaxSize().padding(padding).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Text("Permissions & Safety Settings", style = MaterialTheme.typography.headlineMedium)
        FeatureCard("READ_SMS / RECEIVE_SMS", "Reads incoming OTP and payment alerts to identify scam timing and keywords.")
        FeatureCard("Notification Access", "Detects collect requests, autopay approvals, and payment notifications.")
        FeatureCard("Accessibility Service", "Reads visible payment screen details such as amount, UPI ID, and confirm buttons.")
        FeatureCard("Draw Over Other Apps", "Displays the risk overlay before you confirm a suspicious payment.")
        FeatureCard("Biometric", "Reserved for guardian alerts, sensitive settings, and future secure approval flows.")
    }
}

@Composable
private fun GuardianScreen(padding: PaddingValues) {
    Column(
        modifier = Modifier.fillMaxSize().padding(padding).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("Guardian Mode", style = MaterialTheme.typography.headlineMedium)
        FeatureCard("Trusted Contact Alerts", "Future-ready workflow for SMS or push alerts to a guardian when high-risk transactions occur.")
        FeatureCard("Elderly-Friendly UX", "Simple language, large buttons, voice warnings, and strong contrast help vulnerable users act safely.")
    }
}

@Composable
private fun FeatureCard(title: String, body: String) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(title, style = MaterialTheme.typography.titleLarge)
            Text(body, style = MaterialTheme.typography.bodyLarge)
        }
    }
}
