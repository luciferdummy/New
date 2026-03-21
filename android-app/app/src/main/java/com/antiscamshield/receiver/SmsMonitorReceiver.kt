package com.antiscamshield.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import com.antiscamshield.AntiScamApplication
import com.antiscamshield.engine.FraudDetectionEngine
import com.antiscamshield.model.PaymentEvent
import com.antiscamshield.model.RiskLevel
import com.antiscamshield.service.OverlayProtectionService
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

class SmsMonitorReceiver : BroadcastReceiver() {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    override fun onReceive(context: Context, intent: Intent) {
        val messages = Telephony.Sms.Intents.getMessagesFromIntent(intent)
        val body = messages.joinToString(" ") { it.messageBody }
        val repository = (context.applicationContext as AntiScamApplication).repository
        val engine = FraudDetectionEngine(repository)

        scope.launch {
            val sms = engine.analyzeSms(body)
            val event = PaymentEvent(
                source = "SMS",
                amount = sms.amount,
                receiver = messages.firstOrNull()?.originatingAddress,
                upiId = messages.firstOrNull()?.originatingAddress,
                message = body,
                hasOtpContext = sms.otpDetected
            )
            val assessment = engine.analyzeEvent(event)
            repository.persistAssessment(event, assessment)
            if (assessment.riskLevel == RiskLevel.HIGH) {
                context.startService(Intent(context, OverlayProtectionService::class.java).apply {
                    putExtra("riskScore", assessment.riskScore)
                    putExtra("riskLevel", assessment.riskLevel.name)
                    putStringArrayListExtra("reasons", ArrayList(assessment.reasons))
                })
            }
        }
    }
}
